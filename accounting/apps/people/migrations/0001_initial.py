# Generated by Django 2.1.4 on 2019-03-12 13:14

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessOrganization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Business communicated name', max_length=150)),
                ('address_line_1', models.CharField(max_length=128)),
                ('address_line_2', models.CharField(blank=True, max_length=128, null=True)),
                ('city', models.CharField(max_length=64)),
                ('postal_code', models.CharField(max_length=7)),
                ('country', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('businessorganization_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='people.BusinessOrganization')),
            ],
            bases=('people.businessorganization',),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('businessorganization_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='people.BusinessOrganization')),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('payroll_tax_rate', models.DecimalField(decimal_places=5, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('1'))])),
                ('salary_follows_profits', models.BooleanField(default=False)),
                ('shares_percentage', models.DecimalField(decimal_places=5, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('1'))])),
            ],
            bases=('people.businessorganization',),
        ),
        migrations.AddField(
            model_name='businessorganization',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='people_businessorganizations', to='books.Organization'),
        ),
    ]
