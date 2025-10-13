from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Tree, Label
from textual.widgets.tree import TreeNode
from typing import Dict, Any

class TaskViewer(Static):
    """Task viewer component"""
    
    def __init__(self, plan: Dict[str, Any]):
        super().__init__()
        self.plan = plan
    
    def compose(self) -> ComposeResult:
        yield Label("Project Tasks")
        
        tree = Tree("Project Structure")
        tree.root.expand()
        
        # Add modules to tree
        for module in self.plan.get("top_modules", []):
            module_node = tree.root.add(module["name"], expand=False)
            module_node.allow_expand = True
            
            # Add tasks to module
            for task in module.get("tasks", []):
                task_node = module_node.add(
                    f"{task['title']} ({task.get('estimated_hours', 0)}h)",
                    expand=False
                )
                task_node.allow_expand = True
        
        yield tree