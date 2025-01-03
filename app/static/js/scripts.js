window.addEventListener("DOMContentLoaded", (event) => {
  // Toggle the side navigation
  const sidebarToggle = document.body.querySelector("#sidebarToggle");
  if (sidebarToggle) {
    // Uncomment Below to persist sidebar toggle between refreshes
    // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
    //     document.body.classList.toggle('sb-sidenav-toggled');
    // }
    sidebarToggle.addEventListener("click", (event) => {
      event.preventDefault();
      document.body.classList.toggle("sb-sidenav-toggled");
      localStorage.setItem(
        "sb|sidebar-toggle",
        document.body.classList.contains("sb-sidenav-toggled")
      );
    });
  }
});

document.addEventListener("htmx:afterRequest", function () {
  var element = document.getElementById("scrollHere");
  if (element !== null) {
    element.scrollIntoView();
  }
});

function formatDocument(element) {
  let value = element.value.replace(/\D/g, "");

  // Se o valor tem 11 dígitos, é um CPF
  if (value.length <= 11) {
    // Adiciona a formatação de CPF
    value = value.replace(
      /(\d{3})(\d{3})?(\d{3})?(\d{2})?/,
      function (_, p1, p2, p3, p4) {
        return `${p1}${p2 ? "." + p2 : ""}${p3 ? "." + p3 : ""}${
          p4 ? "-" + p4 : ""
        }`;
      }
    );
  } else {
    // Adiciona a formatação de CNPJ
    value = value.replace(
      /(\d{2})(\d{4})(\d{4})(\d{2})/,
      function (_, p1, p2, p3, p4) {
        return `${p1}.${p2}/${p3}-${p4}`;
      }
    );
  }
  element.value = value;
}

function isValidUrl(url) {
  const urlPattern = /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/i;
  return urlPattern.test(url);
}

document.querySelectorAll(".open-pdf").forEach((button) => {
  button.addEventListener("click", function () {
    const pdfUrl = button.getAttribute("data-pdf-url");
    if (isValidUrl(pdfUrl)) {
      document.getElementById("pdfFrame").src = pdfUrl;
      $("#ExibirPDF").modal("show");
    } else {
      // Exibe uma mensagem de erro
    }
  });
});

var selectors = document.getElementsByTagName("select");

if (selectors.length > 0) {
  for (let element of selectors) {
    // Mudança aqui, para usar 'for...of' em vez de 'for...in'

    $(document).ready(function () {
      // Aqui podemos usar jQuery diretamente, pois estamos aplicando ao próprio elemento
      $(element)
        .select2({
          theme: "bootstrap-5",
          width: $(element).data("width")
            ? $(element).data("width")
            : $(element).hasClass("w-100")
            ? "100%"
            : "style",
          placeholder: $(element).data("placeholder"),
          dropdownParent: $(element).closest(".modal").length
            ? $(element).closest(".modal")
            : null, // Verifica se o select está em um modal
        })
        .on("change", function () {
          // Dispara o evento change para o htmx
          if (!this.classList.contains("htmx-dispatched")) {
            this.classList.add("htmx-dispatched");
            this.dispatchEvent(new Event("change", { bubbles: true }));
            this.classList.remove("htmx-dispatched");
          }
        });
    });
  }
}
