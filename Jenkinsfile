pipeline {
    agent {
        label "docker"
    }

    options {
        skipDefaultCheckout(true)
    }

    stages {
        stage ("Checkout") {
            steps {
                checkout scm
                sh "git submodule update --init"
            }
        }
        stage ("Build") {
            steps {
                script {
                    app = docker.build("nicole/web-toolkit")
                    app.tag("${env.BUILD_NUMBER}")
                    app.tag("latest")
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