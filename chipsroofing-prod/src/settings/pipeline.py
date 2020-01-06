from ._pipeline import PIPELINE, Slider

PIPELINE['STYLESHEETS'].update({
    'critical': {
        'source_filenames': (
            'scss/grid.scss',
            'scss/layout.scss',
            'scss/buttons.scss',

            'header/scss/header.scss',
            'menu/scss/main_menu.scss',
            'breadcrumbs/scss/breadcrumbs.scss',
        ),
        'output_filename': 'css_build/critical.css',
    },
    'core': {
        'source_filenames': (
            'scss/forms.scss',
            'scss/preloader.scss',
            'scss/text_styles.scss',

            'scss/popups/popups.scss',
            'scss/popups/preloader.scss',

            'contacts/scss/block.scss',
            'blocks/scss/estimate.scss',
            'blocks/scss/partners.scss',
            'testimonials/scss/block.scss',
            'examples/scss/block.scss',
            'faq/scss/block.scss',
            'services/scss/block.scss',
            'blog/scss/block.scss',
            'footer/scss/footer.scss',
            'css/magnific-popup.css',
            'css/swiper.css',
            'social_networks/scss/social_links.scss',
            'rating/scss/rating.scss',
            'blocks/scss/videos.scss',

        ),
        'output_filename': 'css_build/head_core.css',
    },
    'error': {
        'source_filenames': (
            'scss/error_page.scss',
        ),
        'output_filename': 'css_build/error.css',
    },
    'fonts': {
        'source_filenames': (
            'fonts/Montserrat-Regular/stylesheet.css',
            'fonts/Montserrat-Bold/stylesheet.css',
            'fonts/Montserrat-Italic/stylesheet.css',
        ),
        'output_filename': 'css_build/fonts.css',
    },
    'main': {
        'source_filenames': (
            'css/animate.css',
            'main/scss/index.scss',
        ),
        'output_filename': 'css_build/main.css',
    },
    'std_page_critical': {
        'source_filenames': (
            'std_page/scss/critical.scss',
        ),
        'output_filename': 'css_build/std_page_critical.css',
    },
    'std_page': {
        'source_filenames': (
            'std_page/scss/std_page.scss',
            'std_page/scss/slides.scss',
        ),
        'output_filename': 'css_build/std_page.css',
    },
    'contacts': {
        'source_filenames': (
            'google_maps/scss/label.scss',
            'contacts/scss/index.scss',
        ),
        'output_filename': 'css_build/contacts.css',
    },
    'examples': {
        'source_filenames': (
            'examples/scss/index.scss',
        ),
        'output_filename': 'css_build/examples.css',
    },
    'about': {
        'source_filenames': (
            'about/scss/index.scss',
        ),
        'output_filename': 'css_build/about.css',
    },
    'testimonials': {
        'source_filenames': (
            'testimonials/scss/index.scss',
        ),
        'output_filename': 'css_build/testimonials.css',
    },
    'faq': {
        'source_filenames': (
            'faq/scss/index.scss',
        ),
        'output_filename': 'css_build/faq.css',
    },
    'faq_detail': {
        'source_filenames': (
            'faq/scss/detail.scss',
        ),
        'output_filename': 'css_build/faq_detail.css',
    },
    'services': {
        'source_filenames': (
            'services/scss/index.scss',
        ),
        'output_filename': 'css_build/services.css',
    },
    'service': {
        'source_filenames': Slider.css + (
            'services/scss/detail.scss',
        ),
        'output_filename': 'css_build/service.css',
    },
    'blog': {
        'source_filenames': (
            'blog/scss/index.scss',
        ),
        'output_filename': 'css_build/blog.css',
    },
    'blog_detail':  {
        'source_filenames': Slider.css + (
            'css/likely.css',
            'blog/scss/detail.scss',
        ),
        'output_filename': 'css_build/blog_detail.css',
    },

})

PIPELINE['JAVASCRIPT'].update({
    'core': {
        'source_filenames': (
            'polyfills/modernizr.js',
            'js/jquery-2.2.4.js',
            'js/jquery-ui.js',
            'js/jquery.requestanimationframe.js',

            'common/js/jquery.cookie.js',
            'common/js/jquery.utils.js',
            'common/js/jquery.ajax_csrf.js',

            'js/popups/jquery.popups.js',
            'js/popups/preloader.js',
            'js/jquery.inspectors.js',
            'js/jquery.scrollTo.js',
            'js/jquery.fitvids.js',
            'js/text_styles.js',
            'js/swiper.js',
            'js/preloader.js',
            'blocks/js/partners.js',
            'blocks/js/estimate.js',
            'blocks/js/videos.js',
            'blog/js/block.js',
            'examples/js/block.js',
            'testimonials/js/block.js',

            'attachable_blocks/js/async_blocks.js',
            'placeholder/js/placeholder.js',
            'contacts/js/popups.js',
            'menu/js/main_menu.js',

            'js/jquery.magnific-popup.min.js',
            'rating/js/rating.js',
        ),
        'output_filename': 'js_build/core.js',
    },
    'main': {
        'source_filenames': (
            'js/wow.js',
            'main/js/index.js',
            'main/js/popup.js',
        ),
        'output_filename': 'js_build/main.js',
    },
    'std_page': {
        'source_filenames': (
            'std_page/js/std_page.js',
        ),
        'output_filename': 'js_build/std_page.js',
    },
    'services': {
        'source_filenames': Slider.js + (
            'services/js/index.js',
        ),
        'output_filename': 'js_build/services.js',
    },
    'service': {
        'source_filenames': Slider.js + (
            'services/js/detail.js',
        ),
        'output_filename': 'js_build/service.js',
    },
    'contacts': {
        'source_filenames': (
            'google_maps/js/core.js',
            'contacts/js/index.js',
        ),
        'output_filename': 'js_build/contacts.js',
    },
    'blog': {
        'source_filenames': (
            'blog/js/index.js',
        ),
        'output_filename': 'js_build/blog.js',
    },
    'blog_detail': {
        'source_filenames': Slider.js + (
            'js/likely.js',
            'blog/scss/detail.js',
        ),
        'output_filename': 'css_build/blog_detail.js',
    },
    'about': {
        'source_filenames': (
            'about/js/index.js',
        ),
        'output_filename': 'js_build/about.js',
    },
    'examples': {
        'source_filenames': (
            'examples/js/index.js',
        ),
        'output_filename': 'js_build/examples.js',
    },

})
