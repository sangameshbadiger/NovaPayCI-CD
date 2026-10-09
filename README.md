\# NovaPay Digital Bank – CI/CD Project



\## Project Overview

NovaPay is a sample digital banking web application used to demonstrate a Continuous Integration and Continuous Deployment (CI/CD) pipeline using Jenkins, Docker, Amazon ECR, and Amazon EC2.



\## Technologies Used

\- AWS EC2 – Hosts the application and Jenkins deployment environment

\- Jenkins – Automates the CI/CD pipeline

\- Git and GitHub – Source code management and version control

\- Docker – Builds and runs the application container

\- Amazon ECR – Stores Docker images

\- Linux and Shell scripting – Executes deployment and verification commands



\## CI/CD Workflow

1\. Developer pushes code to GitHub.

2\. Jenkins checks out the source code.

3\. Jenkins builds a Docker image from the `app` directory.

4\. Jenkins tags the image with the build number and `latest`.

5\. Jenkins authenticates with Amazon ECR using AWS CLI.

6\. Jenkins pushes the Docker images to Amazon ECR.

7\. Jenkins deploys the application container on EC2.

8\. Jenkins runs a health check using `curl`.



\## Docker Image

\- ECR Repository: `novapay-app`

\- AWS Region: `ap-south-1`

\- Image tags: Build-number tags and `latest`



\## Deployment

The application container is deployed with port mapping `8081:80`.



Application health check:



```bash

curl -f http://localhost:8081

```



\## Pipeline Stages

\- Checkout

\- Build Docker Image

\- Login to Amazon ECR

\- Push Image to Amazon ECR

\- Deploy Application

\- Application Health Check



\## Result

The Jenkins pipeline completed successfully, the Docker image was pushed to Amazon ECR, and the application returned its HTML response during the health check.



\## Learning Outcomes

\- Created a Jenkins pipeline using a Jenkinsfile

\- Built and tagged Docker images

\- Integrated Jenkins with Amazon ECR

\- Used an EC2 IAM role for AWS access

\- Deployed a containerized web application

\- Verified application availability using a health check



