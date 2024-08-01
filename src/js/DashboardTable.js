window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    const datatablesSimple = document.getElementById('DashboardTable');
    if (datatablesSimple) {
        new DataTable(datatablesSimple);
    }
});
