import pytest
from pathlib import Path
from aria.plugins.base import PluginManager, BasePlugin
from aria.plugins.nextjs import NextJSPlugin
from aria.plugins.python_flask import FlaskPlugin

def test_plugin_manager_initialization():
    """Test PluginManager initialization"""
    manager = PluginManager()
    
    # Should have built-in plugins loaded
    assert "nextjs" in manager.plugins
    assert "flask" in manager.plugins
    assert "code_review" in manager.plugins

def test_nextjs_plugin_properties():
    """Test NextJSPlugin properties"""
    plugin = NextJSPlugin()
    
    assert plugin.name == "nextjs"
    assert plugin.description == "Next.js 14+ project scaffolding and analysis"
    assert plugin.version == "1.0.0"

def test_flask_plugin_properties():
    """Test FlaskPlugin properties"""
    plugin = FlaskPlugin()
    
    assert plugin.name == "flask"
    assert plugin.description == "Flask project scaffolding and analysis"
    assert plugin.version == "1.0.0"

def test_nextjs_plugin_analyze(tmp_path):
    """Test NextJSPlugin analyze method"""
    plugin = NextJSPlugin()
    
    # Create a mock Next.js project
    (tmp_path / "package.json").write_text('{"dependencies": {"next": "14.0.0"}}')
    (tmp_path / "app").mkdir()
    
    analysis = plugin.analyze_project(tmp_path)
    
    assert analysis["framework"] == "nextjs"
    assert analysis["version"] == "14.0.0"
    assert analysis["app_router_used"] == True
    assert analysis["files_analyzed"] > 0

def test_flask_plugin_scaffold(tmp_path):
    """Test FlaskPlugin scaffold method"""
    plugin = FlaskPlugin()
    
    result = plugin.scaffold_project("test-flask-app", tmp_path)
    
    assert result["success"] == True
    assert (tmp_path / "test-flask-app" / "app.py").exists()
    assert (tmp_path / "test-flask-app" / "requirements.txt").exists()
    assert "cd test-flask-app" in result["next_steps"][0]

def test_plugin_manager_scaffold(tmp_path):
    """Test PluginManager scaffold method"""
    manager = PluginManager()
    
    # Test with valid template
    result = manager.scaffold_project("flask", "test-app", tmp_path)
    assert result["success"] == True
    
    # Test with invalid template
    result = manager.scaffold_project("invalid", "test-app", tmp_path)
    assert result["success"] == False
    assert "not found" in result["error"]

def test_code_review_plugin():
    """Test CodeReviewPlugin"""
    from aria.plugins.code_review import CodeReviewPlugin
    
    plugin = CodeReviewPlugin()
    
    assert plugin.name == "code_review"
    assert plugin.description == "AI-powered code review and analysis"
    
    # Test code review with empty code
    task = {"code": ""}
    result = plugin.generate_code(task, {})
    assert result["success"] == False
    assert "No code provided" in result["error"]

def test_abstract_base_plugin():
    """Test that BasePlugin cannot be instantiated"""
    with pytest.raises(TypeError):
        BasePlugin()