function formatarComoCNPJ(elemento) {
  let valor = elemento.value.replace(/[^a-zA-Z0-9]/g, ""); // Remove tudo que não é dígito ou letra
  // Adiciona os pontos, barra e traço para formatação do CNPJ
  valor = valor.replace(/^(\w{2})(\w)/, "$1.$2");
  valor = valor.replace(/^(\w{2})\.(\w{3})(\w)/, "$1.$2.$3");
  valor = valor.replace(/\.(\w{3})(\w)/, ".$1/$2");
  valor = valor.replace(/(\w{4})(\w)/, "$1-$2");
  elemento.value = valor;
}
