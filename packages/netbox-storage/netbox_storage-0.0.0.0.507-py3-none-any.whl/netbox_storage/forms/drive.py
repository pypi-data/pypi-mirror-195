from django.core.validators import MinValueValidator
from django.forms import (
    CharField,
    FloatField,
)

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)
from netbox_storage.models import Drive, StorageConfiguration
from utilities.forms import (
    CSVModelChoiceField,
    DynamicModelChoiceField,
)
from virtualization.models import Cluster, ClusterType


class DriveForm(NetBoxModelForm):
    """Form for creating a new Drive object."""
    # ct = ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the drive e.g. 25",
        validators=[MinValueValidator(1)],
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
    storage_configuration = DynamicModelChoiceField(
        queryset=StorageConfiguration.objects.all(),
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
            ),
        ),
        (
            "Drive Configuration",
            (
                "size",
                "storage_configuration",
                "description",
            ),
        ),
    )

    class Meta:
        model = Drive

        fields = (
            "size",
            "cluster",
            "storage_configuration",
            "description",
        )


class DriveFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering Drive instances."""

    model = Drive

    size = FloatField(
        required=False,
        label="Size (GB)",
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(
            # type__pk=ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
        ),
        required=False,
    )
    storage_configuration = DynamicModelChoiceField(
        queryset=StorageConfiguration.objects.all(),
        required=False
    )


class DriveImportForm(NetBoxModelImportForm):
    cluster = CSVModelChoiceField(
        queryset=Cluster.objects.all(),
        to_field_name='name',
        required=False,
        help_text='Assigned cluster'
    )
    storage_configuration = CSVModelChoiceField(
        queryset=StorageConfiguration.objects.all(),
        required=False,
        to_field_name='name',
        help_text='Required'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Drive

        fields = (
            "size",
            "cluster",
            "storage_configuration",
            "description",
        )


class DriveBulkEditForm(NetBoxModelBulkEditForm):
    model = Drive

    size = FloatField(
        required=False,
        label="Size (GB)",
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        query_params={
            'site_id': '$site'
        }
    )
    storage_configuration = CSVModelChoiceField(
        queryset=StorageConfiguration.objects.all(),
        required=False,
        to_field_name='name',
        help_text='Required'
    )
    description = CharField(max_length=255, required=False)

    fieldsets = (
        (
            None,
            ("size", "cluster", "storage_configuration", "description"),
        ),
    )
    nullable_fields = ["description"]
