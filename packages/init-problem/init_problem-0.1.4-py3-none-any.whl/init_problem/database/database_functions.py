
import os
from sqlite3 import Error
import sqlite3
from ..tex.path_tex import path_chapter

def db_file(chapter, post_type):
    chapter_path = path_chapter(chapter.lower(), post_type)
    path_database = os.path.join(chapter_path, f'{post_type}.db')
    return path_database


def create_connection(db_file):
    """ create a database connection to the SQLite database
        :param db_file: database file
        :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn



def createDatabase(chapter, post_type):
    database = create_connection(db_file(chapter, post_type))

    #cursor = database.cursor()
    if post_type == 'equation':
        database.execute(
            """ CREATE TABLE IF NOT EXISTS equation(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chapter TEXT NOT NULL,
                date TEXT,
                title TEXT,
                equation TEXT,
                tikz TEXT
            ); """
            )
    elif post_type == 'problem':
        database.execute(
            """ CREATE TABLE IF NOT EXISTS problem(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chapter TEXT NOT NULL,
                date TEXT,
                problem TEXT,
                options TEXT,
                tikz TEXT
            ); """
            )
    elif post_type == 'notes':
        database.execute(
            """ CREATE TABLE IF NOT EXISTS notes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chapter TEXT NOT NULL,
                date TEXT,
                note TEXT
            ); """
            )
    elif post_type == 'ideas':
        database.execute(
            """ CREATE TABLE ideas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chapter TEXT NOT NULL,
                date TEXT,
                idea TEXT
            ); """
            )


    database.close()


