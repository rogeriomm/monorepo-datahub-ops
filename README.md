> 🚧 **Work in Progress**  
> This project is currently under active development.  
> Features, structure, and documentation may change frequently.  


# 🏗️ Home-Lab Architecture
<img src="images/LabArchiteture.png" alt="drawing" width="1000"/>

# Jupyter/Zeppelin notebooks
To view the Jupyter notebooks, use the [Jetbrains Big Data Tools](https://www.jetbrains.com/help/idea/jupyter-notebook-support.html),  [GitHub viewer](notebooks/jupyter/quick-start/ScalaHelloWorld.ipynb), or run the container:
```shell
docker run -it -p 6660:8888 -v "${PWD}/notebooks/jupyter":/home/jovyan jupyter/pyspark-notebook start.sh jupyter notebook --NotebookApp.token=''
```

  * http://localhost:6660

# Development Containers
- https://devpod.sh/
  - <img src="images/devpod-feature.png" alt="drawing" width="200"/>

```shell
devpod up . --ide none
```

<img src="images/devpods-sample-1.png" alt="drawing" width="500"/>

# Links
- https://pvel-homepage.worldb.site/

<img src="images/Homepage.png" alt="drawing" width="1000"/>


