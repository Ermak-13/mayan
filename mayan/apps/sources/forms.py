from __future__ import absolute_import

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from documents.forms import DocumentForm
from documents.models import DocumentType

from .models import WebForm, StagingFolder, WatchFolder
from .widgets import IconRadioSelect
from .utils import validate_whitelist_blacklist


class StagingDocumentForm(DocumentForm):
    """
    Form that show all the files in the staging folder specified by the
    StagingFile class passed as 'cls' argument
    """
    def __init__(self, *args, **kwargs):
        cls = kwargs.pop('cls')
        show_expand = kwargs.pop('show_expand', False)
        self.source = kwargs.pop('source')
        super(StagingDocumentForm, self).__init__(*args, **kwargs)
        try:
            self.fields['staging_file_id'].choices = [
                (staging_file.id, staging_file) for staging_file in cls.get_all()
            ]
        except:
            pass

        if show_expand:
            self.fields['expand'] = forms.BooleanField(
                label=_(u'Expand compressed files'), required=False,
                help_text=ugettext(u'Upload a compressed file\'s contained files as individual documents')
            )

        # Put staging_list field first in the field order list
        staging_list_index = self.fields.keyOrder.index('staging_file_id')
        staging_list = self.fields.keyOrder.pop(staging_list_index)
        self.fields.keyOrder.insert(0, staging_list)

    staging_file_id = forms.ChoiceField(label=_(u'Staging file'))

    class Meta(DocumentForm.Meta):
        exclude = ('description', 'file', 'document_type', 'tags')


class WebFormForm(DocumentForm):
    file = forms.FileField(label=_(u'File'))

    def __init__(self, *args, **kwargs):
        show_expand = kwargs.pop('show_expand', False)
        self.source = kwargs.pop('source')
        super(WebFormForm, self).__init__(*args, **kwargs)

        if show_expand:
            self.fields['expand'] = forms.BooleanField(
                label=_(u'Expand compressed files'), required=False,
                help_text=ugettext(u'Upload a compressed file\'s contained files as individual documents')
            )

        # Move the file filed to the top
        self.fields.keyOrder.remove('file')
        self.fields.keyOrder.insert(0, 'file')

    def clean_file(self):
        data = self.cleaned_data['file']
        validate_whitelist_blacklist(data.name, self.source.whitelist.split(','), self.source.blacklist.split(','))

        return data


class WebFormSetupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WebFormSetupForm, self).__init__(*args, **kwargs)
        self.fields['icon'].widget = IconRadioSelect(
            attrs=self.fields['icon'].widget.attrs,
            choices=self.fields['icon'].widget.choices,
        )

    class Meta:
        model = WebForm


class StagingFolderSetupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StagingFolderSetupForm, self).__init__(*args, **kwargs)
        self.fields['icon'].widget = IconRadioSelect(
            attrs=self.fields['icon'].widget.attrs,
            choices=self.fields['icon'].widget.choices,
        )

    class Meta:
        model = StagingFolder


class WatchFolderSetupForm(forms.ModelForm):
    class Meta:
        model = WatchFolder


class DocumentTypeSelectForm(forms.Form):
    """
    Form to select the document type of a document to be created, used
    as form #1 in the document creation wizard
    """
    document_type = forms.ModelChoiceField(queryset=DocumentType.objects.all(), label=(u'Document type'), required=False)
