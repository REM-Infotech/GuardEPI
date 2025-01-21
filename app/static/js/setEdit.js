function SetModalEdit() {
  setTimeout(() => {
    $("#modalLoading").modal("hide");
  }, 500);

  setTimeout(() => {
    var ModalId = document.querySelector("div[data-modal_edit]");
    $(document).ready(function () {
      $(ModalId).modal("show");
    });
  }, 1500);
}

// Chama a função com o valor obtido
SetModalEdit();

function formatarComoMoeda(elemento) {
  let valor = elemento.value.replace(/\D/g, ""); // Remove tudo que não é dígito
  valor = (parseInt(valor) / 100).toFixed(2); // Divide por 100 e fixa duas casas decimais
  valor = valor.replace(".", ","); // Troca ponto por vírgula

  // Adiciona separadores de milhar
  valor = valor.replace(/\B(?=(\d{3})+(?!\d))/g, ".");

  // Adiciona o símbolo R$
  elemento.value = "R$ " + valor;
}
