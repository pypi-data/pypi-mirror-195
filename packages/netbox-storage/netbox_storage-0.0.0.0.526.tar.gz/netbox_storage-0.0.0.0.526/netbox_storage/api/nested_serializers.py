from rest_framework import serializers

from netbox.api.serializers import WritableNestedSerializer
from netbox_storage.models import Filesystem, Drive, Partition, StorageConfiguration, LinuxVolume


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


#
# Linux Volume
#
class NestedLinuxVolumeSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_storage-api:linuxvolume-detail"
    )

    class Meta:
        model = LinuxVolume
        fields = ["id", "url", "display", "size", "path"]