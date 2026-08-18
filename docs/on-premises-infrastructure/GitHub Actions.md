```shell
gh repo set-default rogeriomm/monorepo-datahub-ops-private
```

```shell
gh workflow run samples-golang-app-1 --ref master
```

```shell
gh run list --workflow=samples-golang-app-1.yaml
```

# Install
```shell
sudo ./svc.sh install --help
```

```shell
sudo ./svc.sh install rogermm
```
```text
Creating launch runner in /etc/systemd/system/actions.runner.rogeriomm-monorepo-datahub-ops-private.world1l-vm.service
Run as user: rogermm
Run as uid: 1000
gid: 1000
Created symlink /etc/systemd/system/multi-user.target.wants/actions.runner.rogeriomm-monorepo-datahub-ops-private.world1l-vm.service → /etc/systemd/system/actions.runner.rogeriomm-monorepo-datahub-ops-private.world1l-vm.service.
```

You can check the active version with:
```shell
cd ~/actions-runner
./bin/Runner.Listener --version
```
![[github-action-runner-version.png|943]]
```shell
sudo ./svc.sh status
```
![[github-action-runner-svc-status.png|944]]

```shell
sudo ./svc.sh stop
sudo ./svc.sh start
```
![[github-action-runner-svc-start-stop.png|950]]

![[github-runners.png|951]]