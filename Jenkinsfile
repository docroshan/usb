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
                echo "Building..."
                sh '''
                echo "doing BUILDING stuff.."
                cd ./user_data/
                pip install -r requirements.txt
                cd ..
                python --version
                cp -r utilities /home/jenkins/.local/lib/python3.11/site-packages/
                '''
            }
        }
        stage('Test') {
            steps {
                echo "Testing..."
                sh '''
                echo "doing TESTING stuff.."
                python usb_run.py
                ls -la results
                cat output.log
                ls -la
                '''
            }
        }
    }
}
