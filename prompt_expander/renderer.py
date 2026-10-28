"""Template rendering for {{variable}} expansion."""

from typing import Dict, Iterable, List

_VARIABLE_RE = __import__("re").compile(r"{{\s*([A-Za-z_][A-Za-z0-9_]*)\s*}}")


def render(template: str, variables: Dict[str, str] = None) -> str:
    """Replace {{name}} occurrences in *template* with values from *variables*.

    Variables missing from *variables* are left unchanged in the output so no
    data is silently destroyed.
    """
    if variables is None:
        variables = {}

    def replace(match):
        name = match.group(1)
        value = variables.get(name)
        if value is None:
            return match.group(0)
        return str(value)

    return _VARIABLE_RE.sub(replace, template)


def find_variables(template: str) -> List[str]:
    """Return the variable names referenced in *template*, in order of appearance."""
    return _VARIABLE_RE.findall(template)


def unresolved(template: str, variables: Dict[str, str]) -> List[str]:
    """Return variable names referenced in *template* that have no value."""
    seen = set()
    missing = []
    for name in find_variables(template):
        if name not in variables and name not in seen:
            seen.add(name)
            missing.append(name)
    return missing
