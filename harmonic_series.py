import colorsys
import cv2
import numpy as np

hue = 0
color = (colorsys.hls_to_rgb(hue, 0.7, 255))

window = 1000
towerHeight = 500
width = 50
height = float(window)/towerHeight
xStart = 10

img = np.zeros((window,window,3), np.uint8)

# draw the vertical start line
img = cv2.line(img,(xStart+width,0),(xStart+width,window-1),color,1)
img = cv2.line(img,(xStart+2*width,0),(xStart+2*width,window-1),color,1)

offset = 0.0
hue = 0.1

for x in range(1,towerHeight):
      offset += 1/(x)
      print()
      print(offset)

      # set new rectangle color
      hue += 1.0/towerHeight

      color = (colorsys.hls_to_rgb(hue, 0.7, 255))
      xpos = xStart + offset * width
      startPoint = (int(xpos),int(x*height))
      endPoint = (int(xpos+width),int((x+1)*height))
      print('start',startPoint)
      print('end',endPoint)
      # draw the actual rect
      img = cv2.rectangle(img,startPoint,endPoint,color,2)


# draw the vertical end line
endLinex = int(xStart + offset * width)
img = cv2.line(img,(endLinex,0),(endLinex,window-1),color,1)
img = cv2.line(img,(endLinex+width,0),(endLinex+width,window-1),color,1)


cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
