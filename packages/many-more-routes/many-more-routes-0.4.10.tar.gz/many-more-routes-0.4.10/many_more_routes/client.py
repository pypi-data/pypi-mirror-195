import typer

from typing import Optional
from typing import List

from pathlib import Path

from . construct import MakeRoute
from . construct import MakeDeparture
from . construct import MakeSelection
from . construct import MakeCustomerExtension
from . construct import MakeCustomerExtensionExtended

from . ducks import OutputRecord
from . models import ValidatedTemplate

from . io import load_excel
from . io import save_excel
from . io import save_template

from . sequence import generator

app = typer.Typer()


@app.command()
def template(file_path: Path):
    save_template(ValidatedTemplate, file_path) #type: ignore

@app.command()
def generate(in_file: Path, out_file: Path, seed: Optional[str] = None):
    records = map(lambda x: ValidatedTemplate.construct(**x), load_excel(in_file))

    if seed:
        routegen = generator(seed)
        for row in records:
            if not row.ROUT:
                row.ROUT = next(routegen)

    results: List[OutputRecord] = []
    for record in records:
        results.append(record)
        results.extend(MakeRoute(record))
        results.extend(MakeDeparture(record))
        results.extend(MakeSelection(record))
        results.extend(MakeCustomerExtension(record))
        results.extend(MakeCustomerExtensionExtended(record))

    save_excel(results, out_file)


if __name__ == '__main__':
    app()
