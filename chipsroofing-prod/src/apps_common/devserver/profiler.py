import sys
import sqlparse
from decimal import Decimal
from functools import wraps
from datetime import datetime
from django.db import connections
from django.utils.termcolors import colorize
from django.utils.decorators import available_attrs

key_color = 'blue'


class Profile:
    """
        Контекстный менеджер для профилирования участков кода.

        Пример:
            from devserver import Profile

            with Profile('FetchEntity', sql=True):
                enities = Entity.objects.get(pk=1)
                ...

            with Profile('LogToFile', stdout='/tmp/log.txt', sql=True):
                enities = Entity.objects.get(pk=1)
                ...

    """
    indent_width = 2

    __slots__ = (
        'name', 'exec_time', 'sqls', 'sql_time', 'sql_count', 'stdout',
        '_colorize', '_show_sql', '_db_start_queries', '_start_time', '_close_stdout'
    )

    def __init__(self, name='dev', sql=False, stdout=None):
        self.name = name
        self.exec_time = 0
        self.sqls = {}
        self.sql_time = 0
        self.sql_count = 0
        self._show_sql = sql
        self._close_stdout = False

        if stdout:
            self._colorize = False
            if isinstance(stdout, str):
                self.stdout = open(stdout, 'a+')
                self._close_stdout = True
            else:
                self.stdout = stdout
        else:
            self._colorize = True
            self.stdout = sys.stdout

    def __enter__(self):
        """ Запоминаем сколько запросов было совешено к каждой БД """
        self._db_start_queries = {}
        for dbname in connections:
            self._db_start_queries[dbname] = len(connections[dbname].queries_log)

        self._start_time = datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        exec_time = datetime.now() - self._start_time
        exec_time = (exec_time.seconds * 1000) + (exec_time.microseconds / 1000.0)
        self.exec_time = exec_time

        sql_count = 0
        sql_time = Decimal()
        for dbname in connections:
            queries = connections[dbname].queries[self._db_start_queries[dbname]:]
            if not queries:
                continue

            self.sqls[dbname] = queries
            sql_time += sum(Decimal(row['time']) for row in queries)
            sql_count += len(queries)

        self.sql_count = sql_count
        self.sql_time = int(sql_time * 1000)

        self.print_info()

        self.stdout.flush()
        if self._close_stdout:
            self.stdout.close()

    def colorize(self, text, **kwargs):
        if self._colorize:
            return colorize(text, **kwargs)
        else:
            return text

    def print_info(self):
        """ Вывод собранной информации """
        # вывод имени профилировщика
        self.stdout.write(
            '{profiler}\n'.format(
                profiler=self.colorize(
                    'Profile "{}":'.format(self.name),
                    fg='white',
                    opts=('bold',)
                )
            )
        )

        # Вывод SQL-запросов
        if self._show_sql:
            for dbname in connections:
                queries = self.sqls.get(dbname)
                if not queries:
                    continue

                for index, sql_data in enumerate(queries, start=1):
                    sql_time = str(Decimal(sql_data['time']) * 1000)
                    sql_time = sql_time.rstrip('0').rstrip('.')

                    caption = '{index}) {sql_time}ms, database "{dbname}":'.format(
                        index=index,
                        dbname=dbname,
                        sql_time=sql_time,
                    )
                    self.stdout.write(
                        '{indent}{caption}\n'.format(
                            indent=' ' * self.indent_width,
                            caption=self.colorize(
                                caption,
                                fg=key_color,
                                opts=('bold',)
                            )
                        )
                    )

                    sql_query = sqlparse.format(
                        sql_data['sql'],
                        reindent=True,
                        keyword_case='upper'
                    )
                    indent = ' ' * self.indent_width * 3
                    sql_query = ('\n' + indent).join(sql_query.split('\n'))
                    self.stdout.write(
                        '{indent}{sql_query}\n'.format(
                            indent=indent,
                            sql_query=self.colorize(
                                sql_query,
                                fg='yellow',
                                opts=('bold',)
                            )
                        )
                    )
            self.stdout.write('\n')

        # Текущее время
        self.stdout.write(
            '{indent}{key} {value}\n'.format(
                indent=' ' * self.indent_width,
                key=self.colorize(
                    '[date] ',
                    fg=key_color,
                    opts=('bold',)
                ),
                value=self.colorize(
                    datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
                    fg='cyan',
                    opts=('bold',)
                )
            )
        )

        # Общее время выполнения
        self.stdout.write(
            '{indent}{key} {value}\n'.format(
                indent=' ' * self.indent_width,
                key=self.colorize(
                    '[execute time] ',
                    fg=key_color,
                    opts=('bold',)
                ),
                value=self.colorize(
                    '{:.0f}ms'.format(self.exec_time),
                    fg='green',
                    opts=('bold',)
                )
            )
        )

        # Общее время SQL
        self.stdout.write(
            '{indent}{key} {value}\n'.format(
                indent=' ' * self.indent_width,
                key=self.colorize(
                    '[sql time] ',
                    fg=key_color,
                    opts=('bold',)
                ),
                value=self.colorize(
                    '{:.0f}ms'.format(self.sql_time),
                    fg='green',
                    opts=('bold',)
                )
            )
        )

        # Кол-во SQL-запросов
        self.stdout.write(
            '{indent}{key} {value}\n'.format(
                indent=' ' * self.indent_width,
                key=self.colorize(
                    '[sql count] ',
                    fg=key_color,
                    opts=('bold',)
                ),
                value=self.colorize(
                    '{:}'.format(self.sql_count),
                    fg='green',
                    opts=('bold',)
                )
            )
        )


def profile(simple=None, **params):
    """
        Декоратор для профилирования функций.

        Пример:
            @profile(sql=True)
            def test(*args, **kwargs):
                ...
    """
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(*args, **kwargs):
            func_fullname = '%s.%s' % (func.__module__, func.__qualname__)
            with Profile(func_fullname, **params):
                result = func(*args, **kwargs)
            return result
        return inner
    return decorator(simple) if simple else decorator
