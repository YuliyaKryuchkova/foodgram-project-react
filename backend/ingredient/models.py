from django.db import models


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингридиента',
        max_length=254
    )
    measurement_unit = models.CharField(
        verbose_name='Еденица измерения',
        max_length=150
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_measurement_unit'
            )
        ]

    def __str__(self):
        return (f'{self.name},'
                f'{self.measurement_unit},'
                )
