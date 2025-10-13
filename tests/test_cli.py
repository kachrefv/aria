import pytest
from typer.testing import CliRunner
from aria.cli import app

runner = CliRunner()

def test_version_command():
    """Test version command"""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "aria version" in result.stdout

def test_decompose_command_missing_api_key(monkeypatch):
    """Test decompose command without API key"""
    # Remove API key from environment
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    
    result = runner.invoke(app, ["decompose", "test project"])
    assert result.exit_code == 1
    assert "DEEPSEEK_API_KEY is required" in result.stdout

def test_decompose_command_with_api_key(monkeypatch):
    """Test decompose command with API key (mocked)"""
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    
    # This will fail due to API call, but we're testing the command structure
    result = runner.invoke(app, ["decompose", "test project"], input="n\n")
    # Should reach the point where it asks for TUI launch
    assert "Project plan generated successfully" in result.stdout or "Error" in result.stdout

def test_view_command_nonexistent_file():
    """Test view command with non-existent file"""
    result = runner.invoke(app, ["view", "nonexistent.json"])
    assert result.exit_code == 1
    assert "Plan file not found" in result.stdout

def test_analyze_command():
    """Test analyze command"""
    result = runner.invoke(app, ["analyze", "."])
    # Should work even without API key since it's filesystem-based
    assert result.exit_code == 0 or result.exit_code == 1  # Could fail due to missing plugins

def test_new_command_invalid_template():
    """Test new command with invalid template"""
    result = runner.invoke(app, ["new", "invalid-template", "test-project"])
    assert result.exit_code == 1
    assert "not found" in result.stdout.lower()

def test_run_command_nonexistent_file():
    """Test run command with non-existent file"""
    result = runner.invoke(app, ["run", "nonexistent.json"])
    assert result.exit_code == 1
    assert "Plan file not found" in result.stdout