import os
import random
from openai_agent import call_openai_with_tools
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich import box

console = Console()

QUOTES = [
    "Discipline is the bridge between goals and accomplishment. — Jim Rohn",
    "Focus on being productive instead of busy. — Tim Ferriss",
    "You don’t need more time, you just need to decide. — Seth Godin",
    "Small disciplines repeated with consistency lead to great achievements. — John Maxwell",
    "Productivity is never an accident. It is always the result of a commitment to excellence. — Paul J. Meyer",
    "Plan your work and work your plan. — Napoleon Hill",
    "The secret of getting ahead is getting started. — Mark Twain"
]

def show_logo_and_intro():
    os.system('clear' if os.name == 'posix' else 'cls')
    quote = random.choice(QUOTES)
    '''image_path = "/home/anirudh/Kaala/assets/Kaala_mascot_d.png"

    if os.path.exists(image_path):
        os.system(f"viu -w 20 {image_path}")
    else:
        console.print("[bold red]⚠ Kaala logo not found at expected path.[/bold red]\n")'''

    # Simulate side-by-side by printing text right after image render
    text_panel = Panel(
        f"[bold green]{quote}[/bold green]\n\n"
        f"[bold white]Type your task or question below.[/bold white]\n"
        f"Type [bold red]exit[/bold red] or [bold red]quit[/bold red] to stop.",
        title="Kaala - Disciplined Planner",
        style="bold white",
        box=box.ROUNDED,
        padding=(1, 4)
    )
    console.print(text_panel, justify="left")


def main():
    show_logo_and_intro()
    while True:
        try:
            user_input = Prompt.ask("[bold green]🧠 Kaala[/bold green]")
            if user_input.strip().lower() in ["exit", "quit"]:
                console.print("\n[bold cyan]👋 See you later! Kaala signing off.[/bold cyan]")
                break
            console.print("[bold yellow]🤖 Thinking...[/bold yellow]")
            response = call_openai_with_tools(user_input)
            console.print(f"\n[bold magenta]Kaala >[/bold magenta] {response}\n")
        except KeyboardInterrupt:
            console.print("\n[bold red]⚠ Interrupted. Use 'exit' or 'quit' to leave Kaala safely.[/bold red]\n")

if __name__ == "__main__":
    main()

