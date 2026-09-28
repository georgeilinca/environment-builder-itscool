pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Validate configuration') {
            steps {
                sh '''
                    mkdir -p generated
                    python3 validator/validator.py config/config.yml
                '''
            }
        }

        stage('Ansible Ping') {
            steps {
                sh '''
                    ansible \
                      -i ansible/inventory.ini \
                      environment_servers \
                      -m ping
                '''
            }
        }

        stage('Install technologies') {
            steps {
                sh '''
                    ansible-playbook \
                        -i ansible/inventory.ini \
                        ansible/install-technologies.yml \
                        -e @generated/generated.yml
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f k8s/
                    kubectl rollout status deployment/environment-builder
                    kubectl get pods
                    kubectl get services
                '''
            }
        }
    }

    post {
        success {
            echo 'Environment Builder pipeline PASSED'
        }

        failure {
            echo 'Environment Builder pipeline FAILED'
        }
    }
}
