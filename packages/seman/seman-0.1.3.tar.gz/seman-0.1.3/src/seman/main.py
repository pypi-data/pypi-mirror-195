import logging
import os
import subprocess
from os import path

import fire
import toml


def _exe(cmd: list):
    try:
        ret = subprocess.run(cmd, cwd=os.getcwd())
        logging.info(cmd)
        logging.info(ret.stdout)
        return ret
    except subprocess.TimeoutExpired as e:
        logging.error(ret.stderr)
        logging.error(f'timeout = {e.timeout}')
    except subprocess.CalledProcessError as e:
        logging.error(ret.stderr)
        logging.error(f'returncode = {e.returncode}')
        logging.error(f'output = {e.output}')


def push():
    """Push main branch and all tags.
    """
    _exe(["git", "push", "--follow-tags", "-f", "origin", "main"])


def release(version: str):
    """Update version in pyproject.toml and commit & create tag. # noqa

    This command bumps the version of the project and writes the new version back to pyproject.toml if a valid bump rule is provided.

    The new version should be a valid PEP 440 string or a valid bump rule.

    Rule: patch, minor, major, prepatch, preminor, premajor, prerelease.

    Args:
        version (str): The version number or the rule to update the version.
    """
    # change version
    _exe(['poetry', 'version', version])

    # get version
    project = toml.load(path.join(os.getcwd(), 'pyproject.toml'))
    version_str = 'v' + project['tool']['poetry']['version']

    # generate tag
    _exe(['git', 'add', 'pyproject.toml'])
    _exe(['git', 'commit', '-S', '-m', version_str])
    _exe(['git', 'tag', '-s', version_str, '-m', version_str])


def sbom():
    """Create SBOM by cyclonedx-py"""
    _exe(["cyclonedx-py", "-e", "--force",
          "--format", "xml", "-o", "sbom.xml"])


def main():
    fire.Fire({"sbom": sbom,
               "push": push,
               "release": release})
