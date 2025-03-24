To view the Zeppelin notebooks use [Jetbrains Big Data Tools](https://www.jetbrains.com/help/idea/big-data-tools-zeppelin-notebooks.html)  or run the container:

```shell
docker run -it -p 6661:8080 -v "$PWD":/opt/zeppelin/notebook apache/zeppelin:0.10.1
```

   * http://localhost:6661
