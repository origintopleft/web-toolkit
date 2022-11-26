pipeline {
    agent any

    stages {
        stage ("Build") {
            script {
                app = docker.build("nicole/web-toolkit")
            }
        }
    }
}