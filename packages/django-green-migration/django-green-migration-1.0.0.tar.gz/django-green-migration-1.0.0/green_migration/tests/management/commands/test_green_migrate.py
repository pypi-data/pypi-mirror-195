import json
import os
from io import StringIO

from django.apps import apps
from django.core.management import call_command

from common.tests.isolated_cache_test_case import TestCase
from libraries.green_migration.tests.management.commands.fake_temp_model import FakeTempModelTest


class GreenMigrateTest(FakeTempModelTest, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.maxDiff = None

        self.app_path = apps.get_app_config('green_migration').path
        self.migration_file = f'{self.app_path}/migrations/0001_initial.py'
        with open(self.migration_file, 'w'):
            pass
        self.start_fake_temp_model('libraries.green_migration.management.commands.green_migrate.apps')

    def tearDown(self) -> None:
        super().tearDown()
        os.unlink(self.migration_file)
        self.stop_fake_temp_model()

    def test_update_migration_file_char_field(self):
        with open(self.migration_file, 'w') as f:
            f.write(
                """
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='temp_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config', models.CharField(default='5', max_length=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='temp_model',
            name='config',
        ),
    ]
""",
            )
        stdout = StringIO()
        call_command('green_migrate', stdout=stdout)
        with open(self.migration_file) as f:
            content = f.read()

        self.assertEqual(
            content.strip(),
            """
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='temp_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config', models.CharField(default='5', max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='temp_model',
            name='config',
            field=models.CharField(blank=True, null=True, max_length=254),
        ),
    ]
""".strip(),
        )

        output = stdout.getvalue().split('------------------deleted_fields------------------')[-1]
        self.assertEqual(
            output.strip(), json.dumps({
                'green_migration': {
                    'temp_model': ['config'],
                },
            }),
        )

    def test_update_migration_only_1_delete_field(self):
        with open(self.migration_file, 'w') as f:
            f.write(
                """
from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RemoveField(
            model_name='temp_model',
            name='config',
        ),
    ]
""",
            )
        stdout = StringIO()
        call_command('green_migrate', stdout=stdout)
        with open(self.migration_file) as f:
            content = f.read()

        self.assertEqual(
            content.strip(),
            """
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.AlterField(
            model_name='temp_model',
            name='config',
            field=models.CharField(blank=True, null=True, max_length=254),
        ),
    ]
""".strip(),
        )

    def test_not_update_migration_file_if_no_remove_field(self):
        with open(self.migration_file, 'w') as f:
            f.write(
                """
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='temp_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config', models.IntegerField(default=5)),
            ],
        ),
    ]
""",
            )

        stdout = StringIO()
        call_command('green_migrate', stdout=stdout)
        with open(self.migration_file) as f:
            content = f.read()

        self.assertEqual(
            content.strip(),
            """
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='temp_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config', models.IntegerField(default=5)),
            ],
        ),
    ]
""".strip(),
        )

        output = stdout.getvalue().split('------------------deleted_fields------------------')[-1]
        self.assertEqual(output.strip(), json.dumps({}))
