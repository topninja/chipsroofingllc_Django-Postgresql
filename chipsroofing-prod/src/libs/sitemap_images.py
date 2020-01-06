from django.contrib.sitemaps import GenericSitemap


class SitemapImages(GenericSitemap):
    """
        Sitemap, позволяющий размечать картинки
    """

    def __init__(self, info_dict, priority=None, changefreq=None):
        super().__init__(info_dict, priority, changefreq)
        self.image_location_field = info_dict.get('image_location_field', None)
        self.image_title_field = info_dict.get('image_title_field', None)
        self.image_caption_field = info_dict.get('image_caption_field', None)
        self.image_geo_location_field = info_dict.get('image_geo_location_field', None)
        self.image_license_field = info_dict.get('image_license_field', None)

    def _absolute_url(self, protocol, domain, url):
        return "%s://%s%s" % (protocol, domain, url)

    def _urls(self, page, protocol, domain):
        urls = []
        latest_lastmod = None
        all_items_lastmod = True  # track if all items have a lastmod
        for item in self.paginator.page(page).object_list:
            loc = self._absolute_url(protocol, domain, self._Sitemap__get('location', item))
            priority = self._Sitemap__get('priority', item, None)
            lastmod = self._Sitemap__get('lastmod', item, None)
            if all_items_lastmod:
                all_items_lastmod = lastmod is not None
                if (all_items_lastmod and
                        (latest_lastmod is None or lastmod > latest_lastmod)):
                    latest_lastmod = lastmod
            url_info = {
                'item': item,
                'location': loc,
                'lastmod': lastmod,
                'changefreq': self._Sitemap__get('changefreq', item, None),
                'priority': str(priority if priority is not None else ''),

                'image_location': self._absolute_url(protocol, domain, self._Sitemap__get('image_location', item, None)),
                'image_title': self._Sitemap__get('image_title', item, None),
                'image_caption': self._Sitemap__get('image_caption', item, None),
                'image_geo_location': self._Sitemap__get('image_geo_location', item, None),
                'image_license': self._absolute_url(protocol, domain, self._Sitemap__get('image_license', item, None)),
            }
            urls.append(url_info)
        if all_items_lastmod and latest_lastmod:
            self.latest_lastmod = latest_lastmod
        return urls

    def image_location(self, item):
        if self.image_location_field is not None:
            return getattr(item, self.image_location_field)
        return None

    def image_title(self, item):
        if self.image_title_field is not None:
            return getattr(item, self.image_title_field)
        return None

    def image_caption(self, item):
        if self.image_caption_field is not None:
            return getattr(item, self.image_caption_field)
        return None

    def image_geo_location(self, item):
        if self.image_geo_location_field is not None:
            return getattr(item, self.image_geo_location_field)
        return None

    def image_license(self, item):
        if self.image_license_field is not None:
            return getattr(item, self.image_license_field)
        return None
