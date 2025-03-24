- https://worldl-datahub.worldb.site/
  - Default user/password: _datahub/datahub_
# Changing the default user datahub
- https://docs.datahub.com/docs/authentication/changing-default-credentials/#helm-chart

- https://github.com/bitnami/charts/issues/35164
   - https://hub.docker.com/r/bitnamilegacy/mysql/tags?name=8.0.32-debian-11-r26

 - https://docs.datahub.com/docs/cli


Mysql root password
```shell
kubectl get secrets mysql-secrets -o jsonpath='{.data.mysql-root-password}' | base64 --decode
```

```shell
mysql -u root -p -e "SHOW DATABASES;"
```

```shell
mysqlcheck -u root -p datahub
```

```shell
mysqlcheck -u root -p --all-databases
```
# Backup database
```shell
mysqldump -u root -p datahub > /tmp/backup.sql
```
# Datahub CLI
 - https://datahub.ing.vm.world1l.worldl.xpt/
 - https://docs.datahub.com/docs/authentication/personal-access-tokens
 - https://docs.datahub.com/docs/authentication/changing-default-credentials
 - https://docs.datahub.com/docs/authentication/guides/add-users

 - https://datahub-gms.ing.vm.world1l.worldl.xpt


Run
```shell
datahub init
```

add line "disable_ssl_verification: true" -> ~/.datahubenv

```shell
cat ~/.datahubenv
```

```yaml
gms:
  ca_certificate_path: null
  client_certificate_path: null
  client_mode: null
  datahub_component: null
  disable_ssl_verification: false
  extra_headers: null
  openapi_ingestion: null
  retry_max_times: null
  retry_status_codes: null
  server: https://datahub-gms.ing.vm.world1l.worldl.xpt
  server_config_refresh_interval: null
  timeout_sec: null
  disable_ssl_verification: true
  token: token_goes_here
```

Check connection

```shell
datahub get --urn "urn:li:corpuser:datahub"  2> /dev/null | jq
```
```javascript
{
  "corpUserEditableInfo": {
    "persona": "urn:li:dataHubPersona:technicalUser",
    "pictureLink": "https://raw.githubusercontent.com/datahub-project/datahub/master/datahub-web-react/src/images/default_avatar.png",
    "platforms": [],
    "skills": [],
    "teams": [],
    "title": "Data Engineer"
  },
  "corpUserInfo": {
    "active": true,
    "displayName": "DataHub",
    "system": true,
    "title": "DataHub Root User"
  },
  "corpUserKey": {
    "username": "datahub"
  },
  "corpUserSettings": {
    "appearance": {
      "showThemeV2": true
    }
  },
  "roleMembership": {
    "roles": []
  }
}
```


## How to Configure the Remote Connection
. Generate a Personal Access Token
First, you need a token to authenticate your API requests.
Log in to your remote DataHub UI in your web browser.
Navigate to Settings > Access Tokens.
Click Generate New Token to create a token for your CLI.
Copy this token immediately and save it somewhere secure. You won't be able to see it again.

