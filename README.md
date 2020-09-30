# Devo Challenge

## Prerequisites
* Docker engine
* Python >= 2.7. Preferably 3
* Flask 
* Pika 
* Pyyaml
* virtualenv

In order to accomplish all the challenge, it has been divided into three main points:
1. (Incubation): Localhost development, tools, build and deploy application, plus package python pplication to distribute over Pypi Server
2. (Dockerization): Dockerized application, continuous integration and deployment pipeline using Jenkinsfile
3. 

# 1. Incubation

## Install the RabbitMQ Server

In order to have a Web page who check the status connection of the MQ Service **running or stopped**, 
must be deployed a RabbitMQ Server

```
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

Once you have the RabbitMQ Server running and up, check it:

* Run a python virtual env in your localhost
```
virtualenv -p python3 envname
```
* Activate this virtual env
```
source envname/bin/activate
```  
* Go to devo/rabbitmq folder and type
```
python receive.py
```

Make the same above steps in other terminal to complete the tests for RabbitMQ server and finally type  
```
python send.py
```  

## Test and Deploy Web check application in your localhost

Go to dev/app and **test** the Web Check application.
```
python test.py
``` 
**Deploy** the Web Check application
```
python app.pyfinal a
```  

Go to your browser and check the Rabbit MQ Server Status
```
http://localhost:5000/
```

## Package Web Check application to install over a EC2 instance 

In order to deploy the Web Check application over a EC2 instances, just run

```
python setup.py
```

Just run in your localhost

```
devo
```

Therefore the Web Check application has been package and could be distribute like any other (pika, flask, etc) over a 
Pypi server repository and been installed like **pip install devo**.

# 2. Dockerization

In order to deploy the Web Check Application over a kubernetes or simple docker solution must be create a image deploy it over a complete pipeline in Jenkins

## Step by Step dockerization process
```
cd devo/app
docker build -f Dockerfile -t devo:latest .
docker run -p 5000:5000 devo:latest
```
That's it, now to test the app/Jenkinsfile execute the next steps:

Create a volume for Jenkins
```
docker volume create jenkins-data
```

Run Jenkins in your localhost
```
docker run         \
      -u root      \
      --rm         \
      -d           \
      -p 8080:8080 \
      -v jenkins-data:/var/jenkins_home            \
      -v /var/run/docker.sock:/var/run/docker.sock \
      --name jenkins                               \
      jenkinsci/blueocean
```

You will find jenkins on http://localhost:8080

Just to find the password:
```
docker exec -it  <id-container> /bin/bash
bash-5.0# cat /var/jenkins_home/secrets/initialAdminPassword
4c247b18af1a4d9e9bd227ba6edcf2c4 by example
```




