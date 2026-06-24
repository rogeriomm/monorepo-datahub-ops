# Project conventions

## Repository Structure

```
.
├── .devcontainer/      # Development containers    
├── .github/            # GitHub CI/CD
├── .idea/              # Jetbrains
├── .obsidian/          # Obsidian configuration
├── .vscode/            # VScode configuration
├── cloud-aws/          # Cloud AWS infrastruture
├── cloud-databricks/   # Databricks Premium and Free comunity
├── docs/               # Documents
└── on-premises/        # Op-premises infrastructure
```

## Documentation Conventions

This repository uses **Obsidian** for writing and organizing documentation.

Documentation files are stored in the `docs/` directory.

## Markdown file names

Markdown file names must use **kebab-case**.

Rules:

* Use lowercase letters.
* Use `-` to separate words.
* Do not use spaces.
* Do not use `_` underscores.
* Do not use accents or special characters.
* Use clear and descriptive names.

Good examples:

```text
documentation-conventions.md
data-platform-overview.md
aws-network-architecture.md
databricks-workspace-setup.md
```

Bad examples:

```text
Documentation Conventions.md
documentation_conventions.md
databricks workspace setup.md
documentação-convenções.md
```

## Obsidian notes

Documentation may use Obsidian-style internal links.

Examples:

```md
[[data-platform-overview]]
[[aws-network-architecture]]
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
