FROM chrislusf/seaweedfs:4.39

RUN apk add --no-cache openssl

COPY --chmod=755 configure-tls.sh /usr/local/bin/configure-tls

ENTRYPOINT ["/usr/local/bin/configure-tls"]
