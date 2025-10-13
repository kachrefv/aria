from textual.widgets import Static
from textual.containers import Horizontal
from textual.app import ComposeResult

class DashboardHeader(Static):
    """Dashboard header component"""
    
    def __init__(self, project_goal: str):
        super().__init__()
        self.project_goal = project_goal
    
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Static("🌀 Aria Dashboard", classes="header-title"),
            Static(f"Project: {self.project_goal}", classes="header-project"),
            classes="header-container"
        )