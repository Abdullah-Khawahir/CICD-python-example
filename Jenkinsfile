pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'flask-app'
        DOCKER_IMAGE_TAG = "${env.BUILD_NUMBER}"
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
        BLUE_GREEN = 'blue'
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

        stage('Deploy to Inactive Environment') {
            steps {
                script {
                    def inactiveEnv = (BLUE_GREEN == 'blue') ? 'green' : 'blue'
                    echo "Deploying to ${inactiveEnv} environment..."

                    // Update Docker Compose file
                    sh """
                        sed -i 's/image: ${DOCKER_IMAGE_NAME}:.*/image: ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}/g' ${inactiveEnv}-${DOCKER_COMPOSE_FILE}
                    """

                    // Start the inactive environment
                    sh "docker-compose -f ${inactiveEnv}-${DOCKER_COMPOSE_FILE} up -d"

                    // Wait for the app to start
                    sleep(time: 10, unit: 'SECONDS')

                    // Debug: Check container status
                    sh "docker ps"

                    // Debug: Check container logs
                    sh "docker-compose -f ${inactiveEnv}-${DOCKER_COMPOSE_FILE} logs"

                    // Health check
                    echo "Running health check on ${inactiveEnv} environment..."
                    sh """
                        curl -f http://localhost:${inactiveEnv == 'blue' ? '5000' : '5001'} || exit 1
                    """
                }
            }
        }

        stage('Switch Traffic') {
            steps {
                script {
                    echo "Switching traffic to the new environment..."
                    sh "docker-compose -f ${BLUE_GREEN}-${DOCKER_COMPOSE_FILE} down"
                    env.BLUE_GREEN = (BLUE_GREEN == 'blue') ? 'green' : 'blue'
                    echo "Traffic is now routed to the ${env.BLUE_GREEN} environment."
                }
            }
        }
    }

    post {
        success {
            echo "Deployment successful! Traffic is now routed to the ${env.BLUE_GREEN} environment."
        }
        failure {
            echo "Deployment failed. Rolling back to the previous environment."
            script {
                sh "docker-compose -f ${env.BLUE_GREEN}-${DOCKER_COMPOSE_FILE} down"
                env.BLUE_GREEN = (env.BLUE_GREEN == 'blue') ? 'green' : 'blue'
                sh "docker-compose -f ${env.BLUE_GREEN}-${DOCKER_COMPOSE_FILE} up -d"
            }
        }
    }
}
