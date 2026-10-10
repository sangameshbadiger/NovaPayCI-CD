pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        ECR_REGISTRY = '570064633022.dkr.ecr.ap-south-1.amazonaws.com'
        ECR_REPOSITORY = 'novapay-app'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    set -e
                    docker build -t novapay-app:${IMAGE_TAG} ./app
                    docker tag novapay-app:${IMAGE_TAG} ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}
                '''
            }
        }

        stage('Trivy Security Scan') {
            steps {
                sh '''
                    set -e
                    /usr/local/bin/trivy image \
                      --severity HIGH,CRITICAL \
                      --exit-code 1 \
                      --format table \
                      "novapay-app:${IMAGE_TAG}"
                '''
            }
        }

        stage('Login to Amazon ECR') {
            steps {
                sh '''
                    set -e
                    aws ecr get-login-password --region "$AWS_REGION" |
                    docker login --username AWS --password-stdin "$ECR_REGISTRY"
                '''
            }
        }

        stage('Push Image to Amazon ECR') {
            steps {
                sh 'docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}'
            }
        }

        stage('Select Inactive Slot') {
            steps {
                script {
                    def active = sh(
                        script: "grep -oE '127\\.0\\.0\\.1:(8081|8082)' /etc/nginx/conf.d/novapay.conf | head -1 | cut -d: -f2",
                        returnStdout: true
                    ).trim()

                    if (active == '8081') {
                        env.PREVIOUS_PORT = '8081'
                        env.TARGET_PORT = '8082'
                        env.TARGET_NAME = 'novapay-green'
                        env.TARGET_SLOT = 'green'
                        env.PREVIOUS_SLOT = 'blue'
                    } else if (active == '8082') {
                        env.PREVIOUS_PORT = '8082'
                        env.TARGET_PORT = '8081'
                        env.TARGET_NAME = 'novapay-blue'
                        env.TARGET_SLOT = 'blue'
                        env.PREVIOUS_SLOT = 'green'
                    } else {
                        error('Cannot determine active Nginx slot. Deployment stopped.')
                    }

                    echo "Active port: ${env.PREVIOUS_PORT}; deploying to inactive port: ${env.TARGET_PORT}"
                }
            }
        }

        stage('Deploy to Inactive Slot') {
            steps {
                sh '''
                    set -e
                    docker rm -f "$TARGET_NAME" >/dev/null 2>&1 || true

                    if [ "$TARGET_PORT" = "8081" ]; then
                        docker rm -f novapay-ci >/dev/null 2>&1 || true
                    fi

                    docker run -d --name "$TARGET_NAME" \
                      --restart unless-stopped \
                      -p "${TARGET_PORT}:80" \
                      "novapay-app:${IMAGE_TAG}"
                '''
            }
        }

        stage('Target Health Check') {
            steps {
                sh '''
                    set -e
                    for attempt in $(seq 1 15); do
                        if curl -fsS "http://127.0.0.1:${TARGET_PORT}/" |
                           grep -q "Application Version"; then
                            echo "Target application is healthy on port ${TARGET_PORT}"
                            exit 0
                        fi
                        sleep 2
                    done
                    echo "Target health check failed"
                    exit 1
                '''
            }
        }

        stage('Switch Traffic') {
            steps {
                sh 'sudo -n /usr/local/bin/novapay-switch "$TARGET_SLOT"'
            }
        }

        stage('Verify Live Application') {
            steps {
                script {
                    try {
                        sh """
                            set -e
                            for attempt in \$(seq 1 10); do
                                if curl --fail --silent --show-error \\
                                    --max-time 3 http://127.0.0.1/ \\
                                    -o /tmp/novapay-live-response.html &&
                                   grep -q "Application Version" \\
                                    /tmp/novapay-live-response.html; then
                                    echo "Live application health check passed"
                                    exit 0
                                fi
                                echo "Health check attempt \${attempt} failed"
                                sleep 2
                            done
                            echo "Live application health check failed"
                            exit 1
                        """
                    } catch (Exception err) {
                        echo 'Live verification failed; attempting rollback.'
                        sh 'sudo -n /usr/local/bin/novapay-switch "$PREVIOUS_SLOT"'
                        error('Deployment verification failed; rollback attempted.')
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'NovaPay Blue-Green deployment SUCCESS!'
        }
        failure {
            echo 'NovaPay deployment FAILED. Check stage logs.'
            echo 'If traffic was switched, inspect the active Nginx slot and application health.'
        }
    }
}
