from pipeline.compressors import CompressorBase
from csscompressor import compress


class CSSCompressor(CompressorBase):
    @staticmethod
    def compress_css(css):
        return compress(css)

