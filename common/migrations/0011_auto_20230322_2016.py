# Generated by Django 3.1.3 on 2023-03-22 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_auto_20230322_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
