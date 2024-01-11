pipeline {
    agent any

    environment {
        PRODUCTION_SERVER = 'settorka@172.21.88.16'
        // PASSWORD = 'Iamasinner100%'
        PUBLIC_KEY_PATH = '/var/jenkins_home/.ssh/id_rsa.pub'

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

         stage('Copy SSH Public Key to WSL Ubuntu') {
            steps {
                script {
                    // Debugging: Print the current directory
                    sh 'pwd'

                    // Debugging: List the contents of the current directory
                    sh 'ls -l'

                    // Copy the SSH public key to the WSL Ubuntu server
                    sh "sshpass -p 'Iamasinner100%' scp $PUBLIC_KEY_PATH $PRODUCTION_SERVER:/home/settorka/.ssh/authorized_keys"
                }
            }
        }

        stage('Transfer Repository to Production Servers') {
            steps {
                script {
                    sh " echo 'Hello'"
                    sh 'scp -i /var/jenkins_home/.ssh/id_rsa -o StrictHostKeyChecking=no useraccess_files.tar.gz $PRODUCTION_SERVER:/home/settorka/myflix'

                }
            }

        }
    }
}
