#!/usr/bin/env bash

# rm -rf dist
# python3 setup.py sdist
# twine upload dist/*

# cd ..
# [ ! -d "staged-recipes" ] && git clone https://github.com/conda-forge/staged-recipes
# cd staged-recipes
# git pull

## https://conda-forge.org/docs/maintainer/adding_pkgs.html
grayskull pypi osmpythontools
cd osmpythontools && sed -i '' 's/AddYourGitHubIdHere/mocnik-science/' meta.yaml && sed -i '' 's/- python/- python >=3.6/' meta.yaml && sed -i '' 's/GPL-3.0/GPL-3.0-only/' meta.yaml

# https://github.com/conda-forge/staged-recipes/pull/21749
