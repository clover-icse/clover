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
( declare-const x_3 Int )
( declare-const y_0 Int )
( declare-const z_0 Int )
( declare-const z_1 Int )
( declare-const z_2 Int )
( declare-const z_3 Int )
( declare-const z_4 Int )

( define-fun inv-f( ( x Int )( y Int )( z Int )( tmp Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( x Int )( y Int )( z Int )( tmp Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( y_0 Int )( z_0 Int )( z_1 Int )( z_2 Int )( z_3 Int )( z_4 Int ) ) Bool
	( and
		( = x x_1 )
		( = y y_0 )
		( = z z_1 )
		( = x_1 0 )
		( >= y_0 25 )
		( = z_1 0 )
	)
)

( define-fun trans-f ( ( x Int )( y Int )( z Int )( tmp Int )( x! Int )( y! Int )( z! Int )( tmp! Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( y_0 Int )( z_0 Int )( z_1 Int )( z_2 Int )( z_3 Int )( z_4 Int ) ) Bool
	( or
		( and
			( = x_2 x )
			( = z_2 z )
			( = x_2 x! )
			( = z_2 z! )
			( = x x! )
			( = y y! )
			( = z z! )
			(= tmp tmp! )
		)
		( and
			( = x_2 x )
			( = z_2 z )
			( >= y_0 ( div x_2 50 ) )
			( = z_3 ( + z_2 1 ) )
			( = z_4 z_3 )
			( = x_3 ( + 1 x_2 ) )
			( = x_3 x! )
			( = z_4 z! )
			(= y y_0 )
			(= y! y_0 )
			(= tmp tmp! )
		)
		( and
			( = x_2 x )
			( = z_2 z )
			( not ( >= y_0 ( div x_2 50 ) ) )
			( = z_4 z_2 )
			( = x_3 ( + 1 x_2 ) )
			( = x_3 x! )
			( = z_4 z! )
			(= y y_0 )
			(= y! y_0 )
			(= tmp tmp! )
		)
	)
)

( define-fun post-f ( ( x Int )( y Int )( z Int )( tmp Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( y_0 Int )( z_0 Int )( z_1 Int )( z_2 Int )( z_3 Int )( z_4 Int ) ) Bool
	( or
		( not
			( and
				( = x x_2)
				( = y y_0)
				( = z z_2)
			)
		)
		( not
			( and
				( > x_2 ( * 50 y_0 ) )
				( not ( > z_2 0 ) )
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f x y z tmp x_0 x_1 x_2 x_3 y_0 z_0 z_1 z_2 z_3 z_4  )
		( inv-f x y z tmp )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f x y z tmp )
			( trans-f x y z tmp x! y! z! tmp! x_0 x_1 x_2 x_3 y_0 z_0 z_1 z_2 z_3 z_4 )
		)
		( inv-f x! y! z! tmp! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f x y z tmp  )
		( post-f x y z tmp x_0 x_1 x_2 x_3 y_0 z_0 z_1 z_2 z_3 z_4 )
	)
))

