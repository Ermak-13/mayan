from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _


def has_usable_password(context):
    return context['request'].user.has_usable_password


password_change_view = {'text': _(u'change password'), 'view': 'password_change_view', 'famfam': 'computer_key', 'condition': has_usable_password}
current_user_details = {'text': _(u'user details'), 'view': 'current_user_details', 'famfam': 'vcard'}
current_user_edit = {'text': _(u'edit details'), 'view': 'current_user_edit', 'famfam': 'vcard_edit'}
about_view = {'text': _('about'), 'view': 'about_view', 'famfam': 'information'}
license_view = {'text': _('license'), 'view': 'license_view', 'famfam': 'script'}
