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
                FRAME_PATH=$(pwd)
                ls -la
                cd ./user_data/
                pip install -r requirements.txt
                cd ..
                '''
            }
        }
        stage('Test') {
            steps {
                echo "Testing.."
                sh '''
                echo "doing TESTING stuff.."
                python --version
                PYTHON_PATH=$(which python)
                pwd
                cp -r utilities /home/jenkins/.local/lib/python3.11/site-packages/
                cd /usr/lib/python3.11/site-packages/
                ls -a
                cd /home/jenkins/.local/lib/python3.11/site-packages
                ls -a
                python -m site --user-site
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
