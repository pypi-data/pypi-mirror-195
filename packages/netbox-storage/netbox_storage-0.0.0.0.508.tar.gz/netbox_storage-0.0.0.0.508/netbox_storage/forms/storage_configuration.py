from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)
from utilities.forms import (
    CSVModelChoiceField,
    DynamicModelChoiceField,
)

from netbox_storage.models import Drive, StorageConfiguration
from virtualization.models import Cluster, ClusterType, VirtualMachine


class StorageConfigurationForm(NetBoxModelForm):
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        help_text="Mapping between drive and virtual machine  e.g. vm-testinstall-01",
    )

    fieldsets = (
        (
            "Drive Cluster Config",
            (
                "virtual_machine",
            ),
        ),
    )

    class Meta:
        model = StorageConfiguration

        fields = (
            "virtual_machine",
        )


class StorageConfigurationFilterForm(NetBoxModelFilterSetForm):
    model = StorageConfiguration

    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False
    )


class StorageConfigurationImportForm(NetBoxModelImportForm):
    virtual_machine = CSVModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        to_field_name='name',
        help_text='Required'
    )

    class Meta:
        model = StorageConfiguration

        fields = (
            "virtual_machine",
        )


class StorageConfigurationBulkEditForm(NetBoxModelBulkEditForm):
    model = StorageConfiguration

    virtual_machine = CSVModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        to_field_name='name',
        help_text='Required'
    )

    fieldsets = (
        (
            None,
            ["virtual_machine"],
        ),
    )
