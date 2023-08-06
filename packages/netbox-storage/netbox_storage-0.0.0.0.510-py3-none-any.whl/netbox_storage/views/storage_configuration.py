from netbox.views import generic

from netbox_storage.filters.storageconfiguration import StorageConfigurationFilter
from netbox_storage.forms import (
    StorageConfigurationFilterForm, StorageConfigurationForm
)

from netbox_storage.models import StorageConfiguration
from netbox_storage.tables import StorageConfigurationTable


class StorageConfigurationListView(generic.ObjectListView):
    queryset = StorageConfiguration.objects.all()
    filterset = StorageConfigurationFilter
    filterset_form = StorageConfigurationFilterForm
    table = StorageConfigurationTable


class StorageConfigurationView(generic.ObjectView):
    """Display PhysicalVolume details"""

    queryset = StorageConfiguration.objects.all()


class StorageConfigurationEditView(generic.ObjectEditView):
    """View for editing a PhysicalVolume instance."""

    queryset = StorageConfiguration.objects.all()
    form = StorageConfigurationForm
    default_return_url = "plugins:netbox_storage:storageconfiguration_list"


class StorageConfigurationDeleteView(generic.ObjectDeleteView):
    queryset = StorageConfiguration.objects.all()
    default_return_url = "plugins:netbox_storage:storageconfiguration_list"
