# Flashcards App Deployment to Amazon ECS

This repository automates the deployment of the Flashcards App to Amazon ECS (Elastic Container Service) using GitHub Actions. The workflow builds a Docker image, pushes it to Amazon ECR (Elastic Container Registry), updates the ECS task definition, and deploys the updated task.

## Table of Contents
- [Project Overview](#project-overview)
- [Current Deployment Structure](#current-deployment-structure)
- [Setup](#setup)
- [Future Enhancements](#future-enhancements)

---

## Project Overview

The Flashcards App is a containerized application that I decided to build as part of my language learning journey. This repository enables automated deployment to Amazon ECS via GitHub Actions.

### Key Technologies
- **Terraform**: Defines the infrastructure and deploys resources.
- **Amazon ECS**: Manages the containers and the deployment of the app.
- **Amazon ECR**: Stores the Docker image.
- **GitHub Actions**: Automates the CI/CD pipeline for deployment.
- **Docker**: Containerizes the application.

## Current Deployment Structure

The current version of the app features a Python backend and a basic HTML frontend. Some of the APIs require additional testing, which can be done easily using tools like Postman. The key components of the deployment are as follows:

### Key Components:
1. **ECS Cluster**:
   - The `flashcards-cluster` runs the containerized app as a service within ECS.

2. **ECS Service**:
   - The `flashcards-service` manages the running tasks based on the updated task definitions. It's configured for rolling updates to minimize downtime during deployments.

3. **Task Definition**:
   - The task definition specifies the container settings, including the Docker image pulled from Amazon ECR. The workflow dynamically updates the task definition with the new image URI during each deployment, tagged with the Git commit hash.

4. **GitHub Actions Workflow**:
   - The workflow automates the following steps:
     - Build the Docker image.
     - Push the image to ECR.
     - Register a new task definition revision.
     - Deploy the updated task to ECS.

## Setup

To set up this deployment, ensure that you have the following configured:

1. **AWS Account** with ECS, ECR, and IAM permissions for deployment.
2. **GitHub Repository Secrets**:
   - `AWS_ACCESS_KEY_ID`: Your AWS access key.
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key.

3. **Docker Installed**: Required for local testing and builds.

4. **AWS CLI**: Ensure the AWS CLI is installed and configured on your local machine for managing AWS resources.

## Future Enhancements

While the current structure is functional, I have a number of planned upgrades for the app:

1. **React Frontend**:
   - Transition the frontend to **React** to enhance the user interface and add more functionality. The frontend will be refactored to use **TypeScript** for better maintainability and scalability.

2. **Set Up API Gateway**:
   - Set up an API Gateway to manage the backend API calls more efficiently and securely.

3. **Set Up CloudWatch**:
   - Integrate **AWS CloudWatch** to monitor the app’s performance, track logs, and set up alerts for service health or errors.

4. **CI/CD Pipeline Optimization**:
   - Refactor and optimize the current CI/CD pipeline to reduce complexity and build time.
     
6. **Migrate to Another Cloud Provider**:
   - In the future, I plan to test the deployment by migrating the app to **Azure** to explore multi-cloud deployment options and better understand cloud portability.

---

Feel free to open an issue or submit a pull request if you have suggestions, issues, or improvements to the project!
