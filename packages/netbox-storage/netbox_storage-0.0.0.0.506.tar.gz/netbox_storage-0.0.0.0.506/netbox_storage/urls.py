from django.urls import path

from netbox.views.generic import ObjectChangeLogView

from netbox_storage.models import Drive, Filesystem, Partition, PhysicalVolume, VolumeGroup, LogicalVolume, LinuxVolume
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
    PhysicalVolumeListView,
    PhysicalVolumeEditView,
    PhysicalVolumeBulkImportView,
    PhysicalVolumeBulkEditView,
    PhysicalVolumeBulkDeleteView,
    PhysicalVolumeView,
    PhysicalVolumeDeleteView,
    DrivePartitionListView,
    # VolumeGroup
    VolumeGroupListView,
    VolumeGroupEditView,
    VolumeGroupBulkImportView,
    VolumeGroupBulkEditView,
    VolumeGroupView,
    VolumeGroupDeleteView,
    VolumeGroupBulkDeleteView,
    # LogicalVolume
    LogicalVolumeListView,
    LogicalVolumeEditView,
    LogicalVolumeBulkImportView,
    LogicalVolumeBulkEditView,
    LogicalVolumeBulkDeleteView,
    LogicalVolumeView,
    LogicalVolumeDeleteView,
    # LinuxVolume
    LinuxVolumeListView,
    LinuxVolumeEditView,
    LinuxVolumeBulkImportView,
    LinuxVolumeBulkEditView,
    LinuxVolumeBulkDeleteView,
    LinuxVolumeView,
    LinuxVolumeDeleteView,
    VolumeGroupPhysicalVolumeListView,
    VolumeGroupLogicalVolumeListView,
    LVMAddSimpleView,
    AddVolume,
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
    # LinuxVolume urls
    #
    path("linuxvolume/", LinuxVolumeListView.as_view(), name="linuxvolume_list"),
    path("linuxvolume/add/", LinuxVolumeEditView.as_view(), name="linuxvolume_add"),
    path("linuxvolume/import/", LinuxVolumeBulkImportView.as_view(), name="linuxvolume_import"),
    path("linuxvolume/edit/", LinuxVolumeBulkEditView.as_view(), name="linuxvolume_bulk_edit"),
    path("linuxvolume/delete/", LinuxVolumeBulkDeleteView.as_view(), name="linuxvolume_bulk_delete"),
    path("linuxvolume/<int:pk>/", LinuxVolumeView.as_view(), name="linuxvolume"),
    path("linuxvolume/<int:pk>/edit/", LinuxVolumeEditView.as_view(), name="linuxvolume_edit"),
    path("linuxvolume/<int:pk>/delete/", LinuxVolumeDeleteView.as_view(), name="linuxvolume_delete"),
    path(
        "linuxvolume/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="linuxvolume_changelog",
        kwargs={"model": LinuxVolume},
    ),
    #
    # Simple Configuration
    #
    # path('lvm-add/', LVMAddSimpleView.as_view(), name='lvm_add'),
    # path('volume-add/', AddVolume.as_view(), name="volume_add")
]
