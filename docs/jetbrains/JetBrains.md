# Kubernetes
- [Jetbrains - Custom resource definitions support﻿](https://www.jetbrains.com/help/go/2025.1/kubernetes.html?Kubernetes.crdSpecs&keymap=KDE&utm_source=product&utm_medium=link&utm_campaign=GO&utm_content=2025.1#crd)
   - https://github.com/argoproj/argo-cd/tree/master/manifests/crds


# Jupyter notebooks
```shell
mise where java
```

```shell
mise exec java -- sh -c 'java -XshowSettings:properties -version 2>&1 | grep "java.home"'
```
![[Pasted image 20260817123355.png|1054]]
![[Pasted image 20260817122844.png|1055]]![[Pasted image 20260817123115.png|1059]]

# Mise
Enable **“Use environment variables from mise.”** All packages installed with **mise**, including **Java**, will then be available inside JetBrains.
![[Pasted image 20260817155018.png|1062]]