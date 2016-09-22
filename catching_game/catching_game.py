from microbit import *
import random


DISPLAY_HEIGHT = 5
DISPLAY_WIDTH = 5
PLAYER_REFRESH_RATE = 100


class GameState(object):
    
    def __init__(self, level=0):
        self.player = (2, 4)
        self.rain_drops = []
        self.player_image = Image(DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.rain_drop_image = Image(DISPLAY_WIDTH, DISPLAY_HEIGHT)
        
        self.level = LEVELS[level]
        
        self.score = 0
        self.rate = 0
        
        display.scroll('Level %s' % (self.level.num,))
    
    def run_single_step(self):
        
        if self.rate >= self.level.rain_drop_refresh_rate:
    		self.update_rain_drops()
    		self.update_rain_drop_image()
    		
    		self.rate = 0
    		
    	self.update_player_image()
    	
        display.show(self.player_image + self.rain_drop_image)
        sleep(PLAYER_REFRESH_RATE)
        self.rate += PLAYER_REFRESH_RATE
    	
        collision = self.detect_collision()
        self.check_game_conditions(collision)
        
    def update_player_image(self):
        self.player_image.set_pixel(self.player[0], self.player[1], 0)
        self.update_player()
        self.player_image.set_pixel(self.player[0], self.player[1], 8)
        
    def update_player(self):
        left = button_a.was_pressed() or button_a.is_pressed()
        right = button_b.was_pressed() or button_b.is_pressed()
        
        player_x = self.player[0]
        if left and not right:
            player_x -= 1
            
        elif right and not left:
    	    player_x += 1
    	    
        player_x = max(0, min(player_x, DISPLAY_WIDTH - 1))
        self.player = (player_x, self.player[1])
    	
    def update_rain_drops(self):
        
        updated_rain_drops = []
        
        # Create a new rain drop with certain probability
        if random.random() <= self.level.rain_drop_probability:
            # Randomly choose a column  
            x = random.randint(0, DISPLAY_WIDTH - 1)
            
            # Only create the rain drop if it's not in the same column as last one
            if not self.rain_drops or x != self.rain_drops[-1][0]:
                updated_rain_drops.append((x, 0))
            
        # Iterate over existing rain drops	
        for x, y in self.rain_drops:
            
    		# Update rain drops location by moving it down by 1
    		# If rain drop has dropped sufficiently far down, it is removed
            if y <= 2 * DISPLAY_HEIGHT + 1:
                updated_rain_drops.append((x, y + 1))
            
        self.rain_drops = updated_rain_drops
    	
    def update_rain_drop_image(self):
    	rain_drop_image = self.rain_drop_image * 0.45
    	
    	for x, y in self.rain_drops:
    		# Display a rain drop as a pixel
    		if y < DISPLAY_HEIGHT:
    		    rain_drop_image.set_pixel(x, y, 8)
    			
    	self.rain_drop_image = rain_drop_image
        
    def detect_collision(self):
        
        for x, y in self.rain_drops:
            
            if self.player[0] == x and self.player[1] == y:
                return 1
            
            elif y >= DISPLAY_HEIGHT:
                return -1
        
        return 0
    	
    def check_game_conditions(self, collision):
        
        if collision == -1:
            display.scroll('Game over')
            self.__init__()
            return
            
        elif collision == 1:
            self.score += 1
            
            self.rain_drops = list(
                filter(
                    lambda x: x[0] != self.player[0] or x[1] != self.player[1],
                    self.rain_drops
                )
            )
            
            # display.scroll(str(self.score))
            
        if len(LEVELS) > self.level.num + 1 and self.score >= LEVELS[self.level.num + 1].min_score:
            self.level = LEVELS[self.level.num + 1]
            display.scroll('Level %s' % (self.level.num,))
            
            
    
class Level(object):
    
    def __init__(self, num, min_score, rain_drop_refresh_rate, rain_drop_probability):
        self.num = num
        self.min_score = min_score
        self.rain_drop_refresh_rate = rain_drop_refresh_rate
        self.rain_drop_probability = rain_drop_probability
    

LEVELS = [
    Level(0, 0, 400, 0.2)    
]

game_state = GameState()

while True:
    game_state.run_single_step()
	
		
	
	
