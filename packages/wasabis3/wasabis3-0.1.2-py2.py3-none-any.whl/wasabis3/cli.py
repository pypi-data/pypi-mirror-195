"""Console script for wasabiii."""
import sys
import click
from wasabi import runner
from formatter import indicators


@click.command()
def main(args=None):
    """Console script for wasabi S3."""
    click.echo(f"{indicators.WARNING}Welcome to the Wasabi S3 CLI Tool{indicators.ENDC}")
    click.echo(f"{indicators.OKCYAN}@author: Mohammed Salim Dason{indicators.ENDC}")
    click.echo(f"{indicators.OKCYAN}@version: 0.1.2{indicators.ENDC}\n\n")


if __name__ == "__main__":
    main()
    sys.exit(runner())
