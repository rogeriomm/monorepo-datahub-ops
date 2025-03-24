```shell
docker run -it --rm \
  --network host \
  --cap-add=NET_ADMIN \
  --cap-add=NET_RAW \
  -v "$(pwd)":/mnt \
  nicolaka/netshoot
```

```shell
kubectl run -it netutils --rm --image=wbitt/network-multitool --restart=Never -- bash
```

# Links
- https://github.com/nicolaka/netshoot
