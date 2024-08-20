

window.addEventListener('DOMContentLoaded', event => {

    const datatablesSimple = document.querySelector(
        "#layoutSidenav_content > main > div > div.mt-4.card.mb-4 > div.card-body.table-responsive > table");
    if (datatablesSimple) {
        new DataTable(datatablesSimple);
    }
});