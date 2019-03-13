# Generated by Django 2.1.4 on 2019-03-12 17:14

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20190312_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContributionRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('rate', models.DecimalField(decimal_places=5, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('1'))])),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withholding_rates', to='books.Organization', verbose_name='Attached to Organization')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceContribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contribution_rate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.ContributionRate')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributions', to='books.Invoice')),
                ('tax_rate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.TaxRate')),
            ],
        ),
    ]
