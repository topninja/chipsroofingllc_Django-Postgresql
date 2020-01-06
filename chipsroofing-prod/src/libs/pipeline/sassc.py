import re
import os
import time
import subprocess
from django.utils.encoding import smart_bytes
from django.conf import settings as django_settings
from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler
from pipeline.exceptions import CompilerError

cached_imports = {}
re_import = re.compile('@import\s+[\'"]([^\'"]+)')


class SASSCMetaclass(type):
    def __init__(cls, what, bases=None, attrs=None):
        super().__init__(what, bases, attrs)
        cls.start = time.time()


class SASSCCompiler(SubProcessCompiler, metaclass=SASSCMetaclass):
    """
        Класс для компилирования JS и CSS через sassc.
        В settings.py необходимо добавить:
            SASS_INCLUDE_DIR = BASE_DIR + '/static/scss/'
            PIPELINE['SASS_BINARY'] = '/usr/bin/env sassc --load-path ' + SASS_INCLUDE_DIR
            PIPELINE['SASS_ARGUMENTS'] = '-t nested'
            PIPELINE['COMPILERS'] = (
                'libs.sassc.SASSCCompiler',
            )
            STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
    """
    start = None
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith('.scss')

    def execute_command(self, command, content=None, cwd=None):
        pipe = subprocess.Popen(command, shell=True, cwd=cwd,
                                stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if content:
            content = smart_bytes(content)
        stdout, stderr = pipe.communicate(content)

        if isinstance(stderr, bytes):
            try:
                stderr = stderr.decode()
            except UnicodeDecodeError:
                pass

        if stderr.strip():
            raise CompilerError(stderr, error_output=stderr)

        if self.verbose:
            print(stderr)

        if pipe.returncode != 0:
            msg = "Command '{0}' returned non-zero exit status {1}".format(command, pipe.returncode)
            raise CompilerError(msg, error_output=msg)

        return stdout

    def find_import_file(self, base_dir, import_name):
        if not import_name.endswith('scss'):
            import_name += '.scss'

        scss_dir, scss_file = os.path.split(import_name)

        # Find import files
        imports_lookup = (
            os.path.join(base_dir, import_name),
            os.path.join(base_dir, scss_dir, '_' + scss_file),
            os.path.join(django_settings.SASS_INCLUDE_DIR, import_name),
            os.path.join(django_settings.SASS_INCLUDE_DIR, scss_dir, '_' + scss_file),
        )

        for path in imports_lookup:
            if os.path.exists(path):
                return path
        else:
            print('WARNING: not found SCSS import "%s"' % import_name)

    def get_scss_modified(self, infile):
        infile_dir = os.path.dirname(infile)
        infile_modified = [os.stat(infile).st_mtime]

        # Read imports
        with open(infile, 'r') as fp:
            buffer = fp.read(1024)

        imports = re_import.findall(buffer)
        for import_name in imports:
            import_path = self.find_import_file(infile_dir, import_name)
            if not import_path:
                break

            # Get imported file modify time
            if import_path in cached_imports:
                infile_modified.append(cached_imports[import_path])
            else:
                cached_imports[import_path] = self.get_scss_modified(import_path)
                infile_modified.append(cached_imports[import_path])

        return max(infile_modified)

    def compile_file(self, infile, outfile, outdated=False, force=False):
        if os.path.isfile(outfile):
            # Уже есть скомпиленный файл. Проверяем его свежесть
            infile_modified = self.get_scss_modified(infile)
            outfile_modified = os.stat(outfile).st_mtime
            if outfile_modified > infile_modified:
                return

        command = "%s %s %s" % (
            ' '.join(settings.SASS_BINARY),
            ' '.join(settings.SASS_ARGUMENTS),
            infile
        )
        try:
            output = self.execute_command(command, cwd=os.path.dirname(infile))
        except CompilerError:
            print('CompilerError at file: %s' % infile)
            raise
        else:
            output = output.decode('utf-8-sig')
            with open(outfile, 'w+', encoding='utf-8') as f:
                f.write(output)
