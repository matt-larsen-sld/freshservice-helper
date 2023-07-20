[setup.cfg](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html)

[install_requires](https://packaging.python.org/en/latest/discussions/install-requires-vs-requirements/#install-requires-vs-requirements-files)

`bumpversion <VERSION_INDICATOR>`  [major | minor | patch]

from the root of the project:
`python -m build`

Commit and tag

Upload build to PyPi:
`twine upload -r pypi dist/*<VERSION>*`
