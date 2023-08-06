"""Module to parse the contents of a python file and return the responses of the flask app"""
def get_lines(filename) -> list:
    """Return a list of lines from a file"""
    with open(filename, encoding="utf-8") as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def check_imports(lines) -> bool:
    """Return True if the file contains an import of flask"""
    return any(
        'flask' in line or 'Flask' in line
        for line in lines
        if line.startswith('import') or line.startswith('from')
    )

def get_responses(i_lines) -> list:
    """Return a list of the return statements in the file"""
    route_starts = [i for (i, line) in i_lines if line.startswith('@app.route')]
    return_lines = []
    for j, start in enumerate(route_starts[:-1]):
        return_lines.append([
            (i + 1, line) for (i, line) in i_lines[start:route_starts[j + 1]]
            if line.startswith('return')
        ])
    return_lines.append([
        (i + 1, line) for (i, line) in i_lines[route_starts[-1]:]
        if line.startswith('return')
    ])
    if len(return_lines) < 1:
        return 'No return statements found in file, file is invalid'
    return [line for line_group in return_lines for line in line_group]

def parse_and_return_responses(filename) -> list:
    """Return a list of the return statements in the file (full pipeline for parsing))"""
    lines = get_lines(filename)
    if not check_imports(lines):
        return 'No imports of flask found, file is invalid'
    indexed_lines = list(enumerate(lines))
    return get_responses(indexed_lines)
