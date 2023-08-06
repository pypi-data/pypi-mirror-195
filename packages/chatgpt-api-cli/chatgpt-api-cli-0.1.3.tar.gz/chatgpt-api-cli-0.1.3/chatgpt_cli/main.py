import typer
from pathlib import Path
from chatgpt_cli.services.chatgpt import query_chatgpt
from chatgpt_cli.services.chatgpt import ChatGPTResponse


app = typer.Typer()


@app.command()
def init(
    config_path: Path = typer.Option(
        Path.home() / ".chatgpt-cli/.env",
        help="The destination directory for the .env file",
    ),
    open_api_key: str = typer.Argument(..., help="Your OpenAI API key"),
):
    """Generate the .env file."""
    print(f"Config file: {config_path}")
    if not config_path.is_file():
        print("Config file doesn't exist yet, creating it...")
    else:
        print("Config file already exists")

    config_path.parent.mkdir(parents=True, exist_ok=True)
    with config_path.open("w", encoding="utf-8") as f:
        f.write(f"OPENAI_API_KEY={open_api_key}")

    print("Done!")


@app.command()
def prompt(prompt: str = typer.Argument(..., help="Prompt for ChatGPT")):
    """Query ChatGPT with a prompt."""
    response: ChatGPTResponse = query_chatgpt(prompt=prompt)
    print(response.choices[0].message.content)


def main():
    app()


if __name__ == "__main__":
    main()
