# -> Elusive
def start ():
	return "init",{}

def int_to_char(n):
	return chr (int (n)//256 )+chr (int (n)%256 )

def char_to_int(n):
	return ord (n [0])*256 +ord (n [1])

def get_accel(x1,y1,x2,y2,acc):
	xdiff = x2 - x1
	ydiff = y2 - y1
	hypotenuse =sqrt(xdiff**2+ydiff**2)
	if hypotenuse >0 :
		xmove =xdiff /hypotenuse *(acc *5 )
		ymove =ydiff /hypotenuse *(acc *5 )
	else :
		xmove =xdiff
		ymove =ydiff
	xspeed ,yspeed =get_velocity_tuple ()
	newxmove =(xmove -xspeed )*5
	newymove =(ymove -yspeed )*5
	newhypotenuse =sqrt (newxmove **2 +newymove **2 )
	if newhypotenuse ==0 :
		return 0 ,0
	else :
		return newxmove /newhypotenuse ,newymove /newhypotenuse


def turn_or_fire (angle1,angle2 ):
	turn_cw =0
	turn_ccw =0
	lock_on =False
	angle_diff =((angle1 -angle2 )+360 )%360
	if angle_diff <1 or angle_diff >359 :
		lock_on =True
	elif angle_diff >180 :
		turn_ccw =1
	else :
		turn_cw =1
	return turn_cw ,turn_ccw ,lock_on



def look_for_enemy ():
	found_enemy =False
	ang =None
	dis =None
	bonus =(None ,None ,None )
	for angle in range (0,359):
			(type,distance,bonus)=get_the_radar_data (angle)
			if type =="player":
				found_enemy = True
				dis = distance
				ang = angle
				break

	return found_enemy ,ang ,dis ,bonus

def get_weapon_xy(angle,distance):
	(px,py) = get_position_tuple()
	(wx,wy) = (px + distance * cos(angle), py + distance * sin(angle))
	return wx,wy

def look_for_weapons ():
	found_weapon =False
	ang = None
	dis = 10000
	bonus = None
	for angle in range (0,359):
			(type,distance,bonus)=get_the_radar_data(angle)
			x,y = get_weapon_xy(angle, distance)
			if type =="weapon" and not bonus and (x>150 or x<600 or y>150 or y<600):
				found_weapon = True
				if distance<dis:
					dis = distance
					ang = angle
				break

	return found_weapon ,ang ,dis ,bonus


def init():
	(curr_x ,curr_y )=get_position_tuple ()
	throw_angle =get_throwing_angle ()
	angle1 =(throw_angle +125 )%360
	angle2 =(throw_angle -125 )%360
	temp_angle =angle2
	collision =[]
	while not (temp_angle ==angle1 ):
		(type ,distance ,_ )=get_the_radar_data (temp_angle )
		if type =="column":
			collision.append(distance)
		else :
			collision.append(-1)
		if temp_angle >=360 :
			temp_angle -=360
		elif temp_angle <0 :
			temp_angle +=360
		temp_angle -= 1
	count1 =0
	temp_store =[]
	count2 =0
	store =[]
	for obj in range (len (collision )):
		if collision [obj]>0 :
			if collision[obj]-collision[obj-1]<5 or count1 ==0 :
				temp_store.append (obj)
				count1 +=1
			else :
				if count1 >count2 :
					store =temp_store [:]
					count2 =count1
				count1 =0
				temp_store =[]
		else :
			if count1 >count2 :
				store =temp_store [:]
				count2 =count1
			count1 =0
			temp_store =[]
	new_angle =angle2 -1 *store [int (count2 //2 )]
	(_ ,distance ,_ )=get_the_radar_data (new_angle )
	return "kowalski",{"SAVE_B":int_to_char (0),"SAVE_C":int_to_char (0),"SAVE_X":int_to_char (curr_x +cos (radians (new_angle ))*distance ),"SAVE_Y":int_to_char (curr_y +sin (radians (new_angle ))*distance ),"WEAPON":True }


def kowalski ():
	(curr_x ,curr_y )=get_position_tuple ()
	(curr_dx ,curr_dy )=get_velocity_tuple ()
	curr_angle =degrees (atan2 (curr_dx ,curr_dy ))
	(type ,distance ,_ )=get_the_radar_data (curr_angle )
	if type =="column"and distance <100 :
		return "back_off",{}
	stored =get_my_stored_data ()
	stored_x =char_to_int (stored [6 ])
	stored_y =char_to_int (stored [7 ])

	x_accel ,y_accel =get_accel (curr_x ,curr_y ,stored_x ,stored_y ,1 )
	distance =sqrt ((stored_x -curr_x )**2 +(stored_y -curr_y )**2 )

	if distance <100 :
		ang =int (round (degrees (atan2 (curr_y -stored_y ,curr_x -stored_x )),-1 ))
		return "run_away",{"SAVE_A":int_to_char (ang %360 ),"SAVE_X":stored [6 ],"SAVE_Y":stored [7 ],"ACLT_X":x_accel ,"ACLT_Y":y_accel ,"WEAPON":True }
	else :
		return "kowalski",{"SAVE_X":stored [6 ],"SAVE_Y":stored [7 ],"ACLT_X":x_accel ,"ACLT_Y":y_accel ,"WEAPON":True }


def run_away ():
	(curr_x ,curr_y )=get_position_tuple ()
	(curr_dx ,curr_dy )=get_velocity_tuple ()
	angle =degrees (atan2 (curr_dx ,curr_dy ))
	(type ,distance ,_)=get_the_radar_data (angle)
	if type =="column"and distance <100 :
		return "back_off",{}
	stored =get_my_stored_data ()
	stored_a =char_to_int (stored [0 ])
	stored_b =char_to_int (stored [1 ])
	stored_c =char_to_int (stored [2 ])
	stored_x =char_to_int (stored [6 ])
	stored_y =char_to_int (stored [7 ])
	throw_angle =get_throwing_angle ()
	target_angle =degrees (atan2 (stored_c -curr_y ,stored_b -curr_x ))
	turn_cw ,turn_ccw ,lock_on =turn_or_fire (target_angle ,throw_angle )
	if sqrt ((stored_x -curr_x )**2 +(stored_y -curr_y )**2 )>150 :
		return "back_off",{}
	b =stored_b
	c =stored_c
	x =stored_x +cos (radians (stored_a ))*80
	y =stored_y +sin (radians (stored_a ))*80
	if sqrt ((curr_x-x)**2 +(curr_y-y)**2 )<30 :
		curr_dx ,curr_dy =get_velocity_tuple ()
		distance =sqrt (curr_dx **2 +curr_dy **2 )
		if distance >0 :
			x_accel =-1 *curr_dx /distance
			y_accel =-1 *curr_dy /distance
		else :
			x_accel =0
			y_accel =0
		enemy_found ,enemy_angle ,enemy_distance ,enemy_bonus =look_for_enemy ()
		if enemy_found and enemy_distance>400 and not get_if_have_weapon():
			return "get_weapon",{}
		elif enemy_found and enemy_distance>200 and not enemy_bonus[1] and not get_if_have_weapon():
			return "get_weapon",{}


		elif (not enemy_found) and (not get_if_have_weapon()):
			return "get_weapon",{}
		elif get_if_have_weapon():
			angle = get_throwing_angle()
			(type,dis,bonus) = get_the_radar_data(angle)
			if type == "player" and dis<400 and not bonus[1]:
				return "run_away", {"SAVE_A": int_to_char(stored_a % 360), "SAVE_B": int_to_char(b),
									"SAVE_C": int_to_char(c), "SAVE_X": stored[6], "SAVE_Y": stored[7],
									"ACLT_X": x_accel, "ACLT_Y": y_accel, "ROT_CC": turn_cw, "ROT_CW": turn_ccw,
									"WEAPON": False}

		elif enemy_found:
			b =curr_x +cos (radians (enemy_angle ))*enemy_distance
			c =curr_y +sin (radians (enemy_angle ))*enemy_distance
			throw_angle =get_throwing_angle ()
			target_angle =degrees (atan2 (c -curr_y ,b -curr_x ))
			turn_cw ,turn_ccw ,lock_on =turn_or_fire (target_angle ,throw_angle )

			x1 =stored_x +cos (radians (stored_a +45 ))*70
			y1 =stored_y +sin (radians (stored_a +45 ))*70
			x2 =stored_x +cos (radians (stored_a -45 ))*70
			y2 =stored_y +sin (radians (stored_a -45 ))*70
			d1 =sqrt ((x1 -b )**2 +(y1 -c )**2 )
			d2 =sqrt ((x2 -b )**2 +(y2 -c )**2 )
			if d1 >d2 :
				stored_a +=45
			else :
				stored_a -=45

	else :
		x_accel,y_accel =get_accel (curr_x ,curr_y ,x ,y ,1 )

	return "run_away",{"SAVE_A":int_to_char (stored_a %360 ),"SAVE_B":int_to_char (b ),"SAVE_C":int_to_char (c ),"SAVE_X":stored [6 ],"SAVE_Y":stored [7 ],"ACLT_X":x_accel ,"ACLT_Y":y_accel ,"ROT_CC":turn_cw ,"ROT_CW":turn_ccw ,"WEAPON":not lock_on}


def back_off ():
	(curr_x,curr_y)=get_position_tuple()
	temp_angle = 0
	collision = []
	while temp_angle!=360:
		(type,distance,_)=get_the_radar_data(temp_angle )
		if type =="column":
			collision.append(distance)
		else:
			collision.append(-1)
		if temp_angle >=360 :
			temp_angle -=360 
		elif temp_angle <0 :
			temp_angle +=360 
		temp_angle +=1 
	count1 = 0 
	temp_store = []
	count2 = 0 
	store = []
	temp_angle = 0 
	for obj in range(len(collision)):
		if collision[obj]>0 :
			if collision[obj]-collision[obj-1]<5 or count1 ==0 :
				temp_store.append(obj)
				count1 +=1 
			else :
				if count1 >count2 :
					store =temp_store [:]
					count2 =count1 
				count1 =0 
				temp_store =[]
		else :
			if count1 >count2 :
				store =temp_store [:]
				count2 =count1 
			count1 =0 
			temp_store =[]
		temp_angle +=1 
	new_angle = store [int (count2 //2 )]
	(_ ,distance ,_ )=get_the_radar_data (new_angle )
	store_x =curr_x +cos (radians (new_angle ))*distance 
	store_y =curr_y +sin (radians (new_angle ))*distance 
	return "kowalski",{"SAVE_X":int_to_char (store_x ),"SAVE_Y":int_to_char (store_y ),"WEAPON":True }


def get_weapon():
	(curr_dx, curr_dy) = get_velocity_tuple()
	curr_angle = degrees(atan2(curr_dx, curr_dy))
	(type, distance, _) = get_the_radar_data(curr_angle)
	if type == "column" and distance < 100:
		return "back_off", {}
	(found_enemy,angle_e,dis_e,bonus_e) = look_for_enemy()
	(found_weapon,angle_w,dis_w,bonus_w) = look_for_weapons()
	if found_enemy and dis_e<200:
		return "run_away",{}
	elif found_enemy and dis_e<400 and bonus_e[1]:
		return "run_away", {}
	elif found_weapon and not get_if_have_weapon():
		x = cos(radians(angle_w))/10
		y = sin(radians(angle_w))/10
		return "get_weapon",{"ACLT_X":x ,"ACLT_Y":y, "WEAPON":True}
	else:
		return "run_away",{}