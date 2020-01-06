from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.filters import SimpleListFilter


class HierarchyFilter(SimpleListFilter):
    """
        Фильтр с иерархией (как стандартный фильтр по датам).
    """

    # способ отделения фильтров иерархий от остальных
    hierarchy_filter = True

    # данные параметра для сброса
    empty_name = _('All')

    # значение по умолчанию
    default_value = None

    # шаблон фильтра
    template = 'admin/hierarchy_filter.html'

    def get_branch(self):
        """ Формирование текущего пути в иерархии """
        value = self.value()
        if not value:
            yield {
                'selected': True,
                'display': self.empty_name,
            }
            return

        choices = self.get_branch_choices(value) or ()
        for lookup, title in choices:
            yield {
                'selected': value == force_text(lookup),
                'query_string': '?{}={}'.format(self.parameter_name, lookup),
                'display': title,
            }

    def get_branch_choices(self, value):
        """
            Должен вернуть итератор пар (ключ, имя)
            для формирования пути ссылок к текущему уровню.
        """
        return ()

    def lookups(self, request, model_admin):
        """
            Должен вернуть итератор пар (ключ, имя)
            для формирования ссылок, доступных на текущем уровне.
        """
        return ()

    def value(self):
        value = super().value()
        if value is None and self.default_value is not None:
            return self.default_value
        return value

    def choices(self, cl):
        value = self.value()
        for lookup, title in self.lookup_choices:
            yield {
                'selected': value == force_text(lookup),
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        """
            Фильтрация queryset
        """
        return queryset
