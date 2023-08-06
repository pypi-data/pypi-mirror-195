from django.core.validators import MinValueValidator
from django.forms import (
    CharField,
    FloatField,
)
from django.urls import reverse_lazy

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)
from utilities.forms import (
    CSVModelChoiceField,
    DynamicModelChoiceField, APISelect,
)

from netbox_storage.models import Drive, Filesystem, Partition, PhysicalVolume, VolumeGroup, LogicalVolume
from virtualization.models import Cluster, ClusterType, VirtualMachine
import logging


class LVMSimpleForm(NetBoxModelForm):
    """Form for creating a new Drive object."""
    # ct = ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
    lv_name = CharField(
        label="LV Name",
        help_text="Logical Volume Name e.g. lv_docker",
    )
    vg_name = CharField(
        label="VG Name",
        help_text="Volume Group Name e.g. vg_docker",
    )
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the logical volume e.g. 25",
        validators=[MinValueValidator(0.1)],
    )
    path = CharField(
        label="Path",
        help_text="The mounted path of the volume e.g. /var/lib/docker",
    )
    fs = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        label="Filesystem Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:filesystem-list")}
        ),
        help_text="The Filesystem of the Volume e.g. ext4",
    )
    cluster_type = DynamicModelChoiceField(
        queryset=ClusterType.objects.all(),
        help_text="The Cluster Type of the drive",
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        query_params={
            'type_id': '$cluster_type'  # ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
        },
        help_text="The Storage Cluster of the drive",
    )
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        help_text="Mapping between drive and virtual machine  e.g. vm-testinstall-01",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Hard Drive 1 on SSD Cluster",
    )

    fieldsets = (
        (
            "Drive Cluster Config",
            (
                "cluster_type",
                "cluster",
                "virtual_machine",
            ),
        ),
        (
            "LVM Configuration",
            (
                "lv_name",
                "vg_name",
                "size",
                "path",
                "fs",
                "description",
            ),
        ),
    )

    class Meta:
        model = Drive
        exclude = (
                    "cluster_type",
                    "vg_name",
                    "path",
                    "fs",
                    "description",
        )
        fields = [
            "cluster",
            "virtual_machine",
            "size",
        ]

    def save(self, *args, **kwargs):
        drive = super().save(*args, **kwargs)
        logger = logging.getLogger('netbox.plugins.netbox_storage')

        logger.warning(f'{self.instance}')
        logger.warning(f'{self.instance.lv_name}')
        logger.warning(f'{self.instance.vg_name}')
        logger.warning(f'{self.instance.path}')
        logger.warning(f'{self.instance.fs}')
        logger.warning(f'{self.instance.size}')
        logger.warning(f'{self.instance.virtual_machine}')

        # logger.warning(f'--------- Instance: {instance}')
        # logger.warning(f'--------- Instance: {instance.pk}')
        # partition = Partition(drive=instance, device=instance.device_name, size=instance.size, type="Linux LVM")
        # partition.save()
        # logger.warning(f'{partition}')
        # vg = VolumeGroup(vg_name=self.vg_name)
        # vg.save()
        # logger.warning(f'{vg}')
        # physicalvolume = PhysicalVolume(partition=partition, pv_name=instance.device_name, vg=vg)
        """physicalvolume.save()
        logger.warning(f'{physicalvolume}')
        logicalvolume = LogicalVolume(vg=vg, size=self.size, path=self.path, fs=self.fs)
        logger.warning(f'{logicalvolume}')
        logicalvolume.save()"""

        return drive


class VolumeSimpleForm(NetBoxModelForm):
    """Form for creating a new Drive object."""
    # ct = ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the logical volume e.g. 25",
        validators=[MinValueValidator(0.1)],
        required=False
    )
    lv_name = CharField(
        label="LV Name",
        help_text="The logical volume name e.g. lv_data",
        required=False
    )
    vg_name = CharField(
        label="VG Name",
        help_text="The volume group name e.g. vg_data",
        required=False
    )
    path = CharField(
        label="Path",
        help_text="The mounted path of the volume e.g. /var/lib/docker",
        required=False
    )
    hard_drive_label = CharField(
        label="Hard Drive Label",
        help_text="The label of the hard drive e.g. D",
        required=False
    )
    fs = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        label="Filesystem Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:filesystem-list")}
        ),
        help_text="The Filesystem of the Volume e.g. ext4",
        required=False
    )
    cluster_type = DynamicModelChoiceField(
        queryset=ClusterType.objects.all(),
        help_text="The Cluster Type of the drive",
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        query_params={
            'type_id': '$cluster_type'  # ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
        },
        help_text="The Storage Cluster of the drive",
    )
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        help_text="Mapping between drive and virtual machine  e.g. vm-testinstall-01",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Hard Drive 1 on SSD Cluster",
    )

    class Meta:
        model = Drive

        fields = (
            "size",
            "cluster",
            "virtual_machine",
            "description",
        )

    def save(self, *args, **kwargs):
        drive = super().save(*args, **kwargs)

        # Assign/clear this IPAddress as the primary for the associated Device/VirtualMachine.
        # print(f"{self.instance}")
        print(f"{self.cleaned_data['lv_data']}")
        print(f"{self.cleaned_data['vg_data']}")
        print(f"{self.cleaned_data['size']}")
        print(f"{self.cleaned_data['path']}")
        print(f"{self.cleaned_data['fs']}")

        return drive
