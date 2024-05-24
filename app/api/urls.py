from app.api.webhooks import telegram
from django.urls import path


urlpatterns = [
    path('telegram', telegram, name='telegram_webhook'),
]
