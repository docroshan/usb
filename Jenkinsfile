pipeline {
    agent { 
        node {
            label 'docker-agent-py'
            }
      }
    triggers {
        pollSCM '* * * * *'
    }
    stages {
        stage('Build') {
            steps {
                echo "Building.."
                sh '''
                echo "doing BUILDING stuff.."
                cd ./user_data/
                pip install -r requirements.txt
                cd ..
                python --version
                python -m site --user-site
                PYTHON_PATH=$(which python)
                cp -r utilities /home/jenkins/.local/lib/python3.11/site-packages/
                ls -la /home/jenkins/.local/lib/python3.11/site-packages/utilities
                '''
            }
        }
        stage('Test') {
            steps {
                echo "Testing.."
                sh '''
                echo "doing TESTING stuff.."
                python usb_run.py
                '''
            }
        }
        stage('Deliver') {
            steps {
                echo 'Deliver....'
                sh '''
                echo "doing DELIVERY stuff.."
                '''
            }
        }
    }
}
