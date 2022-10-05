import datetime

from django.contrib.auth import get_user_model
from django.db import models

from petstagram.common.project_validators import MinDateValidator, ImageMaxSizeValidatorInMb

UserModel = get_user_model()


class Pet(models.Model):
    NAME_MAX_LENGTH = 30
    MIN_DATE = datetime.date(1920, 1, 1)

    TYPE_CHOICES = (
        ('Cat', 'Cat'),
        ('Dog', 'Dog'),
        ('Bunny', 'Bunny'),
        ('Parrot', 'Parrot'),
        ('Fish', 'Fish'),
        ('Other', 'Other'),
    )

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    type = models.CharField(
        max_length=max(len(x) for x, _ in TYPE_CHOICES),
        choices=TYPE_CHOICES,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
        validators=(
            MinDateValidator(MIN_DATE),
        ),
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    @property
    def age(self):
        return datetime.datetime.now().year - self.date_of_birth.year

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return f'{self.name}'


class PetPhoto(models.Model):
    IMAGE_MAX_SIZE_VALUE_IN_MB = 5

    photo = models.ImageField(
        validators=(
            ImageMaxSizeValidatorInMb(IMAGE_MAX_SIZE_VALUE_IN_MB),
        ),
    )

    tagged_pets = models.ManyToManyField(
        Pet,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    publication_date = models.DateTimeField(
        auto_now_add=True,
    )

    likes = models.IntegerField(
        default=0,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )
