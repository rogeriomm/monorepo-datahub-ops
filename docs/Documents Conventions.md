# Documentation conventions

This repository uses [Obsidian](https://obsidian.md/) to write and organize its
documentation. Documents may use Obsidian-specific Markdown when it adds value,
but content should remain readable on GitHub whenever practical.

## Directory names

Directories under `docs/` must use kebab-case:

- Use lowercase letters.
- Separate words with hyphens (`-`).
- Do not use spaces, underscores, accented characters, or punctuation other
  than hyphens.
- Choose clear, descriptive names and keep them reasonably short.

Good examples:

```text
cloud-infrastructure/
on-premises-infrastructure/
de-samples/
```

Bad examples:

```text
Cloud Infrastructure/
on_premises_infrastructure/
documentação/
```

## Document file names

Markdown documents under `docs/` must use readable names with spaces between
words. This convention applies at every directory level.

- Use the `.md` extension.
- Start the file name with an uppercase letter.
- Separate words with spaces.
- Preserve the standard capitalization of acronyms and product names, such as
  `AWS`, `GitHub`, and `Databricks`.
- Do not use hyphens or underscores as word separators.
- Do not use accented characters or punctuation in the base name.
- Choose a clear, descriptive name.

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

`README.md` is the exception to this naming convention. When a documentation
directory has a primary document, create a relative symbolic link named
`README.md` so GitHub displays that document when the directory is opened.

For example, from `docs/on-premises-infrastructure/`:

```shell
ln -s "On Premises Infrastructure.md" README.md
```

The link target must be a document in the same directory and must use a relative
path.

## Document structure

- Begin each document with one level-one heading (`#`) that describes the page.
- Use heading levels in order; do not skip directly from `##` to `####`.
- Use sentence case for headings unless a proper name requires different
  capitalization.
- Add a language identifier to fenced code blocks when one is available, such
  as `shell`, `yaml`, `python`, or `sql`.
- Prefer relative links for files stored in this repository.

## Obsidian links and embeds

Obsidian-style internal links and embeds are allowed:

```md
[[Data Platform Overview]]
[[AWS Network Architecture]]
![[attachments/aws-vpc-diagram.png]]
```

For pages intended to be read primarily on GitHub, prefer standard Markdown
because GitHub does not render Obsidian wiki links or embeds:

```md
[Data Platform Overview](Data%20Platform%20Overview.md)
![AWS VPC diagram](attachments/aws-vpc-diagram.png)
```

Use descriptive link text and image alternative text instead of generic labels
such as "click here" or empty image descriptions.

## Diagrams and images

Diagram and image file names must use kebab-case:

- Use lowercase letters and numbers.
- Separate words with hyphens.
- Do not use spaces, underscores, accented characters, or punctuation other
  than hyphens.
- Store assets in an `attachments/` directory near the documents that use them
  when practical.

Good examples:

```text
platform-architecture.drawio
aws-vpc-diagram.png
databricks-workspace-flow.svg
```

## GitHub compatibility

Before committing documentation, confirm that standard Markdown elements such
as headings, lists, links, images, tables, and code blocks render correctly on
GitHub. Use Obsidian-only features deliberately and provide a standard Markdown
alternative when GitHub readers would otherwise lose important context.
