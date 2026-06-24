#kubectl describe -n simple-web secret/simple-web-cert-secret

root_ca=$(kubectl -n cert-manager get secret spnw-root-ca-secret -o jsonpath='{.data.tls\.crt}' | base64 --decode)
echo "Root CA: $root_ca"
echo "================="

inter_ca=$(kubectl -n cert-manager get secret spnw-intermediate-ca1-secret -o jsonpath='{.data.tls\.crt}' | base64 --decode)
echo "Intermediate CA: $inter_ca"
echo "================="

simple_web=$(kubectl -n simple-web get secret simple-web-cert-secret -ojsonpath='{.data.tls\.crt}' | base64 --decode)
echo "Test: $simple_web"
echo "================="

openssl verify -CAfile \
        <(kubectl -n cert-manager get secret spnw-root-ca-secret -o jsonpath='{.data.tls\.crt}' | base64 --decode) -untrusted  \
        <(kubectl -n cert-manager get secret spnw-intermediate-ca1-secret -o jsonpath='{.data.tls\.crt}' | base64 --decode) \
        <(kubectl -n simple-web get secret  simple-web-cert-secret -ojsonpath='{.data.tls\.crt}' | base64 --decode)

