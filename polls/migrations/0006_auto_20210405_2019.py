# Generated by Django 2.2.10 on 2021-04-05 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20210405_2004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='poll',
        ),
        migrations.AddField(
            model_name='question',
            name='poll',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='polls.Poll'),
        ),
    ]
