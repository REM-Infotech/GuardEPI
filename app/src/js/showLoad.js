function showLoadCautela() {
  $("#EmissãoCautela").modal("hide");

  setTimeout(() => {
    $("#modalLoading").modal("show");
  }, 500);
}
function showLoad() {
  let modalFade = document.querySelectorAll(
    'div[class="modal fade show"][style="display: block;"]'
  );

  if (modalFade != null) {
    try {
      $(modalFade).modal("hide");
    } catch {}
  }

  setTimeout(() => {
    $("#modalLoading").modal("show");
  }, 500);
}
