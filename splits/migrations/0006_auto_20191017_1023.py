# Generated by Django 2.2.4 on 2019-10-17 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('splits', '0005_f_list_friend'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='f_list',
            name='frnd',
        ),
        migrations.AddField(
            model_name='f_list',
            name='frnd',
            field=models.ManyToManyField(to='splits.friend'),
        ),
    ]
