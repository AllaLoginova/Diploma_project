from audioop import reverse

from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from recipes.models import Recipes, Category


@admin.register(Recipes)
class RecipeAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'photo', 'post_photo', 'cat', 'tags'] # отображаемые поля
    # exclude = ['tags', 'is_published'] # исключает эти поля
    readonly_fields = ['post_photo']  # нередактируемые поля
    prepopulated_fields = {'slug': ('title', )} # формирование слага (способ № 2)
    filter_horizontal = ['tags'] # удобный вариант отражения тегов
    # filter_vertical = ['tags']  # удобный вариант отражения тегов
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat') # отражаемые поля
    list_display_links = ('title', ) # кликабельные поля
    ordering = ['-time_create', 'title'] # сортировка по выбранному полю(полям) для админ-панели
    list_editable = ('is_published', ) # поле(я) для редактирования
    list_per_page = 5  # пагинация - max количество отражаемых статей на странице
    actions = ['set_publishd', 'set_draft']   # добавить новое действие
    search_fields = ['title', 'cat__name'] # поиск по полям в панели поиска
    list_filter = ['cat__name', 'is_published'] # на панели фильтрации отображаются выбранные поля
    save_on_top = True


    @admin.display(description='Изображение', ordering='content')
    def post_photo(self, recipe: Recipes):
        if recipe.photo:
            return mark_safe(f"<img src='{recipe.photo.url}' width=50>")
        return 'Без фото'


    @admin.action(description='Опубликовать выбранные записи')
    def set_publishd(self, request, queryset):
        count = queryset.update(is_published=Recipes.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей.")

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Recipes.Status.DRAFT)
        self.message_user(request, f"{count} записей снято с публикации", messages.WARNING)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name') # отражаемые поля
    list_display_links = ('id', 'name') # кликабельные поля





