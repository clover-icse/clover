(set-logic LIA)

( declare-const w Int )
( declare-const w! Int )
( declare-const x Int )
( declare-const x! Int )
( declare-const y Int )
( declare-const y! Int )
( declare-const z Int )
( declare-const z! Int )
( declare-const tmp Int )
( declare-const tmp! Int )

( declare-const w_0 Int )
( declare-const w_1 Int )
( declare-const w_2 Int )
( declare-const w_3 Int )
( declare-const w_4 Int )
( declare-const w_5 Int )
( declare-const x_0 Int )
( declare-const x_1 Int )
( declare-const x_2 Int )
( declare-const x_3 Int )
( declare-const y_0 Int )
( declare-const z_0 Int )

( define-fun inv-f( ( w Int )( x Int )( y Int )( z Int )( tmp Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( w Int )( x Int )( y Int )( z Int )( tmp Int )( w_0 Int )( w_1 Int )( w_2 Int )( w_3 Int )( w_4 Int )( w_5 Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( y_0 Int )( z_0 Int ) ) Bool
	( and
		( = w w_1 )
		( = x x_1 )
		( = y y_0 )
		( = z z_0 )
		( = x_1 0 )
		( = w_1 0 )
		( > y_0 z_0 )
	)
)

( define-fun trans-f ( ( w Int )( x Int )( y Int )( z Int )( tmp Int )( w! Int )( x! Int )( y! Int )( z! Int )( tmp! Int )( w_0 Int )( w_1 Int )( w_2 Int )( w_3 Int )( w_4 Int )( w_5 Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( y_0 Int )( z_0 Int ) ) Bool
	( or
		( and
			( = w_2 w )
			( = x_2 x )
			( = w_2 w! )
			( = x_2 x! )
			( = w w! )
			( = x x! )
			( = y y! )
			( = z z! )
			(= tmp tmp! )
		)
		( and
			( = w_2 w )
			( = x_2 x )
			( < x_2 z_0 )
			( = w_3 ( + w_2 1 ) )
			( = w_4 w_3 )
			( = x_3 ( + x_2 1 ) )
			( = w_4 w! )
			( = x_3 x! )
			(= y y_0 )
			(= y! y_0 )
			(= z z_0 )
			(= z! z_0 )
			(= tmp tmp! )
		)
		( and
			( = w_2 w )
			( = x_2 x )
			( not ( < x_2 z_0 ) )
			( = w_5 ( - w_2 2 ) )
			( = w_4 w_5 )
			( = x_3 ( + x_2 1 ) )
			( = w_4 w! )
			( = x_3 x! )
			(= y y_0 )
			(= y! y_0 )
			(= z z_0 )
			(= z! z_0 )
			(= tmp tmp! )
		)
	)
)

( define-fun post-f ( ( w Int )( x Int )( y Int )( z Int )( tmp Int )( w_0 Int )( w_1 Int )( w_2 Int )( w_3 Int )( w_4 Int )( w_5 Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( y_0 Int )( z_0 Int ) ) Bool
	( or
		( not
			( and
				( = w w_2)
				( = x x_2)
				( = y y_0)
				( = z z_0)
			)
		)
		( not
			( and
				( > x_2 ( + y_0 z_0 ) )
				( not ( <= w_2 0 ) )
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f w x y z tmp w_0 w_1 w_2 w_3 w_4 w_5 x_0 x_1 x_2 x_3 y_0 z_0  )
		( inv-f w x y z tmp )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f w x y z tmp )
			( trans-f w x y z tmp w! x! y! z! tmp! w_0 w_1 w_2 w_3 w_4 w_5 x_0 x_1 x_2 x_3 y_0 z_0 )
		)
		( inv-f w! x! y! z! tmp! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f w x y z tmp  )
		( post-f w x y z tmp w_0 w_1 w_2 w_3 w_4 w_5 x_0 x_1 x_2 x_3 y_0 z_0 )
	)
))

