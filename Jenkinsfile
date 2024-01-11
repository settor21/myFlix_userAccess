pipeline {
    agent any

    environment {
        PRODUCTION_SERVER = 'settorka@172.21.88.16'
        PASSWORD = 'Iamasinner100%'
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

        stage('Transfer Repository to Production Server') {
            steps {
                script {
                    // Set SSHPASS environment variable
                    sh 'export SSHPASS=$PASSWORD'

                    // Use sshpass to execute the scp command
                    sh 'sshpass -e scp -o BatchMode=yes -r useraccess_files.tar.gz $PRODUCTION_SERVER:/home/settorka/'

                }
            }

        }
    }
}
