#!/usr/bin/env zsh

TEMP_DIR=$(mktemp -d)
CA_FILE="$TEMP_DIR/ca.crt"

configure_k3s() {
  sudo mkdir -p /etc/rancher/k3s/certs.d/harbor.ing.vm.pvel.worldl.xpt
  sudo touch /etc/rancher/k3s/certs.d/harbor.ing.vm.pvel.worldl.xpt/ca.crt
  sudo cp "$CA_FILE" /etc/rancher/k3s/certs.d/harbor.ing.vm.pvel.worldl.xpt/ca.crt
  gum confirm "Restart K3S?" && \
    gum spin --spinner dot --title "Restarting K3S..." -- sudo systemctl restart k3s \
    || echo "K3S not restarted"
}

configure_docker() {
  sudo mkdir -p /etc/docker/certs.d/harbor.ing.vm.pvel.worldl.xpt
  sudo touch /etc/docker/certs.d/harbor.ing.vm.pvel.worldl.xpt/ca.crt
  sudo cp "$CA_FILE" /etc/docker/certs.d/harbor.ing.vm.pvel.worldl.xpt/ca.crt

  gum confirm "Restart Docker?" && \
    gum spin --spinner dot --title "Restarting Docker..." -- sudo systemctl restart docker \
    || echo "Docker not restarted"
}

configure_host() {
  sudo cp "$CA_FILE" /usr/local/share/ca-certificates/harbor.crt
  sudo update-ca-certificates
}

echo "$CA_FILE"
#wget --no-check-certificate https://harbor.ing.vm.pvel.worldl.xpt/api/v2.0/systeminfo/getcert -O /tmp/ca.crt

kubectl get -n harbor certificate tls-harbor.ing.vm.pvel.worldl.xpt -o yaml | yq

kubectl get secret tls-harbor.ing.vm.pvel.worldl.xpt -n harbor -o jsonpath='{.data.ca\.crt}' | base64 --decode > "$CA_FILE"

openssl x509 -in "$CA_FILE" -text -noout

configure_host
configure_k3s
configure_docker

