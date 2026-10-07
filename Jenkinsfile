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
                bat 'docker build -t novapay-app:1.0 ./app'
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker rm -f novapay-ci 2>NUL || exit /b 0'
                bat 'docker run -d --name novapay-ci -p 8081:80 novapay-app:1.0'
            }
        }

        stage('Application Test') {
            steps {
                bat 'curl -f http://localhost:8081'
            }
        }
    }

    post {
        always {
            bat 'docker rm -f novapay-ci 2>NUL || exit /b 0'
        }

        success {
            echo 'NovaPay CI Pipeline SUCCESS!'
        }

        failure {
            echo 'NovaPay CI Pipeline FAILED!'
        }
    }
}
