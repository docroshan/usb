pipeline {
    agent { 
        node {
            label 'docker-agent-python'
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
                python3 -m venv myenv
                source myenv/bin/activate
                python --version
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
                pwd
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
