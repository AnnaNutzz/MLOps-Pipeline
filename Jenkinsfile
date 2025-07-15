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
                // Since there are no tests, we don't need to run anything in Docker.
                // When tests are added, they should be run in the container like the training step.
                echo 'No tests found. Skipping this stage.'
            }
        }

        stage('Train Model') {
            steps {
                script {
                    // Run the model training script inside a temporary container from our image.
                    // The --rm flag cleans up the container after the script finishes.
                    sh "docker run --rm ${DOCKER_IMAGE} python /app/src/train_model.py"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Stop any existing container with the same name to avoid conflicts
                    sh "docker stop ${IMAGE_NAME} || true"
                    sh "docker rm ${IMAGE_NAME} || true"
                    
                    // Run the new container in detached mode, mapping port 8080 to 80.
                    sh "docker run -d --name ${IMAGE_NAME} -p 8080:80 ${DOCKER_IMAGE}"
                }
            }
        }
    }
} 