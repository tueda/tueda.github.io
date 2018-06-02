function renderEad(elem) {
  for (var i = 0; i < elem.childNodes.length; i++) {
    var childNode = elem.childNodes[i];
    if (childNode.nodeType === 3) {
      // text nocde
      childNode.textContent = childNode.textContent.replace(' - at - ', '@');
    } else if (childNode.nodeType === 1) {
      // element node
      renderEad(childNode);
    }
  }
}

var eads = document.getElementsByClassName("ead");
for (var i = 0; i < eads.length; i++) {
  renderEad(eads.item(i));
}
