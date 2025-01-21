pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "cicd-python-example"
        DOCKER_TAG = "latest"
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
                    sh "docker build -t ${env.DOCKER_IMAGE}:${env.DOCKER_TAG} ." 
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh "docker run ${DOCKER_IMAGE}:${DOCKER_TAG} python --version"
                sh "docker run ${DOCKER_IMAGE}:${DOCKER_TAG} flask --version"
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh "docker stop ${DOCKER_IMAGE} || true"
                    sh "docker rm ${DOCKER_IMAGE} || true"
                    sh "docker run -d -p 5000:80 --name ${DOCKER_IMAGE} ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed!'
        }
    }
}
