
kubectl create ns homepage

kubectl config set-context --current --namespace homepage

helm install my-release jameswynn/homepage -f values.yaml

kubectl get services/my-release -o yaml | yq

