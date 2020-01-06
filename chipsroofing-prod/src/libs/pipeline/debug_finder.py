from django.conf import settings
from pipeline.finders import PipelineFinder as DefaultPipelineFinder


class PipelineFinder(DefaultPipelineFinder):
    """
        Включаем поиск статики при DEBUG=True
    """
    def find(self, *args, **kwargs):
        if settings.DEBUG or not settings.PIPELINE_ENABLED:
            return super(DefaultPipelineFinder, self).find(*args, **kwargs)
        else:
            return []
