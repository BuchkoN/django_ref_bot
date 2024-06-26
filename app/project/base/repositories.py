from dataclasses import dataclass

from django.db.models.manager import Manager


@dataclass
class BaseRepositoryDjango:
    manager: Manager
