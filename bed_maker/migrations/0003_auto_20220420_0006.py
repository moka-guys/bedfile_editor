# Generated by Django 3.0.3 on 2022-04-19 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bed_maker', '0002_auto_20220420_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinvarcoverage_grch38',
            name='clinvar_coverage_fraction',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='clinvarcoverage_grch38',
            name='clinvar_variants',
            field=models.CharField(max_length=50, null=True),
        ),
    ]