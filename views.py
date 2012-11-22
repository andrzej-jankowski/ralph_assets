#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from lck.django.common import nested_commit_on_success
from ralph.assets.forms import AddDeviceAssetForm
from ralph.assets.models import DeviceInfo
from ralph.ui.views.common import Base


class Index(Base):
    template_name = 'assets/base.html'


class AddDeviceAssets(Base):
    template_name = 'assets/add_device_assets.html'

    def get_context_data(self, **kwargs):
        ret = super(AddDeviceAssets, self).get_context_data(**kwargs)
        ret.update({
            'form': self.form,
            'form_id': 'add_device_asset_form'
        })
        return ret

    def get(self, *args, **kwargs):
        self.form = AddDeviceAssetForm()
        return super(AddDeviceAssets, self).get(*args, **kwargs)

    @nested_commit_on_success
    def post(self, *args, **kwargs):
        self.form = AddDeviceAssetForm(self.request.POST)
        if self.form.is_valid():
            data = {}
            for field_name, field_value in self.form.cleanded_data.items():
                if field_name != "barcode":
                    data[field_name] = field_value
            barcodes = self.form.cleaned_data['barcode']
            if barcodes.find(",") > 0:
                barcodes = filter(len, barcodes.split(","))
            else:
                barcodes = filter(len, barcodes.split("\n"))
            for barcode in barcodes:
                DeviceInfo.objects.create(barcode=barcode, **data)
                messages.success(self.request, _("Assets saved."))
        else:
            messages.error(self.request, _("Please correct the errors."))
        return super(AddDeviceAssets, self).get(*args, **kwargs)


