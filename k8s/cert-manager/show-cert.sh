# https://raymii.org/s/tutorials/Self_signed_Root_CA_in_Kubernetes_with_k3s_cert-manager_and_traefik.html

echo "Cluster Issuer"
kubectl get ClusterIssuer

echo "Cluster issuer describe"
kubectl describe ClusterIssuer -n cert-manager

echo "Certificate"
kubectl get Certificate -A

