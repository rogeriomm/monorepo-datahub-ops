kubectl config set-context argo-cd \
  --cluster=$(kubectl config current-context | xargs -I{} kubectl config get-contexts {} --no-headers | awk '{print $3}') \
  --user=$(kubectl config current-context | xargs -I{} kubectl config get-contexts {} --no-headers | awk '{print $4}') \
  --namespace=argo-cd