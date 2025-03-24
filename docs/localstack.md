# Install
```shell
kubectl -n localstack create secret generic localstack-auth \
  --from-literal=token=${TOKEN}
```
 - File ~/.aws/config
   - https://docs.aws.amazon.com/cli/latest/topic/config-vars.html
```toml
[profile localstack]
region= us-east-1
output = json
endpoint_url = https://localstack.ing.vm.pvel.world.xpt
verify_ssl = false
#ca_bundle = /home/rogermm/.aws/ca.crt
```

 - File ~/.aws/credentials
```toml
[localstack]
aws_access_key_id=xxx
aws_secret_access_key=xxx
aws_session_token=xxx  
```

```shell
kubectl get secrets localstack-cert-secret -o yaml | yq -r '.data."ca.crt"' | base64 --decode > ca.crt
```

To trust multiple CAs, just append them all into a new file

```shell
cat ~/.aws/ca.crt
```
```text
-----BEGIN CERTIFICATE-----
MIIBbzCCARWgAwIBAgIRANzF5GBmEUvivo5z+kMLMMcwCgYIKoZIzj0EAwIwFzEV
MBMGA1UEAxMMc3Budy1yb290LWNhMB4XDTI1MTAxMTExNDA1OFoXDTM1MTAwOTEx
NDA1OFowFzEVMBMGA1UEAxMMc3Budy1yb290LWNhMFkwEwYHKoZIzj0CAQYIKoZI
zj0DAQcDQgAETv8Hs8qOkWkM5GiOS8Qv3c1noupvsVUgKMKoqmPf7A3CPXSQG6OI
pG7oAAjrw5jo3GxFc2V0pcwJcKzASBBgWaNCMEAwDgYDVR0PAQH/BAQDAgKkMA8G
A1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYEFLlWlTZ8f0EtCYNKX0qLszmJOsJHMAoG
CCqGSM49BAMCA0gAMEUCIQDRftWKpk0VG47m+fJixen46fRKQJHZ38yqvt/h64P9
9QIgGDztLmQWKszWy5BZC8ddepZ9d+ullyXEvQ7PGLOLP7k=
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIBbjCCARSgAwIBAgIQQcIFxmqMchogkJ+RNUThPzAKBggqhkjOPQQDAjAXMRUw
EwYDVQQDEwxzcG53LXJvb3QtY2EwHhcNMjUxMDEzMTE1NjEyWhcNMzUxMDExMTE1
NjEyWjAXMRUwEwYDVQQDEwxzcG53LXJvb3QtY2EwWTATBgcqhkjOPQIBBggqhkjO
PQMBBwNCAASx6prWX7zrsy+DdfZcM3qfXsIr0T1nf1ThuoRuTvJKHwfLMUHFuhpH
LwewCEQAhAFt12oEuicnLFjMIgg+VNqao0IwQDAOBgNVHQ8BAf8EBAMCAqQwDwYD
VR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUuTbJ+wu808RJ5l7Z9C4EUALoMrAwCgYI
KoZIzj0EAwIDSAAwRQIgDoSj6momcyqI7W4Z94mvpcGKk+gDd2hfpo/NF0Uom3UC
IQD1DVsFBhYeA+giwKV7RfC/WU+ORGiEwWL8Q8QL6znyLw==
-----END CERTIFICATE-----
```

 - Edit ~/.zshrc
```shell
export AWS_CA_BUNDLE=~/.aws/ca.crt
export AWS_PAGER=""
alias aws='aws --profile localstack'
alias awslocal='aws --profile localstack'
```

# Test
```shell
aws s3 mb s3://my-first-bucket --profile localstack --no-verify-ssl
```

```shell
aws s3 mb s3://my-first-bucket
```


```shell
aws s3 mb s3://my-first-bucket
```

```shell
aws --profile localstack s3api list-buckets | yq
```

```shell
aws iam create-user --user-name star
```

