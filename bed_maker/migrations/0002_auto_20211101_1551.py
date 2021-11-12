# Generated by Django 3.0.3 on 2021-11-01 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bed_maker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcript',
            name='clinvar_coverage',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transcript',
            name='clinvar_variants',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transcript',
            name='coverage',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]