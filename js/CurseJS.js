/*
 * @author: timon w. mesulam
 * @email: timon.w.mesulam935xpacenuchra@gmail.com
 * @version: 0.0.7
 * @licence:
 * @date Thu, 07-04-2019 20:45:09
 * @description:
 */

//$(function() {
+function ( factory, root ) { "use stric";
	
    //if (!root[1]) throw("CurseJS requires JQuery to be defined!")

	factory( root[ 0 ], root[ 1 ] );
	
}( function( window, env ) {

var
	plugin = 'curse',
	version = '0.0.7',

	curse = function ( spec ){
	
		if ( !(this instanceof curse) ) {
			//protoCopy( curse,  E );
			//protoCopy(spec, E)
			return new curse( spec );
		}
		
		protoCopy(this, E);
		this.ctx = spec; // declare the context for use in E()

		//var i, r='';for (i in spec)/*spec.hasOwnProperty(i)?*/r+=i+': '+spec[ i ]+'\n\n';alert(spec+'\n\n\n\n'+r);
		return this ;
	};

	 
	function E () {
	// Keep this empty so it's easier to inherit from
	// (via https://github.com/lipsmack from https://github.com/scottcorgan/tiny-emitter/issues/3)
	}
	 
	E.prototype = {
	 	e: {},
	 	//NOTE: -this- is curse's context
	 	type: function( type ){
	 		for ( t in this.en) { if (t === type) return t; }
	 	},
	 	
		on: function (type, handler, data) {
			//-data- Array containing the arguments to pass to pass to the handlers
			var data = [].slice.call( arguments, data !== undefined ? 2 : 1 ),
				handler = typeof handler !== 'function' ? null : handler,
				e = this.e;
				
			( e[ type ] || (e[ type ] = []) ).push({
				fn: handler,
				ctx: this.ctx,
				data: data[ 0 ].splice ? data[ 0 ] : data
			});
			
			//alert('type: '+type+' ...data: '+data)
			walker( e[ type ], [function ( i ,k, v){
				//alert( this+'\n'+k+': '+v+'\n\n'+handler);
			}] )
			//alert(e[ type ][1].fn)
			//alert(typeof e[ type ][ 0 ][ 'type' ])
			//	var y, r='';for (y in this.types)/*this.hasOwnProperty(i)?*/r+=y+': '+this.types[ y ]+'\n\n';alert(curse+'\n\n\n\n'+r);
			return this;
		},
		
		once: function ( type, handler, data ) {
			var self = this,
				data = [].slice.call( arguments, data !== undefined ? 2 : 1 );

			function listener () {
				self.off(type, listener);
				handler.apply(self.ctx, arguments);
			};
			listener._ = handler;
			
			return this.on(type, listener, data[ 0 ]);
		},
		
		emit: function ( type, walk, deep ) {
			var
				evtArr = (this.e[ type ] || []).slice(),
				len = evtArr.length;
			
			if ( typeof type === 'function' ){
				deep = walk; // type = function; execute all handlers for all registerd -type-s
				
				for ( k in this.e ){
					var varr = this.e[ k ];
					
					for ( var i = 0, valen = varr.length; i < valen; i++ ){
						walker( varr[ i ].ctx, [ type, varr[ i ].fn ], [ varr[ i ].data, k ], deep );
					}
				}
			// if walk is'nt a function just supply it to walker()—it will be filterd out
			} else if ( len ) {
				typeof walk === 'function' ? walk = walk : deep = walk;
				
				for ( var i = 0; i < len; i++) {
					walker( evtArr[ i ].ctx, [ walk, evtArr[ i ].fn ], [ evtArr[ i ].data, type ], deep );
				 }
			}
			return this;
		},
		
		off: function (type, handler) {
			var e = this.e,
				liveEvents = [  ];
			
			if (e[ type ] && handler) {
			
				for (var i = 0, len = e[ type ].length; i < len; i++) {
						//	alert('off:\n\n\n'+e[ type ][ 0 ].fn._); //'off: evts && handler');
					if (e[ type ][ i ].fn !== handler && e[ type ][ i ].fn._ !== handler) {
					//	alert('::live')
						liveEvents.push( e[ type ][ i ] );
					}
				}
			}
			
			// Remove event from queue to prevent memory leak
			// Suggested by https://github.com/lazd
			// Ref: https://github.com/scottcorgan/tiny-emitter/commit/c6ebfaa9bc973b33d110a84a307742b7cf94c953#commitcomment-5024910
			liveEvents.length ? e[ type ] = liveEvents : delete e[ type ];
				//	var y, r='';for (y in e[ type ][ 0 ])/*this.hasOwnProperty(i)?*/r+=y+': '+e[ type ][ 0 ][ y ]+'\n\n';alert(curse+'\n\n\n\n'+r);
			return this;
		}
	}
	 
	function protoCopy( sub, sup ){
		var _sup = sup.prototype;
			
		if (typeof sub === 'function') sub.prototype = { _sup }['_sup'];

		Object.setPrototypeOf ? Object.setPrototypeOf( sub, { _sup }['_sup'] ) : sub.__proto__ = { _sup }['_sup'];
		//var i, r='';for (i in sub)r+=i+': '+sub[ i ]+'\n\n';alert(r);
	}
 
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
	
	 
	 
	 
	if ( env ){
		//alert( $ );
		$.fn['curse'] = function(  ){	
	}}

	window[ plugin ] = curse;
	
	return curse;
	
}, [ 
	(typeof window !== "undefined" ? window : this),
	(typeof jQuery !== "undefined" && jQuery)
 ])
//})



/*________________________________________________________________________________________

DOCUMENTATION (defacto).[ key concepts ]

________________________________________________________________________________________

Traverse JavaScript objects (objects and arrays) with added power to fire custom events s you go.


— For data and handlers in cache to be executed, you'll need to invoke the .emit() method with type,
  optional hander and or -deep- parameters to it.
  All data stored for specific or all registerd -type-s can optionally pass through a given handler
  before being executed by its bond handler as described below.

— NOTE:
  -ALWAYS the event type is sent as last and indices as first argmuments to the cached methods when
  the .fire() method is invoked for that specific event type.
  -If you supply a function as 1st or 2nd argmument to .emit(), it will be feed with the
  current indicies, key-value pairs of the object or array in context, and all handlers
  (if a function is 1st parameter) or handlers that have been registerd for a specific event
  type (if function is 2nd parameter) will be invoked.
  -Supply true (to iterate throug all levels) or a number -n- (to iterate upto n levels deep) as value
  to the -deep-  argument of .emit();
  
  //example
		var ctx = {spam: 3, foo: 'life'},
			arr = [ 'baz', ' ...bar' ];
			
		curse(ctx).once( 'evt', (a, b, c, d)=>{
			alert('ABC:\n\n'+a+'\n'+b+': '+c+' ...'+d );
		}, arr).on('', ER).on( 'evt1', ()=>{} )
			.emit( (x, y, z)=>{alert('E: '+x+' '+y+' '+z)} )
			.emit( 'evt', ( i )=>{ alert( 'Anonn: '+i ) }, true )
			.emit( '', 3 );
		
		function ER( i, k , v){
			alert( 'ER:\n\n'+i+'\n'+k+': '+v );
		}

*/