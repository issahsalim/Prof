# Generated by Django 5.1.1 on 2025-03-22 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessementApp', '0016_about'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication_number', models.CharField(max_length=20)),
                ('publication_link', models.CharField(max_length=20)),
            ],
        ),
    ]
