# Generated by Django 5.0.6 on 2024-05-24 18:07

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_options_alter_user_language_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telegram_username',
            field=models.CharField(max_length=250, null=True, verbose_name='Telegram username'),
        ),
    ]
