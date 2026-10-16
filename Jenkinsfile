pipeline {
    agent any
    
    environment {
        WORKSPACE = "${WORKSPACE}"
        TARGET_SLOT = "blue"
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
                echo "Building application target layers..."
                docker build -t novapay-app:${BUILD_NUMBER} ./app
                '''
            }
        }
        stage('Trivy License Scan') {
            steps {
                sh '''
                echo "Scanning software bills of materials and package registries..."
                trivy image --exit-code 0 --severity CRITICAL,HIGH novapay-app:${BUILD_NUMBER}
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
