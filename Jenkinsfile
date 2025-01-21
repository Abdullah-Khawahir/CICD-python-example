pipeline {
    agent any
    environment {
        DOCKER_IMAGE_NAME = "cicd-python-example"
    }
    stages {
        stage('Build') {
            agent any
            steps {
                script {
                    sh "docker --version"
                    sh "docker build -t ${env.DOCKER_IMAGE_NAME} ."
                }
            }
        }
    }
}
