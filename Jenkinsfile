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
