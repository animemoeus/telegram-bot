# Generated by Django 3.2.15 on 2022-10-05 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moegram_bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='send_like_interval',
            field=models.IntegerField(choices=[(5, 'Five Minute'), (10, 'Ten Minute'), (15, 'Fifteen Minute'), (20, 'Twenty Minute'), (30, 'Thirty Minute'), (60, 'One Hour')], default=60),
        ),
    ]
