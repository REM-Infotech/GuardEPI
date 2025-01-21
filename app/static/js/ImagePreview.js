function previewImage(e, id_element) {
  var file = e.target.files[0];
  var reader = new FileReader();

  reader.onload = function (e) {
    document.getElementById(id_element).src = e.target.result;
  };

  reader.readAsDataURL(file);
}

function teste() {}
