from __future__ import absolute_import

import logging

from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.db.models.signals import post_save, post_syncdb
from django.dispatch import receiver
from django.db.utils import DatabaseError

from navigation.api import bind_links, register_multi_item_links
from documents.models import Document, DocumentVersion
from maintenance.api import MaintenanceNamespace
from project_tools.api import register_tool
from acls.api import class_permissions

from scheduler.api import register_interval_job

from .conf.settings import (AUTOMATIC_OCR, QUEUE_PROCESSING_INTERVAL)
from .models import DocumentQueue, QueueTransformation
from .tasks import task_process_document_queues
from .permissions import (PERMISSION_OCR_DOCUMENT,
    PERMISSION_OCR_DOCUMENT_DELETE, PERMISSION_OCR_QUEUE_ENABLE_DISABLE,
    PERMISSION_OCR_CLEAN_ALL_PAGES)
from .exceptions import AlreadyQueued
from . import models as ocr_models
from .links import (submit_document, submit_document_multiple, re_queue_document,
    re_queue_multiple_document, queue_document_delete, queue_document_multiple_delete,
    document_queue_disable, document_queue_enable, all_document_ocr_cleanup,
    queue_document_list, ocr_tool_link, setup_queue_transformation_list,
    setup_queue_transformation_create, setup_queue_transformation_edit,
    setup_queue_transformation_delete)

logger = logging.getLogger(__name__)

bind_links([Document], [submit_document])
register_multi_item_links(['document_find_duplicates', 'folder_view', 'index_instance_node_view', 'document_type_document_list', 'search', 'results', 'document_group_view', 'document_list', 'document_list_recent', 'tag_tagged_item_list'], [submit_document_multiple])

bind_links([DocumentQueue], [document_queue_disable, document_queue_enable, setup_queue_transformation_list])
bind_links([QueueTransformation], [setup_queue_transformation_edit, setup_queue_transformation_delete])

register_multi_item_links(['queue_document_list'], [re_queue_multiple_document, queue_document_multiple_delete])

bind_links(['setup_queue_transformation_create', 'setup_queue_transformation_edit', 'setup_queue_transformation_delete', 'document_queue_disable', 'document_queue_enable', 'queue_document_list', 'setup_queue_transformation_list'], [queue_document_list], menu_name='secondary_menu')
bind_links(['setup_queue_transformation_edit', 'setup_queue_transformation_delete', 'setup_queue_transformation_list', 'setup_queue_transformation_create'], [setup_queue_transformation_create], menu_name='sidebar')

namespace = MaintenanceNamespace(_(u'OCR'))
namespace.create_tool(all_document_ocr_cleanup)


@transaction.commit_on_success
def create_default_queue():
    try:
        default_queue, created = DocumentQueue.objects.get_or_create(name='default')
    except DatabaseError:
        transaction.rollback()
    else:
        if created:
            default_queue.label = ugettext(u'Default')
            default_queue.save()


@receiver(post_save, dispatch_uid='document_post_save', sender=DocumentVersion)
def document_post_save(sender, instance, **kwargs):
    logger.debug('received post save signal')
    logger.debug('instance: %s' % instance)
    if kwargs.get('created', False):
        if AUTOMATIC_OCR:
            try:
                DocumentQueue.objects.queue_document(instance.document)
            except AlreadyQueued:
                pass

# Disabled because it appears Django execute signals using the same
# process of the signal emiter effectively blocking the view until
# the OCR process completes which could take several minutes :/
#@receiver(post_save, dispatch_uid='call_queue', sender=QueueDocument)
#def call_queue(sender, **kwargs):
#    if kwargs.get('created', False):
#        logger.debug('got call_queue signal: %s' % kwargs)
#        task_process_document_queues()

@receiver(post_syncdb, dispatch_uid='create_default_queue', sender=ocr_models)
def create_default_queue_signal_handler(sender, **kwargs):
    create_default_queue()

register_interval_job('task_process_document_queues', _(u'Checks the OCR queue for pending documents.'), task_process_document_queues, seconds=QUEUE_PROCESSING_INTERVAL)

register_tool(ocr_tool_link)

class_permissions(Document, [
    PERMISSION_OCR_DOCUMENT,
])
