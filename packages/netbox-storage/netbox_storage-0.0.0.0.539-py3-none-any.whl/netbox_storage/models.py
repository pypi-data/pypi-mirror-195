from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.urls import reverse

from netbox.models import NetBoxModel


class Drive(NetBoxModel):
    cluster = models.ForeignKey(
        to='virtualization.Cluster',
        on_delete=models.PROTECT,
        related_name='cluster_drive',
    )
    size = models.FloatField(
        verbose_name="Size (GB)"
    )
    identifier = models.CharField(
        max_length=255,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = ["cluster", "size", "identifier", "description"]

    prerequisite_models = (
        'virtualization.Cluster',
        'virtualization.VirtualMachine',
    )

    class Meta:
        ordering = ["size"]

    def __str__(self):
        return f"VM: ({self.identifier}-{self.size}GB-{self.cluster})"

    def get_absolute_url(self):
        return reverse("plugins:netbox_storage:drive", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        is_already_implemented = Drive.objects.filter(id=self.pk).count()
        if is_already_implemented == 0:
            number_of_hard_drives = Drive.objects.all().\
                order_by("created").count()

            self.identifier = f"Hard Drive {number_of_hard_drives + 1}"

        super(Drive, self).save(*args, **kwargs)

    @property
    def docs_url(self):
        return f'https://confluence.ti8m.ch/docs/models/drive/'

    def partition_count(self):
        return Partition.objects.filter(drive=self).count()

    def device_name(self):
        return f"/dev/sd{chr(ord('`') + int(self.identifier[-1]))}"

    def physicalvolumes_in_drive_count(self):
        return PhysicalVolume.objects.filter(drive=self).count()

    def left_free_space(self):
        current_partition_allocated_space = Partition.objects.filter(drive=self).aggregate(sum=Sum("size")).get(
            "sum") or 0
        return self.size - current_partition_allocated_space


class LinuxDevice(NetBoxModel):
    drive = models.ForeignKey(
        Drive,
        on_delete=models.CASCADE,
        related_name='drive_device',
    )
    device = models.CharField(
        max_length=255,
    )
    size = models.FloatField(
        verbose_name="Size (GB)"
    )
    type = models.CharField(
        max_length=255,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = ["drive", "device", "size", "type", "description"]

    prerequisite_models = (
        'netbox_storage.Drive',
    )

    class Meta:
        ordering = ["size"]

    def __str__(self):
        return f'{self.device}'


class Partition(NetBoxModel):
    drive = models.ForeignKey(
        Drive,
        on_delete=models.CASCADE,
        related_name='drive_partition',
    )
    device = models.CharField(
        max_length=255,
    )
    size = models.FloatField(
        verbose_name="Size (GB)"
    )
    type = models.CharField(
        max_length=255,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = ["drive", "device", "size", "type", "description"]

    prerequisite_models = (
        'netbox_storage.Drive',
    )

    class Meta:
        ordering = ["size"]

    def __str__(self):
        return f'{self.device}'

    def get_absolute_url(self):
        return reverse("plugins:netbox_storage:partition", kwargs={"pk": self.pk})

    @property
    def docs_url(self):
        return f'https://confluence.ti8m.ch/docs/models/partition/'

    def clean(self, *args, **kwargs):
        total_allocated_space = Partition.objects.filter(drive=self.drive).aggregate(sum=Sum("size")).get("sum") or 0
        current_partition_size = Partition.objects.filter(drive=self.drive, id=self.pk) \
                                     .aggregate(sum=Sum("size")).get("sum") or 0
        if self.size is None:
            raise ValidationError(
                {
                    "size": f"The Value for Size must be greater than 0"
                }
            )
        diff_to_allocated_space = self.size - current_partition_size
        if diff_to_allocated_space > 0:
            if total_allocated_space == self.drive.size:
                raise ValidationError(
                    {
                        "size": f"The maximum Space of the hard drive was already allocated."
                    }
                )
            if self.size > self.drive.size:
                raise ValidationError(
                    {
                        "size": f"The size of the Partition is bigger than the size of the Hard Drive."
                    }
                )
            if total_allocated_space + self.size > self.drive.size:
                raise ValidationError(
                    {
                        "size": f"The size of the Partition is bigger than the size of the Hard Drive."
                    }
                )

    def get_affiliated_physical_volume(self):
        return PhysicalVolume.objects.filter(partition=self).first()


class VolumeGroup(NetBoxModel):
    vg_name = models.CharField(
        max_length=255,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = [
        "vg_name",
        "description",
    ]

    def get_absolute_url(self):
        return reverse("plugins:netbox_storage:volumegroup", kwargs={"pk": self.pk})

    def __str__(self):
        return self.vg_name

    class Meta:
        ordering = ("vg_name", "description")

    def physical_volume_count(self):
        return PhysicalVolume.objects.filter(vg=self).count()

    def logical_volume_count(self):
        return LogicalVolume.objects.filter(vg=self).count()

    def get_total_affiliated_size(self):
        total_sum = 0
        for PV in PhysicalVolume.objects.filter(vg=self):
            total_sum += PV.partition.size
        return total_sum


class PhysicalVolume(NetBoxModel):
    partition = models.OneToOneField(
        Partition,
        on_delete=models.CASCADE,
        related_name='partition_physicalvolume',
    )
    pv_name = models.CharField(
        max_length=255,
    )
    vg = models.ForeignKey(
        VolumeGroup,
        on_delete=models.CASCADE,
        related_name='volumegroup_physicalvolume',
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = [
        "partition",
        "pv_name",
        "vg",
        "description",
    ]

    # prerequisite_models = (
    #     'netbox_storage.VolumeGroup',
    # )

    def get_absolute_url(self):
        return reverse("plugins:netbox_storage:physicalvolume", kwargs={"pk": self.pk})

    def __str__(self):
        return self.pv_name

    class Meta:
        ordering = ("partition", "description")

    @property
    def size(self):
        return self.partition.size


class Filesystem(NetBoxModel):
    filesystem = models.CharField(
        unique=True,
        max_length=255,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = ["filesystem", "description"]

    def get_absolute_url(self):
        return reverse("plugins:netbox_storage:filesystem", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.filesystem}"

    class Meta:
        ordering = ("filesystem", "description")


class LogicalVolume(NetBoxModel):
    vg = models.ForeignKey(VolumeGroup, on_delete=models.CASCADE, related_name='volumegroup_logicalvolume')
    lv_name = models.CharField(
        max_length=255,
    )
    size = models.FloatField(
        verbose_name="Size (GB)"
    )
    path = models.CharField(
        max_length=255,
    )
    fs = models.ForeignKey(
        Filesystem,
        on_delete=models.CASCADE,
        related_name="fs_lvm",
        verbose_name="Filesystem",
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = [
        "vg",
        "lv_name",
        "size",
        "path",
        "fs",
        "description",
    ]

    def get_absolute_url(self):
        return reverse("plugins:netbox_storage:logicalvolume", kwargs={"pk": self.pk})

    def __str__(self):
        return self.lv_name

    class Meta:
        ordering = ("lv_name", "description")


class MountedVolume(NetBoxModel):
    device = models.ForeignKey(
        LinuxDevice,
        on_delete=models.CASCADE,
        related_name='device_mounted_volume',
    )
    size = models.FloatField(
        verbose_name="Size (GB)"
    )
    path = models.CharField(
        max_length=255,
    )
    label = models.CharField(
        max_length=255,
    )
    fs = models.ForeignKey(
        Filesystem,
        on_delete=models.CASCADE,
        related_name="fs_linux",
        verbose_name="Filesystem",
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = [
        "device",
        "size",
        "path",
        "fs",
        "description",
    ]

    def get_absolute_url(self):
        return reverse("plugins:netbox_storage:mountedvolume", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.device.device}"

    class Meta:
        ordering = ("size", "path", "description")


class StorageConfigurationLinuxVolume(NetBoxModel):
    virtual_machine = models.ForeignKey(
        to='virtualization.VirtualMachine',
        on_delete=models.CASCADE,
        related_name='virtual_machine_storage_configuration',
    )
    linux_volume = models.ForeignKey(
        MountedVolume,
        on_delete=models.CASCADE,
        related_name='linux_volume_storage_configuration'
    )

    clone_fields = [
        "virtual_machine",
        "linux_volume"
    ]

    class Meta:
        ordering = ["virtual_machine", "linux_volume"]

    #def get_absolute_url(self):
    #    return reverse("plugins:netbox_storage:storageconfiguration", kwargs={"pk": self.pk})

    def __str__(self):
        return f"Storage Configuration of the VM {self.virtual_machine}"


class TemplateConfigurationLinuxVolume(NetBoxModel):
    platform = models.ForeignKey(
        to='dcim.platform',
        on_delete=models.CASCADE,
        related_name='platform_template_configuration',
    )
    linux_volume = models.ForeignKey(
        MountedVolume,
        on_delete=models.CASCADE,
        related_name='linux_volume_template_configuration'
    )

    clone_fields = [
        "virtual_machine",
        "platform"
    ]

    class Meta:
        ordering = ["linux_volume", "platform"]

    # def get_absolute_url(self):
    #     return reverse("plugins:netbox_storage:storageconfiguration", kwargs={"pk": self.pk})

    def __str__(self):
        return f"Template Configuration of the Platform {self.platform}"
