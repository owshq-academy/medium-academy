# Kubernetes & Apache Kafka ~ Strimzi

* [Minikube download & installation](https://minikube.sigs.k8s.io/docs/start/?arch=%2Fmacos%2Farm64%2Fstable%2Fbinary+download)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)

```shell
# Minikube with Docker Driver for local development 
minikube start --driver=docker
# enable loadbalancer as localhost (WARN = Dont use the same port in this local env)
minikube tunnel
```

### create namespace
```sh
# create namespace
kubectl create namespace ingestion
```
### add & update repositories
```sh
# add & update helm list repo
helm repo add strimzi https://strimzi.io/charts/
helm repo update
```

## Ingestion

```sh
### install crd's [custom resources]
# strimzi
helm install kafka strimzi/strimzi-kafka-operator --namespace ingestion --version 0.43.0
```

```sh
kubens ingestion

#  kraft deployment without volume
kubectl apply -f deployment/strimzi/broker/kafka-kraft-ephemeral.yaml -n ingestion

# schema registry
helm install schema-registry deployment/strimzi/cp-schema-registry --namespace ingestion

# load balancers
kubectl apply -f deployment/strimzi/services/svc-lb-schema-registry.yaml -n ingestion
```