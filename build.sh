#! /bin/bash

set -eux

hugo
cd public
npx -y prettier --write "**/*.{html,css}"
git rm -r pagefind || true
npx -y pagefind --site .
git add * && git commit -m "Rebuild" && git push
cd ..
git add public
git commit -m "Rebuild site" && git push
