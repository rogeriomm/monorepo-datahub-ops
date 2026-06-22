 - Delete all pods in the "ContainerStatusUnknown" state across all namespaces
```shell
status='ContainerStatusUnknown'
kubectl get pods --all-namespaces | grep ${status} | awk '{print $2 " -n " $1}' | xargs -L 1 kubectl delete pod
```