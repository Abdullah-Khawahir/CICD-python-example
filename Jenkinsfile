pipeline {
    agent { dockerfile true}
    stages {
        stage("Test") {
            steps {
                sh 'python --version'
                sh 'flask --version'
                sh 'curl --version'
            }
        }
    }
}
