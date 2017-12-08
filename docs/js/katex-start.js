renderMathInElement(document.body);
var items = document.getElementsByClassName("MathJax_Preview");
for (var i = 0; i < items.length; i++) {
  katex.render(items[i].innerText, items[i]);
}
