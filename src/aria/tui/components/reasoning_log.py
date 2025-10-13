from textual.widgets import Static, TextArea
from textual.containers import Vertical
from textual.app import ComposeResult

class ReasoningLog(Static):
    """AI reasoning log display"""
    
    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("🤖 AI Reasoning Log", classes="log-header"),
            TextArea("AI reasoning will appear here...", language="markdown", read_only=True),
            classes="reasoning-container"
        )