# Generated by Django 2.1.7 on 2019-03-22 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20190322_1406'),
        ('people', '0002_client_vat_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='vat_number',
            field=models.CharField(help_text='Fiscal id of the client', max_length=30),
        ),
        migrations.AlterUniqueTogether(
            name='client',
            unique_together={('organization', 'vat_number')},
        ),
    ]