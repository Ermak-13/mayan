from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.classes import Link

from .icons import icon_tool

tools_menu_link = Link(text=_(u'tools'), view='tools_list', icon=icon_tool)
