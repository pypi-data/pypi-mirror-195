from netbox.views import generic

from netbox_storage.forms import LVMSimpleForm, VolumeSimpleForm
from netbox_storage.models import Drive, StorageConfiguration


class LVMAddSimpleView(generic.ObjectEditView):
    """View for editing a Drive instance."""

    queryset = StorageConfiguration.objects.all()
    form = LVMSimpleForm
    default_return_url = "plugins:netbox_storage:drive_list"


class AddVolume(generic.ObjectEditView):
    """View for editing a Drive instance."""
    template_name = "netbox_storage/inc/volume_add.html"
    queryset = Drive.objects.all()
    form = VolumeSimpleForm
    default_return_url = "plugins:netbox_storage:drive_list"
    # default_return_url = "virtualization:virtualmachine"
