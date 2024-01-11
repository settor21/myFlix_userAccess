pipeline {
    agent any

    environment {
        NFS_SERVER = '172.21.88.16' // Replace with your NFS server IP
        NFS_HTTP_PORT = '4000'       // Replace with the port of your HTTP server
        NFS_SHARED_FOLDER = '/home/settorka/myflix'
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
                   
                   // Transfer the tar file using curl
                    sh "curl --upload-file useraccess_files.tar.gz http://${env.NFS_SERVER}:${env.NFS_HTTP_PORT}/${env.NFS_SHARED_FOLDER}/"
                }
            }

        }
    }
}
