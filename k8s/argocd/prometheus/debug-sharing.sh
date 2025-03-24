kubectl debug -it $1 -n cloudflare --image=nicolaka/netshoot --target=cloudflared --share-processes -- bash
