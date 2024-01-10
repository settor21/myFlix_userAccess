pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS = credentials('DOCKER_HUB_CREDENTIALS_ID')
        PRODUCTION_SERVER = 'settorka@172.21.88.16'
    }

    stages {
        stage('Checkout and Build') {
            steps {
                // This step automatically checks out the code into the workspace
                checkout scm

                // // Your build logic goes here
                // sh 'mvn clean install'
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                   // Build and tag Docker image
                    sh 'docker build -t altesande/useraccess:latest .'
                    sh 'docker push altesande/useraccess:latest'
                }
            }
        }

        stage('Transfer Docker Image to Production Server') {
            when {
                expression { params.TRANSFER_TO_PRODUCTION == 'true' }
            }
            steps {
                script {
                    // Save Docker image to tar file (optional)
                    sh 'docker save -o useraccess_latest.tar altesande/useraccess:latest'

                    // Transfer Docker image to production server using SSH (optional)
                    sh "scp useraccess_latest.tar $PRODUCTION_SERVER:~/useraccess_latest.tar"

                    // Connect to production server and load Docker image (optional)
                    sh "ssh $PRODUCTION_SERVER 'docker load -i ~/useraccess_latest.tar'"
                }
            }
        }
    }
}
