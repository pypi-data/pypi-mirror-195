from extras.plugins import PluginMenuButton, PluginMenuItem
from extras.plugins import PluginMenu
from utilities.choices import ButtonColorChoices

drive_menu_item = PluginMenuItem(
    link="plugins:netbox_storage:drive_list",
    link_text="Drives",
    permissions=["netbox_storage.drive_view"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_storage:drive_add",
            "Add",
            "mdi mdi-plus-thick",
            ButtonColorChoices.GREEN,
            permissions=["netbox_storage.add_drive"],
        ),
        PluginMenuButton(
            "plugins:netbox_storage:drive_import",
            "Import",
            "mdi mdi-upload",
            ButtonColorChoices.CYAN,
            permissions=["netbox_storage.add_drive"],
        ),
    ),
)

filesystem_menu_item = PluginMenuItem(
    link="plugins:netbox_storage:filesystem_list",
    link_text="Filesystem",
    permissions=["netbox_storage.storage_view"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_storage:filesystem_add",
            "Add",
            "mdi mdi-plus-thick",
            ButtonColorChoices.GREEN,
            permissions=["netbox_storage.add_storage"],
        ),
        PluginMenuButton(
            "plugins:netbox_storage:filesystem_import",
            "Import",
            "mdi mdi-upload",
            ButtonColorChoices.CYAN,
            permissions=["netbox_storage.add_storage"],
        ),
    ),
)


partition_menu_item = PluginMenuItem(
    link="plugins:netbox_storage:partition_list",
    link_text="Partition",
    permissions=["netbox_storage.disk_view"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_storage:partition_add",
            "Add",
            "mdi mdi-plus-thick",
            ButtonColorChoices.GREEN,
            permissions=["netbox_storage.add_disk"],
        ),
        PluginMenuButton(
            "plugins:netbox_storage:partition_import",
            "Import",
            "mdi mdi-upload",
            ButtonColorChoices.CYAN,
            permissions=["netbox_storage.add_disk"],
        ),
    ),
)

linuxvolume_menu_item = PluginMenuItem(
    link="plugins:netbox_storage:linuxvolume_list",
    link_text="Linux Volume",
    permissions=["netbox_storage.disk_view"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_storage:linuxvolume_add",
            "Add",
            "mdi mdi-plus-thick",
            ButtonColorChoices.GREEN,
            permissions=["netbox_storage.add_disk"],
        ),
        PluginMenuButton(
            "plugins:netbox_storage:linuxvolume_import",
            "Import",
            "mdi mdi-upload",
            ButtonColorChoices.CYAN,
            permissions=["netbox_storage.add_disk"],
        ),
    ),
)

menu = PluginMenu(
    label="NetBox Storage",
    groups=(
        (
            "General Configuration",
            (
                filesystem_menu_item,
            ),
        ),
        (
            "Linux Volume Configuration",
            (
                linuxvolume_menu_item,
            ),
        ),
        (
            "Storage Configuration",
            (
                drive_menu_item,
                partition_menu_item,
            ),
        ),

    ),
    icon_class="mdi mdi-disc",
)
