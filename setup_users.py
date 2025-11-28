import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User, Group

# Create Groups
admin_group, created = Group.objects.get_or_create(name='Admin')
user_group, created = Group.objects.get_or_create(name='User')

# Create Admin User
if not User.objects.filter(username='admin_user').exists():
    admin_user = User.objects.create_user('admin_user', 'admin@example.com', 'password123')
    admin_user.groups.add(admin_group)
    admin_user.is_staff = True # Optional, for Django Admin
    admin_user.save()
    print("Admin user created.")
else:
    print("Admin user already exists.")

# Create Normal User
if not User.objects.filter(username='normal_user').exists():
    normal_user = User.objects.create_user('normal_user', 'user@example.com', 'password123')
    normal_user.groups.add(user_group)
    normal_user.save()
    print("Normal user created.")
else:
    print("Normal user already exists.")
