window.addEventListener('DOMContentLoaded', event => {
    const datatablesSimple = document.getElementById('DashboardTable');
    if (datatablesSimple) {
        new DataTable(datatablesSimple);
    }
});
