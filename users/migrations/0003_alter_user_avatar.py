# Generated by Django 3.2.9 on 2022-01-22 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_is_email_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='static/img/blank_avatar.png', upload_to='static/img/'),
        ),
    ]