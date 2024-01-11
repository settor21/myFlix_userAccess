pipeline {
    agent any

    environment {
        PRODUCTION_SERVER = 'settorka@172.21.88.16'
        CREDENTIAL_ID = 'github-private-key'

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
                    sh " echo 'Hello'"
                    sh " pwd useraccess_files.tar.gz"
                    sh "scp -i ${CREDENTIAL_ID} -o StrictHostKeyChecking=no /var/jenkins_home/workspace/myFlix-userAccess/useraccess_files.tar.gz $PRODUCTION_SERVER:/home/settorka/myflix"

                    // sh "sshpass -p 'Iamasinner100%' ssh settorka@172.21.88.16 'echo hello world'"

                }
            }

        }
    }
}
