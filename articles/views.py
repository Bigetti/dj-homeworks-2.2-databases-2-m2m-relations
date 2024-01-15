from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'

    # Получаем все статьи и упорядочиваем их по дате публикации
    articles = Article.objects.order_by('-published_at')
    context = {'object_list': articles}  # Важно использовать 'object_list' для совместимости с вашим шаблоном


    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    ordering = '-published_at'

    return render(request, template, context)
