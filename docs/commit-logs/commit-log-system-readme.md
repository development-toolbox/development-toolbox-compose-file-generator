# Commit Log System README

This project uses an automated commit logging system to ensure that all changes are clearly documented and easy to track. This README explains the structure, purpose, and behavior of the commit logs, as well as the meaning of certain commit indicators.

---

## Commit Log Structure

After each commit, a detailed commit log is generated in the `docs/commit-logs` directory, sorted by branch. Each log file is named using the commit hash for traceability.

### Example Structure
```plaintext
docs/
└── commit-logs
    ├── main
    │   ├── 305f3093.md
    │   ├── 8d917eb1.md
    │   └── README.md
    └── commit-log-system-readme.md
```

### README Structure
The `README.md` file within each branch directory summarizes all commits in a table format with links to detailed commit logs:

```markdown
# Commit Log for Branch: `main`

This file provides a summary of all commits in the branch `main`.
Each commit links to its detailed log.

| Commit Hash | Date       | Author       | Message           |
|-------------|------------|--------------|-------------------|
| [305f3093](./305f3093.md) | 2025-01-08 | Johan Sörell | chore: Updated git hooks setup |
| [8d917eb1](./8d917eb1.md) | 2025-01-08 | Johan Sörell | chore: Rename script for clarity |
```

---

## Changed Files Explained

The **Changed Files** section uses Git's status codes to describe the changes made. Here's a breakdown:

- **R** – Renamed file
- **096** – Similarity index (96% similarity with the original file)
- **A** – Added file
- **D** – Deleted file
- **M** – Modified file

### Rename with Similarity Index (`R096`)
The `R096` indicates a **file rename with 96% similarity**. This means the file was renamed but retains most of its original content.

- **100% similarity** (`R100`) indicates a pure rename.
- Lower percentages indicate heavier modifications along with the rename.

---

## How the Commit Logs Work

The commit log system is managed by a `post-commit` hook located in `.git/hooks/post-commit`. The steps are:

1. **Marker File Check:** Prevents recursive execution using a marker file.
2. **Commit Information Collection:** Gathers commit hash, message, author, date, and branch information.
3. **Changed Files Detection:** Extracts a list of changed files with their Git status.
4. **Log Generation:** Writes the commit details and file changes into a structured Markdown file.
5. **Automatic Commit and Push (Optional):** If the `GIT_AUTO_PUSH` variable is set to `true`, the commit log will be automatically committed and pushed.

The original `git-hooks-installer` files used in this system are located in the [development-toolbox-core](https://github.com/development-toolbox/development-toolbox-core) repository.

---

## Usage and Maintenance

- The commit log system helps keep a clear historical record for better collaboration and traceability.
- To disable auto-pushing, ensure `GIT_AUTO_PUSH` is not set to `true`.

For more details or issues, feel free to raise a pull request or issue in the repository.

---

**Maintained by:** Johan Sörell  
**GitHub:** [J-SirL](https://github.com/J-SirL)
**Project main**[Git-Hooks-Installer] (https://github.com/development-toolbox/development-toolbox-core/tree/main/github-tools/git-hooks-installer)

