 - Delete all tags
```shell
gh api repos/:owner/:repo/tags --jq '.[].name' | xargs -n1 -I{} gh api --method DELETE repos/:owner/:repo/git/refs/tags/{}
```

```shell
docker image rm -f $(docker image ls -q "local/sample-go-app-*")
```