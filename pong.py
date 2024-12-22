# This example demonstrates moving of a rectangle 
# press r key to move the green rectangle to the right edge of the window
# press l key to move the green rectangle to the left edge of the window
import pygame,random,math

# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Pong')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 


# User-defined classes

class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # === game objects ====
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # === game specific objects ====
      self.paddle_increment = 10
      self.paddle1 = Paddle(40,(self.surface.get_height() / 2), 15,80,'white',self.surface)
      self.paddle2 = Paddle((self.surface.get_width() - 55),(self.surface.get_height() / 2), 15,80,'white',self.surface)
      self.both_players = [self.paddle1, self.paddle2]
      self.ball = Ball('white', 10, [250, 200], [6, 3], self.surface)
      self.p1_score = 0
      self.p2_score = 0
   def play(self):
      # Play the game until the player presses the close box.
      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()            
         if self.continue_game:
            self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         elif event.type == pygame.KEYDOWN:
            self.handle_key_down(event)
         elif event.type == pygame.KEYUP:
            self.handle_key_up(event)
   def handle_key_down(self,event):
      # reponds to KEYDOWN event
      if event.key == pygame.K_q:
         self.paddle1.set_vertical_velocity(-self.paddle_increment)
      elif event.key == pygame.K_a:
         self.paddle1.set_vertical_velocity(self.paddle_increment)
      if event.key == pygame.K_p:
         self.paddle2.set_vertical_velocity(-self.paddle_increment)
      elif event.key == pygame.K_l:
         self.paddle2.set_vertical_velocity(self.paddle_increment)      
   def handle_key_up(self,event):
      # responds to KEYUP event

      if event.key == pygame.K_q:
         self.paddle1.set_vertical_velocity(0)
      elif event.key == pygame.K_a:
         self.paddle1.set_vertical_velocity(0)         
      if event.key == pygame.K_p:
         self.paddle2.set_vertical_velocity(0)
      elif event.key == pygame.K_l:
         self.paddle2.set_vertical_velocity(0)       
   def draw(self):
      # Draw the score, the ball, and each paddle
      
      self.surface.fill(self.bg_color) # clear the display surface first
      self.ball.draw()
      self.paddle1.draw()
      self.paddle2.draw()
      self.draw_score()
      pygame.display.update() # make the updated surface appear on the display
   
   
   def update(self):
      # Update the game objects for the next frame.
      bounce = self.ball.move() # determine if the ball has bounced 
      if bounce == 'Player 1': # increment score accordingly
         self.p1_score += 1
      elif bounce == 'Player 2':
         self.p2_score += 1
      
      # move the paddles
      self.paddle1.move()   
      self.paddle2.move()   
      if self.paddle1.collide((self.ball.get_x()), (self.ball.get_y())) and self.ball.get_horizontal_velocity() < 0:
            self.ball.reverse_horizontal_velocity()  
      if self.paddle2.collide((self.ball.get_x()), (self.ball.get_y())) and self.ball.get_horizontal_velocity() > 0:
            self.ball.reverse_horizontal_velocity()              
   def draw_score(self):
      # draw the score at the top left corner of the window
      p1_score = ('Score: ' + str(self.p1_score))
      p2_score = ('Score: ' + str(self.p2_score))
      fg_color = pygame.Color('white')
      # create a font object
      font = pygame.font.SysFont('Comic Sans', 60)
      p1_box = font.render(p1_score, True, fg_color, self.bg_color)
      p2_box = font.render(p2_score, True, fg_color, self.bg_color)
      p1_location = (0, 0)
      p2_location = ((self.surface.get_width() - p2_box.get_width()), 0)
      self.surface.blit(p1_box, p1_location)
      self.surface.blit(p2_box, p2_location)

   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check
      if self.p1_score == 11 or self.p2_score == 11:
         self.continue_game = False
   
class Paddle:
   # An object in this class represents a Paddle that moves
   
   def __init__(self,x,y,width,height,color,surface):
      # - self is the Paddle object
      # - x, y are the top left corner coordinates of the rectangle of type int
      # - width is the width of the rectangle of type int
      # - height is the heightof the rectangle of type int
      # - surface is the pygame.Surface object on which the rectangle is drawn
      
      self.rect = pygame.Rect(x, y, width, height)
      self.color = pygame.Color(color)
      self.surface = surface
      self.vertical_velocity = 0  # paddle is not moving at the start
   def draw(self):
      # -self is the Paddle object to draw
      pygame.draw.rect(self.surface,self.color,self.rect)
   def set_vertical_velocity(self, vertical_distance):
      # set the horizontal velocity of the Paddle object
      # -self is the Paddle object
      # -horizontal_distance is the int increment by which the paddle moves horizontally
      self.vertical_velocity = vertical_distance
   def move(self):
      # moves the paddle such that paddle does not move outside the window
      # - self is the Paddle object
      self.rect.move_ip(0, self.vertical_velocity)
      if self.rect.bottom >= self.surface.get_height():
         self.rect.bottom = self.surface.get_height()
      elif self.rect.top  <= 0:
         self.rect.top = 0
   
   def collide(self, other_x, other_y):
      # 
      return self.rect.collidepoint(other_x, other_y)

         
   
class Ball:
   def __init__(self, ball_color, ball_radius, ball_center, ball_velocity, surface):
      # initializes the instace attributes of a ball
      self.color = pygame.Color(ball_color)
      self.radius = ball_radius
      self.center = ball_center
      self.velocity = ball_velocity
      self.surface = surface
   def draw(self):
      # draws the ball to the screen
      pygame.draw.circle(self.surface, self.color, self.center, self.radius)
   def move(self):  
      for i in range(0,2):
         # iterates each position and reverses velocity if edge collision occurs
         self.center[i] = self.center[i] + self.velocity[i]
         if self.center[i] <= self.radius or self.center[i] + self.radius >= self.surface.get_size()[i]:
            self.velocity[i] = -self.velocity[i]
            # determines who has scored depending on bouncing side
            if self.side_collision() == 'Left':
               return 'Player 2'
            elif self.side_collision() == 'Right':
               return 'Player 1'
   
   
   def side_collision(self):
      # returns the side the ball has collided with to decide score
      if self.center[0] <= self.radius:
         return 'Left'
      elif self.surface.get_width() <= (self.center[0] + self.radius):
         return 'Right'
      
   # ====== getter and setter methods for various ball attributes =======
   def get_x(self):
      return self.center[0]
   def get_y(self):
      return self.center[1]
   def get_horizontal_velocity(self):
      return self.velocity[0]
   def reverse_horizontal_velocity(self):
      self.velocity[0] = -self.velocity[0]
   def get_radius(self):
      return self.radius

main()