# Jupyter notebooks
To view the Jupyter notebooks, use the [Jetbrains Big Data Tools](https://www.jetbrains.com/help/idea/jupyter-notebook-support.html),  [GitHub viewer](../../notebooks/jupyter/quick-start/ScalaHelloWorld.ipynb), or run the container:
```shell
docker run -it -p 6660:8888 -v "${PWD}/notebooks/jupyter":/home/jovyan jupyter/pyspark-notebook start.sh jupyter notebook --NotebookApp.token=''
```

Open the JupyterLab: http://localhost:6660/lab


Alternatively you can run the [[devcontainers]] and open the same http://localhost:6660/lab