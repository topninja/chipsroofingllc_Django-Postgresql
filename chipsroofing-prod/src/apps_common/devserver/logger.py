import io
import re
import logging
import threading
from django.utils.termcolors import colorize


class ThreadedConsoleHandler(logging.StreamHandler):
    buffers = {}
    bash_colors = re.compile(r'\x1b\[[^m]*m')

    @property
    def buffer(self):
        key = threading.get_ident()
        return self.buffers.setdefault(key, io.StringIO())

    @property
    def buffer_data(self):
        key = threading.get_ident()
        buffer = self.buffers.get(key)
        if buffer is None:
            return ''

        buffer.seek(0)
        buffered_data = buffer.read()
        buffer.close()
        del self.buffers[key]
        return buffered_data

    def format(self, record):
        # Форматируем префикс
        prefix = record.prefix.format(**record.__dict__)

        # Форматируем сообщение по шаблону
        message = super().format(record)

        if record.multiline_indent:
            clean_prefix = self.bash_colors.sub('', prefix)
            multiline_indent = record.indent + ' ' * len(clean_prefix)
        else:
            multiline_indent = record.indent

        new_message = []
        first = True
        for line in message.split('\n'):
            if first:
                new_message.append(line)
                first = False
            else:
                new_message.append('%s%s' % (multiline_indent, line))

        return record.indent + prefix + '\n'.join(new_message)

    def emit(self, record):
        try:
            msg = self.format(record)
            buffer = self.buffer
            buffer.write(msg)
            buffer.write(self.terminator)
        except Exception:
            self.handleError(record)

    def flush(self):
        self.acquire()
        try:
            data = self.buffer_data
            if data:
                self.stream.write(data)

            if self.stream and hasattr(self.stream, "flush"):
                self.stream.flush()
        finally:
            self.release()


class ThreadedConsoleLogger(logging.Logger):
    """ Логгер, накапливающий выводимые сообщения в буффер, а затем выводящий результат в консоль """
    def flush(self):
        for handler in self.handlers:
            handler.flush()

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, **kwargs):
        indent = kwargs.pop('indent', '    ')
        name = kwargs.pop('name', self.name)

        prefix = colorize('[{}] '.format(name), fg='green', opts=('bold', ))
        duration = kwargs.pop('duration', None)
        if duration:
            prefix += colorize('(%dms) ' % duration, fg='white')

        defaults = {
            'indent': indent,
            'prefix': prefix,
            'multiline_indent': True,
        }
        defaults.update(kwargs)
        defaults.update(extra or {})
        super()._log(level, msg, args, exc_info, defaults, stack_info)
