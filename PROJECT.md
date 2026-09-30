# Project conventions

This document describes the repository's high-level structure and shared
conventions. Component-specific instructions should live next to the component
they describe.

## Repository structure

```text
.
├── .devcontainer/                 # Dev Container editor configuration
├── .github/
│   └── workflows/                 # GitHub Actions workflows
├── .idea/                         # Shared JetBrains project configuration
├── .obsidian/                     # Obsidian vault configuration
├── .vscode/                       # Shared Visual Studio Code configuration
├── cloud-aws/
│   └── infra/                     # AWS cloud infrastructure
├── cloud-databricks/              # Databricks Asset Bundles and samples
│   ├── free-edition/              # Databricks Free Edition projects
│   └── premium/                   # Databricks Premium projects
├── data-projects/                 # Standalone data engineering projects
├── docs/                          # Project documentation
│   ├── attachments/               # Shared documentation assets
│   └── on-premises-infrastructure/ # On-premises documentation
├── notebooks/
│   ├── jupyter/                   # Jupyter notebooks and supporting files
│   │   └── databricks/            # Databricks notebooks exported as Jupyter
│   │       ├── free-edition/      # Databricks Free Edition notebooks
│   │       └── premium/           # Databricks Premium notebooks
│   └── zeppelin/                  # Zeppelin notebooks
└── on-premises/                   # Local and on-premises infrastructure
    ├── ansible/                   # Ansible collections and automation
    ├── container-data/            # Persistent container data configuration
    ├── docker/                    # Local Compose services and image builds
    ├── grafana/                   # Grafana configuration and dashboards
    ├── k3s/                       # K3s cluster configuration
    ├── k8s/                       # Kubernetes workloads and services
    ├── lang-samples/              # Language-specific examples
    ├── scripts/                   # Operational scripts
    └── tools/                     # Operational tooling
```

The tree documents the main project areas rather than every directory. Add new
top-level directories only when their responsibility does not fit an existing
area, and update this section when the repository structure changes.

## Naming conventions

- Use lowercase kebab-case for new project-owned directory names unless an
  external tool requires a different name.
- Prefer lowercase kebab-case for scripts and configuration files when their
  ecosystem does not prescribe a name.
- Preserve established product capitalization in prose, including `AWS`,
  `Databricks`, `GitHub`, `Jupyter`, `K3s`, and `Kubernetes`.
- Follow an ecosystem's required names for files such as `Dockerfile`,
  `README.md`, `pyproject.toml`, and `databricks.yml`.

## Notebook conventions

- Use lowercase kebab-case for new or renamed notebook files.
- Store Jupyter notebooks with the `.ipynb` extension.
- Preserve the workspace-relative directory tree when exporting Databricks
  notebooks into `notebooks/jupyter/databricks/`.
- Do not commit `.ipynb_checkpoints/`, caches, logs, virtual environments, or
  other runtime-generated files.
- Do not store credentials, access tokens, or other secrets in notebook cells,
  outputs, or metadata.
- Clear large or sensitive cell outputs before committing a notebook unless the
  output is necessary to understand the example.

Existing notebook names do not need to be changed solely to satisfy these
conventions. Apply the conventions when adding or renaming notebooks.

## Generated and local files

Do not commit local runtime state, generated caches, credentials, or persistent
service data unless a component explicitly tracks a sanitized fixture. Keep
machine-specific configuration out of shared files and provide documented
examples for required local settings.

## Documentation conventions

Documentation under `docs/` follows a separate naming scheme designed for
Obsidian and GitHub. See
[Documentation conventions](docs/Documents%20Conventions.md) for document,
directory, asset, linking, and formatting rules.
