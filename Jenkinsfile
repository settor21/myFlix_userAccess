pipeline {
    agent any

    environment {
        PRODUCTION_SERVER = 'settorka@172.21.88.16'
        CREDENTIAL_ID = credentials('SSHKey')
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_USERNAME = 'altesande'
        DOCKER_IMAGE_NAME = 'user-access-deployment'
        DOCKER_IMAGE_TAG = 'latest'
    }

    stages {
        stage('Checkout') {
            steps {
                // This step automatically checks out the code into the workspace
                checkout scm

                // Your build logic goes here
                // sh 'mvn clean install'
            }
        }

        stage('Build') {
            steps {
                // Your build logic goes here
                // Example: sh 'mvn clean install'

                // Docker build and push
                script {
                    sh "docker build -t $DOCKER_REGISTRY/$DOCKER_USERNAME/$DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG ."
                    withCredentials([usernamePassword(credentialsId: 'DOCKER_HUB_CREDENTIALS', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh "docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD $DOCKER_REGISTRY"
                    }
                    sh "docker push $DOCKER_REGISTRY/$DOCKER_USERNAME/$DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG"
                }
            }
        }

        stage('Deploy to Production') {
            steps {
                script {
                    // SSH into the production server and pull the Docker image
                    sshagent(credentials: [CREDENTIAL_ID]) {
                        sh "ssh $PRODUCTION_SERVER 'docker pull $DOCKER_REGISTRY/$DOCKER_USERNAME/$DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG'"
                        sh "ssh $PRODUCTION_SERVER 'docker stop user-access || true && docker rm user-access || true'"
                        sh "ssh $PRODUCTION_SERVER 'docker run -d --name user-access -p 8080:8080 $DOCKER_REGISTRY/$DOCKER_USERNAME/$DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG'"
                    }
                }
            }
        }
        
    }
}
