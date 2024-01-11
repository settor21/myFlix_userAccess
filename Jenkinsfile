pipeline {
    agent any

    environment {
        PROD_USERNAME = 'amedikusettor'
        PROD_SERVER = '34.139.58.141'
        PROD_DIR = '/home/amedikusettor/myflix'
        DOCKER_IMAGE_NAME = 'user-access-deployment'
        DOCKER_CONTAINER_NAME = 'user-access'
        DOCKER_CONTAINER_PORT = '5000'
        DOCKER_HOST_PORT = '80'
    }

    stages {
        stage('Checkout and Build') {
            steps {
                // This step automatically checks out the code into the workspace
                checkout scm

                // Your build logic goes here
                // sh 'mvn clean install'
            }
        }

        stage('Archive Repository Files') {
            steps {
                script {
                    // Archive the repository files
                    sh 'tar -czf useraccess_files.tar.gz *'
                }
            }
        }

        stage('Transfer Repository to Production Servers') {
            steps {
                script {
                    // Remove existing tar file on the production server
                    sh "ssh ${PROD_USERNAME}@${PROD_SERVER} 'rm -f ${PROD_DIR}/useraccess_files.tar.gz'"
        
                    // Transfer the zipped repository to the production server
                    sh "scp -o StrictHostKeyChecking=no useraccess_files.tar.gz ${PROD_USERNAME}@${PROD_SERVER}:${PROD_DIR}"
                }
            }
        }

        stage('Dockerize') {
            steps {
                script {
                    // SSH into the production server and remove existing files in the folder
                    sh "ssh ${PROD_USERNAME}@${PROD_SERVER} 'rm -rf ${PROD_DIR}/*'"
        
                    // Extract the zipped repository and build the Docker image on the production server
                    sh "ssh ${PROD_USERNAME}@${PROD_SERVER} 'cd ${PROD_DIR} && tar -xzf useraccess_files.tar.gz && docker build -t ${DOCKER_IMAGE_NAME} .'"
                }
            }
        }


        stage('Run Container') {
            steps {
                script {
                    // Run the Docker container on the production server
                    sh "ssh ${PROD_USERNAME}@${PROD_SERVER} 'docker run -d -p ${DOCKER_HOST_PORT}:${DOCKER_CONTAINER_PORT} --name ${DOCKER_CONTAINER_NAME} ${DOCKER_IMAGE_NAME}'"
                }
            }
        }
    }
}
