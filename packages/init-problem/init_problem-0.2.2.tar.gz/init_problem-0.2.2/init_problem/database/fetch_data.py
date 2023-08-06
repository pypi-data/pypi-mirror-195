import click
import os
import time
from sqlite3 import Error

from ..tex.path_tex import path_chapter
from ..tex.path_tex import chapters
from .insert_data import insertData
from .get_data import getData
from .database_functions import db_file
from .database_functions import create_connection
from .database_functions import createDatabase
from .get_data import get_n_data


eqn_number_without_database = int(time.strftime("%H%M%S%d%m%Y"))

@click.command(
        help="Creates equation format tex file"
        )
@click.option(
        '-c',
        '--chapter',
        default='rotation',
        help="Chapter name",
        type=click.Choice(
            chapters,
            case_sensitive=False),
        show_default=True
        )
@click.option(
        '-n',
        '--number',
        default=3,
        type=click.INT,
        show_default=True
        )
@click.option(
        '-p',
        '--post_type',
        default='equation',
        type=click.Choice([
            'equation',
            'problem',
            'notes',
            'ideas'
            ]),
        help="Type of post ",
        show_default=True
        )
def fetchdata(chapter, post_type, number):
    try:
        data = get_n_data(chapter, post_type, number)
        if data != None:
            for d in data:
                print(d)
    except Error as e:
        print(e)

