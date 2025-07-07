# Run this once in a separate file (e.g., create_image.py)

from PIL import Image

# Create a blank white image
img = Image.new('RGB', (640, 480), color=(255, 255, 255))
img.save("/home/user123/Bandhav_project/AI_lawyer/data/client/ravi_case/evidence/photo_1.jpg")
