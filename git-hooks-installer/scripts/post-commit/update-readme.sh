#!/bin/bash
# Update branch-specific README.md with commit logs

# Ensure branch name is passed correctly
if [ -z "$BRANCH_NAME" ]; then
  echo "ERROR: Branch name not set. Exiting."
  exit 1
fi

# Ensure we are in the repository root
cd "$REPO_ROOT" || { echo "ERROR: Could not navigate to repository root"; exit 1; }

# Define branch log directory
LOG_DIR="docs/commit-logs/$BRANCH_NAME"
README_FILE="$LOG_DIR/README.md"

# Check if the log directory exists
if [ ! -d "$LOG_DIR" ]; then
  echo "ERROR: Log directory $LOG_DIR does not exist. Skipping README update."
  exit 1
fi

# Generate README content
{
  echo "# Commit Log for Branch: \`$BRANCH_NAME\`"
  echo
  echo "This file provides a summary of all commits in the branch \`$BRANCH_NAME\`."
  echo "Each commit links to its detailed log."
  echo
  echo "| Commit Hash | Date       | Author       | Message           |"
  echo "|-------------|------------|--------------|-------------------|"

  # Loop through all Markdown files in the log directory
  for log_file in "$LOG_DIR"/*.md; do
    # Exclude README.md itself
    if [[ $(basename "$log_file") == "README.md" ]]; then
      continue
    fi

    if [ -f "$log_file" ]; then
      # Extract commit details from the file name and content
      COMMIT_HASH=$(basename "$log_file" .md)
      COMMIT_DATE=$(git show -s --format="%ad" --date=short "$COMMIT_HASH")
      COMMIT_AUTHOR=$(git show -s --format="%an" "$COMMIT_HASH")
      COMMIT_MESSAGE=$(git show -s --format="%s" "$COMMIT_HASH")

      # Add a row to the table
      echo "| [$COMMIT_HASH](./$COMMIT_HASH.md) | $COMMIT_DATE | $COMMIT_AUTHOR | $COMMIT_MESSAGE |"
    fi
  done
  echo
} > "$README_FILE"

# Debugging output
echo "README.md updated at $README_FILE"

# Stage the README file for commit
git add "$README_FILE"
if [ $? -ne 0 ]; then
  echo "ERROR: Failed to stage $README_FILE"
  exit 1
fi
echo "DEBUG: Successfully staged $README_FILE"
