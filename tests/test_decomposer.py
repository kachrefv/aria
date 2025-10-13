import pytest
from aria.core.decomposer import TaskDecomposer
from aria.core.ai_engine import AIEngine

def test_task_decomposer_initialization():
    """Test TaskDecomposer initialization"""
    decomposer = TaskDecomposer(
        goal="Test project",
        tech_stack="Python, FastAPI",
        constraints=["test constraint"]
    )
    
    assert decomposer.goal == "Test project"
    assert decomposer.tech_stack == "Python, FastAPI"
    assert decomposer.constraints == ["test constraint"]

def test_ai_engine_initialization(monkeypatch):
    """Test AIEngine initialization"""
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    
    engine = AIEngine()
    assert engine.provider == "deepseek"
    assert engine.api_key == "test-key"

def test_plan_validation():
    """Test plan validation logic"""
    from aria.core.decomposer import TaskDecomposer
    
    decomposer = TaskDecomposer("test")
    
    # Valid plan
    valid_plan = {
        "goal": "test",
        "top_modules": [
            {
                "id": "module-1",
                "name": "Test Module",
                "tasks": [
                    {
                        "id": "task-1", 
                        "title": "Test Task",
                        "dependencies": []
                    }
                ]
            }
        ]
    }
    
    # This should not raise an exception
    decomposer._validate_plan(valid_plan)
    
    # Invalid plan - missing goal
    invalid_plan = {
        "top_modules": []
    }
    
    with pytest.raises(ValueError, match="missing required key: goal"):
        decomposer._validate_plan(invalid_plan)
    
    # Invalid plan - top_modules not a list
    invalid_plan2 = {
        "goal": "test",
        "top_modules": "not a list"
    }
    
    with pytest.raises(ValueError, match="top_modules must be a list"):
        decomposer._validate_plan(invalid_plan2)

def test_plan_enhancement():
    """Test plan enhancement with metadata"""
    from aria.core.decomposer import TaskDecomposer
    
    decomposer = TaskDecomposer("test", "Python", ["constraint1"])
    
    basic_plan = {
        "goal": "test",
        "top_modules": [
            {
                "name": "Module 1",
                "tasks": [
                    {
                        "title": "Task 1",
                        "estimated_hours": 5
                    }
                ]
            }
        ]
    }
    
    enhanced = decomposer._enhance_plan(basic_plan)
    
    # Check metadata was added
    assert enhanced["tech_stack"] == "Python"
    assert enhanced["constraints"] == ["constraint1"]
    assert "decomposer_version" in enhanced
    
    # Check IDs were added
    assert "id" in enhanced["top_modules"][0]
    assert "id" in enhanced["top_modules"][0]["tasks"][0]
    
    # Check total hours calculated
    assert enhanced["total_hours"] == 5
    
    # Check default values
    assert enhanced["top_modules"][0]["tasks"][0]["status"] == "pending"
    assert enhanced["top_modules"][0]["tasks"][0]["priority"] == "medium"