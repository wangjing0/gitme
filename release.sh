#!/bin/bash
# Release script for gitme-cli

# Check if version argument is provided
if [ -z "$1" ]; then
    echo "Usage: ./release.sh <version> [--yes]"
    echo "Example: ./release.sh 0.2.0"
    echo "Use --yes to skip confirmation prompt"
    exit 1
fi

VERSION=$1
SKIP_CONFIRM=false

# Check for --yes flag
if [ "$2" = "--yes" ]; then
    SKIP_CONFIRM=true
fi

# Update version in files
echo "Updating version to $VERSION..."
sed -i '' "s/version = \"[^\"]*\"/version = \"$VERSION\"/" pyproject.toml
sed -i '' "s/__version__ = \"[^\"]*\"/__version__ = \"$VERSION\"/" src/gitme/__init__.py

# Clean and build
echo "Building package..."
rm -rf dist/ build/ src/*.egg-info
python -m build

# Check package
echo "Checking package..."
twine check dist/*

# Confirm before uploading
echo "Ready to upload version $VERSION to PyPI"

if [ "$SKIP_CONFIRM" = true ]; then
    REPLY="y"
    echo "Skipping confirmation (--yes flag provided)"
else
    read -p "Continue? (y/n) " -n 1 -r
    echo
fi

if [[ $REPLY =~ ^[Yy]$ ]]; then
    twine upload dist/*
    
    # Create git tag
    git add -A
    git commit -m "Release version $VERSION"
    git tag "v$VERSION"
    git push origin main --tags
    
    echo "Release $VERSION complete!"
else
    echo "Release cancelled"
fi