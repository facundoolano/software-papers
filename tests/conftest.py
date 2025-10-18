"""Shared pytest fixtures for all tests."""

import tempfile
from pathlib import Path
from typing import Dict, Any

import pytest


@pytest.fixture
def temp_dir(tmp_path):
    """
    Provide a temporary directory for test file operations.

    Args:
        tmp_path: pytest's built-in temporary directory fixture

    Returns:
        Path: A pathlib.Path object pointing to the temporary directory
    """
    return tmp_path


@pytest.fixture
def temp_file(temp_dir):
    """
    Create a temporary file in the temp directory.

    Args:
        temp_dir: The temporary directory fixture

    Returns:
        Path: A pathlib.Path object pointing to the temporary file
    """
    temp_file = temp_dir / "test_file.txt"
    temp_file.touch()
    return temp_file


@pytest.fixture
def sample_yaml_data() -> Dict[str, Any]:
    """
    Provide sample YAML data structure for testing.

    Returns:
        Dict: A sample data structure representing paper information
    """
    return {
        "title": "Test Paper",
        "author": "John Doe",
        "year": 2024,
        "link": "https://example.com/paper.pdf",
        "topics": ["testing", "software engineering"],
        "related": []
    }


@pytest.fixture
def sample_paper_entry() -> Dict[str, Any]:
    """
    Provide a complete sample paper entry with related papers.

    Returns:
        Dict: A complete paper entry structure
    """
    return {
        "title": "The Art of Testing",
        "author": "Jane Smith, Bob Johnson",
        "year": 2023,
        "link": "https://example.com/testing.pdf",
        "topics": ["testing", "quality assurance"],
        "related": [
            {
                "title": "Testing Best Practices",
                "author": "Alice Brown",
                "year": 2022,
                "link": "https://example.com/best-practices.pdf"
            }
        ]
    }


@pytest.fixture
def sample_yaml_file(temp_dir, sample_yaml_data):
    """
    Create a temporary YAML file with sample data.

    Args:
        temp_dir: The temporary directory fixture
        sample_yaml_data: Sample YAML data to write

    Returns:
        Path: Path to the created YAML file
    """
    import yaml

    yaml_file = temp_dir / "test_papers.yml"
    with open(yaml_file, 'w') as f:
        yaml.dump([sample_yaml_data], f)

    return yaml_file


@pytest.fixture
def mock_response(mocker):
    """
    Create a mock HTTP response object.

    Args:
        mocker: pytest-mock fixture

    Returns:
        Mock: A configured mock response object
    """
    mock = mocker.Mock()
    mock.status_code = 200
    mock.ok = True
    return mock


@pytest.fixture
def mock_requests_head(mocker, mock_response):
    """
    Mock requests.head() to return a successful response.

    Args:
        mocker: pytest-mock fixture
        mock_response: Mock response fixture

    Returns:
        Mock: The mocked requests.head function
    """
    return mocker.patch('requests.head', return_value=mock_response)


@pytest.fixture
def mock_requests_get(mocker, mock_response):
    """
    Mock requests.get() to return a successful response.

    Args:
        mocker: pytest-mock fixture
        mock_response: Mock response fixture

    Returns:
        Mock: The mocked requests.get function
    """
    return mocker.patch('requests.get', return_value=mock_response)


@pytest.fixture
def papers_yml_path():
    """
    Provide the path to the actual papers.yml file.

    Returns:
        Path: Path to papers.yml in the project root
    """
    return Path(__file__).parent.parent / "papers.yml"


@pytest.fixture
def readme_template_path():
    """
    Provide the path to the README template file.

    Returns:
        Path: Path to README.md.template in the project root
    """
    return Path(__file__).parent.parent / "README.md.template"
