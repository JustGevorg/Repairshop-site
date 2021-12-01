from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# Суть каждой модели в документации к ней же


class Workshop(models.Model):
    """Мастерская"""
    title = models.CharField('Название', unique = True, max_length = 50)
    description = models.TextField('Описание')
    time_table = models.CharField('Расписание', max_length = 25, default = 'без выходных')
    addres = models.CharField('Адрес', unique = True,  max_length = 100, default = '')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Мастерская'
        verbose_name_plural = 'Мастерские'


class Master(models.Model):
    """Мастер"""
    name = models.CharField('Имя', max_length = 50, default = '', unique = True)
    experience = models.PositiveIntegerField('Общий стаж(лет)', default = 0, help_text = 'укажите стаж мастера')
    spec = models.CharField('Специальность', max_length = 50, default = '')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'


class WorksOn(models.Model):
    """Занятость мастеров в мастерских(мастер работает только в одной мастерской,
    в мастерской может быть несколько мастеров)
    """
    workshop = models.ForeignKey(Workshop, verbose_name = 'Мастерская', on_delete = models.CASCADE, related_name='work')
    master = models.OneToOneField(Master, verbose_name = 'Мастер', on_delete = models.CASCADE, related_name='worker')

    class Meta:
        verbose_name = 'Занятость'
        verbose_name_plural = 'Занятости'


class Guard(models.Model):
    """Охранная фирма"""
    title = models.CharField('Название', unique = True, max_length = 50)
    status = models.CharField('Репутация', max_length = 50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Охранная фирма'
        verbose_name_plural = 'Охранные фирмы'


class Defend(models.Model):
    """Охранные фирмы охраняют мастерские, фирма может охранять несколько
    мастерских, мастерская может быть под охраной одной фирмы"""

    guard = models.ForeignKey(Guard, on_delete = models.CASCADE, verbose_name = 'Охранная фирма')
    workshop = models.OneToOneField(Workshop, on_delete = models.CASCADE, verbose_name = 'Мастерская')

    class Meta:
        verbose_name = 'Договор с охранной фирмы'
        verbose_name_plural = 'Договоры с охранными фирмами'


class Review(models.Model):
    """Отзывы о мастерских, отзыв пишется для одной мастерской,
    на мастерскую может быть написано несколько отзывов"""
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'Автор', null = True, blank = True)
    workshop = models.ForeignKey(Workshop, on_delete = models.CASCADE, verbose_name = 'Мастерская', blank = True, null = True)
    theme = models.CharField('Тема', max_length = 50)
    text = models.TextField('Текст отзыва')

    def __int__(self):
        return self.theme

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class AdminRequest(models.Model):
    """Модель для админского запроса напрямую в БД"""
    req = models.CharField('Запрос', max_length = 200)

    def __str__(self):
        return self.req

    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'
