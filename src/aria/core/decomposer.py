import uuid
from typing import Dict, List, Any
from .ai_engine import AIEngine
from .plans_manager import PlansManager
from ..utils.logger import setup_logger

logger = setup_logger()

class TaskDecomposer:
    """Main task decomposition engine"""
    
    def __init__(self, goal: str, tech_stack: str = "", constraints: List[str] = None):
        self.goal = goal
        self.tech_stack = tech_stack
        self.constraints = constraints or []
        self.ai_engine = AIEngine()
        self.plans_manager = PlansManager()
        
    def run(self) -> Dict[str, Any]:
        """Run full decomposition pipeline"""
        
        logger.info(f"Starting decomposition for goal: {self.goal}")
        
        # 1. AI-powered decomposition
        ai_plan = self.ai_engine.decompose_task(
            self.goal, self.tech_stack, self.constraints
        )
        
        # 2. Enhance with additional metadata
        enhanced_plan = self._enhance_plan(ai_plan)
        
        # 3. Validate plan structure
        self._validate_plan(enhanced_plan)
        
        logger.info(f"Decomposition completed. Modules: {len(enhanced_plan.get('top_modules', []))}")
        
        return enhanced_plan
    
    def _enhance_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Add additional metadata and structure to AI plan"""
        
        enhanced = plan.copy()
        
        # Add metadata
        enhanced["decomposer_version"] = "1.0"
        enhanced["tech_stack"] = self.tech_stack
        enhanced["constraints"] = self.constraints
        
        # Ensure all tasks have IDs and proper structure
        total_hours = 0
        for module in enhanced.get("top_modules", []):
            module.setdefault("id", f"module-{uuid.uuid4().hex[:8]}")
            
            for task in module.get("tasks", []):
                task.setdefault("id", f"task-{uuid.uuid4().hex[:8]}")
                task.setdefault("status", "pending")
                task.setdefault("dependencies", [])
                task.setdefault("priority", "medium")
                
                # Calculate total hours
                total_hours += task.get("estimated_hours", 0)
        
        enhanced["total_hours"] = total_hours
        
        return enhanced
    
    def _validate_plan(self, plan: Dict[str, Any]):
        """Validate plan structure"""
        
        required_keys = ["goal", "top_modules"]
        for key in required_keys:
            if key not in plan:
                raise ValueError(f"Plan missing required key: {key}")
        
        if not isinstance(plan["top_modules"], list):
            raise ValueError("top_modules must be a list")
        
        # Validate task dependencies exist
        all_task_ids = []
        for module in plan["top_modules"]:
            for task in module.get("tasks", []):
                all_task_ids.append(task["id"])
        
        for module in plan["top_modules"]:
            for task in module.get("tasks", []):
                for dep_id in task.get("dependencies", []):
                    if dep_id not in all_task_ids:
                        logger.warning(f"Task {task['id']} has invalid dependency: {dep_id}")