from pathlib import Path
from typing import Dict, List, Any
from ..core.ai_engine import AIEngine
from .base import BasePlugin

class CodeReviewPlugin(BasePlugin):
    """Code review plugin for aria"""
    
    def __init__(self):
        self.ai_engine = AIEngine()
    
    @property
    def name(self) -> str:
        return "code_review"
    
    @property
    def description(self) -> str:
        return "AI-powered code review and analysis"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    def analyze_project(self, project_path: Path) -> Dict[str, Any]:
        """Analyze code quality"""
        return {
            "framework": "code_review",
            "files_analyzed": 0,
            "issues": [],
            "recommendations": ["Use 'aria review <file>' to analyze specific files"]
        }
    
    def scaffold_project(self, project_name: str, target_path: Path) -> Dict[str, Any]:
        """Code review doesn't scaffold projects"""
        return {
            "success": False,
            "error": "Code review plugin cannot scaffold projects"
        }
    
    def generate_code(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code review"""
        
        code_to_review = task.get('code', '')
        if not code_to_review:
            return {
                "success": False,
                "error": "No code provided for review"
            }
        
        system_prompt = """You are an expert code reviewer. Analyze the provided code for:
1. Security vulnerabilities
2. Performance issues
3. Code smells and anti-patterns
4. Best practices compliance
5. Potential bugs
6. Readability and maintainability

Provide specific, actionable feedback."""
        
        user_prompt = f"Please review this code:\n\n```\n{code_to_review}\n```"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = self.ai_engine.chat_completion(messages, temperature=0.1)
            review = response["choices"][0]["message"]["content"]
            
            return {
                "success": True,
                "review": review,
                "files_created": []
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Code review failed: {str(e)}"
            }