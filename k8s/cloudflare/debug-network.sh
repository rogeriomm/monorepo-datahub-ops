kubectl run curl-ubuntu \
  --rm -i -t \
  --image=nicolaka/netshoot \
  --labels=app=cloudflared \
  -- bash
