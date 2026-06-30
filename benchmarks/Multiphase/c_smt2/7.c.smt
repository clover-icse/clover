(set-logic LIA)

( declare-const v Int )
( declare-const v! Int )
( declare-const x Int )
( declare-const x! Int )
( declare-const y Int )
( declare-const y! Int )
( declare-const z Int )
( declare-const z! Int )
( declare-const tmp Int )
( declare-const tmp! Int )

( declare-const v_0 Int )
( declare-const v_1 Int )
( declare-const v_2 Int )
( declare-const v_3 Int )
( declare-const v_4 Int )
( declare-const x_0 Int )
( declare-const x_1 Int )
( declare-const x_2 Int )
( declare-const y_0 Int )
( declare-const y_1 Int )
( declare-const y_2 Int )
( declare-const z_0 Int )
( declare-const z_1 Int )
( declare-const z_2 Int )

( define-fun inv-f( ( v Int )( x Int )( y Int )( z Int )( tmp Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( v Int )( x Int )( y Int )( z Int )( tmp Int )( v_0 Int )( v_1 Int )( v_2 Int )( v_3 Int )( v_4 Int )( x_0 Int )( x_1 Int )( x_2 Int )( y_0 Int )( y_1 Int )( y_2 Int )( z_0 Int )( z_1 Int )( z_2 Int ) ) Bool
	( and
		( = v v_1 )
		( = x x_0 )
		( = y y_0 )
		( = z z_0 )
		( > x_0 y_0 )
		( > y_0 z_0 )
		( = v_1 0 )
	)
)

( define-fun trans-f ( ( v Int )( x Int )( y Int )( z Int )( tmp Int )( v! Int )( x! Int )( y! Int )( z! Int )( tmp! Int )( v_0 Int )( v_1 Int )( v_2 Int )( v_3 Int )( v_4 Int )( x_0 Int )( x_1 Int )( x_2 Int )( y_0 Int )( y_1 Int )( y_2 Int )( z_0 Int )( z_1 Int )( z_2 Int ) ) Bool
	( or
		( and
			( = v_2 v )
			( = x_1 x )
			( = y_1 y )
			( = z_1 z )
			( = v_2 v! )
			( = x_1 x! )
			( = y_1 y! )
			( = z_1 z! )
			( = v v! )
			( = x x! )
			( = y y! )
			( = z z! )
			(= tmp tmp! )
		)
		( and
			( = v_2 v )
			( = x_1 x )
			( = y_1 y )
			( = z_1 z )
			( < x_1 y_1 )
			( = v_3 ( + v_2 1 ) )
			( = v_4 v_3 )
			( = x_2 ( + x_1 1 ) )
			( = y_2 ( + y_1 3 ) )
			( = z_2 ( + z_1 2 ) )
			( = v_4 v! )
			( = x_2 x! )
			( = y_2 y! )
			( = z_2 z! )
			(= tmp tmp! )
		)
		( and
			( = v_2 v )
			( = x_1 x )
			( = y_1 y )
			( = z_1 z )
			( not ( < x_1 y_1 ) )
			( = v_4 v_2 )
			( = x_2 ( + x_1 1 ) )
			( = y_2 ( + y_1 3 ) )
			( = z_2 ( + z_1 2 ) )
			( = v_4 v! )
			( = x_2 x! )
			( = y_2 y! )
			( = z_2 z! )
			(= tmp tmp! )
		)
	)
)

( define-fun post-f ( ( v Int )( x Int )( y Int )( z Int )( tmp Int )( v_0 Int )( v_1 Int )( v_2 Int )( v_3 Int )( v_4 Int )( x_0 Int )( x_1 Int )( x_2 Int )( y_0 Int )( y_1 Int )( y_2 Int )( z_0 Int )( z_1 Int )( z_2 Int ) ) Bool
	( or
		( not
			( and
				( = v v_2)
				( = x x_1)
				( = y y_1)
				( = z z_1)
			)
		)
		( not
			( and
				( > ( - z_1 x_1 ) 72531 )
				( not ( > v_2 0 ) )
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f v x y z tmp v_0 v_1 v_2 v_3 v_4 x_0 x_1 x_2 y_0 y_1 y_2 z_0 z_1 z_2  )
		( inv-f v x y z tmp )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f v x y z tmp )
			( trans-f v x y z tmp v! x! y! z! tmp! v_0 v_1 v_2 v_3 v_4 x_0 x_1 x_2 y_0 y_1 y_2 z_0 z_1 z_2 )
		)
		( inv-f v! x! y! z! tmp! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f v x y z tmp  )
		( post-f v x y z tmp v_0 v_1 v_2 v_3 v_4 x_0 x_1 x_2 y_0 y_1 y_2 z_0 z_1 z_2 )
	)
))

