# Generated by Django 2.1.1 on 2018-10-23 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='question title')),
                ('content', models.TextField(verbose_name='question content')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
    ]
