#!/usr/bin/env zsh

case "$1" in
  "build")
    docker build . -t spark-zeppelin-0.12:3.5.6
    ;;
  "history")
    docker history --no-trunc spark-zeppelin-0.12:3.5.6
    ;;
  "run")
  docker run -it spark-zeppelin-0.12:3.5.6 /bin/bash
  ;;
esac
