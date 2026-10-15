pipeline {
    agent any
    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'
        ECR_REGISTRY       = '://amazonaws.com'
        APP_NAME           = 'novapay-app'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('SAST - Semgrep') {
            steps {
                sh 'docker run --rm -v ${WORKSPACE}:/src:ro semgrep/semgrep semgrep scan --config auto /src/app'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t ${APP_NAME}:${BUILD_NUMBER} ./app
                docker tag ${APP_NAME}:${BUILD_NUMBER} ${ECR_REGISTRY}/${APP_NAME}:${BUILD_NUMBER}
                '''
            }
        }
        stage('Trivy Security Scan') {
            steps {
                sh '/usr/local/bin/trivy image --scanners vuln --severity HIGH,CRITICAL --exit-code 1 --format table ${APP_NAME}:${BUILD_NUMBER}'
            }
        }
        stage('Switch Traffic') {
            steps {
                sh 'sudo -n /usr/local/bin/novapay-switch "$TARGET_SLOT"'
            }
        }
    }
}
