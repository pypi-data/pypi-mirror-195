from netbox.views import generic

from netbox_storage.forms import LVMSimpleForm, VolumeSimpleForm, LinuxVolumeSimpleForm
from netbox_storage.models import Drive, StorageConfigurationLinuxVolume


class LVMAddSimpleView(generic.ObjectEditView):
    """View for editing a Drive instance."""

    queryset = StorageConfigurationLinuxVolume.objects.all()
    form = LVMSimpleForm
    default_return_url = "plugins:netbox_storage:drive_list"


class AddSimpleLinuxVolumeView(generic.ObjectEditView):
    """View for editing a Drive instance."""
    # template_name = "netbox_storage/inc/volume_add.html"
    queryset = StorageConfigurationLinuxVolume.objects.all()
    form = LinuxVolumeSimpleForm
    default_return_url = "plugins:netbox_storage:drive_list"
    # default_return_url = "virtualization:virtualmachine"
