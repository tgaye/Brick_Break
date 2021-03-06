# Remake of classic 'Brickbreak' game with Pygame
import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()

# Set the width and height of the screen. (w,h)
size = (700, 500)
screen = pygame.display.set_mode(size)

# Create our Ball object
class Ball(object):
    def __init__ (self, screen, radius,x,y):
        self.__screen = screen
        self._radius = radius
        self._xLoc = x
        self._yLoc = y
        self.__xVel = 5
        self.__yVel = -3
        w, h = pygame.display.get_surface().get_size()
        self.__width = w
        self.__height = h

    # Draws our ball
    def draw(self):
        pygame.draw.circle(screen,(255, 0, 0) , (self._xLoc,self._yLoc), int((self._radius * .75)))

    # Update balls location.  Detect collision.
    def update(self, paddle, brickwall):

        self._xLoc += self.__xVel
        self._yLoc += self.__yVel
        if self._xLoc == self._radius:
            self.__xVel *= -1
        elif self._xLoc >= self.__width - self._radius:
            self.__xVel *= -1
        if self._yLoc == self._radius:
            self.__yVel *= -1
        elif self._yLoc >= self.__height - self._radius:
            return True

        # If ball bounces off brick, Y velocity changes direction
        if brickwall.collide(self):
            self.__yVel *= -1

        # Collision detection between ball and paddle
        paddleX = paddle._xLoc
        paddleY = paddle._yLoc
        paddleW = paddle._width
        paddleH = paddle._height
        ballX = self._xLoc
        ballY = self._yLoc

        if ((ballX + self._radius) >= paddleX and ballX <= (paddleX + paddleW)) \
        and ((ballY + self._radius) >= paddleY and ballY <= (paddleY + paddleH)):
            self.__yVel *= -1

        return False
        
# Create our paddle object (player)
class Paddle (object):
    def __init__ (self, screen, width, height,x,y):
        self.__screen = screen
        self._width = width
        self._height = height
        self._xLoc = x
        self._yLoc = y
        w, h = pygame.display.get_surface().get_size()
        self.__W = w
        self.__H = h

    # Draw paddle
    def draw(self):
        pygame.draw.rect(screen, (0,0,0), (self._xLoc,self._yLoc,self._width,self._height),0)

    # Move paddle via mouse (player controls)
    def update(self):
        x,y = pygame.mouse.get_pos()
        if x >= 0 and x <= (self.__W - self._width):
            self._xLoc = x
 
# Create our brick object
class Brick (pygame.sprite.Sprite):
    def __init__(self, screen, width, height, x,y):
        self.__screen = screen
        self._width = width
        self._height = height
        self._xLoc = x
        self._yLoc = y
        w, h = pygame.display.get_surface().get_size()
        self.__W = w
        self.__H = h
        self.__isInGroup = True

    # Draws the brick onto screen: color = rgb(56, 177, 237)
    def draw(self):
        pygame.draw.rect(screen, (56, 177, 237), (self._xLoc,self._yLoc,self._width,self._height),0)

    # Add brick to group
    def add (self, group):
        group.add(self)
        self.__isInGroup = True

    # Remove brick from group
    def remove(self, group):
        group.remove(self)
        self.__isInGroup = False

    # Returns true if brick is in group (alive), false if not (hit).
    def alive(self):
        return self.__isInGroup

    # Detects collision between input ball object and this brick object
    def collide(self, ball):

        brickX = self._xLoc
        brickY = self._yLoc
        brickW = self._width
        brickH = self._height
        ballX = ball._xLoc
        ballY = ball._yLoc
        radius = ball._radius

        if ((ballX + radius) >= brickX and ballX <= (brickX + brickW)) \
        and ((ballY + radius) >= brickY and ballY <= (brickY + brickH)):
            return True

        return False


# Create our brickwall object (calls multiple brick() objects)
class BrickWall (pygame.sprite.Group):
    def __init__ (self,screen, x, y, width, height):
        self.__screen = screen
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._bricks = []

        X = x
        Y = y
        for i in range(3):
            for j in range(4):
                self._bricks.append(Brick(screen,width,height,X,Y))
                X += width + (width/ 7.0)
            Y += height + (height / 7.0)
            X = x

    # Add brick to this wall
    def add(self,brick):
        self._bricks.append(brick)

    # Remove brick from this wall
    def remove(self,brick):
        self._bricks.remove(brick)

    # Draws all bricks for wall
    def draw(self):

        for brick in self._bricks:
            if brick != None:
                brick.draw()

    # Check collision of ball, updates list of bricks.
    def update(self, ball):
        # Check collision
        for i in range(len(self._bricks)):
            if ((self._bricks[i] != None) and self._bricks[i].collide(ball)):
                self._bricks[i] = None
        
        # Update brick list
        for brick in self._bricks:
            if brick == None:
                self._bricks.remove(brick)

    # Check if player has won
    def hasWin(self):
        return len(self._bricks) == 0 # No bricks remaining

    # Collision detection.  Used in update() function.
    def collide (self, ball):
        for brick in self._bricks:
            if brick.collide(ball):
                return True
        return False

# The game objects: ball, paddle and brick wall
ball = Ball(screen,25,350,250)
paddle = Paddle(screen,100,20,250,450)
brickWall = BrickWall(screen,25,25,150,50)

# Game states:
isGameOver = False # determines whether game is lost
gameStatus = True # game is still running
done = False # loop until the user clicks the close button.
score = 0 # initial score for the game.

pygame.display.set_caption("Brickout-game") # set game title
clock = pygame.time.Clock() # used to manage how fast the screen updates
pygame.font.init() # for displaying text in the game

# Game messages:
mgGameOver = pygame.font.SysFont('Comic Sans MS', 60) # message for game over
mgWin = pygame.font.SysFont('Comic Sans MS', 60) # message for winning the game
mgScore = pygame.font.SysFont('Comic Sans MS', 60) # message for score

textsurfaceGameOver = mgGameOver.render('Game Over!', False, (0, 0, 0))
textsurfaceWin = mgWin.render("You win!",False,(0,0,0))
textsurfaceScore = mgScore.render("score: "+str(score),False,(0,0,0))
 
# Run our game
while not done:
    # Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(WHITE) # make screen white

    if gameStatus:
        brickWall.draw()

         # Track player score
        if brickWall.collide(ball):
            score += 10
        textsurfaceScore = mgScore.render("score: "+str(score),False,(0,0,0))
        screen.blit(textsurfaceScore,(300,0))
        brickWall.update(ball) # remove hit brick from list

        # Draw and update paddle (player)
        paddle.draw()
        paddle.update()

        # Game win and loss logic
        if ball.update(paddle, brickWall):
            isGameOver = True
            gameStatus = False

        if brickWall.hasWin():
            gameStatus = False
        ball.draw()

    else: # game isn't running.
        if isGameOver: # player lose
            screen.blit(textsurfaceGameOver,(0,0))
            textsurfaceScore = mgScore.render("score: "+str(score),False,(0,0,0))
            screen.blit(textsurfaceScore,(300,0))
        elif brickWall.hasWin(): # player win
            screen.blit(textsurfaceWin,(0,0))
            textsurfaceScore = mgScore.render("score: "+str(score),False,(0,0,0))
            screen.blit(textsurfaceScore,(300,0))

    pygame.display.flip() # update screen
    clock.tick(60) # set FPS

pygame.quit( )# close the window and quit.
