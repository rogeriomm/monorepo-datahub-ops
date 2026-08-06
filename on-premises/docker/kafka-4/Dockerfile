FROM apache/kafka:4.1.0

COPY --chmod=755 configure-tls.sh /etc/kafka/docker/configure-tls

CMD ["/etc/kafka/docker/configure-tls"]
