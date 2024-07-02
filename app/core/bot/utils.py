import re as regex

from django.conf import settings


def extract_ref_code(value: str) -> str | None:
    if (
        value is not None
        and (match := regex.search(rf'{settings.REFERRAL_CODE_PREFIX}_(.*)', value))
    ):
        return match.group(1)
    return None
