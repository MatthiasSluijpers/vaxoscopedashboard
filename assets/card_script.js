path = window.location.pathname;

setTimeout(function() { setReportCardLinks(); }, 1000);


function setReportCardLinks(){
  if (path =="/") {
    addReportCardLinks();}
  home_nav_link = document.querySelector(".nav-link");
  home_nav_link.addEventListener("click", restoreReportCardLinks);
}

function restoreReportCardLinks(){
  setTimeout(function() { addReportCardLinks(); }, 500);

}

function addReportCardLinks() {
  addNLReportCardLink();
  addUKReportCardLink();
  addUSAReportCardLink();
  addCompReportCardLink();
}


function addNLReportCardLink(){
  c = document.querySelector(".target-report-card-NL")
  c.addEventListener("click", ()=>{window.location.replace("/NL");})
}

function addUKReportCardLink(){
  c = document.querySelector(".target-report-card-UK")
  c.addEventListener("click", ()=>{window.location.replace("/UK");})
}

function addUSAReportCardLink(){
  c = document.querySelector(".target-report-card-USA")
  c.addEventListener("click", ()=>{window.location.replace("/USA");})
}

function addCompReportCardLink(){
  c = document.querySelector(".target-report-card-comp")
  c.addEventListener("click", ()=>{window.location.replace("/Comparison");})
}
