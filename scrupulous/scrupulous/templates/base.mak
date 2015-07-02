<html>
<head>

    <title>Scrupulous</title>

    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <link rel="stylesheet" href="static/foundation/css/foundation.css" />
    <link rel="stylesheet" href="static/foundation/css/foundation-datepicker.css" />

    <link href='http://fonts.googleapis.com/css?family=Lato' rel='stylesheet' type='text/css'>

</head>
<body>

   
    <script src="static/foundation/js/vendor/jquery.js"></script>
   
    <script src="static/foundation/js/foundation/foundation.js"></script>
    
    <script src="static/foundation/js/foundation/foundation.dropdown.js"></script>
    <script src="static/foundation/js/foundation/foundation.reveal.js"></script>
    <script src="static/foundation/js/foundation/foundation.topbar.js"></script>

    <script src="static/foundation/js/vendor/modernizr.js"></script> 

    <script src="/static/js/rest.js"></script>
    <script src="/static/js/site.js"></script>

    <script>
        $(document).foundation({});
        _site.load();
    </script>
    
    <div id="site-wrapper">
        ${self.body()}
    </div>

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
