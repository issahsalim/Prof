# Generated by Django 5.1.1 on 2025-03-15 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessementApp', '0014_absencereport_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='Class',
            field=models.CharField(max_length=10),
        ),
    ]
