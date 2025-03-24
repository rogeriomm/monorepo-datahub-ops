root_ca=$(kubectl -n cert-manager get secret spnw-root-ca-secret -o jsonpath='{.data.tls\.crt}' | base64 --decode)
echo "Root CA: $root_ca"
echo "================="

inter_ca=$(kubectl -n cert-manager get secret spnw-intermediate-ca1-secret -o jsonpath='{.data.tls\.crt}' | base64 --decode)
echo "Intermediate CA: $inter_ca"
echo "================="

test_srv=$(kubectl -n cert-test get secret test-server-secret -ojsonpath='{.data.tls\.crt}' | base64 --decode)
echo "Test: $test_srv"
echo "================="

openssl verify -CAfile \
        <(kubectl -n cert-manager get secret spnw-root-ca-secret -o jsonpath='{.data.tls\.crt}' | base64 --decode) -untrusted  \
        <(kubectl -n cert-manager get secret spnw-intermediate-ca1-secret -o jsonpath='{.data.tls\.crt}' | base64 --decode) \
        <(kubectl -n cert-test get secret test-server-secret -ojsonpath='{.data.tls\.crt}' | base64 --decode)

