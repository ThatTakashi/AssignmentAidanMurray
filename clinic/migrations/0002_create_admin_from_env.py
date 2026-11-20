"""
Creates an administrator account from environment variables during deploy.

Set these env vars before deploying (Render dashboard -> Environment):
    ADMIN_USERNAME   e.g. admin
    ADMIN_PASSWORD   e.g. a strong password
    ADMIN_EMAIL      optional, e.g. admin@example.com

If the vars are not set, or the user already exists, this does nothing.
NOTE: migrations run once per database - if you delete the admin later,
this will not recreate it (delete the row in django_migrations to re-run).
"""
import os

from django.db import migrations


def create_admin(apps, schema_editor):
    User = apps.get_model('auth', 'User')

    username = os.environ.get('ADMIN_USERNAME')
    password = os.environ.get('ADMIN_PASSWORD')
    email = os.environ.get('ADMIN_EMAIL', '')

    # Skip silently if env vars are not configured
    if not username or not password:
        print('ADMIN_USERNAME/ADMIN_PASSWORD not set - skipping admin creation')
        return

    # Skip if the user already exists (safe on redeploys)
    if User.objects.filter(username=username).exists():
        print(f'Admin user "{username}" already exists - skipping')
        return

    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Created admin user "{username}"')


def remove_admin(apps, schema_editor):
    # Reverse migration: do nothing (we don't delete user accounts on rollback)
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin, remove_admin),
    ]
