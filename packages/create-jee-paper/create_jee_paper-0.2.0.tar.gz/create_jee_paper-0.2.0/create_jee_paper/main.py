import typer
import click
import os

from .choice_option import ChoiceOption

CONTEXT_SETTINGS = dict(
		help_option_names = [
			'-h',
			'--help'
		]
)



@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-e', 
			  '--exam', 
			  prompt='Exam', 
			  type=click.Choice(['JEE', 'NEET', 'JEE ADVANCED']), 
			  cls=ChoiceOption, 
			  default=1, 
			  show_default=True)
@click.option('-s', 
			  '--subject', 
			  prompt='Subject', 
			  type=click.Choice(['Physics', 'Maths', 'Chemistry', 'Combined']), 
			  cls=ChoiceOption,
			  default=1,
			  show_default=True)
@click.option('-p',
			  '--path',
			  prompt='Path',
			  type=click.Path(),
			  default='.',
			  show_default=True,
			  help='Path at which project needs to initiated')
def main(exam, subject, path):
	path_dir = os.makedirs(f'{path}/{exam.lower()}')
	path_main = os.path.join(f'{path}/{exam.lower()}', 'main.tex')
	print(path_main)
	path_v_test_paper_sty = os.system(f'cp v-test-paper.sty {path_dir}/v-test-paper.sty')
	with open(path_main, 'w') as file:
		file.write(r'\documentclass{article}')
		file.write(r'\usepackage{v-test-paper}')
		file.write(r'\begin{document}')
		file.write(r'\end{document}')
	
	print('Hello Sir!')









