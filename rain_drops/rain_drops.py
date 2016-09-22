from microbit import *
import random

display_width = 5
display_height = 5

# Initialize rain drop list and empty image
rain_drops = []
image = Image(display_width, display_height)

# Infinite loop 
while True:
    
	# Create a new rain drop with 80% probability
    if random.random() <= 0.8:
		# Randomly choose a column  
        x = random.randint(0, display_width - 1)
		
		# Only create the rain drop if it's not in the same column as last one
        if not rain_drops or x != rain_drops[-1][0]:
            rain_drops.append((x, 0))
        
	# Iterate over existing rain drops	
    updated_rain_drops = []
    for x, y in rain_drops:
        
		# Display a rain drop as a pixel
        if y < display_height:
            image.set_pixel(x, y, 8)
        
		# Update rain drops location for next loop iteration by moving it down by 1
		# If rain drop has dropped sufficiently far down, it is removed
        if y <= 2 * display_height + 1:
            updated_rain_drops.append((x, y + 1))
        
	# Display the image and sleep 
    display.show(image)
    sleep(200)
    
	# Before new loop iteration, fade current pixels a bit so that rain drops create trails
    image = image * 0.45
    rain_drops = updated_rain_drops

    
    