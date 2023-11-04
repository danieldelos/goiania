
  function executarScript() {
   alert("ok veio do arquivo js")
  }

  function chamarFuncaoDaView() {
    fetch('/executar-script/')
        .then(response => response.json())
        .then(data => {
            alert("ok deu certo")
        })
        .catch(error => {
            // Lidar com erros aqui
        });
}