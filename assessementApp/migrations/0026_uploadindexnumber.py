# Generated by Django 5.2.3 on 2025-06-16 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessementApp', '0025_rename_user_id_chatbot_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='uploadIndexNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='indexnumbers')),
            ],
        ),
    ]
