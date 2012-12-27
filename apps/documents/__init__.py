from __future__ import absolute_import

import tempfile

from django.utils.translation import ugettext_lazy as _

from common.utils import validate_path, encapsulate
from navigation.api import (register_links, register_top_menu,
    register_model_list_columns, register_multi_item_links,
    register_sidebar_template)
from main.api import register_diagnostic, register_maintenance_links
from history.api import register_history_type
from history.permissions import PERMISSION_HISTORY_VIEW
from project_setup.api import register_setup
from acls.api import class_permissions

from .models import (Document, DocumentPage,
    DocumentPageTransformation, DocumentType, DocumentTypeFilename,
    DocumentVersion)
from .permissions import (PERMISSION_DOCUMENT_CREATE,
    PERMISSION_DOCUMENT_PROPERTIES_EDIT, PERMISSION_DOCUMENT_VIEW,
    PERMISSION_DOCUMENT_DELETE, PERMISSION_DOCUMENT_DOWNLOAD,
    PERMISSION_DOCUMENT_TRANSFORM, PERMISSION_DOCUMENT_TOOLS,
    PERMISSION_DOCUMENT_EDIT, PERMISSION_DOCUMENT_VERSION_REVERT,
    PERMISSION_DOCUMENT_TYPE_EDIT, PERMISSION_DOCUMENT_TYPE_DELETE,
    PERMISSION_DOCUMENT_TYPE_CREATE, PERMISSION_DOCUMENT_TYPE_VIEW,
    PERMISSION_DOCUMENT_NEW_VERSION)
from .events import (HISTORY_DOCUMENT_CREATED,
    HISTORY_DOCUMENT_EDITED, HISTORY_DOCUMENT_DELETED)
from .conf import settings as document_settings
from .widgets import document_thumbnail
from .links import (document_list, document_list_recent, document_create_multiple,
    document_create_siblings, document_view_simple, document_view_advanced,
    document_delete, document_multiple_delete, document_edit, document_preview,
    document_download, document_multiple_download, document_version_download,
    document_find_duplicates, document_find_all_duplicates, document_update_page_count,
    document_clear_transformations, document_multiple_clear_transformations,
    document_print, document_history_view, document_missing_list, document_clear_image_cache,
    document_page_transformation_list, document_page_transformation_create, document_page_transformation_edit,
    document_page_transformation_delete, document_page_view, document_page_text,
    document_page_edit, document_page_navigation_next, document_page_navigation_previous,
    document_page_navigation_first, document_page_navigation_last, document_page_zoom_in,
    document_page_zoom_out, document_page_rotate_right, document_page_rotate_left,
    document_page_view_reset, document_version_list, document_version_revert,
    document_type_list, document_type_setup, document_type_document_list,
    document_type_edit, document_type_delete, document_type_create, 
    document_type_filename_list, document_type_filename_create, document_type_filename_edit,
    document_type_filename_delete)

# History setup
register_history_type(HISTORY_DOCUMENT_CREATED)
register_history_type(HISTORY_DOCUMENT_EDITED)
register_history_type(HISTORY_DOCUMENT_DELETED)

# Register document type links
register_links(DocumentType, [document_type_edit, document_type_delete, document_type_document_list, document_type_filename_list])
register_links(DocumentTypeFilename, [document_type_filename_edit, document_type_filename_delete])

register_links(['setup_document_type_metadata', 'document_type_filename_delete', 'document_type_create', 'document_type_filename_create', 'document_type_filename_edit', 'document_type_filename_list', 'document_type_list', 'document_type_document_list', 'document_type_edit', 'document_type_delete'], [document_type_list, document_type_create], menu_name='secondary_menu')
register_links([DocumentTypeFilename, 'document_type_filename_list', 'document_type_filename_create'], [document_type_filename_create], menu_name='sidebar')

