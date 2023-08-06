from netbox.api.routers import NetBoxRouter

from netbox_storage.api.views import (
    NetboxStorageRootView,
    DriveViewSet,
    FilesystemViewSet,
    PartitionViewSet,
    MountedVolumeViewSet,
)

router = NetBoxRouter()
router.APIRootView = NetboxStorageRootView

router.register("drive", DriveViewSet)
router.register("filesystem", FilesystemViewSet)
router.register("partition", PartitionViewSet)
router.register("mountedvolume", MountedVolumeViewSet)

urlpatterns = router.urls
