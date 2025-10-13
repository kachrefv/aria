import json
import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from .config import config
from .core.decomposer import TaskDecomposer
from .core.plans_manager import PlansManager
from .tui.dashboard import run_tui
from .utils.logger import setup_logger

app = typer.Typer(
    name="aria",
    help="🌀 Achref Riahi AI Assistant - Open-source AI coding architect",
    rich_markup_mode="rich"
)
console = Console()
logger = setup_logger()

@app.command()
def version():
    """Display aria version"""
    from . import __version__
    console.print(f"🌀 [bold cyan]aria[/bold cyan] version [bold green]{__version__}[/bold green]")

@app.command()
def decompose(
    goal: str = typer.Argument(..., help="Project goal to decompose"),
    output: Path = typer.Option(None, help="Output plan file path"),
    tech_stack: str = typer.Option("", help="Technology stack (e.g., 'Next.js, TypeScript, Tailwind')"),
    constraints: str = typer.Option("", help="Project constraints separated by commas"),
):
    """
    Decompose a project goal into structured development plan
    
    Example:
    [bold]aria decompose[/bold] "Build an AI-powered ecommerce platform with Next.js and Stripe"
    """
    try:
        config.validate()
        
        console.print(Panel.fit(
            f"[bold cyan]Goal:[/bold cyan] {goal}\n"
            f"[bold cyan]Tech Stack:[/bold cyan] {tech_stack or 'Not specified'}\n"
            f"[bold cyan]Constraints:[/bold cyan] {constraints or 'None'}",
            title="🧠 Aria Task Decomposition",
            border_style="cyan"
        ))
        
        # Parse constraints
        constraint_list = [c.strip() for c in constraints.split(",")] if constraints else []
        
        # Initialize decomposer
        decomposer = TaskDecomposer(goal, tech_stack, constraint_list)
        
        with console.status("[bold green]AI is analyzing your project...", spinner="dots"):
            plan = decomposer.run()
        
        # Save plan
        plans_manager = PlansManager()
        saved_path = plans_manager.save_plan(plan, output)
        
        console.print(f"\n✅ [bold green]Project plan generated successfully![/bold green]")
        console.print(f"📁 [bold blue]Saved to:[/bold blue] {saved_path}")
        
        # Show summary
        modules = plan.get("top_modules", [])
        total_tasks = sum(len(module.get("tasks", [])) for module in modules)
        
        console.print(f"\n📊 [bold]Plan Summary:[/bold]")
        console.print(f"   • Modules: [cyan]{len(modules)}[/cyan]")
        console.print(f"   • Total Tasks: [cyan]{total_tasks}[/cyan]")
        console.print(f"   • Estimated Hours: [cyan]{plan.get('total_hours', 'N/A')}[/cyan]")
        
        # Ask if user wants to view in TUI
        console.print(f"\n🎨 [bold]Open in TUI dashboard?[/bold]")
        if typer.confirm("Launch interactive view"):
            run_tui(plan)
            
    except Exception as e:
        console.print(f"❌ [bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)

@app.command()
def view(
    plan_file: Path = typer.Argument(..., help="Plan file to view"),
):
    """
    View project plan in interactive TUI dashboard
    """
    if not plan_file.exists():
        console.print(f"❌ [bold red]Plan file not found: {plan_file}[/bold red]")
        raise typer.Exit(1)
    
    try:
        plans_manager = PlansManager()
        plan = plans_manager.load_plan(plan_file)
        run_tui(plan)
    except Exception as e:
        console.print(f"❌ [bold red]Error loading plan: {e}[/bold red]")
        raise typer.Exit(1)

@app.command()
def analyze(
    path: Path = typer.Argument(..., help="Project path to analyze"),
    output: Path = typer.Option(None, help="Output analysis file"),
):
    """
    Analyze existing project structure and generate insights
    """
    from .plugins.base import PluginManager
    
    try:
        console.print(f"🔍 [bold cyan]Analyzing project: {path}[/bold cyan]")
        
        plugin_manager = PluginManager()
        analysis = plugin_manager.analyze_project(path)
        
        if output:
            with open(output, 'w') as f:
                json.dump(analysis, f, indent=2)
            console.print(f"✅ [bold green]Analysis saved to: {output}[/bold green]")
        
        # Display summary
        console.print(f"\n📊 [bold]Project Analysis Summary:[/bold]")
        console.print(f"   • Framework: [cyan]{analysis.get('framework', 'Unknown')}[/cyan]")
        console.print(f"   • Files Analyzed: [cyan]{analysis.get('files_analyzed', 0)}[/cyan]")
        console.print(f"   • Issues Found: [cyan]{len(analysis.get('issues', []))}[/cyan]")
        console.print(f"   • Recommendations: [cyan]{len(analysis.get('recommendations', []))}[/cyan]")
        
    except Exception as e:
        console.print(f"❌ [bold red]Analysis failed: {e}[/bold red]")
        raise typer.Exit(1)

@app.command()
def new(
    template: str = typer.Argument(..., help="Project template (nextjs, flask, etc.)"),
    name: str = typer.Argument(..., help="Project name"),
    path: Path = typer.Option(Path("."), help="Where to create project"),
):
    """
    Scaffold new project from template
    """
    from .plugins.base import PluginManager
    
    try:
        console.print(f"🏗️  [bold cyan]Creating new {template} project: {name}[/bold cyan]")
        
        plugin_manager = PluginManager()
        result = plugin_manager.scaffold_project(template, name, path)
        
        if result.get("success"):
            console.print(f"✅ [bold green]Project created successfully![/bold green]")
            console.print(f"📁 [blue]Location: {result['path']}[/blue]")
            
            if result.get("next_steps"):
                console.print(f"\n🎯 [bold]Next Steps:[/bold]")
                for step in result["next_steps"]:
                    console.print(f"   • {step}")
        else:
            console.print(f"❌ [bold red]Project creation failed: {result.get('error')}[/bold red]")
            
    except Exception as e:
        console.print(f"❌ [bold red]Scaffolding failed: {e}[/bold red]")
        raise typer.Exit(1)

@app.command()
def run(
    plan_file: Path = typer.Argument(..., help="Plan file to execute"),
    interactive: bool = typer.Option(True, help="Run in interactive mode"),
):
    """
    Execute project plan step-by-step
    """
    if not plan_file.exists():
        console.print(f"❌ [bold red]Plan file not found: {plan_file}[/bold red]")
        raise typer.Exit(1)
    
    try:
        from .core.runner import PlanRunner
        
        plans_manager = PlansManager()
        plan = plans_manager.load_plan(plan_file)
        
        console.print(Panel.fit(
            f"[bold cyan]Executing Plan:[/bold cyan] {plan.get('goal', 'Unknown')}\n"
            f"[bold cyan]Tasks:[/bold cyan] {sum(len(m.get('tasks', [])) for m in plan.get('top_modules', []))}",
            title="🚀 Aria Plan Execution",
            border_style="green"
        ))
        
        runner = PlanRunner(plan)
        
        if interactive:
            runner.run_interactive()
        else:
            runner.run_automated()
            
    except Exception as e:
        console.print(f"❌ [bold red]Execution failed: {e}[/bold red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()