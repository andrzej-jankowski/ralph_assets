# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from ralph_assets.forms_parts import AddPartForm, EditPartForm
from ralph_assets.models import Part
from ralph_assets.views.base import (
    AssetsBase,
    HardwareModeMixin,
    SubmoduleModeMixin,
    get_return_link,
)


class AddPart(HardwareModeMixin, SubmoduleModeMixin, AssetsBase):

    active_sidebar_item = 'add part'
    template_name = 'assets/add_part.html'

    def get_context_data(self, **kwargs):
        ret = super(AddPart, self).get_context_data(**kwargs)
        ret.update({
            'form': self.form,
        })
        return ret

    def get(self, *args, **kwargs):
        self.form = AddPartForm(mode=self.mode)
        return super(AddPart, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.form = AddPartForm(data=self.request.POST, mode=self.mode)
        if self.form.is_valid():
            serial_numbers = self.form.cleaned_data['sn']
            part_data = self.form.cleaned_data
            del part_data['sn']
            for serial_number in serial_numbers:
                Part.objects.create(
                    sn=serial_number,
                    **part_data
                )
            messages.success(self.request, _("Parts saved."))
            return HttpResponseRedirect(
                get_return_link(self.mode)  # todo: go to parts list
            )
        messages.error(self.request, _("Please correct the errors."))
        return super(AddPart, self).get(*args, **kwargs)


class EditPart(HardwareModeMixin, SubmoduleModeMixin, AssetsBase):

    template_name = 'assets/edit_part.html'

    def get_context_data(self, **kwargs):
        ret = super(EditPart, self).get_context_data(**kwargs)
        ret.update({
            'form': self.form,
        })
        return ret

    def get(self, *args, **kwargs):
        self.part = get_object_or_404(
            Part,
            id=kwargs.get('part_id')
        )
        self.form = EditPartForm(instance=self.part, mode=self.mode)
        return super(EditPart, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.part = get_object_or_404(
            Part,
            id=kwargs.get('part_id')
        )
        self.form = EditPartForm(
            data=self.request.POST,
            instance=self.part,
            mode=self.mode,
        )
        if self.form.is_valid():
            self.form.save()
            messages.success(self.request, _("Changes were saved."))
            return HttpResponseRedirect(
                reverse(
                    'part_edit',
                    kwargs={
                        'mode': self.mode,
                        'part_id': self.part.id,
                    },
                )
            )
        messages.error(self.request, _("Please correct the errors."))
        return super(EditPart, self).get(*args, **kwargs)
