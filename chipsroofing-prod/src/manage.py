import os
import sys

# Attachable Blocks: показывать кнопки, если есть права
# StdImage: max_source_dimensions может уменьшить картинку до размера,
#   меньшего, чем min_dimesions
# скрипты в самом начале <head>
# в @cached нужно указывать "kwargs.key" вместо "key", что неочевидно
# Найти сносный сервис для рассылки красивых email-уведомлений
# Вместо {{ domain }} использовать тэг, включающий схему запроса
# Поискать способ для быстрой верстки простых писем
# Удобный способ раздачи прав на поля форм в админке
# Избавиться от излишнего использования get_current_site() в пользу ''.format()
# REST API Python eve
# Отказаться от модуля requests в пользу urllib
# Проверить слайдер в сочетании с GSAP
# Поправить индекс формы formsets.js
# Интеграция с django_cron
# multiselect field: проблема с readonly в админке
# libs.upload: переписать
# Authorize.NET: логирование ошибок API, рефакторинг, void / refund / auth / capture
# FormHelper: hidden-полю нельзя задать класс
# Поле для номера кредитной карточки
# Стили для полей форм вынести в form_helper/scss
# Поле для заполнения GenericForeignKey
# Forms: select, GravityForms
# URLField: относительные адреса
# Платежки: перепроверить + recurring
# StdImage: save GIF animation
# admin bootstrap
# Last-modified прицепить к sitemap
# $.widget
# Импорты для Django 1.9
# Подумать над возможностью реализации Grid через Flexbox.
# Paginator: переделать номера страниц, чтобы их кол-во было более постоянно
# Попытаться избавиться от select_subclasses

# Shop cart example + discounts
# Gallery popup: JS templates
# $.fn.scrolltextarea + autosize
# Share: выводить картинку и дать возможность изменить
# Mobile tables
# Schema.org: per page + get data from models
# Admin: функция "скопировать из"
# Кнопка подтверждения заказа в админке
# Редактирование продуктов магазина в админке
# Logging, checks, tests

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
