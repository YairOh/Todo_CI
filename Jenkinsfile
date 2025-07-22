pipeline {
    agent any

    environment {
        VERSION = 'v1'
        IMAGE_NAME = "yairoh/flask-app:${VERSION}"
        DOCKER_CREDS = credentials('dockerhub-credentials')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/YairOh/Todo_CI'
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('app') {
                    sh "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Run Tests') {
            steps {
                dir('app') {
                    sh "docker run --rm ${IMAGE_NAME} pytest app/tests"
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh """
                    echo ${DOCKER_CREDS_PSW} | docker login -u ${DOCKER_CREDS_USR} --password-stdin
                    docker push ${IMAGE_NAME}
                    docker tag ${IMAGE_NAME} yairoh/flask-app:latest
                    docker push yairoh/flask-app:latest
                """
            }
        }

        stage('Notify') {
            steps {
                echo 'Docker image built, tested, and pushed successfully! 🎉'
            }
        }

        stage('Update CD Repo') {
            steps {
                sh """
                    git clone https://github.com/YairOh/flask-cd-infra.git
                    cd flask-cd-infra
                    sed -i "s|image: .*|image: yairoh/flask-app:${VERSION}|" deployment.yaml
                    git config user.name "JenkinsBot"
                    git config user.email "Jenkins@domain.com"
                    git commit -am "Update Docker image to ${IMAGE_NAME}"
                    git push
                """
            }
        }
    }
}