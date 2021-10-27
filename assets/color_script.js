setTimeout(function() { changeNavColorAccent(); }, 1000);


function changeNavColorAccent() {
  items = document.querySelectorAll(".nav-item");
  items[0].addEventListener("click",accentHome);
  items[1].addEventListener("click",accentNL);
  items[2].addEventListener("click",accentUK);
  items[3].addEventListener("click",accentUSA);
  items[4].addEventListener("click",accentComparison);

  path = window.location.pathname;

  if(path == ""){
    accentHome();
  }else if (path == "/NL"){
    accentNL();
  }else if (path == "/UK"){
    accentUK();
  }else if (path == "/USA"){
    accentUSA();
  }else if (path == "/Comparison"){
    accentComparison();
  }
}

function accentHome() {
  nav = document.querySelector(".nav");
  nav.style.background = "#424242";
  nav.style.borderColor = "#303030";
}

function accentNL() {
  nav = document.querySelector(".nav");
  nav.style.background = "#b67a0c";
  nav.style.borderColor = "#916109";
}

function accentUK() {
  nav = document.querySelector(".nav");
  nav.style.background = "#aa2e39";
  nav.style.borderColor = "#6b2329";
}

function accentUSA() {
  nav = document.querySelector(".nav");
  nav.style.background = "#456888";
  nav.style.borderColor = "#38465c";
}

function accentComparison() {
  nav = document.querySelector(".nav");
  nav.style.background = "#424242";
  nav.style.borderColor = "#303030";
}
