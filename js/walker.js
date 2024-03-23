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
	j = -1,

	w = function (ctx){
		console.log({ctx})
		// Call `options.onNestChange(curIndx, prevIndx, curSubIndx, prevSubIndx, curKey, curCtx)`
		//if (j) onNestChange(j+1, aj_, 0, ai-1, 0, k, ctx)

		var k, ai = -1, aj_ = j++, arr = [aj_, -1];
		//if (!aj_) that = ctx; // aj_ === 0 only twice; At the start and end.
		
		for ( k in ctx ){
			console.log(':: ', k, ctx[k])
		
			i = -1; ai++;
			while (callbacks[ ++i ]) {
				callbacks[ i ].call( that, [aj_,j, ai], k, ctx[ k ], data );
			}
			// Use -typeof ctx[k]==='object'- to match both objects and arrays.
			// Implicit deep === true|false
			if (deep && typeof ctx[ k ] === 'object')
				strategy.run(ctx[ k ], callbacks, data, --deep );

			//arr.splice( aj_ );
		}
		console.log('onNestChange: ',{aj_,j,ai,ctx,deep})
		strategy.onNestChange(aj_, j, ai, )
		//arr[0] = j--;
		j--;
	},

	_strategy = {
		'bredth-first': function () {
			var nested, values = {};
			return {
				run: v => {
					nested = j
					console.log('<<<: ', {j,v,values,arguments});
					values[j] ? values[j].push(v) : values[j] = [v]
				},
				onNestChange: function () {
					console.log('>>>: ',{j,nested,values,arguments})
					if (nested == j){
						//nested = j
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
		deep = typeof deep === 'number' ? (deep >= 0 ? deep : 0) : (!!deep ? -1 : 0)
		w(ctx)
};


var ctx = {
	spam: 3, foo: 'life',
	m: {
		m0: { zero: 'zero' },
		m2: 'two',
	},
	ham: true,
},
arr = [ 'baz', 'bar' ],
abc = er = 0;
walker(ctx, [function(){/*console.log({...arguments})*/}],['data', 'ta'], {onNestChange:function(){/*console.log(arguments)*/}})