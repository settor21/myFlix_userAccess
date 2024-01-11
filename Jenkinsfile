pipeline {
    agent any

    environment {
         PROD_SERVER = 'amedikusettor@34.23.51.67'
        PROD_DIR = '/home/amedikusettor/myflix'
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
                   sh 'echo Hello'
                   sh 'pwd useraccess_files.tar.gz'
                   sh "scp -o StrictHostKeyChecking=no useraccess_files.tar.gz ${PROD_SERVER}:${PROD_DIR}"

                }
            }

        }
    }
}
