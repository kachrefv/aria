from typing import Dict, Any, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich import box

console = Console()

def format_plan_summary(plan: Dict[str, Any]) -> str:
    """Format plan as readable summary"""
    
    summary = f"# {plan['goal']}\n\n"
    
    if plan.get('architecture_overview'):
        summary += f"## Architecture Overview\n\n{plan['architecture_overview']}\n\n"
    
    summary += "## Modules\n\n"
    
    for module in plan.get('top_modules', []):
        summary += f"### {module['name']}\n\n"
        summary += f"**Description**: {module.get('description', 'No description')}\n\n"
        
        for task in module.get('tasks', []):
            summary += f"- **{task['title']}** "
            summary += f"({task.get('estimated_hours', 0)} hours, {task.get('priority', 'medium')} priority)\n"
            
            if task.get('dependencies'):
                summary += f"  - Dependencies: {', '.join(task['dependencies'])}\n"
            
            if task.get('acceptance_criteria'):
                summary += f"  - Acceptance Criteria:\n"
                for criteria in task['acceptance_criteria']:
                    summary += f"    - {criteria}\n"
        
        summary += "\n"
    
    return summary

def display_plan_table(plan: Dict[str, Any]):
    """Display plan as rich table"""
    
    table = Table(
        title=f"Project Plan: {plan['goal']}",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta"
    )
    
    table.add_column("Module", style="cyan")
    table.add_column("Task", style="white")
    table.add_column("Hours", justify="right", style="green")
    table.add_column("Priority", style="yellow")
    table.add_column("Dependencies", style="blue")
    
    for module in plan.get('top_modules', []):
        module_name = module['name']
        first_task = True
        
        for task in module.get('tasks', []):
            task_name = task['title']
            hours = str(task.get('estimated_hours', 0))
            priority = task.get('priority', 'medium')
            deps = ', '.join(task.get('dependencies', []))
            
            if first_task:
                table.add_row(module_name, task_name, hours, priority, deps)
                first_task = False
            else:
                table.add_row("", task_name, hours, priority, deps)
    
    console.print(table)

def create_project_tree(plan: Dict[str, Any]) -> Tree:
    """Create a rich tree visualization of the project"""
    
    tree = Tree(f"[bold cyan]🎯 {plan['goal']}[/bold cyan]")
    
    for module in plan.get('top_modules', []):
        module_branch = tree.add(f"[bold green]📦 {module['name']}[/bold green]")
        
        for task in module.get('tasks', []):
            status_icon = "✅" if task.get('status') == 'completed' else "◯"
            priority_color = {
                'high': 'red',
                'medium': 'yellow', 
                'low': 'green'
            }.get(task.get('priority', 'medium'), 'white')
            
            task_text = (
                f"{status_icon} [{priority_color}]{task['title']}[/{priority_color}] "
                f"({task.get('estimated_hours', 0)}h)"
            )
            
            task_branch = module_branch.add(task_text)
            
            # Add task details as children
            if task.get('description'):
                task_branch.add(f"📝 {task['description']}")
            
            if task.get('acceptance_criteria'):
                criteria_branch = task_branch.add("🎯 Acceptance Criteria")
                for criteria in task['acceptance_criteria']:
                    criteria_branch.add(f"  • {criteria}")
    
    return tree

def display_risk_analysis(risk_analysis: Dict[str, Any]):
    """Display risk analysis in a formatted way"""
    
    if not risk_analysis:
        console.print("[yellow]No risk analysis available[/yellow]")
        return
    
    console.print(Panel.fit(
        "[bold red]Risk Analysis[/bold red]",
        border_style="red"
    ))
    
    # Technical risks
    if risk_analysis.get('technical_risks'):
        console.print("[bold]Technical Risks:[/bold]")
        for risk in risk_analysis['technical_risks']:
            console.print(f"  • [red]{risk}[/red]")
    
    # Project risks
    if risk_analysis.get('project_risks'):
        console.print("\n[bold]Project Risks:[/bold]")
        for risk in risk_analysis['project_risks']:
            console.print(f"  • [yellow]{risk}[/yellow]")
    
    # Mitigation strategies
    if risk_analysis.get('mitigation_strategies'):
        console.print("\n[bold]Mitigation Strategies:[/bold]")
        for strategy in risk_analysis['mitigation_strategies']:
            console.print(f"  • [green]{strategy}[/green]")
    
    # Overall risk level
    risk_level = risk_analysis.get('overall_risk_level', 'unknown')
    risk_color = {
        'low': 'green',
        'medium': 'yellow',
        'high': 'red'
    }.get(risk_level.lower(), 'white')
    
    console.print(f"\n[bold]Overall Risk Level:[/bold] [{risk_color}]{risk_level.upper()}[/{risk_color}]")

def display_module_details(module: Dict[str, Any]):
    """Display detailed information about a module"""
    
    console.print(Panel.fit(
        f"[bold cyan]{module['name']}[/bold cyan]",
        subtitle=f"Estimated: {module.get('estimated_hours', 0)} hours",
        border_style="cyan"
    ))
    
    console.print(f"[bold]Description:[/bold] {module.get('description', 'No description')}")
    
    if module.get('tasks'):
        console.print(f"\n[bold]Tasks:[/bold]")
        for task in module['tasks']:
            status_icon = "✅" if task.get('status') == 'completed' else "⏳"
            console.print(f"  {status_icon} [bold]{task['title']}[/bold]")
            console.print(f"    Hours: {task.get('estimated_hours', 0)} | Priority: {task.get('priority', 'medium')}")
            
            if task.get('dependencies'):
                console.print(f"    Dependencies: {', '.join(task['dependencies'])}")
            
            if task.get('description'):
                console.print(f"    Description: {task['description']}")