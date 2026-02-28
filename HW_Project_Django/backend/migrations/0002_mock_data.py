from django.db import migrations
from django.core.management import call_command


def load_mock_data(apps, schema_editor):
    call_command('loaddata', 'mock_data', app_label='backend')


def remove_mock_data(apps, schema_editor):
    User = apps.get_model('backend', 'User')
    User.objects.filter(
        user_name__in=['Полина', 'Андрей', 'Карина', 'Алиса', 'Артем']
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_mock_data, remove_mock_data),
    ]
