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
                    // Create an expect script dynamically
                    def expectScript = """#!/usr/bin/expect
                        spawn scp useraccess_files.tar.gz $PRODUCTION_SERVER:/home/settorka/
                        expect \"password:\"
                        send \"$PASSWORD\\r\"
                        interact
                    """
                    writeFile file: 'transfer_files.expect', text: expectScript

                    // Make the expect script executable
                    sh 'chmod +x transfer_files.expect'

                    // Run the expect script
                    sh './transfer_files.expect'
                }
            }
        }
    }
}
