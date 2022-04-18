import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Genre(TimeStampedMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
        db_table = f'{settings.DB_SCHEMA}"."genre'
        indexes = [
            models.Index(fields=['name']),
        ]


class FilmworkGenre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE, verbose_name=_('Filmwork'))
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, verbose_name=_('Genre'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
        db_table = f'{settings.DB_SCHEMA}"."genre_film_work'
        unique_together = [['film_work', 'genre']]

    def __str__(self):
        return f'{self.film_work.title}, {self.genre.name}'


class Person(TimeStampedMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(_('Full name'), max_length=255)
    birth_date = models.DateField(_('Birth date'), blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        db_table = f'{settings.DB_SCHEMA}"."person'


class PersonRole(models.TextChoices):
    ACTOR = 'Actor', _('Actor')
    DIRECTOR = 'Director', _('Director')
    WRITER = 'Writer', _('Writer')


class FilmworkPerson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE, verbose_name=_('Filmwork'))
    person = models.ForeignKey('Person', on_delete=models.CASCADE, verbose_name=_('Person'))
    role = models.CharField(_('Role'), max_length=255, choices=PersonRole.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        db_table = f'{settings.DB_SCHEMA}"."person_film_work'
        unique_together = [['film_work', 'person', 'role']]

    def __str__(self):
        return f'{self.film_work.title}, {self.person.full_name}, {self.role}'


class FilmworkType(models.TextChoices):
    MOVIE = 'movie', _('Movie')
    TV_SHOW = 'tv_show', _('TV Show')


class Filmwork(TimeStampedMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    creation_date = models.DateField(_('Creation date'), blank=True)
    certificate = models.TextField(_('Certificate'), blank=True)
    file_path = models.FileField(_('File'), upload_to='film_works/', blank=True)
    rating = models.FloatField(_('Rating'), validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True)
    type = models.CharField(_('Type'), max_length=20, choices=FilmworkType.choices)
    genres = models.ManyToManyField(Genre, through='FilmworkGenre')
    persons = models.ManyToManyField(Person, through='FilmworkPerson')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')
        db_table = f'{settings.DB_SCHEMA}"."film_work'
