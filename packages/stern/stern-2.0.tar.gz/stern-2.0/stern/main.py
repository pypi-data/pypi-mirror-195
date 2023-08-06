from rich.console import Console
from rich.table import Table

table = Table(title="STERN")

table.add_column("Name", justify="left", style="cyan")
table.add_column("What is he doing?", justify="left", style="green")
table.add_column("In the file", justify="left", style="cyan")

table.add_row("sumAB", "Computing the difference between creation Python and PyPI", "stern.py")
table.add_row("SealN", "Written five times Hello beautiful world of programming!", "stern.py")
table.add_row("flip", "Flip the line to the other side", "stern.py")
table.add_row("IPS", "Moving x and y", "stern.py")
table.add_row("letters", "Case of Letters", "stern.py")
table.add_row("listletters", "Spelling a word", "stern.py")
table.add_row("unique", "Unique or NOT unique list", "stern.py")
console = Console()
console.print(table)