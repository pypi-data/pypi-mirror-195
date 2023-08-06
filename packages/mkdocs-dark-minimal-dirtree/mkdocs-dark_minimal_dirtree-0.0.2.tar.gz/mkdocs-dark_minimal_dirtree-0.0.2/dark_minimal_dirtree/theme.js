(function () {
  // ready ?
  console.log("ready");
})();

function handleCollapseToggle() {}

window.addEventListener("load", function (event) {
  // after images and css
  // let lis_el = document.querySelectorAll("li.section");
  let sections_nodelist = this.document.getElementsByClassName("section");
  for (var i = 0, len = sections_nodelist.length; i < len; i++) {
    sections_nodelist[i].addEventListener(
      "click",
      function (event) {
        console.log(event);
        event.target.classList.toggle("collapsed");
      },
      false
    );
  }

  let pages_nodelist = this.document.getElementsByClassName("nav-page");
  for (var i = 0, len = pages_nodelist.length; i < len; i++) {
    pages_nodelist[i].addEventListener(
      "click",
      function (event) {
        console.log(event);
        let page_content = document.getElementById("page_content");
        page_content.innerHTML = "";
        var xhr = new XMLHttpRequest(); // create new XMLHttpRequest object
        xhr.onreadystatechange = function () {
          if (xhr.readyState === 4 && xhr.status === 200) {
            let content = xhr.responseText.split(
              '<div id="page_content" class="content">'
            )[1];
            content = content.split("<br id=\"parse-me-away\"/>")[0]
            document.getElementById("page_content").innerHTML = content; // update DOM with response
            hljs.highlightAll();
          }
        };
        let a_el_page = event.target.firstElementChild; // HTMLAnchorElement
        xhr.open("GET", a_el_page.pathname, true); // open the request with the GET method
        xhr.send(); // send the request
      },
      false
    );
  }
});
