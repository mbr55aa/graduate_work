# Generated by Django 3.2 on 2021-10-25 19:47

import uuid

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filmwork',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('creation_date', models.DateField(blank=True, verbose_name='creation date')),
                ('certificate', models.TextField(blank=True, verbose_name='certificate')),
                ('file_path', models.FileField(blank=True, upload_to='film_works/', verbose_name='file')),
                ('rating', models.FloatField(blank=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='rating')),
                ('type', models.CharField(choices=[('movie', 'movie'), ('tv_show', 'TV Show')], max_length=20, verbose_name='type')),
            ],
            options={
                'verbose_name': 'filmwork',
                'verbose_name_plural': 'filmworks',
                'db_table': 'content"."film_work',
            },
        ),
        migrations.CreateModel(
            name='FilmworkGenre',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'content"."genre_film_work',
            },
        ),
        migrations.CreateModel(
            name='FilmworkPerson',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(max_length=255, verbose_name='role')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'content"."person_film_work',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'genre',
                'verbose_name_plural': 'genres',
                'db_table': 'content"."genre',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255, verbose_name='full name')),
                ('birth_date', models.DateField(blank=True, verbose_name='birth date')),
            ],
            options={
                'verbose_name': 'person',
                'verbose_name_plural': 'persons',
                'db_table': 'content"."person',
            },
        ),
        migrations.AddIndex(
            model_name='genre',
            index=models.Index(fields=['name'], name='genre_name_bff4c4_idx'),
        ),
        migrations.AddField(
            model_name='filmworkperson',
            name='film_work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork'),
        ),
        migrations.AddField(
            model_name='filmworkperson',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.person'),
        ),
        migrations.AddField(
            model_name='filmworkgenre',
            name='film_work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork'),
        ),
        migrations.AddField(
            model_name='filmworkgenre',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.genre'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(through='movies.FilmworkGenre', to='movies.Genre'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(through='movies.FilmworkPerson', to='movies.Person'),
        ),
        migrations.AlterUniqueTogether(
            name='filmworkperson',
            unique_together={('film_work', 'person', 'role')},
        ),
        migrations.AlterUniqueTogether(
            name='filmworkgenre',
            unique_together={('film_work', 'genre')},
        ),
    ]
