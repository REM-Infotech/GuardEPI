window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

document.addEventListener("htmx:afterRequest", function () {
    var element = document.getElementById("scrollHere");
    if (element !== null) {
        element.scrollIntoView();
    }
})

function formatDocument(element) {

    let value = element.value.replace(/\D/g, '');

    // Se o valor tem 11 dígitos, é um CPF
    if (value.length <= 11) {
        // Adiciona a formatação de CPF
        value = value.replace(/(\d{3})(\d{3})?(\d{3})?(\d{2})?/, function (_, p1, p2, p3, p4) {
            return `${p1}${p2 ? '.' + p2 : ''}${p3 ? '.' + p3 : ''}${p4 ? '-' + p4 : ''}`;
        });
    } else {
        // Adiciona a formatação de CNPJ
        value = value.replace(/(\d{2})(\d{4})(\d{4})(\d{2})/, function (_, p1, p2, p3, p4) {
            return `${p1}.${p2}/${p3}-${p4}`;
        });
    };
    element.value = value;
}

document.querySelectorAll('.open-pdf').forEach(button => {
    button.addEventListener('click', function () {
        const pdfUrl = button.getAttribute('data-pdf-url');
        document.getElementById('pdfFrame').src = pdfUrl;
        $('#ExibirPDF').modal('show');
    });
});