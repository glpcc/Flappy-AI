
def comprobar_colisiones(pajaro,tubo):
	if pajaro.pos_x == tubo.pos_x :
		pajaro.score = pajaro.score + 1
	if pajaro.pos_y > 480 or pajaro.pos_y < 20:
		return True
	
	if (tubo.pos_x - 20) <= pajaro.pos_x <= (tubo.pos_x + 70):
		if (tubo.pos_y - 45) <= pajaro.pos_y <= (tubo.pos_y + 45):
			return False
		else:
			return True
	else:
		return False



