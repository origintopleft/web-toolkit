pipeline {
    agent {
        label "docker"
    }

    stages {
        stage ("Build") {
            steps {
                script {
                    app = docker.build("nicole/web-toolkit")
                }
            }
        }
    }

    post {
        success {
            script {
                docker.withRegistry("https://vcs.otl-hga.net", "gitea") {
                    app.push("${env.BUILD_NUMBER}")
                    app.push("latest")
                }
            }
        }
    }
}