pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    if (isUnix()) {
                        sh "python3 -m venv ${VENV_DIR}"
                        sh "source ${VENV_DIR}/bin/activate && pip install -r requirements.txt"
                    } else {
                        bat "python -m venv ${VENV_DIR}"
                        bat "${VENV_DIR}\\Scripts\\activate.bat && pip install -r requirements.txt"
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                echo 'No tests found. Skipping this stage.'
                // In a real project, you would run your tests here.
                // e.g., sh 'pytest'
            }
        }

        stage('Train Model') {
            steps {
                script {
                    if (isUnix()) {
                        sh "source ${VENV_DIR}/bin/activate && python src/train_model.py"
                    } else {
                        bat "${VENV_DIR}\\Scripts\\activate.bat && python src/train_model.py"
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def imageName = "mlops-pipeline:${env.BUILD_NUMBER}"
                    docker.build(imageName, ".")
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    def imageName = "mlops-pipeline:${env.BUILD_NUMBER}"
                    // Stop any existing container with the same name
                    sh "docker stop mlops-pipeline || true"
                    sh "docker rm mlops-pipeline || true"
                    // Run the new container
                    docker.image(imageName).run("--name mlops-pipeline -p 8080:80")
                }
            }
        }
    }
} 