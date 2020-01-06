import os
import logging
import inspect
import sqlparse
import traceback
from time import time
from django.conf import settings
from django.db import connections
from django.utils.termcolors import colorize
from django.template import Node, base, debug
from django.db.backends.utils import CursorWrapper
from ..modules import DevServerModule

sql_logger = logging.getLogger('sql')

BASE_PATTERN = settings.BASE_DIR
TEMPLATE_BASE = os.path.abspath(base.__file__)
TEMPLATE_DEBUG = os.path.abspath(debug.__file__)


def get_stack_calls():
    stack = []
    currentframe = inspect.currentframe()
    if currentframe is None:
        return stack

    try:
        stackframes = inspect.getouterframes(currentframe)
    except IndexError:
        # Возможно шаблон Jinja2
        stackframes = traceback.extract_stack()
        for record in stackframes[2:]:
            filename, lineno, funcname, line = record
            if filename.startswith(BASE_PATTERN) and 'devserver' not in filename:
                filename = filename[len(BASE_PATTERN):]
                caller = '%s (func %r, line %s)' % (filename, funcname, lineno)
                stack.append(caller)
    else:
        for record in stackframes[2:]:
            frame, filename, lineno, funcname, lines, index = record
            if filename in (TEMPLATE_BASE, TEMPLATE_DEBUG):
                # Вызов из шаблона
                node = frame.f_locals.get('node') or frame.f_locals.get('self')
                if isinstance(node, Node):
                    loader = node.source[0]
                    offsets = node.source[1]
                    with open(loader.name, newline='') as source:
                        start = source.read(offsets[0])
                        line_num = start.count('\n') + 1
                        token = source.read(offsets[1] - offsets[0])

                    caller = '%s (node %r, line %s)' % (loader.loadname, token, line_num)
                    stack.append(caller)
                    break
            elif filename.startswith(BASE_PATTERN) and 'devserver' not in filename:
                # Вызов из кода
                filename = filename[len(BASE_PATTERN):]
                caller = '%s (func %r, line %s)' % (filename, funcname, lineno)
                stack.append(caller)

    return reversed(stack)


class DevserverCursorWrapper(CursorWrapper):
    def execute(self, sql, params=None):
        start = time()
        try:
            return super().execute(sql, params)
        finally:
            stop = time()
            duration = stop - start
            self.db._devserver_queries.append({
                'sql': self.db.ops.last_executed_query(self.cursor, sql, params),
                'duration': duration * 1000,
                'times': 1,
                'stack': get_stack_calls(),
            })

    def executemany(self, sql, param_list):
        start = time()
        try:
            return super().executemany(sql, param_list)
        finally:
            stop = time()
            duration = stop - start
            try:
                times = len(param_list)
            except TypeError:
                times = '?'

            self.db._devserver_queries.append({
                'sql': sql,
                'duration': duration * 1000,
                'times': times,
                'stack': get_stack_calls(),
            })


class SQLSummaryModule(DevServerModule):
    """
        Вывод длительности всех запросов
    """
    logger_name = 'db'

    def process_request(self, request):
        for connection in connections.all():
            if not hasattr(connection, '_devserver_cursor_old'):
                connection._devserver_queries = []
                connection._devserver_cursor_old = connection.cursor
                connection.cursor = lambda: DevserverCursorWrapper(connection._devserver_cursor_old(), connection)

    def process_response(self, request, response):
        queries = tuple(
            q
            for connection in connections.all()
            for q in connection._devserver_queries
        )
        if not queries:
            super().process_response(request, response)
            return

        # Подсчет суммарной длительности SQL, нахождение запросов-дубликатов
        sql_time = 0
        unique_queries = set()
        duplicated_queries = {}
        for record in queries:
            sql_time += record['duration']

            sql = record['sql'].lower()
            if sql in unique_queries:
                if sql in duplicated_queries:
                    duplicated_queries[sql]['count'] += 1
                else:
                    duplicated_queries[sql] = {
                        'count': 1,
                        'processed': 0,
                    }
            else:
                unique_queries.add(sql)

        sql_logger.debug('-' * 40 + '\n')
        for index, record in enumerate(queries, start=1):
            duplicate_data = duplicated_queries.get(record['sql'].lower())
            if duplicate_data:
                duplicate_data['processed'] += 1

            sql_logger.debug((
                '{serial_header}: {serial}\t{has_duplicates}\n'
                '{sql_header}: {sql}\n'
                '{duration_header}: {duration}\n'
                '{times_header}: {times}\n'
                '{stack_header}:\n{stack}\n'
            ).format(
                serial_header=colorize('Serial', fg='green'),
                serial=index,
                has_duplicates=(
                    colorize(
                        'HAS DUPLICATES (query {index}/{count})!'.format(
                            index=duplicate_data['processed'],
                            count=duplicate_data['count'] + 1,
                        ),
                        fg='red',
                        opts=('bold',)
                    )
                    if duplicate_data else ''
                ),
                sql_header=colorize('SQL', fg='green'),
                sql='\n'.join(
                    '     %s' % line
                    for line in sqlparse.format(record['sql'], reindent=True, keyword_case='upper').split('\n')
                ).strip(),
                duration_header=colorize('Duration', fg='green'),
                duration='%dms' % (record['duration']),
                times_header=colorize('Times', fg='green'),
                times=record['times'],
                stack_header=colorize('Stack', fg='green'),
                stack='\n'.join(
                    '     %s' % colorize(call, fg='cyan')
                    for call in record['stack']
                )
            ))
        sql_logger.debug('-' * 40 + '\n')

        self.logger.info('%(sql_time)s (%(calls)s queries with %(dupes)s duplicates)' % dict(
            sql_time='%dms' % sql_time,
            calls=len(queries),
            dupes=sum(rec['count'] for rec in duplicated_queries.values()),
        ))

        super().process_response(request, response)
