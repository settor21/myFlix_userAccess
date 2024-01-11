pipeline {
    agent any

    environment {
        PRODUCTION_SERVER = 'settorka@172.21.88.16'
        PASSWORD = 'Iamasinner100%'
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


        stage('Transfer Repository to Production Servers') {
            steps {
                script {
                    sh " echo 'Hello'"
                    sh " pwd useraccess_files.tar.gz"
                    sh "sshpass -p 'Iamasinner100%' ssh settorka@172.21.88.16"

                }
            }

        }
    }
}
