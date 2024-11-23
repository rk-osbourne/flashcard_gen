# Flashcards App Deployment to Amazon ECS

This repository automates the deployment of the Flashcards App to Amazon ECS (Elastic Container Service) using GitHub Actions. The workflow builds a Docker image, pushes it to Amazon ECR (Elastic Container Registry), updates the ECS task definition, and deploys the updated task.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [GitHub Actions Workflow](#github-actions-workflow)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

The Flashcards App is a containerized application designed to assist with interactive learning. This repository enables automated deployment using Amazon ECS, ensuring high availability and easy scaling for the application.

### Key Technologies
- **Amazon ECS**: Hosts the containerized application.
- **Amazon ECR**: Stores the Docker image.
- **GitHub Actions**: Automates CI/CD pipeline.
- **Docker**: Containerizes the application.

---

## Features
- Automated CI/CD pipeline for Amazon ECS.
- Infrastructure-as-Code for task definitions.
- Container orchestration.
