# Generated by Django 3.0.3 on 2022-03-06 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bed_maker', '0002_clinvarcoverage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clinvarcoverage',
            name='ensembl_transcript_version',
        ),
    ]
