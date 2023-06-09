# Generated by Django 3.2 on 2023-05-17 16:29

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20230514_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[users.validators.validate_username, users.validators.UsernameValidator()], verbose_name='Имя пользователя'),
        ),
    ]
