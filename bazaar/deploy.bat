@echo off
REM Deploy Bazaar to GitHub Pages
REM Creates a gh-pages branch with only the bazaar/ files and pushes it.

echo Deploying Bazaar to GitHub Pages...

REM Create temp worktree
git worktree add /tmp/bazaar-deploy gh-pages 2>nul || (
    git worktree add /tmp/bazaar-deploy --orphan gh-pages
)

REM Copy files
xcopy /E /I /Y bazaar\*.* C:\tmp\bazaar-deploy\

REM Commit and push
cd C:\tmp\bazaar-deploy
git add -A
git commit -m "Deploy Bazaar P2P social platform"
git push -f origin gh-pages

REM Cleanup
cd ..\..
git worktree remove /tmp/bazaar-deploy --force

echo Done! Enable GitHub Pages on the gh-pages branch in repo settings.
