import click
import os
import time
import sqlite3

from ..tex.path_tex import path_chapter
from ..tex.path_tex import chapters

@click.command(help="Updates the database")
@click.option('-c', '--chapter', type=click.Choice(chapters, case_sensitive=False))
@click.option('-t', '--title')
@click.option('-e', '--equation')
@click.option('-n', '--equation_number')
@click.option('-T', '--tikz')
def updateequation(chapter, title, equation, tikz, equation_number):
    path_database = os.path.join(
            path_chapter(
                chapter.lower(),
                'equation'
                ),
            'equation.db'
            )
    database = sqlite3.connect(path_database)
    print(f'Databse {database} opened.\n')

    cursor = database.cursor()

    data_table= f'UPDATE equation SET  title= "{title}", equation = "{equation}", tikz = "{tikz}" WHERE id={equation_number};'
    cursor.execute(data_table)
    database.commit()
    database.close()


@click.command(help="Updates the database")
@click.option('-c', '--chapter', type=click.Choice(chapters, case_sensitive=False))
@click.option('-p', '--problem')
@click.option('-n', '--problem_number')
@click.option('-T', '--tikz')
def updateproblem(chapter, problem, options, tikz, problem_number):
    path_database = os.path.join(
            path_chapter(
                chapter.lower(),
                'problem'
                ),
            'problem.db'
            )
    database = sqlite3.connect(path_database)
    print(f'Databse {database} opened.\n')

    cursor = database.cursor()

    data_table= f'UPDATE problem SET  problem= "{problem}", options = "{options}", tikz = "{tikz}" WHERE id={problem_number};'
    cursor.execute(data_table)
    database.commit()
    database.close()



@click.command(help="Updates the database")
@click.option('-c', '--chapter', type=click.Choice(chapters, case_sensitive=False))
@click.option('-N', '--note')
@click.option('-n', '--notes_number')
def updatenotes(chapter, note, notes_number):
    path_database = os.path.join(
            path_chapter(
                chapter.lower(),
                'notes'
                ),
            'notes.db'
            )
    database = sqlite3.connect(path_database)
    print(f'Databse {database} opened.\n')

    cursor = database.cursor()
    data_table = f'UPDATE notes SET  note="{note}" WHERE id={notes_number};'
    print(data_table)
    cursor.execute(data_table)
    database.commit()
    database.close()



@click.command(help="Updates the database")
@click.option('-c', '--chapter', type=click.Choice(chapters, case_sensitive=False))
@click.option('-i', '--idea')
@click.option('-n', '--ideas_number')
def updateideas(chapter, idea, ideas_number):
    path_database = os.path.join(
            path_chapter(
                chapter.lower(),
                'ideas'
                ),
            'ideas.db'
            )
    database = sqlite3.connect(path_database)
    print(f'Databse {database} opened.\n')

    cursor = database.cursor()
    data_table= f'UPDATE ideas SET  idea="{idea}" WHERE id={ideas_number};'
    cursor.execute(data_table)
    database.commit()
    database.close()


