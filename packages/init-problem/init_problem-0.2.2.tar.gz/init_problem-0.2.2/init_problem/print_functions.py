import os
from rich import print

def print_equation(n, chapter, path):
    print(f'\n\tEquation-{n:02} of {chapter} is initiated at :\n\t{path}\n')




def print_problem(n, chapter, path):
    print(f'\n\tProblem-{n:02} of {chapter} is initiated at :\n\n\t{path}\n')




def print_notes(n, chapter, path):
    print(f'\tNotes-{n:02} of {chapter} is initiated at :\n\t{path}')




def print_ideas(n, chapter, path):
    print(f'\tIdea-{n:02} of {chapter} is initiated at :\n\t{path}')




def bat_file(file_path):
    bat_file_path = f'bat {file_path}'
    os.system(bat_file_path)

