import os
import random
from openai_agent import call_openai_with_tools
from rich.console import Console
from rich.panel import Panel
from rich import box
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

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

    instructions = (
        "[bold white]How to use Kaala:[/bold white]\n"
        "- Type your task, plan, or question below.\n"
        "- Press [bold yellow]Enter[/bold yellow] for newline\n"
        "- Press [bold yellow]empty line[/bold yellow] to send\n"
        "- Type [bold red]exit[/bold red] or [bold red]quit[/bold red] anytime to stop.\n"
    )

    text_panel = Panel(
        f"[bold green]{quote}[/bold green]\n\n{instructions}",
        title="Kaala - Disciplined Planner",
        style="bold white",
        box=box.ROUNDED,
        padding=(1, 4)
    )

    console.print("\n" * 2)
    console.print(text_panel, justify="center")

from prompt_toolkit import PromptSession

def get_user_multiline_input():
    console.print("[bold green]🧠 Kaala[/bold green] (Press [bold yellow]Enter[/bold yellow] for newline, [bold yellow]empty line[/bold yellow] to send):")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines).strip()



def main():
    show_logo_and_intro()
    while True:
        try:
            user_input = get_user_multiline_input()

            if user_input.lower() in ["exit", "quit"]:
                console.print("\n[bold cyan]👋 See you later! Kaala signing off.[/bold cyan]")
                break

            if not user_input:
                continue

            console.print("[bold yellow]🤖 Thinking...[/bold yellow]")
            response = call_openai_with_tools(user_input)
            console.print(f"\n[bold magenta]Kaala >[/bold magenta] {response}\n")

        except KeyboardInterrupt:
            console.print("\n[bold red]⚠ Interrupted. Use 'exit' or 'quit' to leave Kaala safely.[/bold red]\n")



if __name__ == "__main__":
    main()

