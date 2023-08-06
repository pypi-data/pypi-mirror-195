import click
import os
import time
import sqlite3
from sqlite3 import Error

from ..tex.path_tex import path_chapter
from ..tex.path_tex import path_mechanics
from ..tex.path_tex import path_electrodynamics
from .database_functions import db_file
from .database_functions import create_connection
from .database_functions import createDatabase

def getData(chapter, post_type):

    try:

        database = create_connection(db_file(chapter, post_type))
        cursor = database.cursor()

        if post_type == 'equation':
	        output = cursor.execute("""SELECT * FROM equation ORDER BY id DESC LIMIT 1;""")
	        return output.fetchmany(1)
	
        elif post_type == 'problem':
	        output = cursor.execute("""SELECT * FROM problem ORDER BY id DESC LIMIT 1;""")
	        return output.fetchmany(1)

        elif post_type == 'notes':
	        output = cursor.execute("""SELECT * FROM notes ORDER BY id DESC LIMIT 1;""")
	        return output.fetchmany(1)
	
        elif post_type == 'ideas':
	        output = cursor.execute("""SELECT * FROM ideas ORDER BY id DESC LIMIT 1;""")
	        return output.fetchmany(1)



        database.close()

    except:

        createDatabase(chapter, post_type)



def get_n_data(chapter, post_type, n):
    try:

        database = create_connection(db_file(chapter, post_type))
        cursor = database.cursor()

        if post_type == 'equation':
            execute_statement = f'SELECT * FROM equation ORDER BY id DESC LIMIT {n};'
            output = cursor.execute(execute_statement)
            return output.fetchmany(n)

        elif post_type == 'problem':
            execute_statement = f'SELECT * FROM problem ORDER BY id DESC LIMIT {n};'
            output = cursor.execute(execute_statement)
            return output.fetchmany(n)

        elif post_type == 'notes':
            execute_statement = f'SELECT * FROM notes ORDER BY id DESC LIMIT {n};'
            output = cursor.execute(execute_statement)
            return output.fetchmany(n)

        elif post_type == 'ideas':
            execute_statement = f'SELECT * FROM ideas ORDER BY id DESC LIMIT {n};'
            output = cursor.execute(execute_statement)
            return output.fetchmany(n)



        database.close()

    except Error as e:
        print(e)









