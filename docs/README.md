   * https://github.com/rogeriomm/monorepo-datahub-ops



   * Github actions
     * [About self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners)

   * https://docs.tigera.io/calico/latest/getting-started/kubernetes/k3s/quickstart


# Github CLI
```shell
gh workflow list | cat
```

```shell
job=40389680269
gh run view --job=$job | cat
```


```shell
gh run watch
```

# Argocd
## Login
```shell
kubectl config set-context --current --namespace argocd
```

```shell
argocd login --core
```


# Links
- https://github.com/cicerojmm/treinamentoDataHandsOnDataQualityAWS
