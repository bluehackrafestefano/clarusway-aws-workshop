# Hands-on Kubernetes-03 : Handling Pods, Volumes, Networking and Service Discovery

Purpose of the this hands-on training is to give students the knowledge of Kubernetes Volumes and Services.

## Learning Outcomes

At the end of the this hands-on training, students will be able to;

- Explain the need for persistent data management.

- Learn `Persistent Volumes` and `Persistent Volume Claims`.

- Explain the benefits of logically grouping `Pods` with `Services` to access an application.

- Explore the service discovery options available in Kubernetes.

- Learn different types of Services in Kubernetes.

## Outline

- Part 1 - Setting up the Kubernetes Cluster

- Part 2 - Kubernetes Volume Persistence

- Part 3 - Services, Load Balancing, and Networking in Kubernetes

## Part 1 - Setting up the Kubernetes Cluster

- Launch a Kubernetes Cluster of Ubuntu 20.04 with two nodes (one master, one worker) using the [Cloudformation Template to Create Kubernetes Cluster](./cfn-template-to-create-k8s-cluster.yml). *Note: Once the master node up and running, worker node automatically joins the cluster.*

>*Note: If you have problem with kubernetes cluster, you can use this link for lesson.*
>https://www.katacoda.com/courses/kubernetes/playground

- Check if Kubernetes is running and nodes are ready.

```bash

```

## Part 2 - Kubernetes Volume Persistence

