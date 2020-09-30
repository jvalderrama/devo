pipeline {

  agent { docker { image 'python:3.7.2' } }

  stages {

    stage('Build') {
      steps {
          sh 'pip install -r requirements.txt'
      }
    }

    stage('Unit Test') {
      steps {
        //sh 'python test.py'
      }
    } 

    stage('Build docker image') {
        steps {
            sh "docker build -f Dockerfile -t devo:latest ."
        }
    }

    stage('Deploy container') {
        steps {
          sh "docker stop devo || true"
          sh "docker run -p 5000:5000 devo:latest"
        }
    }
  }
}
