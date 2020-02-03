import colorsys
import cv2
import numpy as no

hue = 0
color = colorsys.hls_to_rgb(hue, 0.5, 0.8)

width = 30
height = 5
xStart = 10

img = np.zeros((512,512,3), np.uint8)

# draw the vertical start line
img = cv2.line(img,(xStart,0),(xStart,511),color,1)
img = cv2.line(img,(xStart+width,0),(xStart+width,511),color,1)

offset = 0

for x in range(20):
  offset += 1/x
  print(offset)

  # set new rectangle color
  hue += 0.05
  hue = hue % 1
  color = colorsys.hls_to_rgb(hue, 0.5, 0.8)


  xpos = xStart + offset * width
  # draw the actual rect
  cv2.rectangle(img,(xpos,x*height),(xpos+width,(x+1)*height),color,2)
  

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
