from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Header, Footer, Static, Button
from textual.binding import Binding
from typing import Dict, Any

from .components.header import DashboardHeader
from .components.task_tree import TaskTree
from .components.reasoning_log import ReasoningLog

class AriaDashboard(App):
    """Main TUI Dashboard for aria"""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    .sidebar {
        width: 40%;
        border: solid $primary;
        background: $panel;
    }
    
    .main {
        width: 60%;
    }
    
    .task-details {
        height: 60%;
        border: solid $secondary;
        background: $panel;
    }
    
    .reasoning-log {
        height: 40%;
        border: solid $accent;
        background: $panel;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "regenerate", "Regenerate Plan"),
        Binding("s", "save", "Save"),
        Binding("space", "toggle_task", "Toggle Complete"),
        Binding("enter", "expand", "Expand/Collapse"),
    ]
    
    def __init__(self, plan: Dict[str, Any]):
        super().__init__()
        self.plan = plan
    
    def compose(self) -> ComposeResult:
        yield DashboardHeader(self.plan.get("goal", "Unknown Project"))
        
        with Container():
            with Container(classes="sidebar"):
                yield TaskTree(self.plan)
            
            with Container(classes="main"):
                with Container(classes="task-details"):
                    yield Static("Select a task to view details", id="task-details")
                with Container(classes="reasoning-log"):
                    yield ReasoningLog()
        
        yield Footer()
    
    def on_mount(self) -> None:
        self.title = "🌀 Aria Dashboard"
        self.sub_title = "AI-Powered Project Management"
    
    def action_quit(self) -> None:
        self.exit()
    
    def action_regenerate(self) -> None:
        self.notify("🔁 Regenerating plan with AI...")
        # Implementation would call AI to regenerate plan
    
    def action_save(self) -> None:
        self.notify("💾 Plan saved!")
        # Implementation would save current state
    
    def action_toggle_task(self) -> None:
        self.notify("✅ Task status toggled")
        # Implementation would toggle task completion
    
    def action_expand(self) -> None:
        self.notify("📂 Expanded/collapsed section")
        # Implementation would handle expand/collapse

def run_tui(plan: Dict[str, Any]):
    """Run the TUI dashboard with given plan"""
    app = AriaDashboard(plan)
    app.run()