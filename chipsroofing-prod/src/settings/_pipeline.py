from collections import namedtuple

# ===============================
#   Наборы скриптов с зависимостями.
#
#   Пример использования:
#       'some_page': {
#           'source_filenames': PopupGallery.css + (
#           ...
#           ),
#           ...
#       }
# ===============================

# Слайдер
Slider = namedtuple('Slider', ['css', 'js'])(
    css=(
        'scss/slider/slider.scss',
        'scss/slider/section_slider.scss',
        'scss/slider/plugins/controls.scss',
        'scss/slider/plugins/navigation.scss',
    ),
    js=(
        'js/drager.js',
        'js/slider/slider.js',
        'js/slider/plugins/side_animation.js',
        'js/slider/plugins/fade_animation.js',
        'js/slider/plugins/autoscroll.js',
        'js/slider/plugins/navigation.js',
        'js/slider/plugins/controls.js',
        'js/slider/plugins/drag.js',
    )
)

# Галерея во всплывающем окне
PopupGallery = namedtuple('PopupGallery', ['css', 'js'])(
    css=Slider.css + (
        'gallery/scss/gallery_popup.scss',
    ),
    js=(
        'js/jquery.youtube.js',
        'js/jquery.vimeo.js',
    ) + Slider.js + (
        'gallery/js/gallery_popup.js',
    )
)


PIPELINE = {
    'PIPELINE_ENABLED': True,
    'COMPILERS': (
        'libs.pipeline.sassc.SASSCCompiler',
    ),
    'SASS_ARGUMENTS': '-t compressed',
    'CSS_COMPRESSOR': 'libs.pipeline.cssmin.CSSCompressor',
    'JS_COMPRESSOR': 'pipeline.compressors.jsmin.JSMinCompressor',

    'STYLESHEETS': {
        'admin_customize': {
            'source_filenames': (
                'admin/css/jquery-ui/jquery-ui.min.css',
                'admin/scss/admin_fixes.scss',
                'admin/scss/admin_table.scss',
                'admin/scss/dl_core.scss',
                'admin/scss/dl_login.scss',
                'admin/scss/hierarchy_filter.scss',
            ),
            'output_filename': 'admin/css/customize.css',
        },
    },

    'JAVASCRIPT': {
        'admin_customize': {
            'source_filenames': (
                'admin/js/jquery-ui.min.js',
                'common/js/jquery.cookie.js',
                'common/js/jquery.ajax_csrf.js',
                'common/js/jquery.mousewheel.js',
                'common/js/jquery.utils.js',
                'common/js/file_dropper.js',
            ),
            'output_filename': 'admin/js/customize.js',
        },
    }
}
