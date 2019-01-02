function renderFaResearchmap(elem) {
  elem.innerHTML =
    '<span class="fa-stack" style="color:#4cb10d">' +
      '<i class="fa fa-square fa-stack-2x"></i>' +
      '<i class="fa fa-search fa-stack-1x fa-inverse fa-2x"></i>' +
    '</span>';
}

function renderFaQiita(elem) {
  elem.innerHTML =
    '<span class="fa-stack">' +
      '<i class="fa fa-square fa-stack-2x" data-fa-transform="shrink-8 up-6"></i>' +
      '<i class="fas fa-spinner fa-stack-1x fa-inverse"></i>' +
    '</span>';
}

var links = document.getElementsByClassName("fa-researchmap");
for (var i = 0; i < links.length; i++) {
  renderFaResearchmap(links.item(i));
}

var links = document.getElementsByClassName("fa-qiita");
for (var i = 0; i < links.length; i++) {
  renderFaQiita(links.item(i));
}
