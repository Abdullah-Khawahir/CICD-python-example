pipline {
    agent { dockerfile true}
    stages {
        stage("Test") {
            sh 'python --version'
            sh 'flask --version'
            sh 'curl --version'
        }
    }
}
