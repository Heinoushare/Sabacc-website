# Generated by Django 3.1.5 on 2021-04-25 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='player2',
            field=models.TextField(default='Garth'),
            preserve_default=False,
        ),
    ]
