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
( declare-const x_4 Int )
( declare-const x_5 Int )
( declare-const z_0 Int )
( declare-const z_1 Int )
( declare-const z_2 Int )
( declare-const z_3 Int )
( declare-const z_4 Int )

( define-fun inv-f( ( x Int )( z Int )( tmp Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( x Int )( z Int )( tmp Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( x_4 Int )( x_5 Int )( z_0 Int )( z_1 Int )( z_2 Int )( z_3 Int )( z_4 Int ) ) Bool
	( and
		( = x x_1 )
		( = z z_1 )
		( = x_1 0 )
		( = z_1 0 )
	)
)

( define-fun trans-f ( ( x Int )( z Int )( tmp Int )( x! Int )( z! Int )( tmp! Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( x_4 Int )( x_5 Int )( z_0 Int )( z_1 Int )( z_2 Int )( z_3 Int )( z_4 Int ) ) Bool
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
			( < ( * x_2 5 ) z_2 )
			( = x_3 ( + x_2 1 ) )
			( = x_4 x_3 )
			( = z_3 z_2 )
			( = x_4 x! )
			( = z_3 z! )
			(= tmp tmp! )
		)
		( and
			( = x_2 x )
			( = z_2 z )
			( not ( < ( * x_2 5 ) z_2 ) )
			( = x_5 ( div x_2 10 ) )
			( = z_4 ( + 1 z_2 ) )
			( = x_4 x_5 )
			( = z_3 z_4 )
			( = x_4 x! )
			( = z_3 z! )
			(= tmp tmp! )
		)
	)
)

( define-fun post-f ( ( x Int )( z Int )( tmp Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( x_4 Int )( x_5 Int )( z_0 Int )( z_1 Int )( z_2 Int )( z_3 Int )( z_4 Int ) ) Bool
	( or
		( not
			( and
				( = x x_2)
				( = z z_2)
			)
		)
		( not
			( and
				( > z_2 50 )
				( not ( > z_2 x_2 ) )
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f x z tmp x_0 x_1 x_2 x_3 x_4 x_5 z_0 z_1 z_2 z_3 z_4  )
		( inv-f x z tmp )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f x z tmp )
			( trans-f x z tmp x! z! tmp! x_0 x_1 x_2 x_3 x_4 x_5 z_0 z_1 z_2 z_3 z_4 )
		)
		( inv-f x! z! tmp! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f x z tmp  )
		( post-f x z tmp x_0 x_1 x_2 x_3 x_4 x_5 z_0 z_1 z_2 z_3 z_4 )
	)
))

