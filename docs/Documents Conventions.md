This repository uses [**Obsidian** ](https://obsidian.md/) to write and organize documentation.
Some files may contain Obsidian-specific Markdown syntax.

## File names

Documentation file names should use **kebab-case**:

- Use lowercase letters.
- Use `-` to separate words.
- Do not use spaces in file names.
- Prefer clear and descriptive names.
- Do not use accents or special characters.
- Keep names descriptive but not too long.

README.md symbolic link to the filename so GitHub can show the page. Example: [`docs/on-premises-infrastructure/on-premises-infrastructure.md`](on-premises-architecture.md) and "docs/on-premises-infrastructure/README.md"


```shell
ln -s on-premises-infrastructure.md README.md
```