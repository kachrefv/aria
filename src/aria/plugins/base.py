from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from pathlib import Path
import importlib.util
import sys

class BasePlugin(ABC):
    """Base class for all aria plugins"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Plugin description"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version"""
        pass
    
    @abstractmethod
    def analyze_project(self, project_path: Path) -> Dict[str, Any]:
        """Analyze existing project structure"""
        pass
    
    @abstractmethod
    def scaffold_project(self, project_name: str, target_path: Path) -> Dict[str, Any]:
        """Scaffold new project"""
        pass
    
    @abstractmethod
    def generate_code(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code for specific task"""
        pass

class PluginManager:
    """Manage loading and execution of plugins"""
    
    def __init__(self):
        self.plugins: Dict[str, BasePlugin] = {}
        self.load_builtin_plugins()
    
    def load_builtin_plugins(self):
        """Load built-in plugins"""
        try:
            from .nextjs import NextJSPlugin
            self.register_plugin(NextJSPlugin())
        except ImportError as e:
            print(f"Warning: Could not load NextJS plugin: {e}")
        
        try:
            from .python_flask import FlaskPlugin
            self.register_plugin(FlaskPlugin())
        except ImportError as e:
            print(f"Warning: Could not load Flask plugin: {e}")
        
        try:
            from .code_review import CodeReviewPlugin
            self.register_plugin(CodeReviewPlugin())
        except ImportError as e:
            print(f"Warning: Could not load Code Review plugin: {e}")
    
    def register_plugin(self, plugin: BasePlugin):
        """Register a plugin"""
        self.plugins[plugin.name.lower()] = plugin
    
    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        """Get plugin by name"""
        return self.plugins.get(name.lower())
    
    def analyze_project(self, project_path: Path) -> Dict[str, Any]:
        """Auto-detect project type and analyze"""
        # Try to detect project type
        if (project_path / "package.json").exists():
            plugin = self.get_plugin("nextjs")
            if plugin:
                return plugin.analyze_project(project_path)
        elif (project_path / "requirements.txt").exists() or (project_path / "pyproject.toml").exists():
            plugin = self.get_plugin("flask")
            if plugin:
                return plugin.analyze_project(project_path)
        
        return {"framework": "unknown", "files_analyzed": 0, "issues": [], "recommendations": []}
    
    def scaffold_project(self, template: str, name: str, path: Path) -> Dict[str, Any]:
        """Scaffold project using specified template plugin"""
        plugin = self.get_plugin(template)
        if not plugin:
            return {
                "success": False,
                "error": f"Template '{template}' not found. Available: {list(self.plugins.keys())}"
            }
        
        return plugin.scaffold_project(name, path)