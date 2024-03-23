/*
*@date Thu, 11-04-2019 06:53:49
*@description: A function employing depth-first traversal of objects, invoking callbacks for each key-value travesed
*/



/*
* @param [ctx]: Object    the object to iterate.
* @param [callbacks]: Array    An array of callbacks to be invoked on each traversal.
* @param [data]: Any    The data to passed to the callback; It can be anything - it's user defined.
* @param [deep]: Number|Boolen    Flag indicating the traversing depth (if a Number > 0) or if Boolean wether to
*                                 enable travering deep into the object - `false` makes the travesal only on
*                                 the first level, `true` enables traversing all levels.
*
*/
var walker = function (ctx, callbacks, data, options) {

	var options = {
		strategy: //'depth-first',
		'bredth-first',
		onNestChange: () => {},
		deep: true,
		...options
	};

	var that = ctx,
	{ onNestChange, deep } = options,
	j = 0,

	w = function (ctx){
		console.log({ctx})
		// Call `options.onNestChange(curIndx, prevIndx, curSubIndx, prevSubIndx, curKey, curCtx)`
		if (j) onNestChange(j+1, aj_, 0, ai-1, 0, k, ctx)

		var 
		var k, ai = 0, arr = [j, -1], aj_ = j++;
		//if (!aj_) that = ctx; // aj_ === 0 only twice; At the start and end.
		
		for ( k in ctx ){
		
			i = 0; arr[1] =  ++ai;
			while (callbacks[ i ]) {
				callbacks[ i++ ].call( that, [j,ai-1], k, ctx[ k ], data );
			}
			// Use -typeof ctx[k]==='object'- to match both objects and arrays.
			// Implicit deep === true|false
			if ( deep > 0 && ( typeof deep === 'number' || deep === true )
				&& typeof ctx[ k ] === 'object'
			)
				strategy.run(ctx[ k ], callbacks, data, deep = Math.abs( deep ) - 1 );

			//arr.splice( aj_ );
		}
		strategy.onNestChange(j, )
		//arr[0] = j--;
		j--;
	},

	_strategy = {
		'bredth-first': function () {
			var nested = false, values = {};
			return {
				run: v => {console.log('<<<: ', {j,v,values,arguments});values[j] ? values[j].push(v) : values[j] = [v]},
				onNestChange: function () {
					console.log('>>>: ',{j,nested,values})
					if (!nested) {
						nested = true
						for (v of values[j]) w(v);
						// avoid memory leaks
						delete values[j]
					
					}
					onNestChange.apply(that, arguments)
				},
			}
		}(),
		'depth-first': {
			run: w,
			onNestChange: function (){ onNestChange.apply(that, arguments) },
		}
	};

	var strategy = _strategy[options.strategy]
	if (!strategy) throw("Unkown strategy!")

	// Remove non-`function`s from callbacks.
	for ( var i = 0, len = callbacks.length; i < len; i++ )
		if (typeof callbacks[ i ] !== 'function') callbacks.splice( i, 1 );

	if (callbacks.length && ctx && typeof ctx === 'object') // Don't iterate non-objects eg strings.
		w(ctx)
};


var ctx = {
	spam: 3, foo: 'life',
	m: {
		m0: 'zero',
		m2: 'two',
	}
},
arr = [ 'baz', 'bar' ],
abc = er = 0;
walker(ctx, [function(){console.log({...arguments})}],['data', 'ta'])