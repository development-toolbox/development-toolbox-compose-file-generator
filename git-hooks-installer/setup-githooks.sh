#!/bin/bash

# Script: setup-githooks.sh
# Description: Setup git hooks and copy the scripts directory to $REPO_ROOT/scripts.

# Step 1: Get the repository root directory
REPO_ROOT=$(git rev-parse --show-toplevel)
if [ $? -ne 0 ]; then
    echo "Error: Not inside a Git repository."
    exit 1
fi

# Step 2: Locate the script's directory
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Step 3: Define the source directories
HOOKS_SRC="$SCRIPT_DIR/git-hooks"
SCRIPTS_SRC="$SCRIPT_DIR/scripts"

# Step 4: Validate the source directories
if [ ! -d "$HOOKS_SRC" ]; then
    echo "Error: Hook source directory '$HOOKS_SRC' does not exist."
    exit 1
fi

if [ ! -d "$SCRIPTS_SRC" ]; then
    echo "Error: Scripts source directory '$SCRIPTS_SRC' does not exist."
    exit 1
fi

# Step 5: Define the target directories
HOOKS_DIR="$REPO_ROOT/.git/hooks"
SCRIPTS_DEST="$REPO_ROOT/scripts"

# Step 6: Ensure the target directories exist
mkdir -p "$HOOKS_DIR"
mkdir -p "$SCRIPTS_DEST"

# Step 7: Copy hooks to .git/hooks
cp "$HOOKS_SRC"/* "$HOOKS_DIR" || {
    echo "Error: Failed to copy hooks."
    exit 1
}

# Step 8: Copy the entire scripts directory to $REPO_ROOT/scripts
cp -r "$SCRIPTS_SRC/"* "$SCRIPTS_DEST/" || {
    echo "Error: Failed to copy scripts."
    exit 1
}

# Step 9: Make hooks and scripts executable
chmod +x "$HOOKS_DIR/"* || {
    echo "Error: Failed to set hooks as executable."
    exit 1
}
chmod -R +x "$SCRIPTS_DEST" || {
    echo "Error: Failed to set scripts as executable."
    exit 1
}

# Success message
echo "Git hooks installed to '$HOOKS_DIR' and scripts copied to '$SCRIPTS_DEST' successfully!"
