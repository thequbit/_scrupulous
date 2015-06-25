<html>

<body>

  <div id="site-wrapper">
  </div>

  <script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
  <script>
    $(document).ready(function() {
      var c = getCookie('unique');
      if ( c == '' ) {
        setCookie('unique', '1234', 365*10);
      } 
    });
    $('#site-wrapper').html('loaded.')
  </script>

  <script>
    // functions taken from
    //   http://www.w3schools.com/js/js_cookies.asp
    function setCookie(cname, cvalue, exdays) {
      var d = new Date();
      d.setTime(d.getTime() + (exdays*24*60*60*1000));
      var expires = "expires="+d.toUTCString();
      document.cookie = cname + "=" + cvalue + "; " + expires;
    }
    function getCookie(cname) {
      var name = cname + "=";
      var ca = document.cookie.split(';');
      for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
      }
      return "";
    }
  </script>

</body>

</html>
