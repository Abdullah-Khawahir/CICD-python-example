pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'your-docker-registry' // Replace with your Docker registry
        DOCKER_IMAGE_NAME = 'flask-app' // Replace with your Docker image name
        DOCKER_IMAGE_TAG = "${env.BUILD_NUMBER}" // Use the Jenkins build number as the tag
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
        BLUE_GREEN = 'blue' // Tracks which environment is live (blue or green)
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    sh "docker build -t ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    echo "Pushing Docker image to registry..."
                    sh "docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
                }
            }
        }

        stage('Deploy to Inactive Environment') {
            steps {
                script {
                    // Determine the inactive environment
                    def inactiveEnv = (BLUE_GREEN == 'blue') ? 'green' : 'blue'

                    echo "Deploying to ${inactiveEnv} environment..."

                    // Update the Docker Compose file for the inactive environment
                    sh """
                        sed -i 's/image: ${DOCKER_REGISTRY}\\/${DOCKER_IMAGE_NAME}:.*/image: ${DOCKER_REGISTRY}\\/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}/g' ${inactiveEnv}-${DOCKER_COMPOSE_FILE}
                    """

                    // Start the inactive environment
                    sh "docker-compose -f ${inactiveEnv}-${DOCKER_COMPOSE_FILE} up -d"

                    // Wait for the application to start
                    echo "Waiting for the ${inactiveEnv} environment to start..."
                    sleep(time: 10, unit: 'SECONDS') // Adjust the sleep time as needed

                    // Run a health check or smoke test
                    echo "Running health check on ${inactiveEnv} environment..."
                    sh """
                        curl -f http://localhost:${inactiveEnv == 'blue' ? '8080' : '8081'} || exit 1
                    """
                }
            }
        }

        stage('Switch Traffic') {
            steps {
                script {
                    echo "Switching traffic to the new environment..."

                    // Bring down the old environment
                    sh "docker-compose -f ${BLUE_GREEN}-${DOCKER_COMPOSE_FILE} down"

                    // Update the BLUE_GREEN environment variable
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
                // Bring down the failed environment
                sh "docker-compose -f ${env.BLUE_GREEN}-${DOCKER_COMPOSE_FILE} down"

                // Switch back to the previous environment
                env.BLUE_GREEN = (env.BLUE_GREEN == 'blue') ? 'green' : 'blue'

                // Start the previous environment
                sh "docker-compose -f ${env.BLUE_GREEN}-${DOCKER_COMPOSE_FILE} up -d"
            }
        }
    }
}
