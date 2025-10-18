"""Validation tests to verify the testing infrastructure is set up correctly."""

import sys
from pathlib import Path

import pytest


class TestInfrastructure:
    """Tests to validate the testing infrastructure setup."""

    def test_pytest_is_working(self):
        """Verify that pytest is installed and running correctly."""
        assert True

    def test_python_version(self):
        """Verify Python version is 3.8 or higher."""
        assert sys.version_info >= (3, 8), f"Python version {sys.version_info} is too old"

    def test_pytest_markers_available(self, pytestconfig):
        """Verify that custom pytest markers are registered."""
        markers_raw = pytestconfig.getini("markers")
        # markers_raw is a list of strings like "unit: Unit tests..."
        markers = [marker.split(":")[0] for marker in markers_raw]
        assert "unit" in markers, "unit marker not registered"
        assert "integration" in markers, "integration marker not registered"
        assert "slow" in markers, "slow marker not registered"

    def test_project_structure(self):
        """Verify that the expected project structure exists."""
        project_root = Path(__file__).parent.parent

        # Check for key project files
        assert (project_root / "pyproject.toml").exists(), "pyproject.toml not found"
        assert (project_root / "papers.yml").exists(), "papers.yml not found"
        assert (project_root / "README.md").exists(), "README.md not found"

        # Check for Python scripts
        assert (project_root / "gen_readme.py").exists(), "gen_readme.py not found"
        assert (project_root / "check_links.py").exists(), "check_links.py not found"

    def test_test_directory_structure(self):
        """Verify that the test directory structure is set up correctly."""
        tests_dir = Path(__file__).parent

        assert tests_dir.exists(), "tests directory not found"
        assert (tests_dir / "__init__.py").exists(), "tests/__init__.py not found"
        assert (tests_dir / "conftest.py").exists(), "conftest.py not found"
        assert (tests_dir / "unit").exists(), "tests/unit directory not found"
        assert (tests_dir / "unit" / "__init__.py").exists(), "tests/unit/__init__.py not found"
        assert (tests_dir / "integration").exists(), "tests/integration directory not found"
        assert (tests_dir / "integration" / "__init__.py").exists(), "tests/integration/__init__.py not found"


class TestFixtures:
    """Tests to verify that shared fixtures are working correctly."""

    def test_temp_dir_fixture(self, temp_dir):
        """Verify that the temp_dir fixture provides a valid directory."""
        assert temp_dir.exists(), "temp_dir fixture does not provide an existing directory"
        assert temp_dir.is_dir(), "temp_dir fixture does not provide a directory"

    def test_temp_file_fixture(self, temp_file):
        """Verify that the temp_file fixture provides a valid file."""
        assert temp_file.exists(), "temp_file fixture does not provide an existing file"
        assert temp_file.is_file(), "temp_file fixture does not provide a file"

    def test_sample_yaml_data_fixture(self, sample_yaml_data):
        """Verify that the sample_yaml_data fixture provides valid data."""
        assert isinstance(sample_yaml_data, dict), "sample_yaml_data is not a dictionary"
        assert "title" in sample_yaml_data, "sample_yaml_data missing 'title' key"
        assert "author" in sample_yaml_data, "sample_yaml_data missing 'author' key"
        assert "year" in sample_yaml_data, "sample_yaml_data missing 'year' key"
        assert "link" in sample_yaml_data, "sample_yaml_data missing 'link' key"

    def test_sample_paper_entry_fixture(self, sample_paper_entry):
        """Verify that the sample_paper_entry fixture provides valid data."""
        assert isinstance(sample_paper_entry, dict), "sample_paper_entry is not a dictionary"
        assert "related" in sample_paper_entry, "sample_paper_entry missing 'related' key"
        assert isinstance(sample_paper_entry["related"], list), "related field is not a list"

    def test_sample_yaml_file_fixture(self, sample_yaml_file):
        """Verify that the sample_yaml_file fixture creates a valid YAML file."""
        assert sample_yaml_file.exists(), "sample_yaml_file does not exist"
        assert sample_yaml_file.suffix == ".yml", "sample_yaml_file does not have .yml extension"

        import yaml
        with open(sample_yaml_file) as f:
            data = yaml.safe_load(f)

        assert isinstance(data, list), "YAML data is not a list"
        assert len(data) > 0, "YAML data is empty"

    def test_mock_response_fixture(self, mock_response):
        """Verify that the mock_response fixture provides a valid mock."""
        assert mock_response.status_code == 200, "mock_response does not have status_code 200"
        assert mock_response.ok is True, "mock_response.ok is not True"


@pytest.mark.unit
class TestUnitMarker:
    """Test to verify the unit marker works."""

    def test_unit_marker(self):
        """This test should be marked as a unit test."""
        assert True


@pytest.mark.integration
class TestIntegrationMarker:
    """Test to verify the integration marker works."""

    def test_integration_marker(self):
        """This test should be marked as an integration test."""
        assert True


@pytest.mark.slow
class TestSlowMarker:
    """Test to verify the slow marker works."""

    def test_slow_marker(self):
        """This test should be marked as a slow test."""
        assert True
