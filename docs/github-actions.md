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

```shell
sudo ./svc.sh status
```
```text
/etc/systemd/system/actions.runner.rogeriomm-monorepo-datahub-ops-private.world1l-vm.service
○ actions.runner.rogeriomm-monorepo-datahub-ops-private.world1l-vm.service - GitHub Actions Runner (rogeriomm-monorepo-datahub-ops-private.world1l-vm)
     Loaded: loaded (/etc/systemd/system/actions.runner.rogeriomm-monorepo-datahub-ops-private.world1l-vm.service; enabled; preset: enabled)
     Active: inactive (dead)
```

```shell
sudo ./svc.sh start
```
```text

/etc/systemd/system/actions.runner.rogeriomm-monorepo-datahub-ops-private.world1l-vm.service
● actions.runner.rogeriomm-monorepo-datahub-ops-private.world1l-vm.service - GitHub Actions Runner (rogeriomm-monorepo-datahub-ops-private.world1l-vm)
     Loaded: loaded (/etc/systemd/system/actions.runner.rogeriomm-monorepo-datahub-ops-private.world1l-vm.service; enabled; preset: enabled)
     Active: active (running) since Thu 2025-10-02 14:01:34 UTC; 3ms ago
   Main PID: 91362 (runsvc.sh)
      Tasks: 2 (limit: 49263)
     Memory: 1.1M (peak: 1.1M)
        CPU: 1ms
     CGroup: /system.slice/actions.runner.rogeriomm-monorepo-datahub-ops-private.world1l-vm.service
             ├─91362 /bin/bash /home/rogermm/action-runner/runsvc.sh
             └─91365 ./externals/node20/bin/node ./bin/RunnerService.js

Oct 02 14:01:34 vm.worldl1.worldl.xpt systemd[1]: Started actions.runner.rogeriomm-monorepo-datahub-ops-private.world1l-vm.service - GitHub…rld1l-vm).
Oct 02 14:01:34 vm.worldl1.worldl.xpt runsvc.sh[91362]: .path=/home/rogermm/.local/share/mise/installs/bat/0.25.0:/home/rogermm/.local/share/mise/ins…
Hint: Some lines were ellipsized, use -l to show in full.
```
