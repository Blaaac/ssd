function submit(params) {
  console.log("submitting");
  const formData = new FormData(document.querySelector("form"));
  console.log(formData.entries());
  // for (var pair of formData.entries()) {
  //   console.log(pair[0] + ": " + pair[1]);
  // }
}

function subm(params) {
  var months = document.querySelector("#months").innerHTML;
  console.log(months);

  var cash = document.querySelector("#cash").innerHTML;
  console.log(cash);

  fetch(
    "http://localhost:5000/api/fin/?" +
      new URLSearchParams({
        capital: cash,
        months: months,
      })
  )
    .then((response) => response.json())
    .then((data) => console.log(data));
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
