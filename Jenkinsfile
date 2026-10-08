pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t novapay-app:1.0 ./app'
            }
        }

        stage('Deploy Application') {
            steps {
                sh 'docker rm -f novapay-ci || true'
                sh 'docker run -d --name novapay-ci -p 8081:80 novapay-app:1.0'
            }
        }

        stage('Application Health Check') {
            steps {
                sh 'curl -f http://localhost:8081'
            }
        }
    }

    post {
        success {
            echo 'NovaPay CD Deployment SUCCESS!'
        }

        failure {
            echo 'NovaPay CD Deployment FAILED!'
        }
    }
}