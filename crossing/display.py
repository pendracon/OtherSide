#!/usr/bin/python3
# display.py
#
import pygame

# Screen globals
SCR_WIDTH = 800
SCR_HEIGHT = 600
SCR_TITLE = 'The Other Side'

# Color globals
CLR_WHITE = (255, 255, 255)
CLR_BLACK = (0, 0, 0)

class Crossing:
	# Run-loop globals
	CLOCK_RATE = 60  # "60fps"

	def __init__( self, title, width, height ):
		# Initialize resources
		pygame.init()
		pygame.font.init()
		self.FONT = pygame.font.SysFont( 'comicsans', 75 )

		# Set up the main screen
		pygame.display.set_caption( title )
		self.main_screen = pygame.display.set_mode( (width, height) )
		self.background = GameObject( 'assets/images/background.png', 0, 0, width, height )
		self.goal = GameObject( 'assets/images/treasure.png', 375, 25, 50, 50 )
	# End: def Crossing.__init__

	def run(self):
		# Start the run loop
		self.clock = pygame.time.Clock()
		DO_LOOP = True
		WINNER = False
		direction = 0
		player = PlayerCharacter( 'assets/images/player.png', 375, 525, 50, 50 )
		enemies = [
			NonPlayerCharacter( 'assets/images/enemy.png', 120, 150, 50, 50),
			NonPlayerCharacter( 'assets/images/enemy.png', 730, 300, 50, 50),
			NonPlayerCharacter( 'assets/images/enemy.png', 470, 450, 50, 50)]

		while DO_LOOP:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					DO_LOOP = False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						direction = 1
					elif event.key == pygame.K_DOWN:
						direction = -1
				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
						direction = 0

			self.refresh()

			player.move( direction )
			player.draw( self.main_screen )
			if player.isCollided( self.goal ):
				DO_LOOP = False
				WINNER = True

			for enemy in enemies:
				enemy.move( self.background.width )
				enemy.draw( self.main_screen )
				if player.isCollided( enemy ):
					DO_LOOP = False

			if not DO_LOOP:
				if WINNER:
					text = self.FONT.render( 'You WIN!', True, CLR_BLACK )
					DO_LOOP = True
					WINNER = False
				else:
					text = self.FONT.render( 'You Lose!', True, CLR_BLACK )

				self.main_screen.blit( text, (290, 265) )
				self.update( 1 )

				player.reset()
				for enemy in enemies:
					enemy.reset()
			else:
				self.update( self.CLOCK_RATE )

		# That's all folks!
		pygame.quit()
	# End: def Crossing.run

	def update( self, wait_time ):
		pygame.display.update()
		self.clock.tick( wait_time )
	# End: def Crossing.update

	def refresh( self ):
		self.main_screen.fill( CLR_WHITE )
		self.background.draw( self.main_screen )
		self.goal.draw( self.main_screen )
	# End: def Crossing.refresh

# End: class Crossing

class GameObject:

	def __init__( self, imagePath, xPos, yPos, imgWidth, imgHeight):
		self.x_pos = xPos
		self.y_pos = yPos
		self.width = imgWidth
		self.height = imgHeight
		self.starting_x_pos = self.x_pos
		self.starting_y_pos = self.y_pos

		# Load assets
		self.image = pygame.transform.scale( pygame.image.load(imagePath), (imgWidth, imgHeight) )
	# End: def GameObject.__init__

	def draw( self, surface ):
		surface.blit( self.image, [self.x_pos, self.y_pos] )
	# End: def GameObject.draw

	def reset( self ):
		self.x_pos = self.starting_x_pos
		self.y_pos = self.starting_y_pos
	# End: def GameObject.reset

# End: class GameObject

class PlayerCharacter(GameObject):

	MOVE_RATE = 10

	def __init__( self, imagePath, xPos, yPos, imgWidth, imgHeight ):
		super().__init__( imagePath, xPos, yPos, imgWidth, imgHeight )
	# End: def PlayerCharacter.__init__

	def move( self, direction ):
		if direction > 0:
			self.y_pos -= self.MOVE_RATE
		elif direction < 0:
			self.y_pos += self.MOVE_RATE
		if self.y_pos >= self.starting_y_pos:
			self.y_pos = self.starting_y_pos
	# End: def PlayerCharacter.move

	def isCollided( self, object ):
		collided = True

		if self.y_pos + self.height < object.y_pos or self.y_pos > object.y_pos + object.height:
			collided = False
		elif self.x_pos + self.width < object.x_pos or self.x_pos > object.x_pos + object.width:
			collided = False
		
		return collided
	# End: def PlayerCharacter.isCollided

# End: class PlayerCharacter

class NonPlayerCharacter(GameObject):

	MOVE_RATE = 10

	def __init__( self, imagePath, xPos, yPos, imgWidth, imgHeight ):
		super().__init__( imagePath, xPos, yPos, imgWidth, imgHeight )
	# End: def NonPlayerCharacter.__init__

	def move( self, max_width ):
		if self.x_pos <= 20:
			self.MOVE_RATE = abs(self.MOVE_RATE)
		elif self.x_pos >= max_width - (self.width + 20):
			self.MOVE_RATE = -abs(self.MOVE_RATE)
		self.x_pos += self.MOVE_RATE
	# End: def NonPlayerCharacter.move

# End: class PlayerCharacter

# Get the show on the road!
game = Crossing( SCR_TITLE, SCR_WIDTH, SCR_HEIGHT )
game.run()
quit()
