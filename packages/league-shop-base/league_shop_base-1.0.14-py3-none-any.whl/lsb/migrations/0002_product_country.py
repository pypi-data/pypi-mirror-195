# Generated by Django 4.1.4 on 2023-01-16 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lsb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='country',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
