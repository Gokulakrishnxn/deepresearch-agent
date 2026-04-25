"""
DeepSearch CLI — Terminal interface for the Deep Research Agent
Run: python cli.py
"""

import asyncio
import sys
import os
import time

# ── Optional: Rich for beautiful terminal output ───────────────────────────────
try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.rule import Rule
    from rich.text import Text
    from rich.spinner import Spinner
    from rich.live import Live
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

from agent import build_research_agent, create_runner, run_research

BANNER = r"""
  ██████╗ ███████╗███████╗██████╗ ███████╗███████╗ █████╗ ██████╗  ██████╗██╗  ██╗
  ██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║
  ██║  ██║█████╗  █████╗  ██████╔╝███████╗█████╗  ███████║██████╔╝██║     ███████║
  ██║  ██║██╔══╝  ██╔══╝  ██╔═══╝ ╚════██║██╔══╝  ██╔══██║██╔══██╗██║     ██╔══██║
  ██████╔╝███████╗███████╗██║     ███████║███████╗██║  ██║██║  ██║╚██████╗██║  ██║
  ╚═════╝ ╚══════╝╚══════╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
"""

SUBTITLE = "  Powered by Google Gemma 4 × Google ADK — Point-by-point deep research with sources\n"


# ── Print helpers ──────────────────────────────────────────────────────────────

def print_banner():
    if HAS_RICH:
        console = Console()
        console.print(BANNER, style="bold cyan")
        console.print(SUBTITLE, style="dim white")
        console.print(Rule(style="cyan"))
    else:
        print(BANNER)
        print(SUBTITLE)
        print("=" * 80)


def print_help():
    help_text = """
[Commands]
  /help     — Show this help message
  /clear    — Clear the screen
  /new      — Start a new research session (clears history)
  /model    — Show current model
  /exit     — Exit DeepSearch

[Tips]
  • Ask any research question — the agent will give you structured, sourced points
  • Use specific questions for better results
    Example: "What is quantum computing and how does it work?"
    Example: "Latest breakthroughs in cancer treatment 2025"
    Example: "Explain blockchain technology simply"
"""
    if HAS_RICH:
        console = Console()
        console.print(Panel(help_text, title="[bold cyan]DeepSearch Help[/]", border_style="cyan"))
    else:
        print(help_text)


def print_thinking():
    if HAS_RICH:
        console = Console()
        with Live(console=console, refresh_per_second=10) as live:
            for i in range(30):
                frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
                live.update(
                    Text(f"  {frames[i % 10]} Researching... searching the web and synthesizing...", 
                         style="bold yellow")
                )
                time.sleep(0.1)
    else:
        print("\n  🔍 Researching... please wait...\n")


def print_response(response: str, query: str):
    if HAS_RICH:
        console = Console()
        console.print()
        console.print(Rule(f"[bold green]Research Results[/]", style="green"))
        console.print(Markdown(response))
        console.print(Rule(style="green"))
        console.print()
    else:
        print("\n" + "=" * 80)
        print(response)
        print("=" * 80 + "\n")


def get_input() -> str:
    if HAS_RICH:
        console = Console()
        return Prompt.ask("\n[bold cyan]🔬 DeepSearch[/]")
    else:
        return input("\n🔬 DeepSearch > ").strip()


# ── Main CLI Loop ──────────────────────────────────────────────────────────────

async def main():
    # Check for API key
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("\n❌ ERROR: No API key found!")
        print("   Set your Google AI Studio key:")
        print("   export GOOGLE_API_KEY='your-key-here'")
        print("   Get a free key at: https://aistudio.google.com/apikey\n")
        sys.exit(1)

    # Set the key for ADK
    os.environ["GOOGLE_API_KEY"] = api_key
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

    print_banner()
    
    model = os.environ.get("RESEARCH_MODEL", "gemma-3-27b-it")
    
    if HAS_RICH:
        from rich.console import Console
        console = Console()
        console.print(f"  ✅ Model: [bold green]{model}[/]  |  Type [bold cyan]/help[/] for commands\n")
    else:
        print(f"  ✅ Model: {model}  |  Type /help for commands\n")

    # Build agent
    try:
        agent = build_research_agent()
        runner, session_service = create_runner(agent)
    except Exception as e:
        print(f"\n❌ Failed to build agent: {e}")
        sys.exit(1)

    session_counter = [0]

    def new_session_id() -> str:
        session_counter[0] += 1
        return f"session_{session_counter[0]}"

    current_session = new_session_id()

    # ── CLI Loop ──
    while True:
        try:
            user_input = get_input()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  👋 Goodbye! Happy researching.\n")
            break

        if not user_input:
            continue

        # Commands
        if user_input.startswith("/"):
            cmd = user_input.lower().strip()
            if cmd in ("/exit", "/quit", "/q"):
                print("\n  👋 Goodbye! Happy researching.\n")
                break
            elif cmd == "/help":
                print_help()
            elif cmd == "/clear":
                os.system("cls" if os.name == "nt" else "clear")
                print_banner()
            elif cmd == "/new":
                current_session = new_session_id()
                if HAS_RICH:
                    from rich.console import Console
                    Console().print("  ✅ [green]New session started. History cleared.[/]\n")
                else:
                    print("  ✅ New session started.\n")
            elif cmd == "/model":
                if HAS_RICH:
                    from rich.console import Console
                    Console().print(f"  🤖 Current model: [bold green]{model}[/]\n")
                else:
                    print(f"  🤖 Current model: {model}\n")
            else:
                print(f"  ❓ Unknown command: {user_input}. Type /help for help.\n")
            continue

        # Run research
        thinking_task = asyncio.create_task(
            asyncio.to_thread(print_thinking) if not HAS_RICH else asyncio.sleep(0)
        )

        start_time = time.time()

        try:
            if HAS_RICH:
                from rich.console import Console
                from rich.spinner import Spinner
                from rich.live import Live
                from rich.text import Text
                console = Console()

                # Show spinner while researching
                result_holder = {}

                async def do_research():
                    result_holder["response"] = await run_research(
                        runner, session_service, user_input, current_session
                    )

                with console.status(
                    "[bold yellow]🔍 Researching... searching the web and synthesizing...[/]",
                    spinner="dots",
                ):
                    await do_research()
            else:
                print_thinking()
                result_holder = {
                    "response": await run_research(
                        runner, session_service, user_input, current_session
                    )
                }

            elapsed = time.time() - start_time
            response = result_holder.get("response", "No response.")
            print_response(response, user_input)

            if HAS_RICH:
                from rich.console import Console
                Console().print(
                    f"  ⏱  Completed in [dim]{elapsed:.1f}s[/]\n",
                    style="dim"
                )
            else:
                print(f"  ⏱  Completed in {elapsed:.1f}s\n")

        except Exception as e:
            print(f"\n  ❌ Research failed: {e}")
            print("  💡 Check your API key and internet connection.\n")
        finally:
            thinking_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())