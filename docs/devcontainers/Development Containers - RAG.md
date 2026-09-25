# Obsidian RAG

The on-premises Compose project runs [obsidian-mcp](https://github.com/maxkuminov/obsidian-mcp) with PostgreSQL,
pgvector, and Ollama. It indexes the Obsidian vault for full-text and semantic
search and exposes authenticated MCP tools for reading and updating notes.

The services are defined in
[`compose-ai.yaml`](../../on-premises/docker/compose-ai.yaml) and included by
[`docker-compose.yaml`](../../on-premises/docker/docker-compose.yaml). The
`obsidian-mcp` service joins these networks:

- `backend` for access from the devcontainer and other internal services.
- `frontend` for access through Traefik from the host.
- `ai-backend` for its private PostgreSQL and Ollama dependencies.

PostgreSQL and Ollama retain their data in the
`obsidian-rag_postgres-data` and `obsidian-rag_ollama-data` volumes. The MCP
container does not publish a host port. Traefik exposes it on its loopback-only
`mcp` entrypoint instead.

## Configure

Create the ignored environment file if it does not exist:

```shell
cd on-premises/docker
test -f .env || cp dot.env.template .env
```

Generate two different URL-safe secrets:

```shell
openssl rand -hex 32
openssl rand -hex 32
```

Set these values in `on-premises/docker/.env`:

```dotenv
OBSIDIAN_MCP_POSTGRES_PASSWORD=first-generated-value
OBSIDIAN_MCP_POSTGRES_PASSWORD_URLENCODED=first-generated-value
OBSIDIAN_MCP_SECRET_KEY=second-generated-value
OBSIDIAN_VAULT_PATH=../../docs
```

Hexadecimal passwords are already safe in a database URL, so the two password
variables can have the same value. If the database password contains reserved
URL characters, set `OBSIDIAN_MCP_POSTGRES_PASSWORD_URLENCODED` to its
percent-encoded form.

`OBSIDIAN_VAULT_PATH` is resolved relative to `on-premises/docker/`. Its
default value mounts this repository's `docs/` directory at `/obsidian` in the
MCP container.

## Start and verify

From `on-premises/docker`, use the project task:

```shell
mise run ai:start:all
```

The equivalent command from the repository root is:

```shell
docker compose -f on-premises/docker/docker-compose.yaml \
  --profile obsidian_mcp up -d obsidian-mcp traefik
```

The first start builds the server and downloads the `bge-m3` embedding model,
so it can take several minutes. Follow startup and indexing with:

```shell
docker compose -f on-premises/docker/docker-compose.yaml \
  logs -f obsidian-mcp ollama-model
```

Verify the host endpoint and container health:

```shell
curl --fail http://localhost:8000/health
docker compose -f on-premises/docker/docker-compose.yaml \
  --profile obsidian_mcp ps obsidian-mcp obsidian-mcp-postgres ollama traefik
```

Open the control panel at <http://localhost:8000/admin>. Create a read-only or
read-write API key there, according to the MCP client's required access.

The available endpoints are:

| Client | MCP URL |
| --- | --- |
| Host applications, including Codex | `http://localhost:8000/mcp` |
| Devcontainer and backend services | `http://obsidian-mcp:8000/mcp` |

Both MCP endpoints require `Authorization: Bearer omcp_...` with an API key
created in the control panel.

## Connect Codex

The repository configuration in
[`config.toml`](../../.codex/config.toml) registers the server as
`obsidian_rag`:

```toml
[mcp_servers.obsidian_rag]
url = "http://localhost:8000/mcp"
auth = "oauth"
http_headers_helper = ".codex/obsidian-rag-headers.sh"
startup_timeout_sec = 30
tool_timeout_sec = 120
```

Create `.codex/obsidian-rag-token`, put one `omcp_...` API key on its only
line, and restrict its permissions:

```shell
chmod 600 .codex/obsidian-rag-token
```

The token file is ignored by Git. The tracked
[`obsidian-rag-headers.sh`](../../.codex/obsidian-rag-headers.sh) helper reads
it and supplies the authorization header without storing the key in
`config.toml`.

Check that Codex sees the configuration:

```shell
codex mcp list --json
```

Restart the Codex session after changing its MCP configuration or token. Ask a
newly connected agent to call `get_vault_guide` before it reads or writes
notes. A `CLAUDE.md` at the vault root can describe the vault's structure and
conventions to connected agents.

## Connect pgAdmin

The Compose configuration registers the vector database in pgAdmin as
**Obsidian RAG Vector Database** with these settings:

| Setting | Value |
| --- | --- |
| Host | `obsidian-mcp-postgres` |
| Port | `5432` |
| Maintenance database | `obsidian_mcp` |
| Username | `obsidian_mcp` |
| Password | `OBSIDIAN_MCP_POSTGRES_PASSWORD` from `.env` |
| SSL mode | `disable` |

Start pgAdmin with the RAG services:

```shell
docker compose -f on-premises/docker/docker-compose.yaml \
  --profile pgadmin --profile obsidian_mcp up -d pgadmin obsidian-mcp traefik
```

Open <http://pgadmin.localhost:8080/>. The imported server obtains its password
through a Compose-managed secret and pgAdmin's password-exec support; the
tracked server definition does not contain a literal credential.

## Inspect the index

The vault path and title are ordinary columns in `notes_metadata`. Chunk text
and the 1,024-dimensional pgvector value are stored in `note_embeddings`. The
vector does not contain the file name or directory.

Run this query in pgAdmin to list indexed files and their chunk counts:

```sql
SELECT
    n.file_path,
    n.title,
    COUNT(e.id) AS embedded_chunks,
    n.modified_at,
    n.indexed_at
FROM public.notes_metadata AS n
LEFT JOIN public.note_embeddings AS e
    ON e.note_id = n.id
GROUP BY n.id, n.file_path, n.title, n.modified_at, n.indexed_at
ORDER BY n.file_path;
```

Inspect the text chunks for one file without returning the large vector values:

```sql
SELECT
    n.file_path,
    e.chunk_index,
    e.chunk_text
FROM public.notes_metadata AS n
JOIN public.note_embeddings AS e
    ON e.note_id = n.id
WHERE n.file_path = 'devcontainers/Development Containers.md'
ORDER BY e.chunk_index;
```

## Stop or rebuild

Stop the containers while retaining the PostgreSQL index and Ollama model:

```shell
cd on-premises/docker
mise run ai:stop:all
```

To rebuild the upstream server at the pinned `v0.8.1` release:

```shell
docker compose -f on-premises/docker/docker-compose.yaml \
  build --pull obsidian-mcp
docker compose -f on-premises/docker/docker-compose.yaml \
  --profile obsidian_mcp up -d obsidian-mcp traefik
```

## Delete all RAG data

The clean task removes the MCP and PostgreSQL containers and deletes the
`obsidian-rag_postgres-data` volume:

```shell
cd on-premises/docker
mise run ai:rag:clean
```

This deletes the index, API keys, users, OAuth state, usage records, and other
data held in the RAG database. It does not delete Markdown files from the
vault or the Ollama model volume. Start the stack again to create a new
database, reindex the vault, and create a new API key:

```shell
mise run ai:start:all
```
