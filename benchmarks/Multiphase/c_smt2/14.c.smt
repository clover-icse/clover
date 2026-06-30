(set-logic LIA)

( declare-const x Int )
( declare-const x! Int )
( declare-const z Int )
( declare-const z! Int )
( declare-const tmp Int )
( declare-const tmp! Int )

( declare-const x_0 Int )
( declare-const x_1 Int )
( declare-const x_2 Int )
( declare-const x_3 Int )
( declare-const z_0 Int )
( declare-const z_1 Int )
( declare-const z_2 Int )
( declare-const z_3 Int )
( declare-const z_4 Int )
( declare-const z_5 Int )

( define-fun inv-f( ( x Int )( z Int )( tmp Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( x Int )( z Int )( tmp Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( z_0 Int )( z_1 Int )( z_2 Int )( z_3 Int )( z_4 Int )( z_5 Int ) ) Bool
	( and
		( = x x_1 )
		( = z z_1 )
		( = x_1 -100 )
		( = z_1 -100 )
	)
)

( define-fun trans-f ( ( x Int )( z Int )( tmp Int )( x! Int )( z! Int )( tmp! Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( z_0 Int )( z_1 Int )( z_2 Int )( z_3 Int )( z_4 Int )( z_5 Int ) ) Bool
	( or
		( and
			( = x_2 x )
			( = z_2 z )
			( = x_2 x! )
			( = z_2 z! )
			( = x x! )
			( = z z! )
			(= tmp tmp! )
		)
		( and
			( = x_2 x )
			( = z_2 z )
			( = x_3 ( mod ( + x_2 1 ) 5 ) )
			( < z_2 4 )
			( = z_3 ( + z_2 1 ) )
			( = z_4 z_3 )
			( = x_3 x! )
			( = z_4 z! )
			(= tmp tmp! )
		)
		( and
			( = x_2 x )
			( = z_2 z )
			( = x_3 ( mod ( + x_2 1 ) 5 ) )
			( not ( < z_2 4 ) )
			( = z_5 ( mod z_2 4 ) )
			( = z_4 z_5 )
			( = x_3 x! )
			( = z_4 z! )
			(= tmp tmp! )
		)
	)
)

( define-fun post-f ( ( x Int )( z Int )( tmp Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( z_0 Int )( z_1 Int )( z_2 Int )( z_3 Int )( z_4 Int )( z_5 Int ) ) Bool
	( or
		( not
			( and
				( = x x_2)
				( = z z_2)
			)
		)
		( not
			( and
				( >= z_2 0 )
				( not ( = x_2 z_2 ) )
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f x z tmp x_0 x_1 x_2 x_3 z_0 z_1 z_2 z_3 z_4 z_5  )
		( inv-f x z tmp )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f x z tmp )
			( trans-f x z tmp x! z! tmp! x_0 x_1 x_2 x_3 z_0 z_1 z_2 z_3 z_4 z_5 )
		)
		( inv-f x! z! tmp! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f x z tmp  )
		( post-f x z tmp x_0 x_1 x_2 x_3 z_0 z_1 z_2 z_3 z_4 z_5 )
	)
))

