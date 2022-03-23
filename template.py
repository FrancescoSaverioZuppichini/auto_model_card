import re
from re import Match
from typing import Dict, Any

# {{!run_my_code}}
CODE_BLOCK_REGEX = r"{{\!([^}]+)}"


def inject(template: str, variables: Dict[str, Any]) -> str:
    match: Match = re.search(CODE_BLOCK_REGEX, template)
    # evaluate and replace all the code blocks
    while match is not None:
        code = match.group(1)
        evaluated = eval(code, variables)
        template = (
            template[: match.start()] + str(evaluated) + template[match.end() + 1 :]
        )
        match: Match = re.search(CODE_BLOCK_REGEX, template)
    # replace all the variables
    for var, value in variables.items():
        template = re.sub("{{" + var + "}}", str(value), template)

    return template
