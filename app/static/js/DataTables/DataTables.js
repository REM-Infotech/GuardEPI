window.addEventListener("DOMContentLoaded", (event) => {
  var datatablesSimple = document.querySelector(
    "#layoutSidenav_content > main > div > div.mt-4.card.mb-4 > div.card-body.table-responsive > table"
  );
  var datatablesSimple2 = document.querySelector(
    "#layoutSidenav_content > main > div.container-fluid.px-4 > div > div.card-body.bg-secondary.bg-opacity-25 > div.card.mb-4 > div.card-body.table-responsive > table"
  );
  if (datatablesSimple) {
    var _Table = datatablesSimple;
  } else if (datatablesSimple2) {
    var _Table = datatablesSimple2;
  } else {
    var _Table = $("#DataTable");
  }

  new DataTable(_Table);
});
