from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from netbox_storage.api.nested_serializers import NestedFilesystemSerializer, NestedDriveSerializer, \
    NestedPartitionSerializer
from netbox_storage.models import Drive, Filesystem, Partition, LinuxVolume, StorageConfiguration
from virtualization.api.nested_serializers import NestedClusterSerializer, NestedVirtualMachineSerializer


class FilesystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filesystem
        fields = (
            "id",
            "filesystem",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class DriveSerializer(NetBoxModelSerializer):
    cluster = NestedClusterSerializer(required=False, allow_null=True)
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_storage-api:drive-detail")

    class Meta:
        model = Drive
        fields = (
            "id",
            "url",
            "display",
            "size",
            "cluster",
            "identifier",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class PartitionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_storage-api:partition-detail')
    drive = NestedDriveSerializer(required=False, allow_null=True)

    class Meta:
        model = Partition
        fields = (
            "id",
            "url",
            "drive",
            "device",
            "size",
            "type",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class LinuxVolumeSerializer(serializers.ModelSerializer):
    fs = NestedFilesystemSerializer(required=False, allow_null=True)
    partition = NestedPartitionSerializer(required=False, allow_null=True)

    class Meta:
        model = LinuxVolume
        fields = (
            "id",
            "partition",
            "fs",
            "size",
            "path",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )
