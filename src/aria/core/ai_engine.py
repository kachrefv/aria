import json
import httpx
from typing import Dict, List, Any, Optional
from ..config import config
from ..utils.logger import setup_logger

logger = setup_logger()

class AIEngine:
    """Unified AI engine for DeepSeek and OpenAI"""
    
    def __init__(self):
        self.provider = config.AI_PROVIDER
        self.base_url = getattr(config, f"{self.provider.upper()}_BASE_URL")
        self.api_key = getattr(config, f"{self.provider.upper()}_API_KEY")
        
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = config.DEFAULT_TEMPERATURE,
        max_tokens: int = config.DEFAULT_MAX_TOKENS,
        stream: bool = False
    ) -> Dict[str, Any]:
        """Make AI API call"""
        
        if self.provider == "deepseek":
            return self._deepseek_call(messages, temperature, max_tokens, stream)
        elif self.provider == "openai":
            return self._openai_call(messages, temperature, max_tokens, stream)
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")
    
    def _deepseek_call(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int,
        stream: bool
    ) -> Dict[str, Any]:
        """Call DeepSeek API"""
        
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        try:
            with httpx.Client() as client:
                response = client.post(url, json=payload, headers=headers, timeout=30.0)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"DeepSeek API call failed: {e}")
            raise
    
    def _openai_call(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int,
        stream: bool
    ) -> Dict[str, Any]:
        """Call OpenAI-compatible API"""
        
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": "gpt-4",  # Adjust as needed
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        try:
            with httpx.Client() as client:
                response = client.post(url, json=payload, headers=headers, timeout=30.0)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise
    
    def decompose_task(self, goal: str, tech_stack: str = "", constraints: List[str] = None) -> Dict[str, Any]:
        """AI-powered task decomposition"""
        
        system_prompt = """You are an expert software architect and project planner. Your task is to decompose complex software development goals into structured, executable plans.

Output MUST be valid JSON with this structure:
{
    "goal": "original goal",
    "architecture_overview": "high-level description",
    "total_hours": 100,
    "top_modules": [
        {
            "id": "module-1",
            "name": "Module Name",
            "description": "What this module does",
            "estimated_hours": 20,
            "tasks": [
                {
                    "id": "task-1",
                    "title": "Task title",
                    "description": "Detailed description",
                    "priority": "high|medium|low",
                    "estimated_hours": 4,
                    "dependencies": ["other-task-id"],
                    "acceptance_criteria": ["list", "of", "criteria"]
                }
            ]
        }
    ],
    "risks": ["list of potential risks"],
    "success_criteria": ["list of success metrics"]
}"""

        user_prompt = f"""
Project Goal: {goal}
Technology Stack: {tech_stack}
Constraints: {constraints or []}

Please decompose this into a structured development plan. Consider:
1. Modular architecture
2. Task dependencies
3. Risk assessment
4. Realistic time estimates
5. Clear acceptance criteria

Return JSON only, no other text.
"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.chat_completion(messages, temperature=0.2)
        content = response["choices"][0]["message"]["content"]
        
        # Parse JSON from response
        try:
            start = content.find('{')
            end = content.rfind('}') + 1
            json_str = content[start:end]
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            logger.error(f"Raw content: {content}")
            raise ValueError("AI response was not valid JSON")