"""
Tests for the pyclean CLI
"""
import os
import platform

try:
    from unittest.mock import patch
except ImportError:  # Python 2.7, PyPy2
    from mock import patch

from cli_test_helpers import ArgvContext, shell

import pyclean.cli


def test_entrypoint():
    """
    Is entrypoint script installed? (setup.py)
    """
    result = shell('pyclean --help')
    assert result.exit_code == 0


def test_entrypoint_py2_installed():
    """
    Is entrypoint script installed for Python 2? (setup.py)
    """
    result = shell('py2clean --help')
    assert result.exit_code == 0


@patch('pyclean.compat.import_module')
def test_entrypoint_py2_working(mock_import_module):
    """
    Is entrypoint overriding with Python 2 implementation?
    """
    with ArgvContext('py2clean', 'foo'):
        pyclean.cli.py2clean()

    args, _ = mock_import_module.call_args
    assert args == ('pyclean.py2clean',)


def test_entrypoint_py3_installed():
    """
    Is entrypoint script installed for Python 3? (setup.py)
    """
    result = shell('py3clean --help')
    assert result.exit_code == 0


@patch('pyclean.compat.import_module')
def test_entrypoint_py3_working(mock_import_module):
    """
    Is entrypoint overriding with Python 3 implementation?
    """
    with ArgvContext('py3clean', 'foo'):
        pyclean.cli.py3clean()

    args, _ = mock_import_module.call_args
    assert args == ('pyclean.py3clean',)


def test_entrypoint_pypy_installed():
    """
    Is entrypoint script installed for PyPy 2/3? (setup.py)
    """
    result = shell('pypyclean --help')
    assert result.exit_code == 0


@patch('pyclean.compat.import_module')
def test_entrypoint_pypy_working(mock_import_module):
    """
    Is entrypoint overriding with PyPy implementation?
    """
    with ArgvContext('pypyclean', 'foo'):
        pyclean.cli.pypyclean()

    args, _ = mock_import_module.call_args
    assert args == ('pyclean.pypyclean',)


def test_version_option():
    """
    Does --version yield the expected information?
    """
    expected_output = '' if platform.python_version_tuple() < ('3',) \
        else '%s%s' % (
            pyclean.__version__,
            os.linesep
        )

    result = shell('pyclean --version')

    assert result.stdout == expected_output
    assert result.exit_code == 0


@patch('pyclean.compat.get_implementation')
def test_legacy_calls_compat(mock_get_implementation):
    """
    Does calling `pyclean --legacy` invoke the compat layer?
    """
    with ArgvContext('pyclean', '--legacy', 'foo'):
        pyclean.cli.main()

    assert mock_get_implementation.called


@patch('pyclean.modern.pyclean')
def test_default_modern(mock_modern_pyclean):
    """
    Does simply calling `pyclean` invoke the modern implementation?
    """
    with ArgvContext('pyclean', 'foo'):
        pyclean.cli.main()

    assert mock_modern_pyclean.called
