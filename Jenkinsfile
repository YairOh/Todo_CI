pipeline {
    agent any
    environment {
        VERSION = 'v1'
        IMAGE_NAME = "yairoh/flask-app:${VERSION}"
        DOCKER_CREDS = credentials'dockerhub-credentials' 
    }
    stages {
        stage ('Checkout') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/YairOh/Todo_CI'
            }
        }
        stage('Build Docker Image') {
            steps {
                 sh "docker build -t ${IMAGE_NAME} ."
                }
            }
        stage('Run Tests') {
            steps {
                sh "docker run --rm ${IMAGE_NAME} pytest"
            }
        }
        stage('Push Docker Image') {
            steps {
                sh """
                    echo ${DOCKERHUB_CREDS_PSW} | docker login -u ${DOCKERHUB_CREDS_USR} --password-stdin
                    docker push ${IMAGE_NAME}
                    docker tag ${IMAGE_NAME} yairoh/flask-app:latest
                    docker push yairoh/flask-app:latest
                """

                }
            }
        stage('Notify') {
            steps {
                echo 'Docker image built, tested, and pushed successfully!🎉'
            }
        }
        stage('Update CD Repo') {
            steps {
                sh """
                    git clone https://github.com/YairOh/flask-cd-infra.git
                    cd flask-cd-infra
                    sed -i "s|image: .*|image: yairoh/flask-app:v1|" deployment.yaml
                    git config user.name "JenkinsBot"
                    git config user.email "Jenkins@domain.com"
                    git commit -am "Update Docker image to $IMAGE_NAME:latest"
                    git push
                """
        }

    }
    }
}