# Generated by Django 3.0.4 on 2020-04-01 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.IntegerField(db_column='student_id', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='name', max_length=100)),
                ('gender', models.CharField(choices=[('男', '男'), ('女', '女')], db_column='gender', max_length=32)),
                ('birthday', models.DateField(db_column='birthday')),
                ('mobile', models.CharField(db_column='mobile', max_length=64)),
                ('email', models.CharField(db_column='email', max_length=100)),
                ('address', models.CharField(db_column='address', max_length=200)),
                ('image', models.CharField(db_column='image', max_length=200)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Student',
                'managed': True,
            },
        ),
    ]
