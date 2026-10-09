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
                sh 'docker build -t novapay-app:${IMAGE_TAG} ./app'
                sh 'docker tag novapay-app:${IMAGE_TAG} ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}'
                sh 'docker tag novapay-app:${IMAGE_TAG} ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest'
                sh 'docker tag novapay-app:${IMAGE_TAG} novapay-app:latest'
            }
        }

        stage('Login to Amazon ECR') {
            steps {
                sh '''
                    aws ecr get-login-password --region "$AWS_REGION" |
                    docker login --username AWS --password-stdin "$ECR_REGISTRY"
                '''
            }
        }

        stage('Push Image to Amazon ECR') {
            steps {
                sh 'docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}'
                sh 'docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest'
            }
        }

        stage('Deploy Application') {
            steps {
                sh 'docker rm -f novapay-ci || true'
                sh 'docker run -d --name novapay-ci -p 8081:80 novapay-app:${IMAGE_TAG}'
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
            echo 'NovaPay CI/CD with Amazon ECR SUCCESS!'
        }

        failure {
            echo 'NovaPay CI/CD FAILED!'
        }
    }
}
