from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MembersConfig(AppConfig):
    name = "members"
    verbose_name = _("members")

    def ready(self):
        import members.signals

        self._patch_jazzmin_paginator()

    def _patch_jazzmin_paginator(self):
        """
        Patch jazzmin's paginator for Django 6.0 compatibility.

        Django 6.0 requires format_html() calls to include args/kwargs.
        This patch replaces format_html with mark_safe for pagination.
        Reference: https://github.com/farridav/django-jazzmin/issues/655
        """
        try:
            from django.contrib.admin.views.main import PAGE_VAR
            from django.utils.safestring import mark_safe
            from jazzmin.templatetags import jazzmin as jazzmin_tags

            def patched_jazzmin_paginator_number(cl, i):
                """Patched version using mark_safe instead of format_html."""
                if i == "." or i == "…":
                    html_str = '<li class="page-item disabled"><a class="page-link" href="#">...</a></li>'
                elif i == cl.page_num:
                    html_str = f'<li class="page-item active"><a class="page-link" href="#">{i}</a></li>'
                else:
                    link = cl.get_query_string({PAGE_VAR: i})
                    html_str = f'<li class="page-item"><a class="page-link" href="{link}">{i}</a></li>'

                return mark_safe(html_str)

            # Apply patch
            jazzmin_tags.jazzmin_paginator_number = patched_jazzmin_paginator_number
            jazzmin_tags.register.simple_tag(
                patched_jazzmin_paginator_number, name="jazzmin_paginator_number"
            )

        except ImportError:
            pass  # jazzmin not installed
