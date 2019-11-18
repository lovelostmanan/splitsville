# Generated by Django 2.2.4 on 2019-10-17 04:37

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('splits', '0002_auto_20191017_1007'),
    ]

    operations = [
        migrations.CreateModel(
            name='person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='make_groups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gname', models.CharField(max_length=64)),
                ('glist', models.ManyToManyField(to='splits.person')),
            ],
        ),
        migrations.CreateModel(
            name='account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalbalance', models.DecimalField(decimal_places=3, default=Decimal('0.000'), max_digits=5)),
                ('youowe', models.DecimalField(decimal_places=3, default=Decimal('0.000'), max_digits=5)),
                ('youareowed', models.DecimalField(decimal_places=3, default=Decimal('0.000'), max_digits=5)),
                ('holder', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='splits.person')),
            ],
        ),
    ]
