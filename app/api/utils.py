from ipaddress import (
    AddressValueError,
    IPv4Address,
    IPv4Network,
)

from django.conf import settings
from django.http import HttpRequest


def telegram_webhook_verify(request: HttpRequest) -> bool:
    try:
        remote_address = IPv4Address(request.headers.get('X-Forwarded-For', None))
        networks = [IPv4Network(network) for network in settings.TELEGRAM_ALLOWED_NETWORKS]
        return any(remote_address in network for network in networks)
    except AddressValueError:
        return False
