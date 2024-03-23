var typeid = function () {
	var 
		i ,
		type  = "Boolean Number String Function Array Date RegExp Object Error Symbol" ,
		arr   = type.split( " " ) , //creating array of the identifier types
		len   = arr.length ,
		idobj = {};
	
	for (i=0; i < len-1; i +=1){
		idobj[ "[object " + arr[i] + "]" ] = arr[i].toLowerCase();
	}
	
	return function (id) {
		if ( id == null ) {
			return id + "";
		}
		
		// Support: Android <=2.3 only (functionish RegExp)
		return typeof id === "object" || typeof id === "function" ?
			idobj[ toString.call( id ) ] || "object" :
			typeof id;
	}
}();

//____________________________________________________________________________________

//____________________________________________________________________________________

(function(){
var i, l,
	//op = Object.prototype,
	arr = "String Number Function Array Object Boolean Date RegExp Error Null".split( " " );
	
for ( i = 0, l = arr.length; i < l; i++ ){
	window[ 'is' + arr[i] ] = (function() {
		var that = this;
		
		return function( what, force ){
			return {}.toString.call( what ) === '[object '+ that +']' ?
				that.toLowerCase() : force ? getRealType( what ) : false;
		}
	}).call( arr[i] );
}

function getRealType( what ){
	for ( i = 0, l = arr.length; i < l; i++ ){
		if ( {}.toString.call( what ).match( arr[i] ) ){
			return arr[i].toLowerCase();
		}
	}
}
})();