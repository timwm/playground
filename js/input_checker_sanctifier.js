//@version 0.1.3
//@uses js_typeid

$('#txtsize').keyup(function (e){checkvalidate($('#txtsize'), /[^0-9]+/g)})
$('#txtstr').keyup(function (e){checkvalidate($('#txtstr'), /[#\\\/,]+/g, {ntimes:-3})})
 
(function checkvalidate(tget, regex, obj) {
  //by default clean every match return mch, updated value, number of (non-)mch and were each match has been found
  var 
    origtget,
    ntimes,
    leave,
  	cleans 	 = [],
  	res 	 = {},
  	resp 	 = '',
  	
  	init = function (tget, regex, obj) {
  	
  	var origtget = tget;
  tget = tget.val() ? tget.val() : tget.text() ? tget.text() : tget.html()
  mch  = tget.match(regex);
  mchlen = mch ? mch.length : 0;

  if(obj){
      if( $.type(obj) === 'object' ) {
          ntimes = obj["ntimes"] ? obj["ntimes"] : mchlen;
          leave  = obj["leave"]  ? obj["leave"]  : 0;
          cleanit(1); //tell cleanit() early that an array has been given

      } else { 
          cleanit(0); //clean is not an object or not given, simply send it as false to cleanit()
      }
  } else { cleanit(0) }
  
  } ,
  
  cleanit = function (nobj) {
      //NOTE: dont remove nobj its used to quikly check if an array has bee given (cleans)
      if(nobj && ntget) {
          //traverse thougth clean
          if (leave) {
              _(0);
          } else if (Math.abs(ntimes)) {
              var len = Math.abs(ntimes), cleaned = [], ntget = tget;
              
              for (var i = 0; i < len; i++) {
                  if (ntimes < 0 ) { 
                      resp =
                      ntget.replace( ntget.substring(ntget.lastIndexOf(mch[i]),
                      ntget.lastIndexOf(mch[i])+mch[i].length), '');
                      ntget = resp;
                  } else {
                      resp =
                      ntget.replace( ntget.substring(ntget.indexOf(mch[i]),
                      ntget.indexOf(mch[i])+mch[i].length), '');
                      ntget = resp;
                  }
                   cleaned.push(mch[i]);
                  if(i == mchlen ){break;} else{continue;}
              }
              origtget.val(resp);
              _(1);
          }
      } else { _(0); }
      
      function _(updated) {
         if (!updated) {
             resp += tget.replace( regex, '');//objective:1 clean every match
             origtget.val(resp);
         }
         
         $.extend( res, {
              data: tget, //orig seed
              ntimes: ntimes, //number of times to replace
              leave: leave, //wheather not to replace anything
              resp: resp, //result after replace or leave
              mch: mch, //matche in seed
              nmch: mchlen, //number of matches
              cleaned: cleaned ? cleaned : mch, //matches replaced
              regex: regex //original regepr
         });
      }
      //r='';for(ob in res){r += ob+': '+ res[ob]+'\n'}return alert(res+'\n\n.....'+r)
  };
  
  return function (tget, regex, obj) {
       init.apply( null, [tget, regex, obj] );
       
       return res;
    }
 })();
  