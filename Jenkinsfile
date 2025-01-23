pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'flask-app'
        DOCKER_IMAGE_TAG = "${env.BUILD_NUMBER}"
        PORT = "80"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    sh "docker build -t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ."
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo "Running Docker image ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ..."
                    sh "docker run -d -p 5000:80 ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
                    sh "docker ps"
                }
            }
        }
    }

    post {
        success {
            echo "Deployment successful! ."
        }
        failure {
            echo "Deployment failed. Rolling back to the previous environment."
            script {
                echo "Rolling back to ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG-1} ..."
                sh "docker run -d -p 5000:80 ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG-1}"
                sh "docker ps"
            }
        }
    }
}
