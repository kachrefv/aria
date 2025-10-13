import pytest
from pathlib import Path
from aria.utils.file_ops import read_file, write_file, get_directory_structure
from aria.utils.formatting import format_plan_summary, create_project_tree

def test_read_file(tmp_path):
    """Test read_file utility"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, World!")
    
    content = read_file(test_file)
    assert content == "Hello, World!"

def test_read_file_nonexistent():
    """Test read_file with non-existent file"""
    content = read_file(Path("nonexistent.txt"))
    assert "Error reading file" in content

def test_write_file(tmp_path):
    """Test write_file utility"""
    test_file = tmp_path / "output.txt"
    
    result = write_file(test_file, "Test content")
    
    assert result["success"] == True
    assert test_file.exists()
    assert test_file.read_text() == "Test content"

def test_get_directory_structure(tmp_path):
    """Test directory structure utility"""
    # Create test directory structure
    (tmp_path / "subdir").mkdir()
    (tmp_path / "file1.txt").write_text("test")
    (tmp_path / "subdir" / "file2.txt").write_text("test")
    
    structure = get_directory_structure(tmp_path)
    
    assert structure["name"] == tmp_path.name
    assert structure["type"] == "directory"
    assert len(structure["children"]) == 2  # subdir and file1.txt

def test_format_plan_summary():
    """Test plan summary formatting"""
    plan = {
        "goal": "Test Project",
        "architecture_overview": "Test architecture",
        "top_modules": [
            {
                "name": "Module 1",
                "description": "Module description",
                "tasks": [
                    {
                        "title": "Task 1",
                        "estimated_hours": 5,
                        "priority": "high",
                        "dependencies": ["task-0"],
                        "acceptance_criteria": ["Criterion 1", "Criterion 2"]
                    }
                ]
            }
        ]
    }
    
    summary = format_plan_summary(plan)
    
    assert "# Test Project" in summary
    assert "## Architecture Overview" in summary
    assert "### Module 1" in summary
    assert "**Task 1**" in summary
    assert "(5 hours, high priority)" in summary
    assert "Criterion 1" in summary

def test_create_project_tree():
    """Test project tree creation"""
    plan = {
        "goal": "Test Project",
        "top_modules": [
            {
                "name": "Module 1",
                "tasks": [
                    {
                        "title": "Task 1",
                        "estimated_hours": 5,
                        "priority": "high",
                        "description": "Task description",
                        "acceptance_criteria": ["Criterion 1"]
                    }
                ]
            }
        ]
    }
    
    tree = create_project_tree(plan)
    
    # The tree should be created without errors
    assert tree is not None