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
      "http://localhost:3000/api/fin/?" +
      new URLSearchParams({
        investment: cash,
        months: months,
        risk_w: risk,
      }),
    crossDomain: true,
    xhrFields: {
      withCredentials: true,
    },
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
  document.getElementById("txtarea").value = JSON.stringify(res.precision);
  document.getElementById("port").value = JSON.stringify(res.portfolio);
  showPortfolioGraph(res.portfolio);
  showPrecisionGraph(res.metrics);
  document.getElementById("actret").innerText = Number(res.result).toPrecision(
    8
  );
  // renderImage(res.img);
}

window.onload = function () {};

function showPrecisionGraph(data) {
  let datap = {};

  for (const [stock, prec] of Object.entries(data)) {
    for (const [name, val] of Object.entries(prec)) {
      datap[name] = {
        type: "bar",
        showInLegend: true,
        name: name,
        dataPoints: [],
      };
    }
  }

  for (const [stock, prec] of Object.entries(data)) {
    for (const [name, val] of Object.entries(prec)) {
      datap[name].dataPoints.push({ y: val, label: stock });
    }
  }
  console.log(Object.values(datap));
  console.log(data);

  var chart = new CanvasJS.Chart("chartprecision", {
    animationEnabled: true,
    title: {
      text: "Forecast accuracies",
    },
    axisY: {
      title: "Value",
      includeZero: true,
    },
    legend: {
      cursor: "pointer",
      itemclick: toggleDataSeries,
    },
    toolTip: {
      shared: true,
      content: toolTipFormatter,
    },
    data: Object.values(datap),
  });
  chart.render();

  function toolTipFormatter(e) {
    var str = "";
    var total = 0;
    var str3;
    var str2;
    for (var i = 0; i < e.entries.length; i++) {
      var str1 =
        '<span style= "color:' +
        e.entries[i].dataSeries.color +
        '">' +
        e.entries[i].dataSeries.name +
        "</span>: <strong>" +
        e.entries[i].dataPoint.y +
        "</strong> <br/>";
      total = e.entries[i].dataPoint.y + total;
      str = str.concat(str1);
    }
    str2 = "<strong>" + e.entries[0].dataPoint.label + "</strong> <br/>";
    str3 =
      '<span style = "color:Tomato">Total: </span><strong>' +
      total +
      "</strong><br/>";
    return str2.concat(str).concat(str3);
  }

  function toggleDataSeries(e) {
    if (typeof e.dataSeries.visible === "undefined" || e.dataSeries.visible) {
      e.dataSeries.visible = false;
    } else {
      e.dataSeries.visible = true;
    }
    chart.render();
  }
}

function showPortfolioGraph(data) {
  delete data.horizon;

  var elab = [];
  for (const [key, value] of Object.entries(data)) {
    console.log(key);
    console.log(value);
    elab.push({ y: value * 100, label: key });
  }
  console.log(elab);

  var datap = [
    {
      type: "pie",
      startAngle: 240,
      yValueFormatString: '##0.00"%"',
      indexLabel: "{label} {y}",
      dataPoints: elab,
    },
  ];
  var chart = new CanvasJS.Chart("chartportfolio", {
    animationEnabled: true,
    title: {
      text: "Portfolio distribution",
    },
    data: datap,
  });
  chart.render();
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
