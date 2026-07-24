# Project conventions

## Repository Structure

```
.
├── .devcontainer/       # Development containers
├── .github/             # GitHub CI/CD
├── .idea/               # JetBrains configuration
├── .obsidian/           # Obsidian configuration
├── .vscode/             # VS Code configuration
├── cloud-aws/           # AWS cloud infrastructure
├── cloud-databricks/    # Databricks Premium and Free Community
├── container-data/      # Docker container persistent data
├── data-project/        # Data projects
├── docs/                # Documentation
├── docs/attachments/    # Documentation attachments
├── docs/attachments/books/  # Books and PDFs
├── notebooks
├── notebooks/jupyter
├── notebooks/jupyter/databricks # Databricks notebooks
├── notebooks/zeppelin
└── on-premises/         # On-premises infrastructure
```

## Documentation Conventions

This repository uses **Obsidian** to organize documentation.
Documentation files live under `docs/`.

## Document file names

All document files under `docs/`, including its subdirectories, must use
spaces between words. The first letter of each filename must be uppercase.

Rules:

* Start every document filename with an uppercase letter.
* Use spaces to separate words.
* Do not use `-` hyphens or `_` underscores as word separators.
* Do not use accents or special characters.
* Use clear and descriptive names.

Good examples:

```text
Documentation Conventions.md
AWS Network Architecture.md
Databricks Workspace Setup.md
Data Platform Overview.md
```

Bad examples:

```text
documentation-conventions.md
documentation_conventions.md
data platform overview.md
databricks workspace setup.md
documentação-convenções.md
```

## Obsidian notes

Documentation may use Obsidian-style internal links.

Examples:

```md
[[Data Platform Overview]]
[[AWS Network Architecture]]
```

Images and diagrams may also use Obsidian embed syntax.

Examples:

```md
![[images/aws-vpc-diagram.png]]
![[diagrams/platform-architecture.drawio]]
```

## Diagrams and images

Diagram and image file names should also use **kebab-case**.

Good examples:

```text
platform-architecture.drawio
aws-vpc-diagram.png
databricks-workspace-flow.svg
```

## GitHub compatibility

When editing documentation, keep Markdown as compatible with GitHub as possible.

Avoid using Obsidian-only features when a standard Markdown alternative is simple and clear.

# Notebook conventions

Notebook file names should also use **kebab-case**.
