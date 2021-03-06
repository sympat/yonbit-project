# Generated by Django 2.0.2 on 2018-02-12 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('college_id', models.AutoField(primary_key=True, serialize=False)),
                ('college_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('course_number', models.CharField(max_length=50)),
                ('course_semester', models.CharField(max_length=10)),
                ('course_name', models.CharField(max_length=50)),
                ('course_time', models.CharField(max_length=50)),
                ('course_professor', models.CharField(max_length=50)),
                ('course_credit', models.IntegerField()),
                ('course_note', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_id', models.AutoField(primary_key=True, serialize=False)),
                ('department_name', models.CharField(max_length=50)),
                ('college', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mlist.College')),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('university_id', models.AutoField(primary_key=True, serialize=False)),
                ('university_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mlist.Department'),
        ),
        migrations.AddField(
            model_name='college',
            name='university',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mlist.University'),
        ),
    ]
