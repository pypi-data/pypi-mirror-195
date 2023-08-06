from netbox.filtersets import NetBoxModelFilterSet

from netbox_storage.models import StorageConfiguration


class StorageConfigurationFilter(NetBoxModelFilterSet):
    """Filter capabilities for LogicalVolume instances."""

    class Meta:
        model = StorageConfiguration
        fields = [
            "virtual_machine"
        ]

