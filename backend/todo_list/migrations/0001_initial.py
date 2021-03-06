# Generated by Django 2.2.10 on 2021-03-12 11:57

import backend.todo_list.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('text', models.TextField(blank=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('due_date', models.DateField(default=backend.todo_list.models.get_due_date)),
                ('done', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='todo_list', to='todo_list.Category')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
    ]
