[setup.cfg](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html)

[install_requires](https://packaging.python.org/en/latest/discussions/install-requires-vs-requirements/#install-requires-vs-requirements-files)

python3 ./setup.py  sdist bdist_wheel

twine upload -r pypi dist/*<VERSION>*