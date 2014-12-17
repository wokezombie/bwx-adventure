from advent import *

world = World()
# Sample Game - Brightworks Adventure!
loc_sidewalk = world.add_location(
"Sidewalk", """
You are standing in front of a large glass door.
The sign says 'Come In!'
""" )

loc_vestibule = world.add_location(
"Vestibule", """
A small area at the bottom of a flight of stairs.
There is an elevator here (currently locked).
Up the stars you see the reception desk.
""" )

loc_reception = world.add_location( "Reception Desk",
"""Behind an opening in the wall you see an unlit room.
There is a locked sliding door to the south, and an intersection to the north.
""" )

loc_intersection = world.add_location( "Intersection",
"""A boring intersection. There is a passageway to the
north that leads to the shop. To the east is the elevator
landing, to the west is the guest lounge, and to the
south is the reception desk. There is nothing to do here.
""" )

loc_elevator = world.add_location( "Elevator",
"""The elevator is turned off, but the door is open.
The controls on the elevator do not seem to work.
To the west is an intersection.
""" )

# the connections between the places
world.biconnect( loc_sidewalk, loc_vestibule, "Big Door", IN, OUT )
world.biconnect( loc_vestibule, loc_reception, "Stairs", UP, DOWN )
world.biconnect( loc_reception, loc_intersection, "A Few Steps", NORTH, SOUTH )
world.biconnect( loc_intersection, loc_elevator, "A Few Steps", EAST, WEST )

elev_key = Thing( "key", "small tarnished brass key" )
elev_lock = Thing( "lock", "ordinary lock" )
loc_sidewalk.put( elev_key )
loc_sidewalk.put( elev_lock )
loc_sidewalk.put( Thing( "pebble", "round pebble" ) )
loc_sidewalk.put( Thing( "Gary the garden gnome",
                          "a small figure liberated from a nearby garden." ) )

# make the player
hero = Person( world )

# start on the sidewalk
hero.set_location( loc_sidewalk )

# start playing
while True:
	# if the hero moved, describe the room
	if hero.check_if_moved():
		print
		print "        --=( %s )=--" % hero.location.name
		where = hero.describe()
		if len(where) > 0:
			print where

	# get input from the user
	command = raw_input("> ")
	if command == 'q' or command == 'quit':
		break
	words = command.split(" ")

	# reject any command that is more than two words
	if len( words ) > 2:
		print "Sorry, what?"
		continue

	# try to do what the user says
	if len( words ) == 2:
		# action object
		# e.g. take key
		verb, noun = words
		hero.act( verb, noun )
	else:
		# action (implied object/subject)
		# e.g. north
		hero.simple_act( words[0] )
