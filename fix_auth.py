import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

users = ['admin_user', 'normal_user']

for username in users:
    try:
        user = User.objects.get(username=username)
        user.set_password('password123')
        user.save()
        print(f"Password for '{username}' has been reset to 'password123'.")
    except User.DoesNotExist:
        print(f"User '{username}' does not exist! Creating it now...")
        if username == 'admin_user':
            User.objects.create_superuser(username, 'admin@example.com', 'password123')
        else:
            User.objects.create_user(username, 'user@example.com', 'password123')
        print(f"User '{username}' created with password 'password123'.")

print("Done.")
