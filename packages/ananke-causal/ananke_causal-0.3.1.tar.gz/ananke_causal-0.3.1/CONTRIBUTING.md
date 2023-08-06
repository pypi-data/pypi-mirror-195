# Contributing

# Development Quickstart

- Install `poetry` from [https://python-poetry.org](here).

```{bash}
git clone git@gitlab.com:causal/ananke.git

cd ananke

poetry install

source $(poetry env info --path)/bin/activate # this activates your environment
```

- Install development packages:

```{bash}
poetry install --with dev
```

- Install pre-commit hooks (ensure that all code is formatted correctly before committing)

```{bash}
pre-commit install
```

- Building the sphinx-notebook support:
```{bash}
# this will depend on your environment, e.g.
sudo apt install pandoc # ubuntu
sudo dnf install pandoc # fedora
```

- graphviz (see [README.md](README.md))


Now you are ready to develop!


# Developing Notes 
## Running Tests
```
## Adding Requirements

Python packages that are required for development purposes but not for production purposes (e.g. `pytest`) should be placed into `dev_requirements.txt`. Python packages that are required for both development and production purposes should be added to the `requirement` list in `setup.py`.

Non-Python packages should be separately added to the CI configuration in `.gitlab.ci.yml` as well as `tox.ini`, and a note on how to install this non-Python package added to the documentation in `docs`.

## Before Pushing 
Consider using the following command to lint the code

`flake8 ananke/`


## Test Coverage

```{bash}
pytest --cov=ananke tests/  # to generate the base report

```

## Running tests through tox
Tox runs tests as if they were installed from the pypi repository. Run `tox` in the project root to run the pytest tests in a virtualenv with ananke installed as a non-editable package.

## Development Git pattern

Ideally the cycle should work like this:

* An issue is created requesting a feature or a bugfix
* Create branch from `dev` (e.g. `mybranch`) and make changes
* Add a line in `CHANGELOG.md` to describe your feature
* Update docs if required
* Push changes to `mybranch`

## Building docs
* To build docs, run `bash run.sh` from the `docs` folder.
* Add tutorial notebooks in `docs/notebooks`. These are automatically built into webpages.
* Maintain a `references.bib` in `docs/source`. 

## How to update the pypi repository
* `git fetch --all`
* `git checkout dev`
* (OPTIONAL) `git merge master` (in case of any merge conflicts with master)
* `poetry version <type>` where `<type> = major/minor/patch` as appropriate
* Update `CHANGELOG.md` 
* Commit `CHANGELOG.md` with message `v*.*.*` as appropriate
* Tag the gitlab release with the new version number using `git tag -a v*.*.* -m "v*.*.*"`
* `git push origin --tags`
* `git checkout master && git merge dev` (this prepares master for the new release)
* `git push origin dev`
* `git push origin master`
* `poetry build`
* `poetry publish`
