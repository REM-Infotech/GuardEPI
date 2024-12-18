window.addEventListener("DOMContentLoaded", (event) => {
  // Simple-DataTables
  // https://github.com/fiduswriter/Simple-DataTables/wiki

  const datatablesSimple = document.getElementById("DepartamentosTable");
  if (datatablesSimple) {
    let table = new DataTable(datatablesSimple);
  }
});
