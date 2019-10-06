# Generated by Django 2.2 on 2019-07-14 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0004_pay'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.EmailField(default='123@163.com', max_length=128, unique=True)),
                ('Name', models.CharField(default='xxx', max_length=128)),
                ('Password', models.CharField(default='123456789', max_length=128)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
