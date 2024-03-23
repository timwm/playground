//@date Thu, 11-04-2019 06:53:49

var walker = (function (){
var k, j = 0, that, arr = [];

return function ( ctx, callback, data, deep ) {

	for ( var i = 0, len = callback.length; i < len; i++ ){
		typeof callback[ i ] !== 'function' ? callback.splice( i, 1 ) : 0;
	}
	
	if ( callback.length && ctx && typeof ctx === 'object' ){ //don't iterate non-objects eg strings
		var ai = 0, aj_ = j++;
		!aj_ ? that = ctx : 0; //aj_ === 0 only twice; At the start and end
		
		for ( k in ctx ){
		
			i = 0; arr.push( ai++ );
			while (callback[ i ]) {
				callback[ i++ ].call( that, arr, k, ctx[ k ], data );
			}
			// use -typeof ctx[k]==='object'- to match both object and array objects
			if ( deep && ( typeof deep === 'number' || deep === true ) &&
				typeof ctx[ k ] === 'object' ){
			
				var deep_ = deep === true ? deep : Math.abs( deep ) - 1;
				walker( ctx[ k ], callback,data, deep_ );
			}
			arr.splice( aj_ );
		}
		j--;
	}
}})();