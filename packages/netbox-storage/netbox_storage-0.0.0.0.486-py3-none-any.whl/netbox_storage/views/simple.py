from netbox.views import generic

from netbox_storage.forms import LVSimpleForm, LVMSimpleForm
from netbox_storage.models import LinuxVolume, LogicalVolume, Drive


class LVMAddSimpleView(generic.ObjectEditView):
    """View for editing a Drive instance."""

    queryset = Drive.objects.all()
    form = LVMSimpleForm
    default_return_url = "plugins:netbox_storage:drive_list"


class LVAddSimpleView(generic.ObjectEditView):
    """View for editing a Drive instance."""

    queryset = LinuxVolume.objects.all()
    form = LVSimpleForm
    default_return_url = "plugins:netbox_storage:drive_list"


class AddVolume(generic.ObjectEditView):
    """View for editing a Drive instance."""
    template_name = "netbox_storage/inc/volume_add.html"
    queryset = Drive.objects.all()
    form = LVSimpleForm
    default_return_url = "plugins:netbox_storage:drive_list"