```shell
aws iam list-users
```

```shell
aws iam attach-user-policy --user-name star --policy-arn=arn:aws:iam::aws:policy/AmazonEC2FullAccess
```

```shell
aws iam list-attached-user-policies --user-name star
```

```shell
aws iam create-access-key --user-name star
```

 - https://github.com/localstack-samples/localstack-pro-samples/tree/master/sample-archive/emr-hadoop-spark-jobs

```shell
aws emr create-cluster \
          --release-label emr-5.9.0 \
          --instance-groups InstanceGroupType=MASTER,InstanceCount=1,InstanceType=m4.large InstanceGroupType=CORE,InstanceCount=1,InstanceType=m4.large
```

 - https://app.localstack.cloud/dashboard

# Internal endpoints
 - https://youtu.be/P7CMTR5h_44?t=561
 - https://docs.localstack.cloud/aws/capabilities/networking/internal-endpoints/

```shell
kubectl -n localstack get services -o yaml | yq
```
```text
apiVersion: v1
items:
  - apiVersion: v1
    kind: Service
    metadata:
      annotations:
        argocd.argoproj.io/tracking-id: localstack-helm:/Service:localstack/localstack-helm
        kubectl.kubernetes.io/last-applied-configuration: |
          {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{"argocd.argoproj.io/tracking-id":"localstack-helm:/Service:localstack/localstack-helm"},"labels":{"app.kubernetes.io/instance":"localstack-helm","app.kubernetes.io/managed-by":"Helm","app.kubernetes.io/name":"localstack","app.kubernetes.io/version":"latest","helm.sh/chart":"localstack-0.6.26"},"name":"localstack-helm","namespace":"localstack"},"spec":{"externalTrafficPolicy":"","ports":[{"name":"edge","nodePort":31566,"port":4566,"targetPort":4566},{"name":"external-service-port-4510","port":4510,"targetPort":"ext-svc-4510"},{"name":"external-service-port-4511","port":4511,"targetPort":"ext-svc-4511"},{"name":"external-service-port-4512","port":4512,"targetPort":"ext-svc-4512"},{"name":"external-service-port-4513","port":4513,"targetPort":"ext-svc-4513"},{"name":"external-service-port-4514","port":4514,"targetPort":"ext-svc-4514"},{"name":"external-service-port-4515","port":4515,"targetPort":"ext-svc-4515"},{"name":"external-service-port-4516","port":4516,"targetPort":"ext-svc-4516"},{"name":"external-service-port-4517","port":4517,"targetPort":"ext-svc-4517"},{"name":"external-service-port-4518","port":4518,"targetPort":"ext-svc-4518"},{"name":"external-service-port-4519","port":4519,"targetPort":"ext-svc-4519"},{"name":"external-service-port-4520","port":4520,"targetPort":"ext-svc-4520"},{"name":"external-service-port-4521","port":4521,"targetPort":"ext-svc-4521"},{"name":"external-service-port-4522","port":4522,"targetPort":"ext-svc-4522"},{"name":"external-service-port-4523","port":4523,"targetPort":"ext-svc-4523"},{"name":"external-service-port-4524","port":4524,"targetPort":"ext-svc-4524"},{"name":"external-service-port-4525","port":4525,"targetPort":"ext-svc-4525"},{"name":"external-service-port-4526","port":4526,"targetPort":"ext-svc-4526"},{"name":"external-service-port-4527","port":4527,"targetPort":"ext-svc-4527"},{"name":"external-service-port-4528","port":4528,"targetPort":"ext-svc-4528"},{"name":"external-service-port-4529","port":4529,"targetPort":"ext-svc-4529"},{"name":"external-service-port-4530","port":4530,"targetPort":"ext-svc-4530"},{"name":"external-service-port-4531","port":4531,"targetPort":"ext-svc-4531"},{"name":"external-service-port-4532","port":4532,"targetPort":"ext-svc-4532"},{"name":"external-service-port-4533","port":4533,"targetPort":"ext-svc-4533"},{"name":"external-service-port-4534","port":4534,"targetPort":"ext-svc-4534"},{"name":"external-service-port-4535","port":4535,"targetPort":"ext-svc-4535"},{"name":"external-service-port-4536","port":4536,"targetPort":"ext-svc-4536"},{"name":"external-service-port-4537","port":4537,"targetPort":"ext-svc-4537"},{"name":"external-service-port-4538","port":4538,"targetPort":"ext-svc-4538"},{"name":"external-service-port-4539","port":4539,"targetPort":"ext-svc-4539"},{"name":"external-service-port-4540","port":4540,"targetPort":"ext-svc-4540"},{"name":"external-service-port-4541","port":4541,"targetPort":"ext-svc-4541"},{"name":"external-service-port-4542","port":4542,"targetPort":"ext-svc-4542"},{"name":"external-service-port-4543","port":4543,"targetPort":"ext-svc-4543"},{"name":"external-service-port-4544","port":4544,"targetPort":"ext-svc-4544"},{"name":"external-service-port-4545","port":4545,"targetPort":"ext-svc-4545"},{"name":"external-service-port-4546","port":4546,"targetPort":"ext-svc-4546"},{"name":"external-service-port-4547","port":4547,"targetPort":"ext-svc-4547"},{"name":"external-service-port-4548","port":4548,"targetPort":"ext-svc-4548"},{"name":"external-service-port-4549","port":4549,"targetPort":"ext-svc-4549"},{"name":"external-service-port-4550","port":4550,"targetPort":"ext-svc-4550"},{"name":"external-service-port-4551","port":4551,"targetPort":"ext-svc-4551"},{"name":"external-service-port-4552","port":4552,"targetPort":"ext-svc-4552"},{"name":"external-service-port-4553","port":4553,"targetPort":"ext-svc-4553"},{"name":"external-service-port-4554","port":4554,"targetPort":"ext-svc-4554"},{"name":"external-service-port-4555","port":4555,"targetPort":"ext-svc-4555"},{"name":"external-service-port-4556","port":4556,"targetPort":"ext-svc-4556"},{"name":"external-service-port-4557","port":4557,"targetPort":"ext-svc-4557"},{"name":"external-service-port-4558","port":4558,"targetPort":"ext-svc-4558"},{"name":"external-service-port-4559","port":4559,"targetPort":"ext-svc-4559"}],"selector":{"app.kubernetes.io/instance":"localstack-helm","app.kubernetes.io/name":"localstack"},"type":"LoadBalancer"}}
        metallb.io/ip-allocated-from-pool: first-pool
      creationTimestamp: "2025-06-03T14:07:31Z"
      labels:
        app.kubernetes.io/instance: localstack-helm
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/name: localstack
        app.kubernetes.io/version: latest
        helm.sh/chart: localstack-0.6.26
      name: localstack-helm
      namespace: localstack
      resourceVersion: "3538917"
      uid: 921f9559-98b5-4458-96fb-e982fd6d9523
    spec:
      allocateLoadBalancerNodePorts: true
      clusterIP: 10.43.218.236
      clusterIPs:
        - 10.43.218.236
      externalTrafficPolicy: Cluster
      internalTrafficPolicy: Cluster
      ipFamilies:
        - IPv4
      ipFamilyPolicy: SingleStack
      ports:
        - name: edge
          nodePort: 31566
          port: 4566
          protocol: TCP
          targetPort: 4566
        - name: external-service-port-4510
          nodePort: 30895
          port: 4510
          protocol: TCP
          targetPort: ext-svc-4510
        - name: external-service-port-4511
          nodePort: 31893
          port: 4511
          protocol: TCP
          targetPort: ext-svc-4511
        - name: external-service-port-4512
          nodePort: 30323
          port: 4512
          protocol: TCP
          targetPort: ext-svc-4512
        - name: external-service-port-4513
          nodePort: 30553
          port: 4513
          protocol: TCP
          targetPort: ext-svc-4513
        - name: external-service-port-4514
          nodePort: 30333
          port: 4514
          protocol: TCP
          targetPort: ext-svc-4514
        - name: external-service-port-4515
          nodePort: 30236
          port: 4515
          protocol: TCP
          targetPort: ext-svc-4515
        - name: external-service-port-4516
          nodePort: 32585
          port: 4516
          protocol: TCP
          targetPort: ext-svc-4516
        - name: external-service-port-4517
          nodePort: 32212
          port: 4517
          protocol: TCP
          targetPort: ext-svc-4517
        - name: external-service-port-4518
          nodePort: 32070
          port: 4518
          protocol: TCP
          targetPort: ext-svc-4518
        - name: external-service-port-4519
          nodePort: 32071
          port: 4519
          protocol: TCP
          targetPort: ext-svc-4519
        - name: external-service-port-4520
          nodePort: 32345
          port: 4520
          protocol: TCP
          targetPort: ext-svc-4520
        - name: external-service-port-4521
          nodePort: 31836
          port: 4521
          protocol: TCP
          targetPort: ext-svc-4521
        - name: external-service-port-4522
          nodePort: 30994
          port: 4522
          protocol: TCP
          targetPort: ext-svc-4522
        - name: external-service-port-4523
          nodePort: 30150
          port: 4523
          protocol: TCP
          targetPort: ext-svc-4523
        - name: external-service-port-4524
          nodePort: 30663
          port: 4524
          protocol: TCP
          targetPort: ext-svc-4524
        - name: external-service-port-4525
          nodePort: 31558
          port: 4525
          protocol: TCP
          targetPort: ext-svc-4525
        - name: external-service-port-4526
          nodePort: 30862
          port: 4526
          protocol: TCP
          targetPort: ext-svc-4526
        - name: external-service-port-4527
          nodePort: 31501
          port: 4527
          protocol: TCP
          targetPort: ext-svc-4527
        - name: external-service-port-4528
          nodePort: 32247
          port: 4528
          protocol: TCP
          targetPort: ext-svc-4528
        - name: external-service-port-4529
          nodePort: 31276
          port: 4529
          protocol: TCP
          targetPort: ext-svc-4529
        - name: external-service-port-4530
          nodePort: 32114
          port: 4530
          protocol: TCP
          targetPort: ext-svc-4530
        - name: external-service-port-4531
          nodePort: 32323
          port: 4531
          protocol: TCP
          targetPort: ext-svc-4531
        - name: external-service-port-4532
          nodePort: 31779
          port: 4532
          protocol: TCP
          targetPort: ext-svc-4532
        - name: external-service-port-4533
          nodePort: 31231
          port: 4533
          protocol: TCP
          targetPort: ext-svc-4533
        - name: external-service-port-4534
          nodePort: 32497
          port: 4534
          protocol: TCP
          targetPort: ext-svc-4534
        - name: external-service-port-4535
          nodePort: 30196
          port: 4535
          protocol: TCP
          targetPort: ext-svc-4535
        - name: external-service-port-4536
          nodePort: 31042
          port: 4536
          protocol: TCP
          targetPort: ext-svc-4536
        - name: external-service-port-4537
          nodePort: 31698
          port: 4537
          protocol: TCP
          targetPort: ext-svc-4537
        - name: external-service-port-4538
          nodePort: 32267
          port: 4538
          protocol: TCP
          targetPort: ext-svc-4538
        - name: external-service-port-4539
          nodePort: 32072
          port: 4539
          protocol: TCP
          targetPort: ext-svc-4539
        - name: external-service-port-4540
          nodePort: 31858
          port: 4540
          protocol: TCP
          targetPort: ext-svc-4540
        - name: external-service-port-4541
          nodePort: 31430
          port: 4541
          protocol: TCP
          targetPort: ext-svc-4541
        - name: external-service-port-4542
          nodePort: 31177
          port: 4542
          protocol: TCP
          targetPort: ext-svc-4542
        - name: external-service-port-4543
          nodePort: 32730
          port: 4543
          protocol: TCP
          targetPort: ext-svc-4543
        - name: external-service-port-4544
          nodePort: 31801
          port: 4544
          protocol: TCP
          targetPort: ext-svc-4544
        - name: external-service-port-4545
          nodePort: 31459
          port: 4545
          protocol: TCP
          targetPort: ext-svc-4545
        - name: external-service-port-4546
          nodePort: 31033
          port: 4546
          protocol: TCP
          targetPort: ext-svc-4546
        - name: external-service-port-4547
          nodePort: 30887
          port: 4547
          protocol: TCP
          targetPort: ext-svc-4547
        - name: external-service-port-4548
          nodePort: 30394
          port: 4548
          protocol: TCP
          targetPort: ext-svc-4548
        - name: external-service-port-4549
          nodePort: 30319
          port: 4549
          protocol: TCP
          targetPort: ext-svc-4549
        - name: external-service-port-4550
          nodePort: 31828
          port: 4550
          protocol: TCP
          targetPort: ext-svc-4550
        - name: external-service-port-4551
          nodePort: 31593
          port: 4551
          protocol: TCP
          targetPort: ext-svc-4551
        - name: external-service-port-4552
          nodePort: 32077
          port: 4552
          protocol: TCP
          targetPort: ext-svc-4552
        - name: external-service-port-4553
          nodePort: 31290
          port: 4553
          protocol: TCP
          targetPort: ext-svc-4553
        - name: external-service-port-4554
          nodePort: 31770
          port: 4554
          protocol: TCP
          targetPort: ext-svc-4554
        - name: external-service-port-4555
          nodePort: 30639
          port: 4555
          protocol: TCP
          targetPort: ext-svc-4555
        - name: external-service-port-4556
          nodePort: 32448
          port: 4556
          protocol: TCP
          targetPort: ext-svc-4556
        - name: external-service-port-4557
          nodePort: 32441
          port: 4557
          protocol: TCP
          targetPort: ext-svc-4557
        - name: external-service-port-4558
          nodePort: 32310
          port: 4558
          protocol: TCP
          targetPort: ext-svc-4558
        - name: external-service-port-4559
          nodePort: 30285
          port: 4559
          protocol: TCP
          targetPort: ext-svc-4559
      selector:
        app.kubernetes.io/instance: localstack-helm
        app.kubernetes.io/name: localstack
      sessionAffinity: None
      type: LoadBalancer
    status:
      loadBalancer:
        ingress:
          - ip: 192.168.15.151
            ipMode: VIP
kind: List
metadata:
  resourceVersion: ""
```

```shell
curl -k https://192.168.15.151:4566/_localstack/health | jq
```
```shell
curl -k https://localstack.ing.vm.world1l.worldl.xpt/_localstack/health | jq
```


```shell
git clone https://github.com/localstack-samples/
```

```shell
cd localstack-samples/route53-dns-failover
make run
```



# Links
 - https://github.com/localstack-samples/localstack-pro-samples/tree/master
 - https://github.com/localstack/localstack-artifacts
 - https://github.com/localstack/helm-charts/tree/main/charts/localstack
   - https://github.com/localstack/helm-charts/blob/main/charts/localstack/templates/service.yaml 
 - https://purushothamkdr453.medium.com/localstack-setup-on-kubernetes-cluster-f055402a961c
 - https://docs.localstack.cloud/aws/enterprise/k8s-operator/
   - Only Enterprise 
 - https://www.youtube.com/watch?v=P7CMTR5h_44


