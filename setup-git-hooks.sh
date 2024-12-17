#!/bin/bash

echo "Starting installation of Git hooks for compose-file-generator!"


# Ensure the .git/hooks directory exists
HOOKS_DIR=".git/hooks"
mkdir -p "$HOOKS_DIR"

# Copy all custom hooks from git-hooks to .git/hooks
cp git-hooks/* "$HOOKS_DIR"
chmod +x "$HOOKS_DIR/"*

echo "Git hooks installed successfully!"

