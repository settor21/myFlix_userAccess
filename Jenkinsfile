pipeline {
    agent any

    environment {
        PRODUCTION_SERVER = 'settorka@172.21.88.16'
        PRIVATE_KEY_PATH = '/var/jenkins_home/.ssh/jenkins_rsa'
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
                    // Transfer the archive to the production server using SCP with private key
                    sh "scp -i $PRIVATE_KEY_PATH useraccess_files.tar.gz $PRODUCTION_SERVER:/home/settorka/useraccess_files.tar.gz"
                }

                }
            }
        }
    }
