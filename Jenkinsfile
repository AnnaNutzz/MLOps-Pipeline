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
                    // Run tests inside the container. If you have tests, replace the 'echo' command.
                    docker.image(DOCKER_IMAGE).inside {
                        echo 'No tests found. Skipping this stage.'
                        // Example: sh 'pytest'
                    }
                }
            }
        }

        stage('Train Model') {
            steps {
                script {
                    // Run the model training script inside the container
                    docker.image(DOCKER_IMAGE).inside {
                        sh "python /app/src/train_model.py"
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Stop any existing container with the same name to avoid conflicts
                    sh "docker stop ${IMAGE_NAME} || true"
                    sh "docker rm ${IMAGE_NAME} || true"
                    
                    // Run the new container, mapping port 8080 on the host to port 80 in the container
                    docker.image(DOCKER_IMAGE).run("--name ${IMAGE_NAME} -p 8080:80")
                }
            }
        }
    }
} 