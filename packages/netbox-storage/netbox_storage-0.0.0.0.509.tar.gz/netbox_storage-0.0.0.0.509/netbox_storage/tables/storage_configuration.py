from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
)

from netbox_storage.models import StorageConfiguration


class StorageConfigurationTable(NetBoxTable):
    pk = ToggleColumn()

    class Meta(NetBoxTable.Meta):
        model = StorageConfiguration
        fields = (
            "pk",
        )
        default_columns = (
            "pk",
        )
