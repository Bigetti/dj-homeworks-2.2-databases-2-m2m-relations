from django.contrib import admin

from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope



class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        for form in self.forms:
            if form.cleaned_data.get('article') and form.cleaned_data['article'].pk:
                # Ваша логика проверок, которая не зависит от свойств 'Article' до сохранения
                pass
            else:
                raise ValidationError('Article instance needs to be saved first.')
        return super().clean()





class ScopeInlineForm(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInlineForm]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [ScopeInlineForm]
