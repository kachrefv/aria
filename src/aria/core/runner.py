import time
from typing import Dict, Any, List
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Confirm, IntPrompt

from .generator import CodeGenerator
from ..utils.logger import setup_logger

logger = setup_logger()

class PlanRunner:
    """Execute project plans step-by-step"""
    
    def __init__(self, plan: Dict[str, Any]):
        self.plan = plan
        self.generator = CodeGenerator()
        self.console = Console()
    
    def run_interactive(self):
        """Run plan in interactive mode"""
        
        self.console.print(Panel.fit(
            f"[bold green]Starting Interactive Execution[/bold green]\n"
            f"Goal: {self.plan['goal']}\n"
            f"Total Modules: {len(self.plan.get('top_modules', []))}",
            border_style="green"
        ))
        
        # Show plan summary
        total_tasks = sum(len(m.get('tasks', [])) for m in self.plan.get('top_modules', []))
        completed_tasks = 0
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            transient=True,
        ) as progress:
            
            main_task = progress.add_task("Executing project plan...", total=total_tasks)
            
            # Execute each module
            for module in self.plan.get('top_modules', []):
                if not self._execute_module_interactive(module, progress, main_task):
                    self.console.print(f"[yellow]Execution paused at module: {module['name']}[/yellow]")
                    break
        
        self.console.print("[bold green]✅ Project execution completed![/bold green]")
    
    def run_automated(self):
        """Run plan in automated mode"""
        
        self.console.print(Panel.fit(
            f"[bold blue]Starting Automated Execution[/bold blue]\n"
            f"Goal: {self.plan['goal']}",
            border_style="blue"
        ))
        
        results = self.generator.generate_project(self.plan, Path("./generated-project"))
        
        if results["success"]:
            self.console.print(f"[green]✅ Project generated successfully![/green]")
            self.console.print(f"[blue]Generated {len(results['generated_files'])} files[/blue]")
        else:
            self.console.print(f"[red]❌ Project generation failed[/red]")
            for error in results["errors"]:
                self.console.print(f"[red]  - {error}[/red]")
    
    def _execute_module_interactive(self, module: Dict[str, Any], progress, main_task) -> bool:
        """Execute a single module interactively"""
        
        self.console.print(f"\n[bold cyan]Module: {module['name']}[/bold cyan]")
        self.console.print(f"{module.get('description', '')}")
        
        for task in module.get('tasks', []):
            task_description = f"{task['title']} ({task.get('estimated_hours', 0)}h)"
            
            # Check dependencies
            dependencies_met = self._check_dependencies(task)
            if not dependencies_met:
                self.console.print(f"[yellow]⚠️  Skipping {task['title']} - dependencies not met[/yellow]")
                continue
            
            # Ask for confirmation
            if not Confirm.ask(f"Execute: {task_description}?"):
                if not Confirm.ask("Skip this task and continue?"):
                    return False  # Stop execution
                continue
            
            # Execute task
            progress.update(main_task, advance=1, description=f"Executing: {task['title']}")
            
            # Simulate task execution (would be replaced with actual code generation)
            time.sleep(1)  # Simulate work
            
            # Mark task as completed
            task['status'] = 'completed'
            self.console.print(f"[green]✅ Completed: {task['title']}[/green]")
        
        return True
    
    def _check_dependencies(self, task: Dict[str, Any]) -> bool:
        """Check if task dependencies are met"""
        
        dependencies = task.get('dependencies', [])
        if not dependencies:
            return True
        
        # This would check actual task completion status
        # For now, we'll assume all dependencies are met
        return True