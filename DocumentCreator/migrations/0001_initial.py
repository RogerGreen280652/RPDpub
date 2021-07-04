# Generated by Django 3.2.5 on 2021-07-04 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RpdDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='RpdPlaceDiscipline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disciplines', models.TextField()),
                ('type', models.IntegerField()),
                ('document_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DocumentCreator.rpddocument')),
            ],
        ),
        migrations.CreateModel(
            name='RpdDocumentTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('discipline_name', models.CharField(max_length=255)),
                ('direction_name', models.CharField(max_length=255)),
                ('document_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DocumentCreator.rpddocument')),
            ],
        ),
        migrations.CreateModel(
            name='RpdDocumentTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=255)),
                ('document_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DocumentCreator.rpddocument')),
            ],
        ),
        migrations.CreateModel(
            name='RpdDocumentTargets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('targets', models.TextField()),
                ('document_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DocumentCreator.rpddocument')),
            ],
        ),
    ]
