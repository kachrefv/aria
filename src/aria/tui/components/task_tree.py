from textual.widgets import Tree, Static
from textual.widgets.tree import TreeNode
from textual.app import ComposeResult
from typing import Dict, Any

class TaskTree(Static):
    """Interactive task tree component"""
    
    def __init__(self, plan: Dict[str, Any]):
        super().__init__()
        self.plan = plan
    
    def compose(self) -> ComposeResult:
        tree = Tree("Project Plan")
        tree.root.expand()
        
        # Build tree structure
        for module in self.plan.get("top_modules", []):
            module_node = tree.root.add(
                f"📦 {module['name']}",
                data={"type": "module", "id": module["id"]}
            )
            module_node.expand()
            
            for task in module.get("tasks", []):
                status_icon = "◯" if task.get("status") == "pending" else "✅"
                priority_icon = {
                    "high": "🔴",
                    "medium": "🟡", 
                    "low": "🟢"
                }.get(task.get("priority", "medium"), "⚪")
                
                task_node = module_node.add(
                    f"{status_icon} {priority_icon} {task['title']} ({task.get('estimated_hours', 0)}h)",
                    data={"type": "task", "id": task["id"]}
                )
        
        yield tree