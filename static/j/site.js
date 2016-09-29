(function () {
  // TODO feature test other bits
  if (window.history && document.addEventListener) {
    document.body.className += ' init';
  }

  var t = document.getElementById('text');
  var f = document.getElementById('form');
  t.focus();
  t.setSelectionRange(t.value.length, t.value.length);

  function fs (e) {
    e && e.preventDefault();

    var tm;
    clearTimeout(tm);
    document.body.classList.add('saving');

    var h = new window.XMLHttpRequest();
    var u = f.action;
    var p = 'a=1&t=' + t.value;
    h.open('POST', u, true);

    h.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    h.onreadystatechange = function () {
      if (h.readyState === 4 && h.status === 200) {
        var d = JSON.parse(h.responseText);

        window.history.replaceState({}, null, d.url);
        f.action = d.url;
        document.getElementById('panel').innerHTML = d.panel;
        tm = setTimeout(function () {
          document.body.classList.remove('saving');
        }, 1000);
        document.body.className += ' saved';
        panel();
      }
    };
    h.send(p);
    return false;
  }

  f.addEventListener('submit', fs);
  var to;
  t.addEventListener('input', function () {
    clearTimeout(to);
    to = setTimeout(fs, 500);
  });

  function panel () {
    document.getElementById('delete').addEventListener('submit', function () {
      return confirm("Are you sure? Deleted notes can't be recovered.");
    });
    // document.getElementById('s').addEventListener('click', function () {
    //   document.getElementById('panel').className += ' sharing';
    //   return false;
    // });
  }

  if (document.getElementById('panel').innerHTML.trim()) {
    panel();
  }
})();
