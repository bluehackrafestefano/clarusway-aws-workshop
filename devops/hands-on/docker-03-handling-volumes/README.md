# Hands-on Docker-03 : Handling Docker Volumes

Purpose of the this hands-on training is to teach students how to handle volumes in Docker containers.

## Learning Outcomes

At the end of the this hands-on training, students will be able to;

- explain what Alpine container is and why it is widely used.

- list available volumes in Docker.

- create a volume in Docker.

- inspect properties of a volume in Docker.

- locate the Docker volume mount point.

- attach a volume to a Docker container.

- attach same volume to different containers.

- delete Docker volumes.

## Outline

- Part 1 - Launch a Docker Machine Instance and Connect with SSH

```
ssh -i ~/.ssh/kellen_clarus_ec2.pem ec2-user@ec2-54-162-106-173.compute-1.amazonaws.com
```
- Part 2 - Data Persistence in Docker Containers

- Part 3 - Managing Docker Volumes

- Part 4 - Using Same Volume with Different Containers

## Part 1 - Launch a Docker Machine Instance and Connect with SSH

- Launch a Docker machine on Amazon Linux 2 AMI with security group allowing SSH connections using the [Cloudformation Template for Docker Machine Installation](../docker-01-installing-on-ec2-linux2/docker-installation-template.yml).

- Connect to your instance with SSH.

## Part 2 - Data Persistence in Docker Containers

- Check if the docker service is up and running.

```bash
systemctl status docker

# if not running you can 

systemctl start docker
```

- Run a `alpine` container with interactive shell open, and add command to run alpine shell. 

```bash
docker run -it alpine ash
```

- Display the os release of the alpine container.

```
cat /etc/os-release
```

- Create a file named `short-life.txt` under `/home` folder

```
cd /home && touch short-life.txt && ls
```

- Exit the container and return to ec2-user bash shell.

```bash
exit
```


- Show the list of all containers available on Docker machine.

```bash
docker ps -a
```

- Start the alpine container and connect to it.

```bash
docker start <first three digits of container id / container name> && docker attach <first three digits of container id / container name>
```

- Show that the file `short-life.txt` is still there, and explain why it is there. (Container holds it data until removed).

```bash
cd /home && ls
```
- Remove the alpine container.

```bash
#Make sure you have exited the container
exit 
#Then we can use our docker commands
docker ps -a
docker rm <first three digits of container id / container name>
```

- Show the list of all containers, and the alpine container is gone with its data.

```bash
docker ps -a
```

## Part 3 - Managing Docker Volumes

- Explain why we need volumes in Docker.

- List the volumes available in Docker, since not added volume before list should be empty.

```bash
docker volume ls 
```

- Create a volume named `cw-test-vol`.

```bash 
docker volume create cw-test-volume
```

- List the volumes available in Docker, should see local volume `cw-test-vol` in the list.

```bash
docker volume ls 
```


- Show details and explain the volume `cw-test-vol`. Note the mount point: `/var/lib/docker/volumes/cw-test-vol/_data`.

```bash
docker volume inspect cw-test-volume
```

- List all files/folders under the mount point of the volume `cw-test-vol`, should see nothing listed.

```bash
sudo ls -al  /var/lib/docker/volumes/cw-test-volume/_data
```

- Run a `alpine` container with interactive shell open, name the container as `clarus`, attach the volume `cw-test-volume` to `/mountpoint` mount point in the container, and add command to run alpine shell. Here, explain `--volume` and `v` flags.

```bash
docker run -it --name volume-container -v cw-test-volume:/mountpoint alpine ash
```

- List files/folder in `clarus` container, show mounting point `/mountpoint`, and explain the mounted volume `cw-test-volume`.

```bash 
ls -la /mountpoint
```

- Create a file in `clarus` container under `/mountpoint` folder.

```bash
cd /mountpoint && echo "This file is created in the container volume-container" > i-will-persist.txt
```

- List the files in `/mountpoint` folder, and show content of `i-will-persist.txt`.

```bash
ls && cat i-will-persist.txt
```

- Exit the `clarus` container and return to ec2-user bash shell.

```bash
exit
```

- Show the list of all containers available on Docker machine.

```bash 
docker ps -a
```

- Remove the `clarus` container.

```bash
docker rm volume-container
```

- Show the list of all containers, and the `clarus` container is gone.

```bash 
docker ps -a
```

- List all files/folders under the volume `cw-test-vol`, show that the file `i-will-persist.txt` is there.

```bash
sudo ls -al  /var/lib/docker/volumes/cw-test-volume/_data && sudo cat /var/lib/docker/volumes/cw-test-volume/_data/i-will-persist.txt
```

## Part 4 - Using Same Volume with Different Containers

- Run a `alpine` container with interactive shell open, name the container as `second-volume-container`, attach the volume `cw-test-vol` to `/secondmountpoint` mount point in the container, and add command to run alpine shell.

```bash
docker run -it --name second-volume-container -v cw-test-volume:/second
point alpine ash
```

- List the files in `/secondmountpoint` folder, and show that we can reach the file `i-will-persist.txt`.

```bash
ls -l /secondmountpoint && cat /secondmountpoint/i-will-persist.txt
```

- Create an another file in `second-volume-container` container under `/secondmountpoint` folder.

```bash
#To see what mountpoints are available to us we can check:
ls /
cd secondmountpoint && echo "This is a file of the container second-volume-container" > loadmore.txt
```

- List the files in `/mountpoint` folder, and show content of `loadmore.txt`.

```bash
ls && cat loadmore.txt
```

- Exit the `second-volume-container` container and return to ec2-user bash shell.

```bash 
exit
```

- Run a `ubuntu` container with interactive shell open, name the container as `third-volume-container`, attach the volume `cw-test-volume` to `/thirdmountpoint` mount point in the container, and add command to run bash shell.

```bash
docker run -it --name third-volume-container -v cw-test-volume:/thirdmountpoint ubuntu bash
```

- List the files in `/thirdmountpoint` folder, and show that we can reach the all files created earlier.

```bash
ls -l /thirdmountpoint
```

- Create an another file in `third-volume-container` container under `/thirdmountpoint` folder.

```bash
cd thirdmountpoint && touch file-from-3rd.txt && ls
```

- Exit the `third-volume-container` container and return to ec2-user bash shell.

```bash
exit
```

- Run an another `ubuntu` container with interactive shell open, name the container as `fourth-volume-container`, attach the volume `cw-test-volume` as read-only to `/fourthmountpoint` mount point in the container, and add command to run bash shell.

```bash
docker run -it --name fourth-volume-container -v cw-test-volume:/fourthmountpoint:ro ubuntu bash
```

- List the files in `/fourthmountpoint` folder, and show that we can reach the all files created earlier.

```bash
ls -l /fourthmountpoint
```

- Try to create an another file under `/mountpoint4th` folder. Should see error `read-only file system`

```bash
cd fourthmountpoint && touch file-from-4th.txt
```

- Exit the `clarus4th` container and return to ec2-user bash shell.

```bash
exit
```

- List all containers.

```bash 
docker ps -a 
```

- Delete `second-volume-container`, `third-volume-container` and `fourth-volume-container` containers.

```bash
docker rm second-volume-container third-volume-container fourth-volume-container

#Check that they are gone 
docker ps -a 
```

- Delete `cw-test-volume` volume.

```bash
docker volume rm cw-test-volume

#Check that the volume is gone 
docker volume ls 
```
