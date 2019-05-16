# Generated by Django 2.1.7 on 2019-03-22 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20190322_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='description',
            field=models.TextField(blank=True, help_text='Insert notes, description or any relevant information', null=True),
        ),
        migrations.AddField(
            model_name='estimate',
            name='description',
            field=models.TextField(blank=True, help_text='Insert notes, description or any relevant information', null=True),
        ),
        migrations.AddField(
            model_name='expenseclaim',
            name='description',
            field=models.TextField(blank=True, help_text='Insert notes, description or any relevant information', null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='description',
            field=models.TextField(blank=True, help_text='Insert notes, description or any relevant information', null=True),
        ),
    ]