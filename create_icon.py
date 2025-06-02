from PIL import Image, ImageDraw, ImageFont
import os

# Create a new image with a white background
size = (256, 256)
image = Image.new('RGB', size, 'white')
draw = ImageDraw.Draw(image)

# Draw a simple bee shape
def draw_bee():
    # Body (yellow ellipse)
    draw.ellipse([78, 98, 178, 158], fill='#FFD700')
    
    # Stripes (black)
    for i in range(3):
        y = 108 + i * 15
        draw.rectangle([98 + i*10, y, 158 - i*10, y+10], fill='black')
    
    # Wings (light blue)
    draw.ellipse([118, 68, 158, 108], fill='#ADD8E6')
    draw.ellipse([98, 68, 138, 108], fill='#ADD8E6')
    
    # Eyes (black dots)
    draw.ellipse([168, 118, 178, 128], fill='black')
    
    # Add text "MT" for Montana
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    draw.text((98, 178), "MT", fill='black', font=font)

# Draw the bee
draw_bee()

# Save as PNG first
image.save('app_icon.png')

# Convert to ICO
image.save('app_icon.ico', format='ICO', sizes=[(256, 256)]) 