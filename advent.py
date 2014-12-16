#
# adventure module
#

# A "direction" is all the ways you can describe going some way
directions = {}
NORTH = 1
SOUTH = 2
EAST = 3
WEST = 4
UP = 5
DOWN = 6
RIGHT = 7
LEFT = 8
IN = 9
OUT = 10
FORWARD = 11
BACK = 12
NORTH_WEST = 13
NORTH_EAST = 14
SOUTH_WEST = 15
SOUTH_EAST = 16
NOT_DIRECTION = -1

# map direction names to direction numbers
def define_direction( number, name ):
	# check to see if we are trying to redefine an existing direction
	if name in directions:
		print name, "is already defined as,", directions[name] 
	directions[name] = number

# see if a word is a defined direction
def lookup_dir( d ):
	if d in directions:
		return directions[d]
	else:
		return NOT_DIRECTION

define_direction( NORTH, "north" )
define_direction( NORTH, "n" )
define_direction( SOUTH, "south" )
define_direction( SOUTH, "s" )
define_direction( EAST, "east" )
define_direction( EAST, "e" )
define_direction( WEST, "west" )
define_direction( WEST, "w" )
define_direction( UP, "up" )
define_direction( UP, "u" )
define_direction( DOWN, "down" )
define_direction( DOWN, "d" )
define_direction( RIGHT, "right" )
define_direction( RIGHT, "r" )
define_direction( LEFT, "left" )
define_direction( LEFT, "l" )
define_direction( IN, "in" )
define_direction( OUT, "out" )
define_direction( FORWARD, "forward" )
define_direction( FORWARD, "fd" )
define_direction( FORWARD, "fwd" )
define_direction( FORWARD, "f" )
define_direction( BACK, "back" )
define_direction( BACK, "bk" )
define_direction( BACK, "b" )
define_direction( NORTH_WEST, "nw" )
define_direction( NORTH_EAST, "ne" )
define_direction( SOUTH_WEST, "sw" )
define_direction( SOUTH_EAST, "se" )

def proper_list_from_dict( d ):
	desc = ""
	stuff = []
	names = d.keys()
	if len(names) == 1:
		desc += "a "
		desc += names[0]
	else:
		for name in names[:-1]:
			stuff.append( name )
		desc += ", ".join( stuff )
		desc += " and a %s." % (names[-1])
	return desc

class Thing:
	name = ""			# short name of this thing
	description = ""
	fixed = False	# is it stuck or can it be taken

	def __init__( self, name, desc, fixed=False ):
		self.name = name
		self.description = desc
		self.fixed = fixed
	
	def describe( self ):
		return self.name

# A "location" is a place in the game.
class Location:
	name = ""			# short name of this location
	description = ""
	contents = None # things that are in a location
	exits = None		# ways to get out of a location
	first_time = True

	def __init__( self, name, desc ):
		self.name = name
		self.description = desc.strip()
		self.contents = {}
		self.exits = {}
		
	def put( self, thing ):
		self.contents[thing.name] = thing

	def describe( self, force=False ):
		desc = ""		# start with a blank string

		# add the description
		if self.first_time or force:
			desc += self.description
			self.first_time = True

		# any things here?
		if len(self.contents) > 0:
			# add a newline so that the list starts on it's own line
			desc += "\n"

			# is it just one thing?
			if len(self.contents) == 1:
				key = self.contents.keys()[0]
				desc += "There is a %s here." % self.contents[key].describe()
			else:
				# try to make a readable list of the things
				desc += "There are a few things here: "
				desc += proper_list_from_dict( self.contents )
		return desc

	def add_exit( self, con, way ):
		self.exits[ way ] = con
	
	def go( self, way ):
		if way in self.exits:
			c = self.exits[ way ]
			return c.point_b
		else:
			return None

	def debug( self ):
		for key in exits:
			print "exit:", directions[key], 

# A "connection" connects point A to point B. Connections are
# always described from the point of view of point A.
class Connection:
	name = ""
	description = ""
	point_a = None
	point_b = None

	def __init__( self, pa, name, pb ):
		self.name = name
		self.point_a = pa
		self.point_b = pb

# a World is how all the locations, things, and connections are organized
class World:
	locations = {}

	# make a connection between point A and point B
	def connect( self, point_a, name, point_b, way ):
		c = Connection( point_a, name, point_b )
		point_a.add_exit( c, way )
		return c

	# make a bidirectional between point A and point B
	def biconnect( self, point_a, point_b, name, ab_way, ba_way ):
		c1 = Connection( point_a, name, point_b )
		point_a.add_exit( c1, ab_way )
		c2 = Connection( point_b, name, point_a )
		point_b.add_exit( c2, ba_way )
		return c1, c2
	
	# add another location to the world
	def add_location( self, name, description ):
		l = Location( name, description )
		self.locations[name] = l
		return l
	
# A "person" is the actor in a world
class Person:
	world = None
	location = None
	inventory = None
	moved = False
	verbs = None

	def __init__( self, w ):
		self.world = w
		self.inventory = {}
		self.verbs = {}

		# associate each of the known actions with functions
		self.verbs['take'] = self.act_take
		self.verbs['inventory'] = self.act_inventory
		self.verbs['i'] = self.act_inventory
		self.verbs['look'] = self.act_look

	# describe where we are
	def describe( self ):
		return self.location.describe()
	
	# establish where we are "now"
	def set_location( self, loc ):
		self.location = loc
		self.moved = True

	# move a thing from the current location to our inventory
	def act_take( self, noun=None ):
		if noun in self.location.contents:
			t = self.location.contents[noun]
			del self.location.contents[noun]
			self.inventory[noun] = t
			return True
		else:
			return False
	
	def act_look( self, noun=None ):
		print self.location.describe( True )
	
	# list the things we're carrying
	def act_inventory( self, noun=None ):
		msg = ""
		if len(self.inventory.keys()) > 0:
			msg += "You are carrying "
			msg += proper_list_from_dict( self.inventory )
			print msg

	# check/clear moved status
	def check_if_moved( self ):
		status = self.moved
		self.moved = False
		return status

	# try to go in a given direction
	def go( self, d ):
		loc = self.location.go( d )
		if loc == None:
			print "Bonk! Sorry, you can't seem to go that way."
		else:
			# update where we are
			self.location = loc
			self.moved = True
		return self.location

	# define action verbs
	def define_action( self, verb, func ):
		self.verbs[verb] = func
	
	def perform_action( self, verb, noun=None ):
		if verb in self.verbs:
			self.verbs[verb]( noun )
			return True
		else:
			return False

	# do something
	def simple_act( self, verb ):
		d = lookup_dir( verb )
		if d == NOT_DIRECTION:
			# see if it's a known action
			if self.perform_action( verb ):
				return
			else:
				print "Sorry, I don't understand '%s'." % verb
		else:
			# try to move in the given direction
			self.location = self.go( d )

	# do something to something
	def act( self, verb, noun ):
		# "go" is a special case
		if verb == 'go':
			self.simple_act( noun )
		else:
			if self.perform_action( verb, noun ):
				return
			else:
				print "Oops. Don't know how to '%s'." % verb
