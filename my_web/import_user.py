# import_users.py
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from my_app.models import Users, AuthUser

def migrate_users():
    for u in Users.objects.all():
        if not AuthUser.objects.filter(username=u.username).exists():
            AuthUser.objects.create(
                username=u.username,
                email=u.email,
                password=make_password(u.password),
                first_name='',
                last_name='',
                is_superuser=False,
                is_staff=False,
                is_active=True,
                date_joined=timezone.now(),
                last_login=None
            )
            print(f'Migrated {u.username}')

migrate_users()