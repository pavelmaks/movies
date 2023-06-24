import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(verbose_name=_('name'), max_length=255)
    description = models.TextField(verbose_name=_('description'), blank=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name


class Gender(models.TextChoices):
    MALE = 'male', _('male')
    FEMALE = 'female', _('female')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(verbose_name=_('full_name'), max_length=255)
    gender = models.TextField(_('gender'), choices=Gender.choices, null=True)

    class Meta:
        db_table = 'content"."person'
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):
    class TypeFilwork(models.TextChoices):
        MOVIE = ('movie', _('film'))
        TV_SHOW = ('tv_show', _('tv_show'))

    title = models.CharField(
        verbose_name=_('title'), max_length=255, blank=True
    )
    certificate = models.CharField(
        _('certificate'), max_length=512, null=True
    )
    file_path = models.FileField(
        _('file'), blank=True, null=True, upload_to='movies/'
    )
    description = models.TextField(verbose_name=_('description'))
    creation_date = models.DateField(verbose_name=_('creation_date'))
    rating = models.FloatField(
        verbose_name=_('rating'),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    film_type = models.CharField(
        verbose_name=_('type'),
        max_length=255,
        choices=TypeFilwork.choices,
        db_column='type',
    )
    genres = models.ManyToManyField(
        Genre, verbose_name=_('genre'), through='GenreFilmwork'
    )
    person = models.ManyToManyField(
        Person, verbose_name=_('person'), through='PersonFilmwork'
    )

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        'Filmwork', verbose_name=_('film'), on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        'Genre', verbose_name=_('genre'), on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        unique_together = ['film_work', 'genre']
        verbose_name = _('genre_film')
        verbose_name_plural = _('genre_films')


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        'Filmwork', verbose_name=_('film'), on_delete=models.CASCADE
    )
    person = models.ForeignKey(
        'Person', verbose_name=_('person'), on_delete=models.CASCADE
    )
    role = models.TextField(verbose_name=_('role'), null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        unique_together = ['film_work', 'person', 'role']
        verbose_name = _('person_film')
        verbose_name_plural = _('persons_film')
