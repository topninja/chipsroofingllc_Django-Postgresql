from hashlib import md5
from random import randint
from functools import wraps
from inspect import signature
from django.core.cache import caches


def make_key(func, params=()):
    """
        Возвращает ключ кэша функции с указанными параметрами.

        Параметры:
            func      - функция
            params    - последовательность значений, которые составят ключ кэша
    """
    final_params = [func.__module__, func.__qualname__]
    for param in params:
        param = str(param)

        # Требуем, чтобы ключ состоял только из latin-1
        try:
            param.encode('latin-1')
        except UnicodeEncodeError:
            param = md5(param.encode()).hexdigest()

        final_params.append(param)

    return '.'.join(final_params)


def get_property(value, prop):
    # Аттрибут
    try:
        value = getattr(value, prop)
    except AttributeError:
        pass
    else:
        return value

    # Индекс
    try:
        value = value[prop]
    except (KeyError, TypeError):
        pass
    else:
        return value

    # Числовой индекс
    try:
        value = value[int(prop)]
    except (KeyError, TypeError, ValueError):
        raise ValueError
    else:
        return value


def cached(*key, time=5*60, backend='default'):
    """
        Декоратор кэширования функций и методов,
        использующий для составления ключа значения параметров функции.

        Поддерживает указание атрибутов параметров, например "request.city.id".
        Данная нотация может быть использована и для свойств и для индексов (dectionary.index).

        Параметры:
            key             - список имен параметров функции, которые
                              будут использованы для составления ключа кэша
            time            - время кэширования в секундах
            backend         - идентификатор используемого бэкенда кэширования

        Пример использования:
            @cached('title', 'address.street', 'addition.key', time=3600)
            def MyFunc(title, address, addition={'key': 1})
                ...
                 return ...
    """
    cache = caches[backend]

    def decorator(func):
        sig = signature(func)
        defaults = {
            k: v.default
            for k, v in sig.parameters.items()
        }

        @wraps(func)
        def wrapper(*args, **kwargs):
            bind_args = sig.bind(*args, **kwargs)
            bind_args = dict(defaults, **bind_args.arguments)

            # Получение значений параметров функции
            real_params = []
            for name in (key or bind_args):
                if name == 'self':
                    continue

                properties = name.split('.')
                value = bind_args.get(properties.pop(0), None)
                for prop in properties:
                    try:
                        value = get_property(value, prop)
                    except ValueError:
                        value = None
                        break

                    if callable(value):
                        value = value()

                real_params.append(value)

            cache_key = make_key(func, real_params)
            if cache_key in cache:
                return cache.get(cache_key)
            else:
                result = func(*args, **kwargs)
                if result is not None:
                    # Размазываем по времени (±10%), чтобы избежать
                    # обновления множества кэшированных данных одновременно.
                    amplitude = round(time * 0.1)
                    final_time = max(20, time + randint(-amplitude, amplitude))
                    cache.set(cache_key, result, final_time)

                return result
        return wrapper
    return decorator
