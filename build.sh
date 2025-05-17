#! /bin/bash

set -eux

hugo
npx -y pagefind --site public
cd public
git add * && git commit -m "Rebuild" && git push
cd ..
git add public
git commit -m "Rebuild site" && git push
