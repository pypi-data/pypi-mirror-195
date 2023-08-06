import typer
import click

from .choice_option import ChoiceOption

CONTEXT_SETTINGS = dict(
		help_option_names = [
			'-h',
			'--help'
		]
)



@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-e', '--exam', prompt='Exam', type=click.Choice(['JEE', 'NEET']), cls=ChoiceOption)
def main(exam):
	print('Hello Sir!')









