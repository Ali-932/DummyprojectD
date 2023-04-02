document.addEventListener('DOMContentLoaded', function () {
    const permissionsField = document.querySelector('#id_permissions');
    const selectedObjectsField = document.querySelector('#id_selected_objects');

    function fetchObjects(permissionIds, isInitial = false) {
        fetch(`/fetch_objects/?permission_ids=${permissionIds.join(',')}&is_initial=${isInitial}`)
            .then(response => response.json())
            .then(data => {
                // Remove existing options
                while (selectedObjectsField.firstChild) {
                    selectedObjectsField.firstChild.remove();
                }

                // Add new options
                data.forEach(item => {
                    const option = document.createElement('option');
                    option.value = item.id;
                    option.text = item.display;
                    selectedObjectsField.add(option);
                });
            });
    }

    if (permissionsField && selectedObjectsField) {
        // Load objects when the page loads if there's a selected permission
        const initialPermissionIds = Array.from(permissionsField.selectedOptions).map(option => option.value);
        if (initialPermissionIds.length) {
            fetchObjects(initialPermissionIds, true);
        }

        // Update objects when the permission selection changes
        permissionsField.addEventListener('change', function () {
            const permissionIds = Array.from(permissionsField.selectedOptions).map(option => option.value);
            if (permissionIds.length) {
                fetchObjects(permissionIds);
            } else {
                selectedObjectsField.innerHTML = '';
            }
        });
    }
});
