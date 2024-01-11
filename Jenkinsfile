pipeline {
    agent any

    environment {
        PROD_USERNAME = 'amedikusettor'
        PROD_SERVER = '34.139.58.141'
        PROD_DIR = '/home/amedikusettor/myflix/user-access'
        DOCKER_IMAGE_NAME = 'user-access-deployment'
        DOCKER_CONTAINER_NAME = 'user-access'
        DOCKER_CONTAINER_PORT = '5000'
        DOCKER_HOST_PORT = '5000'
    }

    stages {
        stage('Load Code to Workspace') {
            steps {
                // This step automatically checks out the code into the workspace
                checkout scm             

                // Your build logic goes here
                // sh 'mvn clean install' 
            }
        }

        stage('Deploy Repo to Prod. Server') {
            steps {
                script {
                    sh 'echo Packaging files ....'
                    // sh 'ls -l'
                    // sh 'pwd useraccess_files.tar.gz'
                    // Archive the repository files
                    sh 'tar -czf useraccess_files.tar.gz *'
                    // Transfer the zipped repository to the production server
                    sh "scp -o StrictHostKeyChecking=no useraccess_files.tar.gz ${PROD_USERNAME}@${PROD_SERVER}:${PROD_DIR}"
                    sh 'echo Files transferred to server. Unpacking ...'
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'pwd && cd myflix/user-access && tar -xzf useraccess_files.tar.gz && ls -l'"
                    sh 'echo Repo unloaded on Prod. Server. Preparing to dockerize application ...'
                }
            }
        }

        stage('Dockerize Application') {
            steps {
                script {

                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix/user-access && docker build -t ${DOCKER_IMAGE_NAME} .'"
                    sh "echo Docker image for userAccess rebuilt. Preparing to redeploy container to web..."
                }
            }
        }


        stage('Redeploy Container to Web') {
            steps {
                script {
                    // Stop  the old Docker container on the production server
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix/user-access && docker stop ${DOCKER_CONTAINER_NAME}'"

                    // Stop  the old Docker container on the production server
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix/user-access && docker rm ${DOCKER_CONTAINER_NAME}'"
                    sh "echo Container stopped and removed. Preparing to redeploy new version"
                    // Run the Docker container on the production server
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix/user-access && docker run -d -p ${DOCKER_HOST_PORT}:${DOCKER_CONTAINER_PORT} --name ${DOCKER_CONTAINER_NAME} ${DOCKER_IMAGE_NAME}'"

                    sh "echo userAccess Microservice Deployed!"
                    
                }
            }
        }
    }
}
