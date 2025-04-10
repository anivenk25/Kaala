import os
from openai_agent import call_openai_with_tools
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

def show_logo():
    image_path = "/home/anirudh/Kaala/assets/Kaala_mascot_d.png"    
    if os.path.exists(image_path):
        os.system(f"viu -w 10 {image_path}")  # adjust width as needed
    else:
        console.print("[bold red]Kaala logo not found.[/bold red]")

def show_intro():
    os.system('clear' if os.name == 'posix' else 'cls')
    #show_logo()
    console.print(Panel("Type your question below. Type [bold red]exit[/bold red] or [bold red]quit[/bold red] to stop.\n", style="bold white"))

def main():
    show_intro()
    while True:
        try:
            user_input = Prompt.ask("[bold green]🧠 Kaala[/bold green]")
            if user_input.strip().lower() in ["exit", "quit"]:
                console.print("\n[bold cyan]👋 See you later! Kaala signing off.[/bold cyan]")
                break
            console.print("[bold yellow]🤖 Thinking...[/bold yellow]")
            response = call_openai_with_tools(user_input)
            console.print(f"[bold magenta]Kaala >[/bold magenta] {response}\n")
        except KeyboardInterrupt:
            console.print("\n[bold red]⚠ Interrupted. Use 'exit' or 'quit' to leave Kaala safely.[/bold red]\n")

if __name__ == "__main__":
    main()

