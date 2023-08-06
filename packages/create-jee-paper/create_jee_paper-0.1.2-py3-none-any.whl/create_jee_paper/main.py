import typer
import click

from .choice_option import ChoiceOption

CONTEXT_SETTINGS = dict(
		help_option_names = [
			'-h',
			'--help'
		]
)


@click.group(context_settings=CONTEXT_SETTINGS)
def main():
	pass


@click.command()
@click.option('-e', '--exam', prompt='Exam', type=click.Choice(['JEE', 'NEET']), cls=ChoiceOption)
def create_jee_paper(exam):
	print('Hello Sir!')







main.add_command(create_jee_paper)


