pipeline {
    agent any

    environment {
        PRODUCTION_SERVER = 'settorka@172.21.88.16'
        CREDENTIAL_ID = credentials('SSHKey')

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
    }
}
