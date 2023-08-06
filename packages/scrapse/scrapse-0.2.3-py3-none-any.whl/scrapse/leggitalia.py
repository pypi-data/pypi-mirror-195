import math

import typer
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn, TimeElapsedColumn
from rich import print
from scrapse import utils
from scrapse.utils import LeggiDiItalia
from concurrent.futures import ThreadPoolExecutor

leggitalia_app = typer.Typer()


def search_judgments(ldi):
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=False,
    ) as progress:
        progress.add_task(description="Searching for judgments...", total=None)
        request = requests.post(url=ldi.baseurl, headers=ldi.headers,
                                params=ldi.search_params)
    judgments_found = request.json()['result']['rows']
    progress.console.print(f'\u2713 Found {judgments_found} judgments')
    return typer.prompt('How many judgments do you want to download?', default=judgments_found, type=int)


def build_pagination(ldi, judgments_to_download):
    pagination = list()
    for index in range(0, math.ceil(judgments_to_download / ldi.batch_size), 1):
        start = index * ldi.batch_size
        rows = ldi.batch_size if (judgments_to_download - (
                (index + 1) * ldi.batch_size)) >= 0 else judgments_to_download - (ldi.batch_size * index)

        pagination.append((start, rows))
    #print(pagination)
    return pagination


def export_judgments_id(ldi, page):
    request = requests.post(url=ldi.baseurl, headers=ldi.headers, params=ldi.pagination_query(page))
    judgments_id = list()
    for item in request.json()['result']['items']:
        judgments_id.append(item['id'])

    formatted_judgments_id = ['|'.join(judgments_id[i:i + ldi.batch_size]) for i in
                              range(0, len(judgments_id), ldi.batch_size)]

    return judgments_id, formatted_judgments_id


def export_judgments(ldi, judgments_id, formatted_judgments_id):
    # print(formatted_judgments_id)
    request = requests.post(url=ldi.baseurl, headers=ldi.headers, params=ldi.build_export_query(formatted_judgments_id))
    # print(request.status_code)
    # print(request.text)
    # print(f'page {page} - ids {formatted_judgments_id}')
    soup = BeautifulSoup(request.text, 'html.parser')
    for index, judgment in enumerate(soup.find_all("div", {"class": "doc_body"})):
        output_file = Path('/'.join((f'{ldi.directory_path}', f'{judgments_id[index]}.{ldi.extension}')))
        output_file.write_text(str(judgment))


@leggitalia_app.command()
def save_cookie(cookie: str):
    file_path = '/'.join([str(Path.cwd().absolute()), 'ldi_cookie.txt'])
    output_file = Path(file_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(str(cookie))


@leggitalia_app.command()
def scrap(
        judicial_bodies: str = typer.Option(None, "--judicial-bodies", "-j", help="Filter judging bodies"),
        location: str = typer.Option(None, "--location", "-l", help="Filter location of the court of reference"),
        sections: str = typer.Option(None, "--sections", "-s", help="Reference section filter, may change by location"),
        path: Path = typer.Option(Path.home(), "--path", "-p", help="Path where to save downloaded judgments"),
        extension: str = typer.Option("HTM", "--extension", "-e", help="Desired extension of judgments"),
):
    """
        Download the judgments from the platform https://pa.leggiditalia.it """'\n'"""
        It is necessary to specify at least one filter among: -j, -l and -s. """'\n'"""
        Provide an input list with the following formatting: -s 'par1, par2, ...'
    """
    ldi = LeggiDiItalia(judicial_bodies=judicial_bodies, location=location, sections=sections,
                        path=path, extension=extension)
    number_of_judgments = search_judgments(ldi)
    pagination = build_pagination(ldi, number_of_judgments)

    with Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
            TimeElapsedColumn(),
            refresh_per_second=5,
    ) as progress:
        futures = []
        overall_progress_task = progress.add_task(description="[green]Extraction of all judgments",
                                                  total=len(pagination))
        # for index, page in enumerate(pagination):
        # export_sentences(ldi, page)
        # progress.update(overall_progress_task, completed=index + 1, total=len(pagination))
        with ThreadPoolExecutor() as executor:
            for index, page in enumerate(pagination):
                judgments_id, formatted_judgments_id = export_judgments_id(ldi, page)
                futures.append(executor.submit(export_judgments, ldi, judgments_id, formatted_judgments_id))
                progress.update(overall_progress_task, completed=(index / 2))
            while (n_finished := sum([future.done() for future in futures])) < len(futures):
                progress.update(overall_progress_task, completed=n_finished + 1)
        # for task_id, update_data in _progress.items():
        #   progress.update(task_id, description=update_data["description"],
        #                  completed=update_data["progress"], total=update_data["total"],
        #                 visible=update_data["progress"] < update_data["total"])
        # raise any errors:
        # for future in futures:
        # future.result()


@leggitalia_app.command()
def show(j: bool = True, s: bool = True, l: bool = True):
    """
        Shows the possible values to be assigned to the respective filters.
    """
    if j:
        print(f'Judicial bodies {utils.JUDICIAL_BODIES}\n')
    if s:
        print(f'Sections {utils.SECTIONS}\n')
    if l:
        print(f'Locations {utils.LOCATIONS}\n')


@leggitalia_app.callback()
def callback():
    """
       Dedicated command to the site LEGGI D'ITALIA PA
    """


if __name__ == "__main__":
    leggitalia_app()
