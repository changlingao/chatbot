
// SIDEBAR TOGGLE

var sidebarOpen = false;
var sidebar = document.getElementById("sidebar");

function openSidebar() {
  if(!sidebarOpen) {
    sidebar.classList.add("sidebar-responsive");
    sidebarOpen = true;
  }
}

function closeSidebar() {
  if(sidebarOpen) {
    sidebar.classList.remove("sidebar-responsive");
    sidebarOpen = false;
  }
}

// ---------- CHARTS ----------

const satisfaction = rating.map(i=>Number(i));
var pieChartOptions = {
  series: satisfaction,
  chart: {
  width: 500,
  type: 'pie',
  },
  labels: ["Very Bad", "Bad", "Neutral", "Good", "Very Good"],
};


var pieChart = new ApexCharts(document.querySelector("#pie-chart"), pieChartOptions);
pieChart.render();

console.log(usage_dates)

// AREA CHART
var areaChartOptions = {
  series: [{
    name: 'Number of conversations',
    data: usage
  }],
  chart: {
    height: 350,
    type: 'area',
    toolbar: {
      show: false,
    },
  },
  colors: ["#4f35a1", "#246dec"],
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: 'smooth'
  },
  labels: usage_dates,
  markers: {
    size: 0
  },

  tooltip: {
    shared: true,
    intersect: false,
  }
};

var areaChart = new ApexCharts(document.querySelector("#area-chart"), areaChartOptions);
areaChart.render();

// ---------- FAQ ----------
function changeView(c)
{ 
  var allBtn = document.getElementById("all-btn");
  var firstBtn = document.getElementById("first-btn");
  var secondBtn = document.getElementById("second-btn");
  var thirdBtn = document.getElementById("third-btn");
  var fourthBtn = document.getElementById("fourth-btn");
  var fifthBtn = document.getElementById("fifth-btn");
  var all = document.getElementById("all");
  var first = document.getElementById("first");
  var second = document.getElementById("second");
  var third = document.getElementById("third");
  var fourth = document.getElementById("fourth");
  var fifth = document.getElementById("fifth");

  all.style.display = "none";
  first.style.display = "none";
  second.style.display = "none";
  third.style.display = "none";
  fourth.style.display = "none";
  fifth.style.display = "none";

  allBtn.className = allBtn.className.replace(" active", "");
  firstBtn.className = firstBtn.className.replace(" active", "");
  secondBtn.className = secondBtn.className.replace(" active", "");
  thirdBtn.className = thirdBtn.className.replace(" active", "");
  fourthBtn.className = fourthBtn.className.replace(" active", "");
  fifthBtn.className = fifthBtn.className.replace(" active", "");

  if (c == "all") {
    all.style.display = "block";
    allBtn.className += " active";
  } else if (c == "first") {
    first.style.display = "block";
    firstBtn.className += " active";
  } else if (c == "second") {
    second.style.display = "block";
    secondBtn.className += " active";
  } else if (c == "third") {
    third.style.display = "block";
    thirdBtn.className += " active";
  } else if (c == "fourth") {
    fourth.style.display = "block";
    fourthBtn.className += " active";
  } else if (c == "fifth") {
    fifth.style.display = "block";
    fifthBtn.className += " active";
  }

}


// ---------- FEEDBACK ----------
function changeTable(c)
{ 
  var pos = document.getElementById("positive");
  var neg = document.getElementById("negative");
  var posBtn = document.getElementById("btn pos");
  var negBtn = document.getElementById("btn neg");

  posBtn.className = posBtn.className.replace(" active", "");
  negBtn.className = negBtn.className.replace(" active", "");

  if (c == "positive") {
    pos.style.display = "block";
    neg.style.display = "none";
    posBtn.className += " active";
  } else {
    pos.style.display = "none";
    neg.style.display = "block";
    negBtn.className += " active";
  }
}
