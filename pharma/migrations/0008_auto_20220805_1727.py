# Generated by Django 3.0.7 on 2022-08-05 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pharma', '0007_auto_20220626_1203'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stockentry',
            options={'ordering': ['-date']},
        ),
    ]
