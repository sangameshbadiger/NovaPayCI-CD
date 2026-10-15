pipeline {
    agent any
    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'
        ECR_REGISTRY       = '570064633022.dkr.ecr.ap-south-1.amazonaws.com'
        APP_NAME           = 'novapay-app'
        TARGET_SLOT        = 'blue' // Default deployment slot to prevent blank arguments
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
       stage('Trivy License Scan') {
            steps {
                sh '''
                mkdir -p evidence/test-results/licenses
                /usr/local/bin/trivy image --scanners license --format json -o evidence/test-results/licenses/license-scan.json ${APP_NAME}:${BUILD_NUMBER} || true
                '''
            }
        }       
            
       stage('Switch Traffic') {
            steps {
                sh 'sudo -n /usr/local/bin/novapay-switch "${TARGET_SLOT}"'
            }
        }
    }
}
