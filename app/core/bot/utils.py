import re as regex


def extract_ref_code(value: str) -> str | None:
    if (
        value is not None
        and (match := regex.search(r'ref_(.*)', value))
    ):
        return match.group(1)
    return None
