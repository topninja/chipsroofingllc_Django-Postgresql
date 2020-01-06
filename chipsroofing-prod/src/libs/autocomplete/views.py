import math
import pickle
import importlib
from django.apps import apps
from django.db.models import Q
from django.contrib import admin
from django.core.cache import caches
from django.http import Http404, JsonResponse
from . import conf

cache = caches[conf.AUTOCOMPLETE_CACHE_BACKEND]


@admin.site.admin_view
def autocomplete_widget(request, application, model_name, name):
    if not request.is_ajax():
        raise Http404

    try:
        page = int(request.POST.get('page', 1))
        page_limit = int(request.POST.get('page_limit', 0))
    except (TypeError, ValueError):
        raise Http404

    # Получаем данные из Redis
    redis_data = pickle.loads(
        cache.get('autocomplete.%s' % '.'.join((application, model_name, name)))
    )

    # Восстанавливаем queryset
    model = apps.get_model(application, model_name)
    if model is None:
        raise Http404

    data = {
        'result': [],
    }

    queryset = model.objects.all()
    queryset.query = redis_data['query']

    # Зависимое поле
    query = {}
    values = request.POST.get('values', '').split(';')
    filters = tuple(item[0] for item in redis_data['filters'])
    is_multiple = tuple(item[2] if len(item) > 2 else False for item in redis_data['filters'])
    for index, key in enumerate(filters):
        try:
            value = values[index]
            multiple = is_multiple[index]
        except KeyError:
            return JsonResponse(data)

        if not value:
            value = None
        elif multiple:
            value = value.split(',')
            key += '__in'

        query[key] = value

    queryset = queryset.filter(**query)

    # Поиск по выражениям
    expressions = request.POST.get('expressions')
    if not expressions:
        raise Http404
    else:
        expressions_query = Q()
        token = request.POST.get('q', '')
        for expression in expressions.split(','):
            if expression.endswith('__in'):
                expressions_query |= Q((expression, token.split(",")))
            else:
                expressions_query |= Q((expression, token))

        queryset = queryset.filter(expressions_query)

    # Постраничная навигация
    if page and page_limit:
        count = data['total'] = queryset.count()
        max_pages = math.ceil(count / page_limit)
        real_page = max(1, min(page, max_pages))
        offset = (real_page - 1) * page_limit
        queryset = queryset[offset:offset+page_limit]

    # Кастомное форматирование списка
    module = importlib.import_module(redis_data['format_item_module'])
    current_obj = module
    for part in redis_data['format_item_method'].split('.'):
        current_obj = getattr(current_obj, part)
    else:
        format_item = current_obj

    for item in queryset.iterator():
        item_dict = format_item(item)
        if not isinstance(item_dict, dict):
            raise ValueError('autocomplete format_item should return dict')
        if ('id' not in item_dict) or ('text' not in item_dict):
            raise ValueError('autocomplete format_item should contain "id" and "text"')
        data['result'].append(item_dict)

    return JsonResponse(data)


@admin.site.admin_view
def autocomplete_filter(request, application, model_name):
    if not request.is_ajax():
        raise Http404

    try:
        page = int(request.POST.get('page', 1))
        page_limit = int(request.POST.get('page_limit', 0))
    except (TypeError, ValueError):
        raise Http404

    model = apps.get_model(application, model_name)
    if model is None:
        raise Http404

    # Получаем данные из Redis
    redis_data = pickle.loads(
        cache.get('autocomplete_filter.%s' % '.'.join((application, model_name)))
    )

    data = {
        'result': [],
    }

    query = {}
    values = request.POST.get('values', '').split(';')
    filters = tuple(item[0] for item in redis_data['filters'])
    for index, key in enumerate(filters):
        try:
            value = values[index]
        except KeyError:
            return JsonResponse(data)

        if not value:
            value = None

        query[key] = value

    queryset = model.objects.filter(**query)

    # Поиск по выражениям
    expression = request.POST.get('expression')
    if not expression:
        raise Http404
    else:
        token = request.POST.get('q', '')
        if expression.endswith('__in'):
            expression_query = Q((expression, token.split(",")))
        else:
            expression_query = Q((expression, token))

        queryset = queryset.filter(expression_query)

    # Постраничная навигация
    if page and page_limit:
        count = data['total'] = queryset.count()
        max_pages = math.ceil(count / page_limit)
        real_page = max(1, min(page, max_pages))
        offset = (real_page - 1) * page_limit
        queryset = queryset[offset:offset + page_limit]

    for item in queryset.iterator():
        data['result'].append({
            'id': item.pk,
            'text': str(item)
        })

    return JsonResponse(data)
