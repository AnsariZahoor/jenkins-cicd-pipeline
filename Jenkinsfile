pipeline {
    agent any

    environment {
        AWS_REGION   = 'ap-south-1'
        ECR_REGISTRY = '860201979633.dkr.ecr.ap-south-1.amazonaws.com'
        ECR_REPO     = 'fastapi-app'
        ECS_CLUSTER  = 'fastapi-cluster'
        ECS_SERVICE  = 'fastapi-app'
        IMAGE_TAG    = "${env.BUILD_NUMBER}"
        FULL_IMAGE   = "${ECR_REGISTRY}/${ECR_REPO}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh "docker build -f app.Dockerfile --target production -t ${FULL_IMAGE}:${IMAGE_TAG} -t ${FULL_IMAGE}:latest ."
            }
        }

        stage('Test') {
            steps {
                sh "docker build -f app.Dockerfile --target test ."
            }
        }

        stage('Push to ECR') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding',
                                  credentialsId: 'aws-credentials',
                                  accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                                  secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    sh """
                        aws ecr get-login-password --region ${AWS_REGION} | \
                            docker login --username AWS --password-stdin ${ECR_REGISTRY}
                        docker push ${FULL_IMAGE}:${IMAGE_TAG}
                        docker push ${FULL_IMAGE}:latest
                    """
                }
            }
        }

        stage('Deploy to ECS') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding',
                                  credentialsId: 'aws-credentials',
                                  accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                                  secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    sh """
                        aws ecs update-service \
                            --cluster ${ECS_CLUSTER} \
                            --service ${ECS_SERVICE} \
                            --force-new-deployment \
                            --region ${AWS_REGION}
                    """
                }
            }
        }
    }

    post {
        always {
            sh "docker rmi ${FULL_IMAGE}:${IMAGE_TAG} ${FULL_IMAGE}:latest || true"
        }
        success {
            echo "Pipeline completed — image ${FULL_IMAGE}:${IMAGE_TAG} deployed to ECS."
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
