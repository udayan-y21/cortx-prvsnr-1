# CORTX-Provisioner Deployment in Kubernetes Test Environment

## Steps to deploy CORTX STACK in Kubernetes environment
<br>

## System specifications prerequisite for CORTX Deployment  
OS  
Ensure all the nodes are installed with CentOS with 7.9 release  
```bash
CentOS Linux release 7.9 (Core)
```
<br>

System Specifications    
Please refer to this [URL](https://seagate-systems.atlassian.net/wiki/spaces/PRIVATECOR/pages/708313290/Integration+Framework+Specifications#Specifications) for the required system specifications for CORTX Deployment in kubernetes.  
<br>

Kubernetes Cluster Formation  
Use this [URL](http://eos-jenkins.mero.colo.seagate.com/job/Cortx-kubernetes/job/setup-kubernetes-cluster/) Jenkins Job to Form the Kubernetes cluster of 3 Nodes with Master node Tainted.  
<br>

## Deploy Cortx Stack on Kubernetes Environment  

Prerequisite for Deployment **(On all Nodes)** 

Run reimage.sh script to install helm, pull 3rd party as well as cortx-all docker image. Reimage script will also clean mount paths volumes inside the container. reimage.sh will by default pull cortx-all image with latest docker tag. If some custom cortx-all tag is to be tested then --tag <custom-tag> can be passed to script.
```bash
./reimage.sh
```
<br>

Deploy Provisioner Deployment POD **(Run Only on Master Node)**  

Run deploy.sh script to create cortx-deployment and Launch 1 cortx-provisioner deployment container on each POD. Once the script is executed, 3 Storage deployment POD’s will be running on 3 Nodes and 1 Control Pod will be running on master node. Each POD will have provisioner container which will execute cortx_setup config apply and cluster bootstrap commands.  
```bash
Note: Before running the deploy.sh script, In test/deploy/kubernetes/solution-config/cluster.yaml 
Make changes according to the number of nodes in the cluster.yaml and config.yaml. 

1. Below deploy.sh script will deploy provisioner container in 3-node Kubernetes cluster.

2. If More than 3-nodes deployment is to be done then create storage pod files under test/deploy/kubernetes/provisioner-pods for each node. 

3. Also, create respective PV and PVC files inside test/deploy/kubernetes/persistent-volumes and test/deploy/kubernetes/volume-claims folder. 

4. And create headless service files inside test/deploy/kubernetes/external-services folder for each storage pod.
```
```bash
./deploy.sh
```
<br>

Deploy Component Service POD's **(Run Only on Master Node)** 

```bash
Note: test/deploy/kubernetes/runtime-pods has component service pod files supporting for 3-node deployment. For more than 3-node deployment Add storage pod files with respect to a number of nodes.
```
```bash
./service.sh
```
<br>

Validate Services Startup **(On Master node)**  
```bash
# Go inside any storage pod on the cluster
kubectl exec -it storage-node1 -- /bin/bash

# Check servies status
[root@storage-node/]# hctl status
```
<br>

Basic Kubernetes Commands to Validate Deployment and cluster Formation
```bash
kubectl get nodes
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```
<br>

## Destroy ALL CORTX PODs **(On Master Node)**
```bash
./destroy.sh
```