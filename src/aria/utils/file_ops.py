import os
import shutil
from pathlib import Path
from typing import List, Dict, Any

def read_file(file_path: Path) -> str:
    """Read file content with error handling"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(file_path: Path, content: str) -> Dict[str, Any]:
    """Write content to file with directory creation"""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return {"success": True, "file_path": str(file_path)}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_directory_structure(root_path: Path, max_depth: int = 3) -> Dict[str, Any]:
    """Get hierarchical directory structure"""
    
    def build_tree(path: Path, depth: int = 0) -> Dict[str, Any]:
        if depth > max_depth:
            return {"name": path.name, "type": "directory", "content": "max_depth_reached"}
        
        result = {
            "name": path.name,
            "type": "directory" if path.is_dir() else "file",
            "path": str(path)
        }
        
        if path.is_dir():
            result["children"] = []
            try:
                for item in sorted(path.iterdir()):
                    if item.name.startswith('.'):
                        continue  # Skip hidden files
                    if item.is_dir() and item.name in ['node_modules', '__pycache__', '.git']:
                        continue  # Skip large directories
                    
                    result["children"].append(build_tree(item, depth + 1))
            except PermissionError:
                result["error"] = "Permission denied"
        
        return result
    
    return build_tree(root_path)

def copy_template(template_path: Path, destination: Path, variables: Dict[str, str] = None) -> bool:
    """Copy template files with variable substitution"""
    try:
        if template_path.is_file():
            content = read_file(template_path)
            
            # Replace variables
            if variables:
                for key, value in variables.items():
                    content = content.replace(f"{{{{ {key} }}}}", value)
            
            write_file(destination, content)
            return True
            
        elif template_path.is_dir():
            shutil.copytree(template_path, destination, dirs_exist_ok=True)
            return True
            
    except Exception as e:
        print(f"Template copy failed: {e}")
        return False
    
    return False