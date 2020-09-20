# Hands-on Jenkins-01 : Installing Jenkins on Amazon Linux 2 EC2 Instance

Purpose of the this hands-on training is to learn how to install Jenkins Server on Amazon Linux 2 EC2 instance with three different ways.

## Learning Outcomes

At the end of the this hands-on training, students will be able to;

- install and configure Jenkins Server on Amazon Linux 2 EC2 instance using `yum` repo.

- install and configure Jenkins Server on Amazon Linux 2 EC2 instance using Docker.

- install and configure Jenkins Server on Amazon Linux 2 EC2 instance using `war` file.

## Outline

- Part 1 - Installing Jenkins Server on Amazon Linux 2 with `yum` Repo

- Part 2 - Installing Jenkins Server on Amazon Linux 2 Docker

- Part 3 - Installing Jenkins Server on Amazon Linux 2 with `war` File

## Part 1 - Installing Jenkins Server on Amazon Linux 2 with `yum` Repo

- Launch an AWS EC2 instance of Amazon Linux 2 AMI with security group allowing SSH and Tomcat (8080) ports and name it as `call-jenkins`.

- Connect to the `call-jenkins` instance with SSH.

- Update the installed packages and package cache on your instance.

- Install `Java 11 openjdk` Java Development Kit.

- Check the java version.

- Add Jenkins repo to the `yum` repository.

- Import a key file from Jenkins-CI to enable installation from the package.

- Install Jenkins.

- Start Jenkins service.

- Enable Jenkins service so that Jenkins service can restart automatically after reboots.

- Check if the Jenkins service is up and running.

- Get the initial administrative password.

- Enter the temporary password to unlock the Jenkins.

- Install suggested plugins.

- Create first admin user (call-jenkins:Call-jenkins1234).

- Check the URL, then save and finish the installation.

## Part 2 - Installing Jenkins Server on Amazon Linux 2 with Docker

- Launch an AWS EC2 instance of Amazon Linux 2 AMI with security group allowing SSH and Tomcat (8080) ports and name it as `call-jenkins`.

- Connect to the `call-jenkins` instance with SSH.

- Update the installed packages and package cache on your instance.

- Install the most recent Docker Community Edition package.

- Start Docker service.

- Enable Docker service so that docker service can restart automatically after reboots.

- Check if the Docker service is up and running.

- Add the `ec2-user` to the `docker` group to run Docker commands without using `sudo`.

- Normally, the user needs to re-login into bash shell for the group `docker` to be effective, but `newgrp` command can be used activate `docker` group for `ec2-user`, not to re-login into bash shell.

- Check the Docker version without `sudo`.

- Run Docker Jenkins image from Docker Hub `Jenkins` repo.

- Get the administrator password from `var/jenkins_home/secrets/initialAdminPassword` file.

- The administrator password can also be taken from Docker logs.

- Enter the temporary password to unlock the Jenkins.

- Install suggested plugins.

- Create first admin user (call-jenkins:Call-jenkins1234).

- Check the URL, then save and finish the installation.

## Part 3 - Installing Jenkins Server on Amazon Linux 2 with `war` File

- Launch an AWS EC2 instance of Amazon Linux 2 AMI with security group allowing SSH and Tomcat (8080) ports and name it as `call-jenkins`.

- Connect to the `call-jenkins` instance with SSH.

```bash
ssh -i .ssh/call-training.pem ec2-user@ec2-3-133-106-98.us-east-2.compute.amazonaws.com
```

- Update the installed packages and package cache on your instance.

```bash
sudo yum update -y
```

- Install `Java 11 openjdk` Java Development Kit.

```bash
sudo amazon-linux-extras install java-openjdk11 -y
```

- Check the java version.

```bash
java -version
```

- Download Jenkins application.

```bash
wget http://mirrors.jenkins.io/war-stable/latest/jenkins.war
```

- Start Jenkins application.

```bash
java -jar jenkins.war --httpPort=8080
```

- Copy the admin password from log or from the file `~/.jenkins/secrets/initialAdminPassword`.

```bash
cat ~/.jenkins/secrets/initialAdminPassword
```

- Open Jenkins initial setup page from web browser using the Public DNS name of the `call-jenkins` instance using port 8080.

- Enter the temporary password to unlock the Jenkins.

- Install suggested plugins.

- Create first admin user (call-jenkins:Call-jenkins1234).

- Check the URL, then save and finish the installation.
