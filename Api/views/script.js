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
}
