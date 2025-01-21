pipeline {
    agent any
        environment { 
        DOCKER_IMAGE_NAME = "cicd-python-example"
        }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${env.DOCKER_IMAGE_NAME} ."
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def containerId = sh(returnStdout: true, script: "docker run -d -p 5000:80 ${env.DOCKER_IMAGE_NAME}").trim()
                        sh "sleep 5 && curl http://localhost:5000"
                        sh "docker stop ${containerId} && docker rm ${containerId}"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh "docker run -d -p 5000:80 ${env.DOCKER_IMAGE_NAME}"
                }
            }
        }
    }

    post {
        always {
            sh "docker system prune -f"
        }
    }
}
