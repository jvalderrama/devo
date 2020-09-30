# Devo Challenge

## Prerequisites
* Docker engine
* Python >= 2.7. Preferably 3
* Flask 
* Pika 
* Pyyaml
* virtualenv
* Ansible
* Terraform

In order to accomplish the entire challenge, it has been divided into three main points/parts:
1. **Incubation**: Localhost development, tools, build and deploy application, plus package python application to distribute over a Pypi Server/Repository
2. **Dockerization**: Dockerized application, continuous integration and deployment pipeline using a Jenkinsfile, tested over local Jenkins
3. **IaC and K8s**: Ansible to update host/port configuration application file for RabbitMQ Server, Terraform for EC2 instance, Templates for k8s and Helm Chart

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
* Go to **devo/rabbitmq** folder and type
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
python app.py
```  

Go to your browser and check the Rabbit MQ Server Status
```
http://localhost:5000/
```

## Package Web Check application to install over an EC2 instance 

In order to deploy the Web Check application over an EC2 instances just run.
Note: See section [3. IaC and K8s](https://github.com/jvalderrama/devo#EC2-Instance) in order to deploy an
 EC2 instance with Terraform). 

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

In order to deploy the Web Check Application over a kubernetes or simple docker solution must be created an image 
to deploy it over a complete Jenkins pipeline

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

Configure your Multibranch Job I - Repository

![Jenkins Multibranch Configuration 1](/images/MultibranchJobConfiguration1.png)

Configure your Multibranch Job II - Jenkinsfile

![Jenkins Multibranch Configuration 2](/images/MultibranchJobConfiguration2.png)

Execute with Jenkins pipeline with any change made in the repository

![Jenkins Pipeline_Execution](/images/PipelineExecution.png)

# 3. IaC and K8s

In order to update the host/port configuration application file for RabbitMQ Server has been created an Ansible recipe 
who can be parametrized with hosts/port and also a destination, but at the same time it has its own **defaults** 
configuration variables and can be managed through and **static** or **template** file generated.

## Run the playbook

Got to **devo/ansible** folder and run the next command, before it check the file **all.yaml** to define your custom variables

```
ansible-playbook -i hosts.yaml all.yaml --connection=local -vv
```   

Executed playbook

![Jenkins Pipeline_Execution](/images/UpdateRabbitMQConfigFile.png)

## EC2 Instance

By other hand a EC2 instance needs to be created, therefore a terraform recipe is given:

Go to **devo/terraform** folder

1. Create main file (AWS provider with credentials)
2. Create a VPC on AWS
3. Create EC2 instances over VPC
4. Output public IP once the instance has been created

Just type
```
terraform init
terraform plan
terraform apply

```

## K8s and Chart Deployment

In order to deploy the Web Check Application over a kubernetes cluster in HA has been created a set of templates:
The HA is guaranteed using **PodAntiaffinity** k8s feature, it means who at least the Deployment is going to deploy 
**two or more replicas in different nodes in the cluster**, not just two or more replicas in a single node.

HA in K8s Deployment

![Jenkins Pipeline_Execution](/images/HA-devo-appi.png)


Go to folder **devo/k8s** and execute. 
NOTE: A kubeconfig file must be exists and kubectl client installed on your localhost, it assumes the docker images 
has been pushed to **devo-repo/devo:latest**

```
kubectl apply -f app.yaml
``` 

For high workload capacity has been created and HPA (Horozontal Pod Autoscaler) for the deployment and an Ingress to 
access per DNS (See devo/k8s/1app.yaml)

Finally in order to create a Chart for Helm, please read the next training course created by me who guides to accomplish
this feature: [3. Packages Helm apps](https://github.com/jvalderrama/helm-training)

## Conclusions

1. Has been created and API application who check the status (running or stopped) of a RabbitMQ Server, the first part demonstrates
how to create the API using `Flask framework` and a `configuration file for RabbitMQ server`, the application has its own 
tests and has been tested against a RabbitMQ server who is running as docker container.

2. The API application can be installed and package as `PIP distribution (setup.py)`, therefore once an `EC2 instances` is created 
with `Terrraform` (no tested yet), the API application can be installed like `pip install devo` over the EC2 instances 
without any container or image.

3. Once made the above a second parts demonstrates a complete pipeline created to `dockerized` and deploy the 
application like a docker container. It has been accomplish through a `Dockerfile, requirements file` and a 
`Jenkinsfile (Declarative Pipeline)` tested over a local `Jenkins installation from scratch`.

4. The third part demonstrates an `ansible recipe` created and tested to update de host/port/destination of the API application
configuration file, along with a `Terraform recipe to crate EC2 instances with its VPC`.

5. A `kubernetes deployment` has been provided assuming the `push` of the previous docker images to a Devo repository, 
generated and guaranteed a minimum number of pods in different workers nodes in the K8s cluster to have a `first HA approach 
for the API application using the PodAntiaffinity` feature and using a 'infrastructure' namespace. Finally a `Pod elasticity` 
has been created in order to attend high or low demand of the service using `HPA` resource with its corresponding `Ingress resource`. 

6. Finally a guide is given to create a `Helm Chart` for the API application, and ansible can be used as before to deploy the k8s templates
in a Jenkins pipeline as well.

## References

* https://www.rabbitmq.com/download.html
* https://martin-thoma.com/configuration-files-in-python/
* https://docs.python-guide.org/shipping/packaging/
* https://github.com/jvalderrama/helm-training
* https://serversforhackers.com/c/an-ansible2-tutorial
* https://github.blog/2013-01-31-relative-links-in-markup-files/
* https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#more-practical-use-cases  