- Get the documentation of `PersistentVolume` and its fields. Explain the volumes, types of volumes in Kubernetes and how it differs from the Docker volumes. [Volumes in Kubernetes](https://kubernetes.io/docs/concepts/storage/volumes/)

```bash

```

- Log into the `kube20-worker-1` node, create a `pv-data` directory under home folder, also create an `index.html` file with `Welcome to Kubernetes persistence volume lesson` text and note down path of the `pv-data` folder.

```bash

```

- Log into `kube20-master` node, create a `clarus-pv.yaml` file using the following content with the volume type of `hostPath` to build a `PersistentVolume` and explain fields.

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: clarus-pv-vol
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/home/ubuntu/pv-data"
```

- Create the PersistentVolume `clarus-pv-vol`.

```bash

```

- View information about the `PersistentVolume` and notice that the `PersistentVolume` has a `STATUS` of available which means it has not been bound yet to a `PersistentVolumeClaim`.

```bash

```

- Get the documentation of `PersistentVolumeClaim` and its fields.

```bash

```

- Create a `clarus-pv-claim.yaml` file using the following content to create a `PersistentVolumeClaim` and explain fields.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: clarus-pv-claim
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

- Create the PersistentVolumeClaim `clarus-pv-claim`.

```bash

```

> After we create the PersistentVolumeClaim, the Kubernetes control plane looks for a PersistentVolume that satisfies the claim's requirements. If the control plane finds a suitable `PersistentVolume` with the same `StorageClass`, it binds the claim to the volume. Look for details at [Persistent Volumes and Claims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#introduction)

- View information about the `PersistentVolumeClaim` and show that the `PersistentVolumeClaim` is bound to your PersistentVolume `clarus-pv-vol`.

```bash

```

- View information about the `PersistentVolume` and show that the PersistentVolume `STATUS` changed from Available to `Bound`.

```bash

```

- Create a `clarus-pod.yaml` file that uses your PersistentVolumeClaim as a volume using the following content.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: clarus-pod
spec:
  volumes:
    - name: clarus-pv-storage
      persistentVolumeClaim:
        claimName: clarus-pv-claim
  containers:
    - name: clarus-pv-container
      image: nginx
      ports:
        - containerPort: 80
          name: "http-server"
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: clarus-pv-storage
```

- Create the Pod `clarus-pod`.

```bash

```

- Verify that the Pod is running.

```bash

```

- Open a shell to the container running in your Pod.

```bash

```

- Verify that `nginx` is serving the `index.html` file from the `hostPath` volume.

```bash

```

- Log into the `kube20-worker-1` node, change the `index.html`.

```bash

```

- Log into the `kube20-master` node, check if the change is in effect.

```bash

```

- Delete the `Pod`, the `PersistentVolumeClaim` and the `PersistentVolume`.

```bash

```

## Part 3 - Services, Load Balancing, and Networking in Kubernetes

Kubernetes networking addresses four concerns:

- Containers within a Pod use networking to communicate via loopback.

- Cluster networking provides communication between different Pods.

- The Service resource lets you expose an application running in Pods to be reachable from outside your cluster.

- You can also use Services to publish services only for consumption inside your cluster.

### Service

An abstract way to expose an application running on a set of Pods as a network service.

With Kubernetes you don't need to modify your application to use an unfamiliar service discovery mechanism.

Kubernetes gives Pods their own IP addresses and a single DNS name for a set of Pods, and can load-balance across them.

### Motivation

Kubernetes Pods are mortal. They are born and when they die, they are not resurrected. If you use a Deployment to run your app, it can create and destroy Pods dynamically.

Each Pod gets its own IP address, however in a Deployment, the set of Pods running in one moment in time could be different from the set of Pods running that application a moment later.

### Service Discovery

The basic building block starts with the Pod, which is just a resource that can be created and destroyed on demand. Because a Pod can be moved or rescheduled to another Node, any internal IPs that this Pod is assigned can change over time.

If we were to connect to this Pod to access our application, it would not work on the next re-deployment. To make a Pod reachable to external networks or clusters without relying on any internal IPs, we need another layer of abstraction. K8s offers that abstraction with what we call a `Service Deployment`.

`Services` provide network connectivity to Pods that work uniformly across clusters.
K8s services provide discovery and load balancing. `Service Discovery` is the process of figuring out how to connect to a service.

- Service Discovery is like networking your Containers.

- DNS in Kubernetes is an `Built-in Service` managed by `Kube-DNS`.

- DNS Service is used within PODs to find other services running on the same Cluster.

- Multiple containers running with-in same POD don’t need DNS service, as they can contact each other.

- Containers within same POD can connect to other container using `PORT` on `localhost`.

- To make DNS work POD always need `Service Definition`.

- Kube-DNS is a database containing key-value pairs for lookup.

- Keys are names of services and values are IP addresses on which those services are running.

### Defining and Deploying Services

- Let's define a setup to observe the behaviour of `services` in Kubernetes and how they work in practice.

- First, define `development` namespace using `development-namespace.yml` file.

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: development
```

- Then, define `production` namespace using `production-namespace.yml` file.

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
```

- Create the `development` and `production` namespaces.

```bash
kubectl apply -f web-flask-development.yaml
kubectl apply -f web-flask-production.yaml
```

- Create `yaml` file named `web_flask_dev.yaml` for `development` namespace and explain fields of it.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-flask-deploy
  namespace: development
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-flask
  minReadySeconds: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  template:
    metadata:
      labels:
        app: web-flask
    spec:
      containers:
      - name: web-flask-pod
        image: clarusways/cw_web_flask1
        ports:
        - containerPort: 5000
```

- Create `yaml` file named `web_flask_prod.yaml` for `production` namespace.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-flask-deploy
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-flask
  minReadySeconds: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  template:
    metadata:
      labels:
        app: web-flask
    spec:
      containers:
      - name: web-flask-pod
        image: clarusways/cw_web_flask1
        ports:
        - containerPort: 5000
```

- Create the apps `development` and `production` Deployments.
  
```bash
kubectl apply -f web-flask-development.yaml
kubectl apply -f web-flask-production.yaml
```

- Show the Pods detailed information in all namespaces and learn their IP addresses:

```bash
kubectl get deployments --all-namespaces
```

- We get an output like below.

```text
NAMESPACE     NAME                                       READY   STATUS    RESTARTS   AGE   IP               NODE
development   web-flask-deploy-7cbb5f5967-24smj          1/1     Running   0          15m   172.16.166.175   node1
development   web-flask-deploy-7cbb5f5967-94g6f          1/1     Running   0          15m   172.16.166.177   node1
development   web-flask-deploy-7cbb5f5967-gjtkx          1/1     Running   0          15m   172.16.166.176   node1
production    web-flask-deploy-7cbb5f5967-9gfzr          1/1     Running   0          15m   172.16.166.178   node1
production    web-flask-deploy-7cbb5f5967-jjktk          1/1     Running   0          15m   172.16.166.179   node1
production    web-flask-deploy-7cbb5f5967-rhngt          1/1     Running   0          15m   172.16.166.180   node1
```

In the output above, for each Pod the IPs are internal and specific to each instance. If we were to redeploy the application, then each time a new IP will be allocated.

We now check we can ping a Pod inside the cluster.

- Create a `forping.yaml` file to create a Pod in default namespace that pings a Pod inside the cluster.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: for-ping
  namespace: default
spec:
  containers:
  - name: for-ping
    image: clarusways/for-ping
    imagePullPolicy: IfNotPresent
  restartPolicy: Always
```

- Create a `for-ping` pod and log into the container.

```bash
kubectl apply -f forping.yaml 
kubectl exec -it for-ping bash

#You can kubectl get pods --all-namespaces -o wide to get a list of the internal ips of all your running pods. We will use this internal IP to attempt a ping. 
#172.16.210.166


```

- Get the documentation of `Services` and its fields.

```bash
kubectl explain svc
```

- Create a `web-svc-development.yaml` file with following content and explain fields of it.

```yaml
apiVersion: v1
kind: Service   # (1)
metadata:
  name: web-flask-svc
  namespace: development
  labels:
    app: web-flask
spec:
  type: NodePort   # (2)
  ports:
  - port: 5000   # (3)
    targetPort: 5000
  selector:
    app: web-flask   # (4)
```

- Create a `web-svc-production.yaml` file with following content.

```yaml
apiVersion: v1
kind: Service   # (1)
metadata:
  name: web-flask-svc
  namespace: production
  labels:
    app: web-flask
spec:
  type: NodePort   # (2)
  ports:
  - port: 5000   # (3)
    targetPort: 5000
  selector:
    app: web-flask   # (4)
```

>Explanation
>
>(1) We define the kind of workload to be a Service.
>
>(2) We define the Service type to be a `NodePort`. This means that it uses the Node IP and a static port to expose the service outside the cluster.
>
>Other options:
>
>- `ClusterIP`: It makes the Service only reachable from within the cluster.
>
>- `LoadBalancer`: It exposes the service externally using a cloud provider’s load balancer.
>
>- `ExternalName`: It maps a Service to a DNS name that we configure elsewhere.
>
>(3) This is the port to expose to the external network.
>
>(4) This is the name of the deployment that we want to connect to.

- Create the Services.
  
```bash
kubectl apply -f web-svc-development.yaml
kubectl apply -f web-svc-production.yaml
```

- List the services.

```bash
kubectl get svc -o wide --all-namespaces
```

```text
NAMESPACE     NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                  AGE     SELECTOR
default       kubernetes      ClusterIP   10.96.0.1       <none>        443/TCP                  4h39m   <none>
development   web-flask-svc   NodePort    10.98.173.110   <none>        5000:32178/TCP           28m     app=web-flask
kube-system   kube-dns        ClusterIP   10.96.0.10      <none>        53/UDP,53/TCP,9153/TCP   4h39m   k8s-app=kube-dns
production    web-flask-svc   NodePort    10.105.28.86    <none>        5000:32050/TCP           28m     app=web-flask
```

- Kubernetes exposes the service in a random port within the range 30000-32767 using the Node’s primary IP address.

- Display information about the `web-flask-svc` Service in `production` namespace and note down the `NodePort` of the service which is `32050` in our case.

```bash
kubectl describe svc web-flask-svc -n production
```

```text
Name:                     web-flask-svc
Namespace:                production
Labels:                   app=web-flask
Annotations:              <none>
Selector:                 app=web-flask
Type:                     NodePort
IP:                       10.105.28.86
Port:                     <unset>  5000/TCP
TargetPort:               5000/TCP
NodePort:                 <unset>  32050/TCP
Endpoints:                172.16.210.142:5000,172.16.210.143:5000,172.16.210.144:5000
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>
```

- We can visit `http://<public-node-ip>:<node-port>` and access the application again. Note: Do not forget to open the Port `<node-port>` in the security group of your node instance.

### Endpoints

As Pods come-and-go (scaling up and down, failures, rolling updates etc.), the Service dynamically updates its list of Pods. It does this through a combination of the label selector and a construct called an Endpoint object.

Each Service that is created automatically gets an associated Endpoint object. This Endpoint object is a dynamic list of all of the Pods that match the Service’s label selector.

Kubernetes is constantly evaluating the Service’s label selector against the current list of Pods in the cluster. Any new Pods that match the selector get added to the Endpoint object, and any Pods that disappear get removed. This ensures the Service is kept up-to-date as Pods come and go.

- Get the documentation of `Endpoints` and its fields.

```bash
kubectl explain ep
```

- List the Endpoints.

```bash
kubectl get ep -o wide --all-namespaces
```

- Scale the deployment up to ten replicas and list the `Endpoints` in development namespace.

```bash
kubectl scale deploy web-flask-deploy --replicas=10 --namespace=development
```

- List the `Endpoints` and explain that the Service has an associated `Endpoint` object with an always-up-to-date list of Pods matching the label selector.

```bash
kubectl get ep -o wide --all-namespaces
```

> Open a browser on any node and explain the `loadbalancing` via browser. (Pay attention to the host ip and node name and note that `host ips` and `endpoints` are same)
>
> http://[public-node-ip]:[node-port]

### Labels and loose coupling

- Pods and Services are loosely coupled via labels and label selectors. For a Service to match a set of Pods, and therefore provide stable networking and load-balance, it only needs to match some of the Pods labels. However, for a Pod to match a Service, the Pod must match all of the values in the Service’s label selector.

- Add `version: v1` to `web-svc-development.yaml --> spec.selector`. So that you end up with:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-flask-svc
  namespace: development
  labels:
    app: web-flask
spec:
  type: NodePort
  ports:
  - port: 5000
    targetPort: 5000
  selector:
    app: web-flask
    version: v1
```

- Use kubectl apply to push your configuration changes to the cluster.

```bash

```

- Reload the page, and see that we can not see the page because of that the Service is selecting on two labels, but the Pods only have one of them. The logic behind this is a Boolean `AND` operation.

- Add `version: v1` to `web-flask-development.yaml --> spec.template.metadata.labels`. So that you end up with:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-flask-deploy
  namespace: development
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-flask
  minReadySeconds: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  template:
    metadata:
      labels:
        app: web-flask
        version: v1
    spec:
      containers:
      - name: web-flask-pod
        image: clarusways/cw_web_flask1
        ports:
        - containerPort: 5000
```

- Use kubectl apply to push your configuration changes to the cluster.

```bash

```

- Reload the page again, and now we can see the page because the `Service` is selecting on two labels and the Pods have all of them.

- Add `test: coupling` to `web-flask-development.yaml --> spec.template.metadata.labels`. So that you end up with:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-flask-deploy
  namespace: development
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-flask
  minReadySeconds: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  template:
    metadata:
      labels:
        app: web-flask
        version: v1
        test: coupling
    spec:
      containers:
      - name: web-flask-pod
        image: clarusways/cw_web_flask1
        ports:
        - containerPort: 5000
```

- Push your configuration changes to the cluster.

```bash

```

- Reload the page again, and we see the page although the `Pods` have additional labels that the `Service` is not selecting on.
