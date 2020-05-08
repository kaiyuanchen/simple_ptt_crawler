pipeline {

    agent {
        dockerfile {
            filename "Dockerfile"
            additionalBuildArgs "--build-arg BRANCH_NAME=master"
        }
    }

    environment {
        HOME = "${env.WORKSPACE}"
    }

    stages {
        stage('build') {
            steps {
                sh "pip install -r requirements.txt --user"
                sh 'pip install pytest  --user'
                sh 'pip install pytest-cov --user'
                sh 'pip install flake8 --user'
            }
        }

        stage('test') {
            steps {
                 sh 'python -m pytest\
                  --cov-config=.coveragerc\
                  --cov-report xml:coverage.xml\
                  --cov=./ test/'
            }
        }

        stage("final") {
            steps {
                cobertura(
                    coberturaReportFile: 'coverage.xml',
                    classCoverageTargets: '0, 0, 0')
            }
        }
    }
}