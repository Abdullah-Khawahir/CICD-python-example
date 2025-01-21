pipeline {
    agent any
    environment {
        DOCKER_IMAGE_NAME = "cicd-python-example"
    }
    stages {
        stage('Test') {
            agent {
                docker {
                    reuseNode true
                }
            }
            steps {
                sh 'python --version'
                sh 'flask --version'
                sh 'pip --version'
            }
        }
        stage('Build') {
            agent {
                docker {
                    reuseNode true
                }
            }
            steps {
                sh "docker build -t ${env.DOCKER_IMAGE_NAME} ."
            }
        }
    }
}

