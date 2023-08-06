from rest_framework import serializers

from netbox.api.serializers import WritableNestedSerializer
from netbox_storage.models import Filesystem, Drive, Partition, PhysicalVolume, VolumeGroup, StorageConfiguration


#
# Filesystem
#

class NestedFilesystemSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_storage-api:filesystem-detail"
    )

    class Meta:
        model = Filesystem
        fields = ["id", "url", "display", "filesystem"]


#
# StorageConfiguration
#
class NestedStorageConfigurationSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_storage-api:storageconfiguration-detail"
    )

    class Meta:
        model = StorageConfiguration
        fields = ["id", "url", "display", "virtual_machine"]


#
# Drive
#
class NestedDriveSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_storage-api:drive-detail"
    )

    class Meta:
        model = Drive
        fields = ["id", "url", "display", "size", "identifier"]


#
# Partition
#
class NestedPartitionSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_storage-api:partition-detail"
    )

    class Meta:
        model = Partition
        fields = ["id", "url", "display", "size", "device", "type"]
