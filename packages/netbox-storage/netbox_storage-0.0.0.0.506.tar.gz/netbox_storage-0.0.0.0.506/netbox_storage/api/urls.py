from netbox.api.routers import NetBoxRouter

from netbox_storage.api.views import (
    NetboxStorageRootView,
    DriveViewSet,
    FilesystemViewSet,
    LogicalVolumeViewSet,
    PartitionViewSet,
    PhysicalVolumeViewSet,
    VolumeGroupViewSet,
    LinuxVolumeViewSet, StorageConfigurationViewSet
)

router = NetBoxRouter()
router.APIRootView = NetboxStorageRootView

router.register("drive", DriveViewSet)
router.register("filesystem", FilesystemViewSet)
router.register("logicalvolume", LogicalVolumeViewSet)
router.register("partition", PartitionViewSet)
router.register("physicalvolume", PhysicalVolumeViewSet)
router.register("volumegroup", VolumeGroupViewSet)
router.register("linuxvolume", LinuxVolumeViewSet)
router.register("storageconfiguration", StorageConfigurationViewSet)

urlpatterns = router.urls
