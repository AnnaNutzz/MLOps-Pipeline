pipeline {
    agent any

    environment {
        // Define the Docker image name and tag
        IMAGE_NAME = "mlops-pipeline"
        IMAGE_TAG = "build-${env.BUILD_NUMBER}"
        DOCKER_IMAGE = "${IMAGE_NAME}:${IMAGE_TAG}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image from the Dockerfile
                    docker.build(DOCKER_IMAGE, ".")
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run pytest inside the container, setting the PYTHONPATH so imports work correctly.
                    bat "docker run --rm --env PYTHONPATH=/app ${DOCKER_IMAGE} pytest /app/tests"
                }
            }
        }

        stage('Train Model') {
            steps {
                script {
                    // Run the model training script inside a temporary container from our image.
                    // The --rm flag cleans up the container after the script finishes.
                    bat "docker run --rm ${DOCKER_IMAGE} python /app/src/train_model.py"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Stop any existing container with the same name to avoid conflicts
                    // The `|| ver > nul` is a Windows batch trick to ignore errors if the container doesn't exist
                    bat "docker stop ${IMAGE_NAME} || ver > nul"
                    bat "docker rm ${IMAGE_NAME} || ver > nul"
                    
                    // Run the new container in detached mode, mapping port 8088 on the host to port 80 in the container
                    bat "docker run -d --name ${IMAGE_NAME} -p 8088:80 ${DOCKER_IMAGE}"
                }
            }
        }
    }
} 