# Generated by Django 2.1.5 on 2019-11-23 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('splits', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='splits.make_group')),
            ],
        ),
    ]