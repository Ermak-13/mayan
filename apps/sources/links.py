from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from documents.permissions import (PERMISSION_DOCUMENT_NEW_VERSION, 
    PERMISSION_DOCUMENT_CREATE)

from .models import (WebForm, StagingFolder, SourceTransformation,
    WatchFolder)
from .permissions import (PERMISSION_SOURCES_SETUP_VIEW,
    PERMISSION_SOURCES_SETUP_EDIT, PERMISSION_SOURCES_SETUP_DELETE,
    PERMISSION_SOURCES_SETUP_CREATE)

staging_file_preview = {'text': _(u'preview'), 'class': 'fancybox-noscaling', 'view': 'staging_file_preview', 'args': ['source.source_type', 'source.pk', 'object.id'], 'famfam': 'zoom', 'permissions': [PERMISSION_DOCUMENT_NEW_VERSION, PERMISSION_DOCUMENT_CREATE]}
staging_file_delete = {'text': _(u'delete'), 'view': 'staging_file_delete', 'args': ['source.source_type', 'source.pk', 'object.id'], 'famfam': 'delete', 'keep_query': True, 'permissions': [PERMISSION_DOCUMENT_NEW_VERSION, PERMISSION_DOCUMENT_CREATE]}

setup_sources = {'text': _(u'sources'), 'view': 'setup_web_form_list', 'famfam': 'application_form', 'icon': 'application_form.png', 'children_classes': [WebForm], 'permissions': [PERMISSION_SOURCES_SETUP_VIEW], 'children_view_regex': [r'setup_web_form', r'setup_staging_folder', r'setup_source_']}
setup_web_form_list = {'text': _(u'web forms'), 'view': 'setup_web_form_list', 'famfam': 'application_form', 'icon': 'application_form.png', 'children_classes': [WebForm], 'permissions': [PERMISSION_SOURCES_SETUP_VIEW]}
setup_staging_folder_list = {'text': _(u'staging folders'), 'view': 'setup_staging_folder_list', 'famfam': 'folder_camera', 'children_classes': [StagingFolder], 'permissions': [PERMISSION_SOURCES_SETUP_VIEW]}
setup_watch_folder_list = {'text': _(u'watch folders'), 'view': 'setup_watch_folder_list', 'famfam': 'folder_magnify', 'children_classes': [WatchFolder], 'permissions': [PERMISSION_SOURCES_SETUP_VIEW]}

setup_source_edit = {'text': _(u'edit'), 'view': 'setup_source_edit', 'args': ['source.source_type', 'source.pk'], 'famfam': 'application_form_edit', 'permissions': [PERMISSION_SOURCES_SETUP_EDIT]}
setup_source_delete = {'text': _(u'delete'), 'view': 'setup_source_delete', 'args': ['source.source_type', 'source.pk'], 'famfam': 'application_form_delete', 'permissions': [PERMISSION_SOURCES_SETUP_DELETE]}
setup_source_create = {'text': _(u'add new source'), 'view': 'setup_source_create', 'args': 'source_type', 'famfam': 'application_form_add', 'permissions': [PERMISSION_SOURCES_SETUP_CREATE]}

setup_source_transformation_list = {'text': _(u'transformations'), 'view': 'setup_source_transformation_list', 'args': ['source.source_type', 'source.pk'], 'famfam': 'shape_move_front', 'permissions': [PERMISSION_SOURCES_SETUP_EDIT]}
setup_source_transformation_create = {'text': _(u'add transformation'), 'view': 'setup_source_transformation_create', 'args': ['source.source_type', 'source.pk'], 'famfam': 'shape_square_add', 'permissions': [PERMISSION_SOURCES_SETUP_EDIT]}
setup_source_transformation_edit = {'text': _(u'edit'), 'view': 'setup_source_transformation_edit', 'args': 'transformation.pk', 'famfam': 'shape_square_edit', 'permissions': [PERMISSION_SOURCES_SETUP_EDIT]}
setup_source_transformation_delete = {'text': _(u'delete'), 'view': 'setup_source_transformation_delete', 'args': 'transformation.pk', 'famfam': 'shape_square_delete', 'permissions': [PERMISSION_SOURCES_SETUP_EDIT]}

source_list = {'text': _(u'Document sources'), 'view': 'setup_web_form_list', 'famfam': 'page_add', 'children_url_regex': [r'sources/setup'], 'permissions': [PERMISSION_SOURCES_SETUP_VIEW]}

upload_version = {'text': _(u'upload new version'), 'view': 'upload_version', 'args': 'object.pk', 'famfam': 'page_add', 'permissions': [PERMISSION_DOCUMENT_NEW_VERSION]}
