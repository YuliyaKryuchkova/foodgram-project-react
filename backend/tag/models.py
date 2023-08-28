from django.core.validators import RegexValidator
from django.db import models


class Tag(models.Model):
    name = models.CharField(
        'Название тега',
        max_length=150
    )
    color = models.CharField(
        verbose_name='HEX-код',
        max_length=7,
        unique=True,
        validators=[
            RegexValidator(
                regex="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
                message='Количество вводимых символов hex-кода не превышает 7',
            )
        ],

    )
    slug = models.SlugField(
        'Ссылка',
        max_length=150,
        unique=True,
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
