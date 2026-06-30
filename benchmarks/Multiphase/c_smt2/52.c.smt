(set-logic LIA)

( declare-const c0 Int )
( declare-const c0! Int )
( declare-const x Int )
( declare-const x! Int )
( declare-const y Int )
( declare-const y! Int )
( declare-const tmp Int )
( declare-const tmp! Int )

( declare-const c0_0 Int )
( declare-const c0_1 Int )
( declare-const x_0 Int )
( declare-const x_1 Int )
( declare-const x_2 Int )
( declare-const x_3 Int )
( declare-const y_0 Int )
( declare-const y_1 Int )
( declare-const y_2 Int )
( declare-const y_3 Int )
( declare-const y_4 Int )
( declare-const y_5 Int )

( define-fun inv-f( ( c0 Int )( x Int )( y Int )( tmp Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( c0 Int )( x Int )( y Int )( tmp Int )( c0_0 Int )( c0_1 Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( y_0 Int )( y_1 Int )( y_2 Int )( y_3 Int )( y_4 Int )( y_5 Int ) ) Bool
	( and
		( = c0 c0_1 )
		( = x x_1 )
		( = y y_1 )
		( = x_1 0 )
		( = c0_1 5000 )
		( = y_1 c0_1 )
	)
)

( define-fun trans-f ( ( c0 Int )( x Int )( y Int )( tmp Int )( c0! Int )( x! Int )( y! Int )( tmp! Int )( c0_0 Int )( c0_1 Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( y_0 Int )( y_1 Int )( y_2 Int )( y_3 Int )( y_4 Int )( y_5 Int ) ) Bool
	( or
		( and
			( = x_2 x )
			( = y_2 y )
			( = x_2 x! )
			( = y_2 y! )
			( = c0 c0! )
			( = x x! )
			( = y y! )
			(= tmp tmp! )
		)
		( and
			( = x_2 x )
			( = y_2 y )
			( >= x_2 c0_1 )
			( = y_3 ( + y_2 1 ) )
			( = y_4 y_3 )
			( = x_3 ( + x_2 1 ) )
			( = x_3 x! )
			( = y_4 y! )
			(= c0 c0_1 )
			(= c0! c0_1 )
			(= tmp tmp! )
		)
		( and
			( = x_2 x )
			( = y_2 y )
			( not ( >= x_2 c0_1 ) )
			( = y_5 ( - y_2 1 ) )
			( = y_4 y_5 )
			( = x_3 ( + x_2 1 ) )
			( = x_3 x! )
			( = y_4 y! )
			(= c0 c0_1 )
			(= c0! c0_1 )
			(= tmp tmp! )
		)
	)
)

( define-fun post-f ( ( c0 Int )( x Int )( y Int )( tmp Int )( c0_0 Int )( c0_1 Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( y_0 Int )( y_1 Int )( y_2 Int )( y_3 Int )( y_4 Int )( y_5 Int ) ) Bool
	( or
		( not
			( and
				( = c0 c0_1)
				( = x x_2)
				( = y y_2)
			)
		)
		( not
			( and
				( = x_2 ( * 2 c0_1 ) )
				( not ( = y_2 c0_1 ) )
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f c0 x y tmp c0_0 c0_1 x_0 x_1 x_2 x_3 y_0 y_1 y_2 y_3 y_4 y_5  )
		( inv-f c0 x y tmp )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f c0 x y tmp )
			( trans-f c0 x y tmp c0! x! y! tmp! c0_0 c0_1 x_0 x_1 x_2 x_3 y_0 y_1 y_2 y_3 y_4 y_5 )
		)
		( inv-f c0! x! y! tmp! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f c0 x y tmp  )
		( post-f c0 x y tmp c0_0 c0_1 x_0 x_1 x_2 x_3 y_0 y_1 y_2 y_3 y_4 y_5 )
	)
))

