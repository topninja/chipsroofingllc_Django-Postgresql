def get_paginator_meta(paginator):
    """
        Получение метаданных из постраничной навигации для SEO.

        <link rel="canonical">
        <link rel="next">,
        <link rel="prev">

        Пример:
            # views.py:
                paginator = Paginator(...)

                seo = Seo()
                seo.set(get_paginator_meta(paginator))
    """
    meta = {
        'canonical': paginator.link_to(paginator.current_page_number, anchor=False),
    }

    if paginator.previous_page_number:
        meta['prev'] = paginator.link_to(paginator.previous_page_number, anchor=False)

    if paginator.next_page_number:
        meta['next'] = paginator.link_to(paginator.next_page_number, anchor=False)

    return meta
