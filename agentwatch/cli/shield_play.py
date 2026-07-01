"""
ELUSoC_2026 - Interactive CLI Safety Playground.
Interactive CLI interface for developers to test and verify safety check policies.
"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from agentwatch.core.safety import SafetyEngine
from agentwatch.core.schema import ToolCallData

console = Console()


def start_safety_playground() -> None:
    """Run an interactive console loop for checking command safety rules."""
    engine = SafetyEngine()
    
    console.print(
        Panel(
            "[bold green]Type commands/prompts to test the Safety Engine policies.[/bold green]\n"
            "Type [bold cyan]exit[/bold cyan] to return to the CLI.",
            title="[bold cyan]🛡️ AGENTWATCH SHIELD PLAYGROUND 🛡️[/bold cyan]",
            border_style="green",
        )
    )

    while True:
        try:
            line = input("SafetyCheck > ").strip()
            if not line:
                continue
            if line.lower() in ("exit", "quit"):
                break

            # Build a ToolCallData payload
            tool_call = ToolCallData(
                tool_name="bash",
                raw_command=line,
                arguments={"command": line}
            )

            blocked, reasons = engine.check_tool_call_sync(tool_call)

            if blocked:
                console.print(f"[bold red]❌ BLOCKED[/bold red] - Match reasons: {', '.join(reasons)}")
            else:
                console.print("[bold green]✅ SAFE[/bold green] - No safety policies violated.")
        except (KeyboardInterrupt, EOFError):
            break
