from django.contrib import admin

from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope



class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        counter = 0
        for form in self.forms:

            if self.deleted_forms and self._should_delete_form(form):
                # Ваша логика проверок, которая не зависит от свойств 'Article' до сохранения
                continue
            elif form.cleaned_data.get('is_main'):
                counter+=1

        if counter < 1:
            raise ValidationError('Article instance needs to be saved first.')
        elif counter > 1:
            raise ValidationError('Must be only one main')

        return super().clean()


   # def clean(self):
        # Проверка, что у статьи есть хотя бы один основной раздел
   #     if hasattr(self, 'scope_set') and not self.scope_set.filter(is_main=True).exists():
   #         raise ValidationError('Статья должна иметь хотя бы один основной раздел')

   #     # Проверка, что у статьи нет более одного основного раздела
   #     main_scopes = self.scope_set.filter(is_main=True).count()
   #     if main_scopes > 1:
    #        raise ValidationError('Статья может иметь только один основной раздел')

    #    super().clean()  # вызываем clean() родительской модели


class ScopeInlineForm(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInlineForm]
    list_display = ['id', 'title', 'published_at']
    list_filter = ['title']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    #  inlines = [ScopeInlineForm]
    list_display = ['id', 'name']
