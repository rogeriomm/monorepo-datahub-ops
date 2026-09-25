# Cloudflare Tunnel overview

The Cloudflare dashboard provides the health and configuration details for
managed tunnels and their connectors.

## Tunnel status

The tunnel list shows the connector type, route count, current status, and
uptime.

![Redacted Cloudflare tunnel overview](attachments/cloudflare-tunnels-overview-redacted.png)

## Tunnel and connector details

The tunnel details page shows its status and the active connector. Identifiers,
hostnames, account information, and origin addresses are intentionally blurred.

![Redacted Cloudflare tunnel and connector details](attachments/cloudflare-tunnel-details-redacted.png)



**Cloudflare Dashboard → Networking → Tunnels → select your tunnel → Routes → Add route → Published application**.


# Cloudflare Origin CA leaf certificate and private key
- https://developers.cloudflare.com/ssl/origin-configuration/origin-ca/


 - Open Cloudflare Dashboard.
 - Select the worldb.site zone.
 - Go to SSL/TLS → Origin Server.
 - Select Create Certificate.
 - Add hostname \*.worldb.site.
 - Choose PEM format.
 - Save the outputs on the on premises server
 