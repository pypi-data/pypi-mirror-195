import os

path_parent = "/Users/vaibhavblayer/10xphysics/physics"
path_mechanics = "/Users/vaibhavblayer/10xphysics/physics/mechanics"
path_electrodynamics = "/Users/vaibhavblayer/10xphysics/physics/electrodynamics"
path_modern_physics = "/Users/vaibhavblayer/10xphysics/physics/modern-physics"
path_optics = "/Users/vaibhavblayer/10xphysics/physics/optics"


modules = [
        'mechanics',
        'electrodynamics',
        'modern-physics',
        'optics'
        ]


chapters_mechanics = [
        'kinematics',
        'projectile',
        'laws-of-motion',
        'work-energy-power',
        'circular-motion',
        'rotation',
        'center-of-mass',
        'gravitation',
        'simple-harmonic-motion',
        'elasticity',
        'fluid-mechanics',
        ]
chapters_electrodynamics = [
        'electrostatics',
        'current-electricity',
        'capacitors',
        'magnetics',
        'electromagnetic-induction',
        'alternating-current',
        'electromagnetic-waves'
        ]
chapters_optics = [
        'ray-optics',
        'wave-optics',
        ]
chapters_modern_physics = [
        'atomic-structure',
        'photoelectric-effect',
        'x-rays',
        'nuclear-physics',
        'semiconductors',
        'communiation-system'
        ]

post_types = [
        'equation',
        'problem',
        'notes',
        'ideas'
        ]


problem_type = [
        'mine',
        'books',
        'jee',
        'neet',
        'jee_advanced'
        ]



chapters = chapters_mechanics + chapters_electrodynamics + chapters_modern_physics + chapters_optics


def path_post(chapter_folder, post_type):
    if post_type == post_types[0]:
        equation_folder = os.path.join(chapter_folder, post_type)
        os.makedirs(equation_folder, exist_ok=True)
        return equation_folder

    elif post_type == post_types[1]:
        problem_folder = os.path.join(chapter_folder, post_type)
        os.makedirs(problem_folder, exist_ok=True)
        return problem_folder

    elif post_type == post_types[2]:
        notes_folder = os.path.join(chapter_folder, post_type)
        os.makedirs(notes_folder, exist_ok=True)
        return notes_folder
    
    elif post_type == post_types[3]:
        ideas_folder = os.path.join(chapter_folder, post_type)
        os.makedirs(ideas_folder, exist_ok=True)
        return ideas_folder


def path_chapter(chapter, post_type):
    """
    chapter -> name of the chapter
    post_type -> ['equation', 'problem', 'notes', 'db']
    """
    if chapter in chapters_mechanics:
        chapter_folder = os.path.join(path_mechanics, chapter)
        return path_post(chapter_folder, post_type)

    elif chapter in chapters_electrodynamics:
        chapter_folder = os.path.join(path_electrodynamics, chapter)
        return path_post(chapter_folder, post_type)

    elif chapter in chapters_modern_physics:
        chapter_folder = os.path.join(path_modern_physics, chapter)
        return path_post(chapter_folder, post_type)

    elif chapter in chapters_optics:
        chapter_folder = os.path.join(path_optics, chapter)
        return path_post(chapter_folder, post_type)





