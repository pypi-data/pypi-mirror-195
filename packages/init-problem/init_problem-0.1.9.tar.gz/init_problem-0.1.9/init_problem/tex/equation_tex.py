
equation_preamble = r"""\documentclass{article}
\usepackage{v-vertical-equation}
\begin{document}
\end{document}"""



equation_vertical_preamble = r"""\documentclass{article}
\usepackage{v-vertical-equation}
\begin{document}
\end{document}"""

equation_square_preamble = r"""\documentclass{article}
\usepackage{v-square-equation}
\begin{document}
\end{document}"""



def equation_head(n):
    return f'{chapter}-{n}'



def equation_title(n):
    return f'{title}'


