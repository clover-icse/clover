(set-logic LIA)

( declare-const x Int )
( declare-const x! Int )
( declare-const y Int )
( declare-const y! Int )
( declare-const z Int )
( declare-const z! Int )
( declare-const tmp Int )
( declare-const tmp! Int )

( declare-const x_0 Int )
( declare-const x_1 Int )
( declare-const x_2 Int )
( declare-const y_0 Int )
( declare-const y_1 Int )
( declare-const y_2 Int )
( declare-const y_3 Int )
( declare-const z_0 Int )

( define-fun inv-f( ( x Int )( y Int )( z Int )( tmp Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( x Int )( y Int )( z Int )( tmp Int )( x_0 Int )( x_1 Int )( x_2 Int )( y_0 Int )( y_1 Int )( y_2 Int )( y_3 Int )( z_0 Int ) ) Bool
	( or
		( and
			( = x x_0 )
			( = y y_0 )
			( = z z_0 )
			( < x_0 0 )
			( > y_0 0 )
			( = z_0 0 )
			( or ( = z_0 0 ) ( = z_0 1 ) )
		)
		( and
			( = x x_0 )
			( = y y_0 )
			( = z z_0 )
			( < x_0 0 )
			( > y_0 0 )
			( not ( = z_0 0 ) )
			( or ( = z_0 0 ) ( = z_0 1 ) )
		)
	)
)

( define-fun trans-f ( ( x Int )( y Int )( z Int )( tmp Int )( x! Int )( y! Int )( z! Int )( tmp! Int )( x_0 Int )( x_1 Int )( x_2 Int )( y_0 Int )( y_1 Int )( y_2 Int )( y_3 Int )( z_0 Int ) ) Bool
	( or
		( and
			( = x_1 x )
			( = y_1 y )
			( = x_1 x! )
			( = y_1 y! )
			( = x x! )
			( = y y! )
			( = z z! )
			(= tmp tmp! )
		)
		( and
			( = x_1 x )
			( = y_1 y )
			( = ( mod x_1 2 ) z_0 )
			( = y_2 ( + y_1 2 ) )
			( = y_3 y_2 )
			( = x_2 ( + x_1 1 ) )
			( = x_2 x! )
			( = y_3 y! )
			(= z z_0 )
			(= z! z_0 )
			(= tmp tmp! )
		)
		( and
			( = x_1 x )
			( = y_1 y )
			( not ( = ( mod x_1 2 ) z_0 ) )
			( = y_3 y_1 )
			( = x_2 ( + x_1 1 ) )
			( = x_2 x! )
			( = y_3 y! )
			(= z z_0 )
			(= z! z_0 )
			(= tmp tmp! )
		)
	)
)

( define-fun post-f ( ( x Int )( y Int )( z Int )( tmp Int )( x_0 Int )( x_1 Int )( x_2 Int )( y_0 Int )( y_1 Int )( y_2 Int )( y_3 Int )( z_0 Int ) ) Bool
	( or
		( not
			( and
				( = x x_1)
				( = y y_1)
				( = z z_0)
			)
		)
		( not
			( and
				( > x_1 54932 )
				( not ( > y_1 54932 ) )
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f x y z tmp x_0 x_1 x_2 y_0 y_1 y_2 y_3 z_0  )
		( inv-f x y z tmp )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f x y z tmp )
			( trans-f x y z tmp x! y! z! tmp! x_0 x_1 x_2 y_0 y_1 y_2 y_3 z_0 )
		)
		( inv-f x! y! z! tmp! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f x y z tmp  )
		( post-f x y z tmp x_0 x_1 x_2 y_0 y_1 y_2 y_3 z_0 )
	)
))

