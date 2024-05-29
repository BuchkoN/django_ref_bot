from django.apps import AppConfig


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.core.bot'
    verbose_name = 'Telegram Bot'

    def ready(self):
        from app.core.bot.services import main  # noqa
