from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.classes import Link


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


link_check_settings = Link(text=_(u'settings'), view='setting_list', condition=is_superuser)#'famfam': 'cog', 'icon': 'cog.png', , 'children_view_regex': [r'^setting_']}
