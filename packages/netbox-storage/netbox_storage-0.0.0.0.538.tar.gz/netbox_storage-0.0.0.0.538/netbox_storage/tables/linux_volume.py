import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
)
from netbox_storage.models import MountedVolume


class MountedVolumeTable(NetBoxTable):

    pk = ToggleColumn()
    fs = tables.Column(
        linkify=True,
        verbose_name="Filesystem"
    )
    partition = tables.Column(
        linkify=True,
        verbose_name="Partition"
    )
    size = tables.Column(
        linkify=True,
        verbose_name="Size"
    )
    path = tables.Column(
        linkify=True,
        verbose_name="Mount Path"
    )

    class Meta(NetBoxTable.Meta):
        model = MountedVolume
        fields = (
            "pk",
            "partition",
            "size",
            "path",
            "fs",
            "description",
        )
        default_columns = (
            "partition",
            "size",
            "path",
            "fs",
            "description",
        )
