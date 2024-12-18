window.addEventListener("DOMContentLoaded", (event) => {
  const datatablesSimple = document.getElementById("EntradasTable");
  if (datatablesSimple) {
    let table = new DataTable(datatablesSimple);
  }
});

document.querySelectorAll(".open-pdf").forEach((button) => {
  button.addEventListener("click", function () {
    const pdfUrl = button.getAttribute("data-pdf-url");
    console.log(pdfUrl);
    document.getElementById("pdfFrame").src = pdfUrl;
    $("#ExibirCautela").modal("show");
  });
});
