#!/bin/sh
# Deploy Bazaar to GitHub Pages
# Creates a gh-pages branch with only the bazaar/ files and pushes it.

set -e
cd "$(dirname "$0")/.."

TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

echo "Building gh-pages branch..."
git worktree add "$TMPDIR" --orphan gh-pages 2>/dev/null || \
  git worktree add "$TMPDIR" gh-pages 2>/dev/null || {
    echo "Creating fresh worktree..."
    git worktree add "$TMPDIR" --orphan gh-pages
  }

cp -r bazaar/* "$TMPDIR/"
cd "$TMPDIR"
git add -A
git commit -m "Deploy Bazaar P2P social platform" --allow-empty
git push -f origin gh-pages
cd -
git worktree remove "$TMPDIR" --force 2>/dev/null

echo "Done! Enable GitHub Pages on the gh-pages branch in your repo settings."
echo "Settings > Pages > Source: Deploy from branch > gh-pages"
