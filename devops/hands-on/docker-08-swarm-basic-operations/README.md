# Hands-on Docker-08 : Docker Swarm Basic Operations

Purpose of the this hands-on training is to give students the understanding to the Docker Swarm basic operations.

## Learning Outcomes

At the end of the this hands-on training, students will be able to;

- Explain the what Docker Swarm cluster is.

- Set up a Docker Swarm cluster.

- Deploy an application as service on Docker Swarm.

- Do basic service operations within the Swarm cluster.

- Manage services within the Swarm.

## Outline

- Part 1 - Launch Docker Machine Instances and Connect with SSH

- Part 2 - Set up a Swarm Cluster with Manager and Worker Nodes

- Part 3 - Managing Docker Swarm Services

## Part 1 - Launch Docker Machine Instances and Connect with SSH

- Launch `five` Compose enabled Docker machines on Amazon Linux 2 with security group allowing SSH connections using the of [Clarusway Docker Swarm Cloudformation Template](./clarusway-docker-swarm-cfn-template.yml).

- Connect to your instances with SSH.

```bash
ssh -i .ssh/call-training.pem ec2-user@ec2-3-133-106-98.us-east-2.compute.amazonaws.com
```

## Part 2 - Set up a Swarm Cluster with Manager and Worker Nodes

- Prerequisites (Those prerequisites are satisfied within cloudformation template in Part 1)

  - Five EC2 instances on Amazon Linux 2 with `Docker` and `Docker Compose` installed.

  - Set these ingress rules on your EC2 security groups:

    - HTTP port 80 from 0.0.0.0\0

    - TCP port 2377 from 0.0.0.0\0

    - TCP port 8080 from 0.0.0.0\0

    - SSH port 22 from 0.0.0.0\0 (for increased security replace this with your own IP)

- Check if the docker is active or not from the list of docker info (should be inactive at first).

```bash
docker info
```

- Get the internal IP addresses of docker machines,  you find out the Private IPs either on the EC2 dashboard, or from the command line by running the following command. Response should be something like `172.31.42.71`.

```bash
hostname -i
```

- Initialize `docker swarm` with Private IP and assign your first docker machine as manager:

```bash
docker swarm init
# or
docker swarm init --advertise-addr <Private IPs>
```

- Check if the `docker swarm` is active or not and explain the swarm part of `docker info`.

```bash
docker info
```

- Add 2 more nodes as manager to improve fault-tolerance. It is recommended to create clusters with an odd number of managers in Swarm, because a majority vote is needed between managers to agree on proposed management tasks according to `Raft Algorithm`. An odd—rather than even—number is strongly recommended to have a tie-breaking consensus. Having two managers is actually worse than having one.

- Get the manager token with `docker swarm join-token manager` command.

```bash
docker swarm join-token manager
```

- Add second and third Docker Machine instances as manager nodes, by connecting with SSH and running the given command above.

```bash
docker swarm join --token <manager_token> <manager_ip>:2377
```

- Add fourth and fifth Docker Machine instances as worker nodes. (Run `docker swarm join-token worker` command to get join-token for worker, if needed)

```bash
docker swarm join --token <worker_token> <manager_ip>:2377
```

- List the connected nodes in `Swarm` and explain difference between leader and other managers.

```bash
# SSH into a manager node then:
docker node ls
```

## Part 3 - Managing Docker Swarm Services

> :warning: Note: If you have problem with `docker swarm` installation, you can use following link for lesson.
https://labs.play-with-docker.com

- Create a service for visualization and check if the visualizer is running by entering `http://<ec2-host-name>:8080` in a browser. (Nothing should be running)

```bash
docker service create \
  --name=viz \
  --publish=8080:8080/tcp \
  --constraint=node.role==manager \
  --mount=type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock \
  dockersamples/visualizer
```

- Check if the visualizer is running by entering `http://<ec2-host-name-of-manager-node>:8080` in a browser. (Should be showing only viz app on manager node)

- Start a `nginx service` with 5 replicas and show the replicas running on visualizer.

```bash
docker service create --name webserver --replicas=5 -p 80:80 -d nginx
```

- List services, explain what service is and the difference between container and service.

```bash
docker service ls 
```

- Check if the `Nginx Web Server` is running by entering `http://<ec2-host-name-of-any-node>` in a browser.

- Display detailed information on service.

```bash
docker service inspect --pretty webserver
```

- List the tasks of service and explain what task is.

```bash
docker service ps webserver
```

- Fetch the logs of the service or a task.

```bash
docker service logs webserver
```

- Reboot a worker node and explain the last situation on visualizer app.

```bash
sudo reboot -f 
```

- Scale up services and show the changes on visualizer app.

```bash
docker service scale webserver=10
```

- Scale down services and show the changes on visualizer app.

```bash
docker service scale webserver=0
docker service scale webserver=3
```

- Remove service and show the changes on visualizer app.

```bash
docker service rm webserver
```

- Create service in `global mod`, show the changes on visualizer app and explain `global mod`.

```bash
docker service create --name glbserver --mode=global -p 80:80 nginx
```

- Remove a container and show that swarm creates a new task immediately.

```bash
docker container rm -f <containerid>
docker service ps glbserver
```

- Leave worker nodes from swarm and show the changes on visualizer app.

```bash
docker swarm leave
```

- Remove the `glbserver` service.

```bash
docker service rm glbserver
```

- Leave manager nodes from swarm

```bash
docker swarm leave --force
```

- Leave worker nodes from swarm.

```bash
docker swarm leave
```
