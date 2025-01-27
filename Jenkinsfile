pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run BDD Tests') {
            steps {
                sh 'pytest tests/test.py --junitxml=results.xml.xml --hide_browser
            }
        }
    }
}