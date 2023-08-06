import datetime
from typing import Optional

import typer
from rich import print

# from rich.progress import track
# from .video_duration import get_length, get_file_list

app = typer.Typer()


@app.callback()
def callback():
    """Здесь наверное должно быть какое-то краткое описание программы"""


@app.command()
def print_something():
    """Напечатает заранее захардкоженый текст"""
    print("[bold red]Alert![/bold red] [green]Portal gun[/green] shooting! :boom:")


# @app.command()
# def say_hello(name: str, city: Optional[str] = None):
#     """Типа говорит привет и приглашает попить кофе"""
#     print(f"Hello {name}")
#     if city:
#         print(f"Let's have a coffee in {city}")
#
#
# @app.command()
# def vd():
#     """Показывает суммарную длительность видео в текущей папке и её подпапках"""
#     file_length_list = [get_length(i) for i in track(get_file_list())]
#     total_video_duration = sum(file_length_list)
#     print(str(datetime.timedelta(seconds=int(total_video_duration))))


if __name__ == "__main__":
    app()