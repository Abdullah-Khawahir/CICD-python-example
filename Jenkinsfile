pipeline {
    agent none
    environment {
        DOCKER_IMAGE_NAME = "cicd-python-example"
        DOCKER_IMAGE_LABEL = "latest"
        GIVEN_PORT = "5000"
        CONTAINER_NAME = "cicd-python-container"
    }
    stages {
        stage("Build") {
            agent any
            steps {
                sh "docker build -t ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_LABEL} ."
            }
        }

        stage("Test") {
            agent { dockerfile true }
            steps {
                sh 'python --version'
                sh 'flask --version'
            }
        }

        stage("Deploy") {
            agent any
            steps {
                script {
                    def runningContainerId = sh(script: "docker ps -q -f name=${env.CONTAINER_NAME}", returnStdout: true).trim()
                    if (runningContainerId) {
                        echo "Stopping running container with ID: ${runningContainerId}"
                        sh "docker stop ${runningContainerId}"
                        sh "docker rm ${runningContainerId}"
                    }

                    sh "docker run -d --name ${env.CONTAINER_NAME} -p ${env.GIVEN_PORT}:80 ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_LABEL}"
                }
            }
        }
    }
}
