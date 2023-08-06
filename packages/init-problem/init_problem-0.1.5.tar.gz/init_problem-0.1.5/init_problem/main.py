import click
import os
import time

from .tex.path_tex import path_chapter
from .tex.path_tex import chapters
from .database.insert_data import insertData
from .database.get_data import getData
from .print_functions import print_problem
from .print_functions import bat_file
from .tex.problem_tex import problem_preamble
from .tex.problem_tex import problem_head
from .choice_option import ChoiceOption


eqn_number_without_database = int(time.strftime("%H%M%S%d%m%Y"))



size_square = f'\\geometry{{\npaperwidth=5in, \npaperheight=5in, \ntop=15mm, \nbottom=15mm, \nleft=10mm, \nright=10mm}}\n\n'
size_h_rectangle = f'\\geometry{{\npaperwidth=8in, \npaperheight=4.5in, \ntop=15mm, \nbottom=15mm, \nleft=10mm, \nright=10mm}}\n\n'
size_v_rectangle = f'\\geometry{{\npaperwidth=4.5in, \npaperheight=8in, \ntop=15mm, \nbottom=15mm, \nleft=10mm, \nright=10mm}}\n\n'

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(
        context_settings = CONTEXT_SETTINGS,
        help="Creates problem format tex file"
        )
@click.option(
        '-c',
        '--chapter',
        prompt='Chapters',
        type=click.Choice(
            chapters,
            case_sensitive=False),
        cls=ChoiceOption,
        help="Chapter name",
        )
@click.option(
        '-s',
        '--size',
        prompt='Size',
        default='square',
        type=click.Choice(['square', 'h-rectangle', 'v-rectangle']),
        cls=ChoiceOption,
        show_default=True,
        help="Size of the canvas"
        )
@click.option(
        '-n',
        '--problem_number',
        type=click.INT
        )
@click.option(
        '-a',
        '--append_to_database',
        default=True,
        prompt="Append to database!",
        type=click.Choice([True, False]),
        cls=ChoiceOption,
        help="flag (-a turns-on) appends the equation to database"
        )
def main(chapter, size, problem_number, append_to_database):
    if append_to_database:
        try:
            problem_number = getData(chapter, 'problem')[0][0] + 1
        except:
            problem_number = 1
        insertData(chapter, 'problem')
    else:
        problem_number = eqn_number_without_database

    path_equation = os.path.join(
            path_chapter(chapter.lower(), 'problem'),
            f'problem-{problem_number:02}'
            )
    
   

    os.makedirs(path_equation, exist_ok=True)
    main_tex = os.path.join(path_equation, 'main.tex')
    with open(main_tex, 'w') as file:
        file.write(f'\\documentclass{{article}}\n')
        file.write(f'\\usepackage{{v-problem}}\n')
        if size == 'square':
            file.write(size_square)
        elif size == 'h-rectangle':
            file.write(size_h_rectangle)
        elif size == 'v-rectangle':
            file.write(size_v_rectangle)

        file.write(f'\\begin{{document}}\n')
        file.write(f'{problem_number}')
        file.write(f'\\end{{document}}\n')

    print_problem(problem_number, chapter, main_tex)
    bat_file(main_tex)
    time.sleep(1)
    os.system(f'open -a texmaker {main_tex}')
    print('\n\topening texmaker ...\n')
    time.sleep(1)



