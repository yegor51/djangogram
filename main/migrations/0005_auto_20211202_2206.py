# Generated by Django 3.2.9 on 2021-12-02 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='publication_name',
            field=models.CharField(default='None', max_length=50),
        ),
        migrations.AlterField(
            model_name='publication',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
