import os

from django.apps import AppConfig
from django.db import OperationalError, ProgrammingError


class ClinicConfig(AppConfig):
    name = 'clinic'

    def ready(self):
        # Runs on every server start (and every manage.py command).
        # Creates the admin account from env vars if it doesn't exist yet.
        # Wrapped in try/except because the DB tables may not exist yet
        # (e.g. while `migrate` itself is running on first deploy).
        try:
            self._create_admin_from_env()
        except (OperationalError, ProgrammingError):
            pass  # DB not ready yet - migrate will run before gunicorn starts

    def _create_admin_from_env(self):
        from django.contrib.auth import get_user_model

        username = os.environ.get('ADMIN_USERNAME')
        password = os.environ.get('ADMIN_PASSWORD')
        email = os.environ.get('ADMIN_EMAIL', '')

        if not username or not password:
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'is_staff': True, 'is_superuser': True},
        )
        if created:
            user.set_password(password)
            user.save()
            print(f'[clinic] Created admin user "{username}" from env')
        elif not user.is_superuser:
            # User exists but isn't admin - promote it and update password
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save()
            print(f'[clinic] Promoted existing user "{username}" to admin')
