window.addEventListener("DOMContentLoaded", (event) => {
  var datatablesSimple = document.querySelector(
    "#layoutSidenav_content > main > div > div.mt-4.card.mb-4 > div.card-body.table-responsive > table"
  );
  if (datatablesSimple) {
    new DataTable(datatablesSimple);
  } else {
    var datatablesSimple = document.querySelector(
      "#layoutSidenav_content > main > div.container-fluid.px-4 > div > div.card-body.bg-secondary.bg-opacity-25 > div.card.mb-4 > div.card-body.table-responsive > table"
    );
    new DataTable(datatablesSimple);
  }
});
