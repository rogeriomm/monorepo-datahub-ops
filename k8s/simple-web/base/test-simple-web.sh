
simple_web=$(kubectl -n simple-web get secret simple-web-cert-secret -ojsonpath='{.data.tls\.crt}' | base64 -d)

echo "$simple_web" | openssl x509 -text -noout

openssl verify -CAfile \
        <(kubectl -n cert-manager get secret spnw-root-ca-secret          -o jsonpath='{.data.tls\.crt}' | base64 --decode) -untrusted  \
        <(kubectl -n cert-manager get secret spnw-intermediate-ca1-secret -o jsonpath='{.data.tls\.crt}' | base64 --decode)             \
        <(kubectl -n simple-web   get secret simple-web-cert-secret       -o jsonpath='{.data.tls\.crt}' | base64 --decode)
