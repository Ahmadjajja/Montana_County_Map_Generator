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

def create_ico(input_file, output_file, sizes=None):
    if sizes is None:
        sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
    
    img = Image.open(input_file)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Create images for all sizes
    img_list = []
    for size in sizes:
        resized_img = img.resize(size, Image.Resampling.LANCZOS)
        img_list.append(resized_img)
    
    # Save the ICO file with all sizes
    img_list[0].save(
        output_file,
        format='ICO',
        sizes=[(img.width, img.height) for img in img_list],
        append_images=img_list[1:]
    )

if __name__ == '__main__':
    # If we have a PNG version, use that, otherwise use existing ICO
    if os.path.exists('app_icon.png'):
        input_file = 'app_icon.png'
    else:
        input_file = 'app_icon.ico'
    
    # Create temporary file first
    create_ico(input_file, 'temp_icon.ico')
    
    # If successful, replace the original
    if os.path.exists('temp_icon.ico'):
        if os.path.exists('app_icon.ico'):
            os.remove('app_icon.ico')
        os.rename('temp_icon.ico', 'app_icon.ico')
        print("Successfully created multi-size icon file!") 