# Register document links
register_links(Document, [document_view_simple, document_edit, document_print, document_delete, document_download, document_find_duplicates, document_clear_transformations, document_create_siblings])
register_multi_item_links(['document_find_duplicates', 'folder_view', 'index_instance_node_view', 'document_type_document_list', 'search', 'results', 'document_group_view', 'document_list', 'document_list_recent', 'tag_tagged_item_list'], [document_multiple_clear_transformations, document_multiple_delete, document_multiple_download])

# Document Version links
register_links(DocumentVersion, [document_version_revert, document_version_download])

secondary_menu_links = [document_list_recent, document_list, document_create_multiple]

register_links(['document_list_recent', 'document_list', 'document_create', 'document_create_multiple', 'upload_interactive', 'staging_file_delete'], secondary_menu_links, menu_name='secondary_menu')
register_links(Document, secondary_menu_links, menu_name='secondary_menu')

# Document page links
register_links(DocumentPage, [
    document_page_transformation_list, document_page_view,
    document_page_text, document_page_edit,
])

# Document page navigation links
register_links(DocumentPage, [
    document_page_navigation_first, document_page_navigation_previous,
    document_page_navigation_next, document_page_navigation_last
], menu_name='related')

register_links(['document_page_view'], [document_page_rotate_left, document_page_rotate_right, document_page_zoom_in, document_page_zoom_out, document_page_view_reset], menu_name='form_header')

register_links(DocumentPageTransformation, [document_page_transformation_edit, document_page_transformation_delete])
register_links('document_page_transformation_list', [document_page_transformation_create], menu_name='sidebar')
register_links('document_page_transformation_create', [document_page_transformation_create], menu_name='sidebar')
register_links(['document_page_transformation_edit', 'document_page_transformation_delete'], [document_page_transformation_create], menu_name='sidebar')

register_diagnostic('documents', _(u'Documents'), document_missing_list)

register_maintenance_links([document_find_all_duplicates, document_update_page_count, document_clear_image_cache], namespace='documents', title=_(u'documents'))

register_model_list_columns(Document, [
        {'name':_(u'thumbnail'), 'attribute':
            encapsulate(lambda x: document_thumbnail(x))
        },
    ])

register_top_menu(
    'documents',
    link={'famfam': 'page', 'text': _(u'documents'), 'view': 'document_list_recent'},
    children_path_regex=[
        r'^documents/[^t]', r'^metadata/[^s]', r'comments', r'tags/document', r'grouping/[^s]', r'history/list/for_object/documents',
    ],
    children_view_regex=[r'document_acl', r'smart_link_instance'],
    children_views=['document_folder_list', 'folder_add_document', 'document_index_list', 'upload_version', ],
    position=1
)

register_sidebar_template(['document_list_recent'], 'recent_document_list_help.html')
register_sidebar_template(['document_type_list'], 'document_types_help.html')

register_links(Document, [document_view_simple], menu_name='form_header', position=0)
register_links(Document, [document_view_advanced], menu_name='form_header', position=1)
register_links(Document, [document_history_view], menu_name='form_header')
register_links(Document, [document_version_list], menu_name='form_header')

if (validate_path(document_settings.CACHE_PATH) == False) or (not document_settings.CACHE_PATH):
    setattr(document_settings, 'CACHE_PATH', tempfile.mkdtemp())

register_setup(document_type_setup)

class_permissions(Document, [
    PERMISSION_DOCUMENT_PROPERTIES_EDIT,
    PERMISSION_DOCUMENT_EDIT,
    PERMISSION_DOCUMENT_VIEW,
    PERMISSION_DOCUMENT_DELETE,
    PERMISSION_DOCUMENT_DOWNLOAD,
    PERMISSION_DOCUMENT_TRANSFORM,
    PERMISSION_DOCUMENT_NEW_VERSION,
    PERMISSION_DOCUMENT_VERSION_REVERT,
    PERMISSION_HISTORY_VIEW
])
