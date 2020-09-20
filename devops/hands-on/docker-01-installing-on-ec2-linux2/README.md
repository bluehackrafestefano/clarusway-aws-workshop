# Hands-on Docker-01 : Installing Docker on Amazon Linux 2 AWS EC2 Instance

Purpose of the this hands-on training is to teach the students how to install Docker on on Amazon Linux 2 EC2 instance.

## Learning Outcomes

At the end of the this hands-on training, students will be able to;

- install Docker on Amazon Linux 2 EC2 instance

- configure a Cloudformation template for creating a Docker machine

## Outline

- Part 1 - Launch Amazon Linux 2 EC2 Instance and Connect with SSH

- Part 2 - Install Docker on Amazon Linux 2 EC2 Instance

- Part 3 - Configure a Cloudformation Template for a Docker machine

## Part 1 - Launch Amazon Linux 2 EC2 Instance and Connect with SSH

- Launch an EC2 instance using the Amazon Linux 2 AMI with security group allowing SSH connections.

- Connect to your instance with SSH.

## Part 2 - Install Docker on Amazon Linux 2 EC2 Instance

- Update the installed packages and package cache on your instance.

- Install the most recent Docker Community Edition package.

- Start docker service.

- Enable docker service so that docker service can restart automatically after reboots.

- Check if the docker service is up and running.

- Add the `ec2-user` to the `docker` group to run docker commands without using `sudo`.

- Normally, the user needs to re-login into bash shell for the group `docker` to be effective, but `newgrp` command can be used activate `docker` group for `ec2-user`, not to re-login into bash shell.

- Check the docker version without `sudo`.

- Check the docker info without `sudo`.

## Part 3 - Configure a Cloudformation Template for a Docker machine

- Write and configure a Cloudformation Template to have a Docker machine ready on Amazon Linux 2 EC2 Instance with security group allowing SSH connections from anywhere.
