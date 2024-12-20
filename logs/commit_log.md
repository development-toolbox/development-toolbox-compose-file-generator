### [b457d15781e5ff9c7b89c66304d7c21c389ef2cf: feat(git-hooks): Implement post-commit hook for detailed commit logging

- Added a post-commit hook to automatically generate detailed commit logs.
- Logs include full commit details in a markdown file (`commit_$COMMIT_HASH.md`) and a summary in the main commit log (`commit_log.md`).
- Logs contain commit hash, author, date, branch, commit message, and changed files.
- Automatically stages, commits, and optionally pushes commit logs to the repository.
- Added security checks to prevent committing sensitive files (e.g., `.env`, `secrets`).
- Prevents recursive commits by using a skip marker file.
- Commits both the individual commit log file and the main log file.](/opt/my-private-repos/development-toolbox-compose-file-generator/logs/commit_b457d15781e5ff9c7b89c66304d7c21c389ef2cf.md)
- **Date**: 2024-12-20 16:18:28 +0100
- **Author**: Johan Sörell
- **Branch**: main

### [7f538fa1df674690da4385a29090008868da400a: added the logs manually because of a bug](/opt/my-private-repos/development-toolbox-compose-file-generator/logs/commit_7f538fa1df674690da4385a29090008868da400a.md)
- **Date**: 2024-12-20 16:52:08 +0100
- **Author**: Johan Sörell
- **Branch**: main

