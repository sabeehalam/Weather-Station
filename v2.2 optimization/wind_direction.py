def windDirection(direction_resistance):  
    if 750 <= direction_resistance <= 830:
        direction = "north"
    elif 70 <= direction_resistance <= 130:
        direction = "east"
    elif 150 <= direction_resistance <= 230:
        direction = "south-east"
    elif 250 <= direction_resistance <= 330:
        direction = "south"
    elif 550 <= direction_resistance <= 700:
        direction = "south-west"
    elif 950 <= direction_resistance <= 990:
        direction = "west"
    elif 400 <= direction_resistance <= 500:
        direction = "north-east"
    elif 850 <= direction_resistance <= 925:
        direction = "north-west"
    else:
        direction = "changing"
    return direction
