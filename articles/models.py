from django.db import models

from django.urls import reverse
from prompt_toolkit.validation import ValidationError


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название тега')

    def __str__(self):
        return self.name


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)
    tags = models.ManyToManyField(Tag, through='Scope', verbose_name='Теги')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def clean(self):
        # Проверка, что у статьи есть хотя бы один основной раздел
        if not self.scope_set.filter(is_main=True).exists():
            raise ValidationError('Статья должна иметь хотя бы один основной раздел')

        # Проверка, что у статьи нет более одного основного раздела
        if self.scope_set.filter(is_main=True).exclude(pk=self.pk).exists():
            raise ValidationError('Статья может иметь только один основной раздел')


class Scope(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='scopes')
    is_main = models.BooleanField(default=False, verbose_name='Остновной тег')

    class Meta:
        unique_together = ('article', 'is_main')

    def __str__(self):
        return f"{self.article.title} - {self.tag.name}"