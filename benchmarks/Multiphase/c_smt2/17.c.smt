(set-logic LIA)

( declare-const v Int )
( declare-const v! Int )
( declare-const w Int )
( declare-const w! Int )
( declare-const x Int )
( declare-const x! Int )
( declare-const z Int )
( declare-const z! Int )
( declare-const tmp Int )
( declare-const tmp! Int )

( declare-const v_0 Int )
( declare-const v_1 Int )
( declare-const v_2 Int )
( declare-const v_3 Int )
( declare-const v_4 Int )
( declare-const w_0 Int )
( declare-const w_1 Int )
( declare-const w_2 Int )
( declare-const w_3 Int )
( declare-const w_4 Int )
( declare-const x_0 Int )
( declare-const x_1 Int )
( declare-const x_2 Int )
( declare-const z_0 Int )
( declare-const z_1 Int )
( declare-const z_2 Int )

( define-fun inv-f( ( v Int )( w Int )( x Int )( z Int )( tmp Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( v Int )( w Int )( x Int )( z Int )( tmp Int )( v_0 Int )( v_1 Int )( v_2 Int )( v_3 Int )( v_4 Int )( w_0 Int )( w_1 Int )( w_2 Int )( w_3 Int )( w_4 Int )( x_0 Int )( x_1 Int )( x_2 Int )( z_0 Int )( z_1 Int )( z_2 Int ) ) Bool
	( and
		( = v v_1 )
		( = w w_1 )
		( = x x_0 )
		( = z z_0 )
		( > x_0 z_0 )
		( = v_1 0 )
		( = w_1 0 )
	)
)

( define-fun trans-f ( ( v Int )( w Int )( x Int )( z Int )( tmp Int )( v! Int )( w! Int )( x! Int )( z! Int )( tmp! Int )( v_0 Int )( v_1 Int )( v_2 Int )( v_3 Int )( v_4 Int )( w_0 Int )( w_1 Int )( w_2 Int )( w_3 Int )( w_4 Int )( x_0 Int )( x_1 Int )( x_2 Int )( z_0 Int )( z_1 Int )( z_2 Int ) ) Bool
	( or
		( and
			( = v_2 v )
			( = w_2 w )
			( = x_1 x )
			( = z_1 z )
			( = v_2 v! )
			( = w_2 w! )
			( = x_1 x! )
			( = z_1 z! )
			( = v v! )
			( = w w! )
			( = x x! )
			( = z z! )
			(= tmp tmp! )
		)
		( and
			( = v_2 v )
			( = w_2 w )
			( = x_1 x )
			( = z_1 z )
			( < x_1 z_1 )
			( = v_3 ( + v_2 1 ) )
			( = v_4 v_3 )
			( = w_3 w_2 )
			( = x_2 ( + x_1 1 ) )
			( = z_2 ( + z_1 2 ) )
			( = v_4 v! )
			( = w_3 w! )
			( = x_2 x! )
			( = z_2 z! )
			(= tmp tmp! )
		)
		( and
			( = v_2 v )
			( = w_2 w )
			( = x_1 x )
			( = z_1 z )
			( not ( < x_1 z_1 ) )
			( = w_4 ( + w_2 1 ) )
			( = v_4 v_2 )
			( = w_3 w_4 )
			( = x_2 ( + x_1 1 ) )
			( = z_2 ( + z_1 2 ) )
			( = v_4 v! )
			( = w_3 w! )
			( = x_2 x! )
			( = z_2 z! )
			(= tmp tmp! )
		)
	)
)

( define-fun post-f ( ( v Int )( w Int )( x Int )( z Int )( tmp Int )( v_0 Int )( v_1 Int )( v_2 Int )( v_3 Int )( v_4 Int )( w_0 Int )( w_1 Int )( w_2 Int )( w_3 Int )( w_4 Int )( x_0 Int )( x_1 Int )( x_2 Int )( z_0 Int )( z_1 Int )( z_2 Int ) ) Bool
	( or
		( not
			( and
				( = v v_2)
				( = w w_2)
				( = x x_1)
				( = z z_1)
			)
		)
		( not
			( and
				( > v_2 1000 )
				( not ( > w_2 0 ) )
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f v w x z tmp v_0 v_1 v_2 v_3 v_4 w_0 w_1 w_2 w_3 w_4 x_0 x_1 x_2 z_0 z_1 z_2  )
		( inv-f v w x z tmp )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f v w x z tmp )
			( trans-f v w x z tmp v! w! x! z! tmp! v_0 v_1 v_2 v_3 v_4 w_0 w_1 w_2 w_3 w_4 x_0 x_1 x_2 z_0 z_1 z_2 )
		)
		( inv-f v! w! x! z! tmp! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f v w x z tmp  )
		( post-f v w x z tmp v_0 v_1 v_2 v_3 v_4 w_0 w_1 w_2 w_3 w_4 x_0 x_1 x_2 z_0 z_1 z_2 )
	)
))

