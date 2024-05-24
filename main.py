import typer
from uuid import uuid4
from rich.progress import Progress, SpinnerColumn, TextColumn
import time
import httpx


app = typer.Typer()


@app.command()
def login(staging: bool = False):
    state = uuid4() # generate auth id (state)
    typer.echo("Continue in your browser to login")
    if staging:
        typer.launch(f"https://staging-api.stowage.dev/auth/login?state={state}")
    else:
        typer.launch(f"https://api.stowage.dev/auth/login?state={state}")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Waiting for login...", total=None)
        max_retries = 25
        
        while max_retries > 0:
            max_retries -= 1
            if max_retries == 0:
                typer.echo("Max retries reached. Please try again.")
                break
            else:
                time.sleep(2.5)
                res = httpx.get("https://api.stowage.dev/auth/status", params={"state": state})
                res_data = res.json()
                if res_data["status"] == "success" and res.status_code == 200:
                    typer.echo("Login successful!")
                    typer.echo("Hello " + res_data["user"]["display_name"] + "!")
                    break
                elif res.status_code != 200:
                    typer.echo("Login failed. Please try again.")



@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()