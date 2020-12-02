function init() {}
function findAll() {
  $.ajax({
    url: "http://localhost:5000/api/Stagione",
    type: "GET",
    contentType: "application/json",
    success: function (result) {
      console.log(result);
      readResult(JSON.stringify(result));
    },
    error: function (xhr, status, p3, p4) {
      var err = "Error " + " " + status + " " + p3;
      if (xhr.responseText && xhr.responseText[0] == "{")
        err = JSON.parse(xhr.responseText).message;
      alert(err);
    },
  });
}
function findById() {
  var id = $("#txtId").val();
  $.ajax({
    url: "http://localhost:5000/api/Stagione/" + id,
    type: "GET",
    contentType: "application/json",
    data: "",
    success: function (result) {
      console.log(result);
      readResult(JSON.stringify(result));
    },
    error: function (xhr, status, p3, p4) {
      var err = "Error " + " " + status + " " + p3;
      if (xhr.responseText && xhr.responseText[0] == "{")
        err = JSON.parse(xhr.responseText).message;
      alert(err);
    },
  });
}
function postItem() {
  var id = $("#txtId").val();
  var anno = $("#txtNewAnno").val();
  var options = {};
  options.url = "http://localhost:5000/api/Stagione/PostStagioneItem";
  options.type = "POST";
  options.data = JSON.stringify({
    id: Number(id),
    anno: Number(anno),
    serie: "C",
  });
  options.dataType = "json";
  options.contentType = "application/json";
  options.success = function (msg) {
    alert(msg);
  };
  options.error = function (err) {
    alert(err.responseText);
  };
  $.ajax(options);
}
function deleteId() {
  var options = {};
  options.url = "http://localhost:5000/api/Stagione/" + $("#txtId").val();
  options.type = "DELETE";
  options.contentType = "application/json";
  options.success = function (msg) {
    alert(msg);
  };
  options.error = function (err) {
    alert(err.statusText);
  };
  $.ajax(options);
}
function updateId() {
  var id = $("#txtId").val();
  var anno = $("#txtNewAnno").val();
  var options = {};
  options.url = "http://localhost:5000/api/Stagione/" + $("#txtId").val();
  options.type = "PUT";
  options.data = JSON.stringify({
    id: Number(id),
    anno: Number(anno),
    serie: "C",
  });
  options.dataType = "json";
  options.contentType = "application/json";
  options.success = function (msg) {
    alert(msg);
  };
  options.error = function (err) {
    alert(err.responseText);
  };
  $.ajax(options);
}
///////////INDICI
function getIndexById() {
  var id = $("#txtId").val();
  $.ajax({
    url: "http://localhost:5000/api/fin/" + id,
    type: "GET",
    contentType: "application/json",
    data: "",
    success: function (result) {
      console.log(result);
      showResult(JSON.parse(result));
    },
    error: function (xhr, status, p3, p4) {
      var err = "Error " + " " + status + " " + p3;
      if (xhr.responseText && xhr.responseText[0] == "{")
        err = JSON.parse(xhr.responseText).message;
      alert(err);
    },
  });
}
function showResult(res) {
  document.getElementById("txtarea").value += res.text;
  renderImage(res.img);
}
function renderImage(b64imgstr) {
  var b64 = b64imgstr;
  b64 = b64.substring(0, ba64.length - 1);
  b64 = b64.substring(2, ba64.length);
  var image = new Image();
  image.src = "data:image/png;base64," + b64;
  document.body.appendChild(image);
}

function readResult(str) {
  document.getElementById("txtarea").value += str;
  console.log(str);
}
