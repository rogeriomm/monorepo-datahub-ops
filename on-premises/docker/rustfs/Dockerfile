FROM rustfs/rustfs:1.0.0

USER root

RUN apk add --no-cache openssl su-exec

COPY --chmod=755 configure-tls.sh /usr/local/bin/configure-tls

ENTRYPOINT ["/usr/local/bin/configure-tls"]
