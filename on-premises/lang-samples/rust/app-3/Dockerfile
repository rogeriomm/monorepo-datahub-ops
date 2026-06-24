FROM ubuntu

# Copy the release binary from the workflow workspace
COPY target/release/my-actix-app /usr/local/bin/my-actix-app

# Expose the same port your app listens on
EXPOSE 8080

ENTRYPOINT ["/usr/local/bin/my-actix-app"]
