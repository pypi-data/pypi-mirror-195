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
			  type=click.Choice(['JEE', 'NEET']), 
			  cls=ChoiceOption, 
			  default=1, 
			  show_default=True)
@click.option('-s', 
			  '--subject', 
			  prompt='Subject', 
			  type=click.Choice(['Physics', 'Maths', 'Chemistry', 'Biology']), 
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
	with open(path_main, 'w') as file:
		file.write(f'\\documentclass{{article}}\n')
		file.write(f'\\usepackage{{v-test-paper}}\n')
		file.write(f'%\\renewcommand{{\\ans}}{{\\quad}}\n')
		file.write(f'%\\def\\ansint#1{{\\quad}}\n')
		file.write(f'\\title{{Test-Paper\\\\({subject}-{exam})}}\n\n')
		file.write(f'\\begin{{document}}\n')
		file.write(f'\\maketitle\n\n')
		file.write(f'\\{exam.lower()}SectionA\n')
		
		file.write(f'\\begin{{enumerate}}\n')
		file.write(f'\\item This is an Objective type question.\n')
		file.write(f'\t\\begin{{tasks}}(2)\n')
		file.write(f'\t\t\\task Option(a) \\ans\n')
		file.write(f'\t\t\\task Option(b)\n')
		file.write(f'\t\t\\task Option(c)\n')
		file.write(f'\t\t\\task Option(d)\n')
		file.write(f'\t\\end{{tasks}}\n')
		file.write(f'\\end{{enumerate}}\n\n')
		
		
		file.write(f'\\{exam.lower()}SectionB\n')
		
		file.write(f'\\begin{{enumerate}}\\addtocounter{{enumi}}{{{20 if exam == "JEE" else 35}}}\n')
		if exam == 'NEET':
			file.write(f'\\item This is section B.\n')
			file.write(f'\t\\begin{{tasks}}(2)\n')
			file.write(f'\t\t\\task Option(a) \\ans\n')
			file.write(f'\t\t\\task Option(b)\n')
			file.write(f'\t\t\\task Option(c)\n')
			file.write(f'\t\t\\task Option(d)\n')
			file.write(f'\t\\end{{tasks}}\n')
		else:
			file.write(f'\\item This is an Integer type question.\\ansint{{7}}\n')
		file.write(f'\\end{{enumerate}}\n\n')

		file.write(f'\\end{{document}}\n')
	
	print(f'\n\tPaper for {subject}({exam}) is initiated.\n')









