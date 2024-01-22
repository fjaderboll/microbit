from microbit import *
import music
import random

class Apple:
    def __init__(self, x, y, blink_delay):
        self._x = x
        self._y = y
        self.blink_delay = blink_delay
    
    def x(self):
        return self._x

    def y(self):
        return self._y
    
    def draw(self):
        value = int((running_time() % self.blink_delay) / self.blink_delay * 9)
        display.set_pixel(self._x, self._y, value)

class Snake:
    def __init__(self, x, y, length, speed_delay):
        self.x = x
        self.y = y
        self.direction = 3
        self.next_direction = self.direction
        self._length = length
        self.next_length = length
        self.speed_delay = speed_delay
        self.tail = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        
        self.tail[self.x][self.y] = self._length
        self.last_move_time = running_time()

    def turn_left(self):
        self.next_direction = (self.direction + 1) % 4
        
    def turn_right(self):
        self.next_direction = (self.direction - 1) % 4
    
    def eat(self, apple):
        if self.test_collide(apple.x(), apple.y()):
            self.next_length = self._length + 1
            return True
        return False

    def test_collide(self, x, y):
        return self.tail[x][y] > 0
    
    def length(self):
        return self.next_length

    def move(self):
        if running_time() - self.last_move_time < self.speed_delay:
            return True
        
        self.direction = self.next_direction
        
        if self.direction == 0:
            self.x -= 1
        elif self.direction == 1:
            self.y += 1
        elif self.direction == 2:
            self.x += 1
        elif self.direction == 3:
            self.y -= 1
        
        if self.x < 0 or self.x >= 5 or self.y < 0 or self.y >= 5:
            return False # out of bounds
        elif self.tail[self.x][self.y] > 0:
            return False # hit tail
        
        if self._length == self.next_length: # move tail
            for x in range(len(self.tail)):
                for y in range(len(self.tail[x])):
                    if self.tail[x][y] >= 0:
                        self.tail[x][y] -= 1
        else: # don't move tail
            self._length = self.next_length
        
        self.tail[self.x][self.y] = self._length
        self.last_move_time = running_time()
        return True
    
    def draw(self):
        for x in range(len(self.tail)):
            for y in range(len(self.tail[x])):
                if self.tail[x][y] == 0:
                    display.set_pixel(x, y, 0) # clear trail
                    self.tail[x][y] = -1
                if self.tail[x][y] > 0:
                    value = min(9, self.tail[x][y] + max(2, 9 - self._length) )
                    display.set_pixel(x, y, value)

# ---------------------------------------
cdImage1 = Image("99999:90009:90009:90009:99999")
cdImage2 = Image("55555:59995:59095:59095:59095")
cdImage3 = Image("11111:15551:19991:19091:19091")
cdImage4 = Image("00000:01110:05550:09990:09090")

START_DELAY = 250
MOVE_DELAY = 500

def create_snake():
    global snake
    snake = Snake(2, 4, 1, MOVE_DELAY)
    snake.draw()

def create_apple():
    global apple
    while True:
        x = random.randint(0, 4)
        y = random.randint(0, 4)
        if not snake.test_collide(x, y):
            apple = Apple(x, y, 2000)
            apple.draw()
            return

def start_game():
    global game_on
    
    do_count_down()
    display.clear()
    create_snake()
    create_apple()
    game_on = True
    sleep(START_DELAY)

def end_game():
    global game_on
    
    music.pitch(300, 200)
    game_on = False
    sleep(START_DELAY * 4)
    music.pitch(300, 100)
    score = snake.length()
    display.scroll(str(score) + ' ', wait=False, loop=True)
    print('Game over! Score: ' + str(score) + ' points')

def do_count_down():
    freq = 1500
    for image in [cdImage1, cdImage2, cdImage3, cdImage4]:
        display.show(image)
        freq -= 300
        music.pitch(freq, START_DELAY)
    
    print('Game started')

# ---------------------------------------
print("Temperature: " + str(temperature()) + "*C")
display.show(Image.HEART)

snake = None
apple = None
game_on = False

while True:
    if game_on:
        if button_a.was_pressed():
            snake.turn_left()
        if button_b.was_pressed():
            snake.turn_right()
        
        alive = snake.move()
        snake.draw()
        apple.draw()
    
        if not alive:
            end_game()
        elif snake.eat(apple):
            music.pitch(1700, 100)
            create_apple()
    elif button_a.was_pressed() and button_b.was_pressed():
        start_game()
    
    sleep(50)

