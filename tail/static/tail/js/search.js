// search filter
var _filterElement ='';
var _filterValue = '';

var _filterElement = function(elem) {
    var pattern = new RegExp(_filterValue, 'i');
    var element = elem;
    if (pattern.test(element.textContent)) {
      element.style.display = '';
    } else {
      element.style.display = 'none';
    }
  };

var _searchInput = document.getElementById("search");
_searchInput.onkeyup = function(e) {
    _filterValue = this.value;
    if (window.event.keyCode == 27) {
        _filterValue = '';
        this.value = '';
    }
    _logChildNodes = self.logChildNodes;
    for (i=0; i<_logChildNodes.length; i++) {
        NodeList = _logChildNodes[i];
        console.log(NodeList);
        for (j=0; j<NodeList.length; j++) {
            _filterElement(NodeList[j])
            console.log(NodeList[j]);
        };
    };
    window.scrollTo(0, document.body.scrollHeight);
}
