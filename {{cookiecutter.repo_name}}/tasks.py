from invoke import run, task
import os
import subprocess
import sys

@task()
def clean(ctx):
	clean_build(ctx)
	clean_pyc(ctx)

@task()
def clean_build(ctx):
	run("rm -fr build/")
	run("rm -fr dist/")
	run("rm -fr *.egg-info")

@task()
def clean_pyc(ctx):
	run("find . -name '*.pyc' -exec rm -f {} +")
	run("find . -name '*.pyo' -exec rm -f {} +")
	run("find . -name '*~' -exec rm -f {} +")

@task()
def lint(ctx):
	run("flake8 {{ cookiecutter.repo_name }} test")

@task()
def test(ctx):
    import pytest
    args = ["--cov-report=term-missing", "-v", "--cov={{ cookiecutter.repo_name }}", "test"]
    return pytest.main(args)

@task()
def test_all(ctx):
	run(tox)

@task()
def coverage(ctx):
	run("coverage run --source {{ cookiecutter.repo_name }} setup.py test")
	run("coverage report -m")
	run("coverage html")
	run("open htmlcov/index.html")

@task()
def docs(ctx):
	run("rm -f docs/{{ cookiecutter.repo_name }}.rst")
	run("rm -f docs/modules.rst")
	run("sphinx-apidoc -o docs/ {{ cookiecutter.repo_name }}")
	run("$(MAKE) -C docs clean")
	run("$(MAKE) -C docs html")
	run("open docs/_build/html/index.html")

@task(pre=[clean])
def release(ctx):
	run("python setup.py sdist upload")
	run("python setup.py bdist_wheel upload")

@task(pre=[clean])
def sdist(ctx):
	run("python setup.py sdist")
	run("python setup.py bdist_wheel upload")
	run("ls -l dist")
