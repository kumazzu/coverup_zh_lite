import pytest
import tempfile
import os
from pathlib import Path
from utils import run


class TestRun:
    """Tests for the run function in utils.py."""
    
    def test_simple_command_success(self):
        """Test running a simple successful command."""
        returncode, stdout, stderr = run(["echo", "hello"])
        assert returncode == 0
        assert stdout.strip() == "hello"
        assert stderr == ""
    
    def test_command_with_string_input(self):
        """Test running a command passed as a string."""
        returncode, stdout, stderr = run("echo hello world")
        assert returncode == 0
        assert stdout.strip() == "hello world"
        assert stderr == ""
    
    def test_command_failure(self):
        """Test running a command that fails."""
        returncode, stdout, stderr = run(["ls", "/nonexistent/directory"])
        assert returncode != 0
        assert "No such file or directory" in stderr or "cannot access" in stderr
    
    def test_command_with_cwd(self):
        """Test running a command with a specific working directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            test_file = tmppath / "test.txt"
            test_file.write_text("test content")
            
            returncode, stdout, stderr = run(["ls"], cwd=tmppath)
            assert returncode == 0
            assert "test.txt" in stdout
    
    def test_command_with_env(self):
        """Test running a command with custom environment variables."""
        import sys
        env = {"TEST_VAR": "test_value"}
        returncode, stdout, stderr = run([sys.executable, "-c", "import os; print(os.environ.get('TEST_VAR', 'not_found'))"], env=env)
        assert returncode == 0
        assert stdout.strip() == "test_value"
    
    def test_command_with_timeout(self):
        """Test that timeout parameter is respected."""
        # This test runs a quick command with a long timeout - should succeed
        returncode, stdout, stderr = run(["echo", "quick"], timeout=10)
        assert returncode == 0
        assert stdout.strip() == "quick"
    
    def test_python_command(self):
        """Test running a Python command."""
        import sys
        returncode, stdout, stderr = run([sys.executable, "-c", "print(2 + 2)"])
        assert returncode == 0
        assert stdout.strip() == "4"
    
    def test_command_with_stderr(self):
        """Test command that writes to stderr."""
        import sys
        returncode, stdout, stderr = run([sys.executable, "-c", "import sys; sys.stderr.write('error message\\n')"])
        assert returncode == 0
        assert stdout == ""
        assert "error message" in stderr
    
    def test_nonexistent_command(self):
        """Test running a nonexistent command raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            run(["nonexistent_command_12345"])
    
    def test_empty_command_list(self):
        """Test that empty command list raises an error."""
        with pytest.raises((ValueError, IndexError)):
            run([])
    
    def test_path_object_cwd(self):
        """Test that Path objects work for cwd parameter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            returncode, stdout, stderr = run(["pwd"], cwd=tmppath)
            assert returncode == 0
            assert str(tmppath) in stdout or tmppath.name in stdout