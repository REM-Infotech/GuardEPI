$(document).ready(function () {
  const pdfUrl = $("#pdfUrl").val();
  document.getElementById("pdfFrame").src = pdfUrl;
  $("#ExibirPDF").modal("show");
});
