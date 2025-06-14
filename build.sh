#! /bin/bash

set -eux

hugo
cd public
git rm -r pagefind
npx -y pagefind --site .
git add * && git commit -m "Rebuild" && git push
cd ..
git add public
git commit -m "Rebuild site" && git push
