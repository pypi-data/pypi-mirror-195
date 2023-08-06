from django.urls import path

from netbox.views.generic import ObjectChangeLogView
from netbox_storage.models import Drive, Filesystem, Partition, MountedVolume
from netbox_storage.views import (
    # Drive View
    DriveListView,
    DriveView,
    DriveEditView,
    DriveDeleteView,
    DriveBulkImportView,
    DriveBulkEditView,
    DriveBulkDeleteView,
    # Filesystem Views
    FilesystemListView,
    FilesystemView,
    FilesystemEditView,
    FilesystemDeleteView,
    FilesystemBulkImportView,
    FilesystemBulkEditView,
    FilesystemBulkDeleteView,
    # Partition
    PartitionListView,
    PartitionEditView,
    PartitionBulkImportView,
    PartitionBulkEditView,
    PartitionBulkDeleteView,
    PartitionView,
    PartitionDeleteView,
    # PhysicalVolume
    DrivePartitionListView,
    # VolumeGroup
    # LogicalVolume
    # LinuxVolume
    MountedVolumeListView,
    MountedVolumeEditView,
    MountedVolumeBulkImportView,
    MountedVolumeBulkEditView,
    MountedVolumeBulkDeleteView,
    MountedVolumeView,
    MountedVolumeDeleteView, LVMAddSimpleView, AddSimpleLinuxVolumeView,
)

app_name = "netbox_storage"

urlpatterns = [
    #
    # Drive urls
    #
    path("drive/", DriveListView.as_view(), name="drive_list"),
    path("drive/add/", DriveEditView.as_view(), name="drive_add"),
    path("drive/import/", DriveBulkImportView.as_view(), name="drive_import"),
    path("drive/edit/", DriveBulkEditView.as_view(), name="drive_bulk_edit"),
    path("drive/delete/", DriveBulkDeleteView.as_view(), name="drive_bulk_delete"),
    path("drive/<int:pk>/", DriveView.as_view(), name="drive"),
    path("drive/<int:pk>/edit/", DriveEditView.as_view(), name="drive_edit"),
    path("drive/<int:pk>/delete/", DriveDeleteView.as_view(), name="drive_delete"),
    path(
        "drive/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="drive_changelog",
        kwargs={"model": Drive},
    ),
    path("drive/<int:pk>/partition/", DrivePartitionListView.as_view(), name="drive_partitions"),
    #
    # Filesystem urls
    #
    path("filesystem/", FilesystemListView.as_view(), name="filesystem_list"),
    path("filesystem/add/", FilesystemEditView.as_view(), name="filesystem_add"),
    path("filesystem/import/", FilesystemBulkImportView.as_view(), name="filesystem_import"),
    path("filesystem/edit/", FilesystemBulkEditView.as_view(), name="filesystem_bulk_edit"),
    path("filesystem/delete/", FilesystemBulkDeleteView.as_view(), name="filesystem_bulk_delete"),
    path("filesystem/<int:pk>/", FilesystemView.as_view(), name="filesystem"),
    path("filesystem/<int:pk>/edit/", FilesystemEditView.as_view(), name="filesystem_edit"),
    path("filesystem/<int:pk>/delete/", FilesystemDeleteView.as_view(), name="filesystem_delete"),
    path(
        "filesystem/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="filesystem_changelog",
        kwargs={"model": Filesystem},
    ),
    #
    # Partition urls
    #
    path("partition/", PartitionListView.as_view(), name="partition_list"),
    path("partition/add/", PartitionEditView.as_view(), name="partition_add"),
    path("partition/import/", PartitionBulkImportView.as_view(), name="partition_import"),
    path("partition/edit/", PartitionBulkEditView.as_view(), name="partition_bulk_edit"),
    path("partition/delete/", PartitionBulkDeleteView.as_view(), name="partition_bulk_delete"),
    path("partition/<int:pk>/", PartitionView.as_view(), name="partition"),
    path("partition/<int:pk>/edit/", PartitionEditView.as_view(), name="partition_edit"),
    path("partition/<int:pk>/delete/", PartitionDeleteView.as_view(), name="partition_delete"),
    path(
        "partition/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="partition_changelog",
        kwargs={"model": Partition},
    ),
    #
    # MountedVolume urls
    #
    path("mountedvolume/", MountedVolumeListView.as_view(), name="mountedvolume_list"),
    path("mountedvolume/add/", MountedVolumeEditView.as_view(), name="mountedvolume_add"),
    path("mountedvolume/import/", MountedVolumeBulkImportView.as_view(), name="mountedvolume_import"),
    path("mountedvolume/edit/", MountedVolumeBulkEditView.as_view(), name="mountedvolume_bulk_edit"),
    path("mountedvolume/delete/", MountedVolumeBulkDeleteView.as_view(), name="mountedvolume_bulk_delete"),
    path("mountedvolume/<int:pk>/", MountedVolumeView.as_view(), name="mountedvolume"),
    path("mountedvolume/<int:pk>/edit/", MountedVolumeEditView.as_view(), name="mountedvolume_edit"),
    path("mountedvolume/<int:pk>/delete/", MountedVolumeDeleteView.as_view(), name="mountedvolume_delete"),
    path(
        "mountedvolume/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="mountedvolume_changelog",
        kwargs={"model": MountedVolume},
    ),
    #
    # Simple Configuration
    #
    path('lvm-add/', LVMAddSimpleView.as_view(), name='lvm_add'),
    path('volume-add/', AddSimpleLinuxVolumeView.as_view(), name="volume_add")
]
