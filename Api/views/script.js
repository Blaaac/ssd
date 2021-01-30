function submit(params) {
  console.log("submitting");
  const formData = new FormData(document.querySelector("form"));
  console.log(formData.entries());
}

function subm(params) {
  var months = +document.querySelector("#months").innerHTML;
  console.log(months);

  var cash = +document.querySelector("#cash").innerHTML;
  console.log(cash);

  var risk = +document.querySelector("#risk").innerHTML;
  console.log(risk);

  $.ajax({
    url:
      "http://localhost:5000/api/fin/?" +
      new URLSearchParams({
        investment: cash,
        months: months,
        risk_w: risk,
      }),
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

function readResult(str) {
  console.log(str);
  document.getElementById("txtarea").value = str;
}

function showResult(res) {
  console.log(res);
  document.getElementById("txtarea").value = res.text;
  document.getElementById("port").value = res.portfolio;
  // renderImage(res.img);
}
function renderImage(b64imgstr) {
  var b64 = b64imgstr;
  b64 = b64.substring(0, b64.length - 1);
  b64 = b64.substring(2, b64.length);
  var image = new Image();
  image.src = "data:image/png;base64," + b64;
  document.body.appendChild(image);
}

function findAll() {
  $.ajax({
    url: "http://localhost:5000/api/Fin",
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

function getIndexById() {
  var id = $("#txtId").val();
  console.log(id);
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
