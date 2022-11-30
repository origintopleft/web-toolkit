pipeline {
    agent {
        label "docker"
    }

    stages {
        stage ("Build") {
            steps {
                script {
                    app = docker.build("nicole/web-toolkit")
                    app.tag("${env.BUILD_NUMBER}")
                }
            }
        }
    }

    post {
        success {
            script {
                docker.withRegistry("https://vcs.otl-hga.net", "gitea-nicole-basic-auth") {
                    app.push("${env.BUILD_NUMBER}")
                    app.push("latest")
                }
            }
        }
    }
}