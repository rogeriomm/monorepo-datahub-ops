# https://raymii.org/s/tutorials/Self_signed_Root_CA_in_Kubernetes_with_k3s_cert-manager_and_traefik.html

kubectl get ClusterIssuer

kubectl get Certificate -A


kubectl describe ClusterIssuer -n cert-manager
