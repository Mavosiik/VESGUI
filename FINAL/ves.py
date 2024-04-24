def render_ves(ves, width):

  from random import randint

  def linePixels(A, B):
    pixels = []
    if A[0] == B[0]:
      if A[1] > B[1]:
          A,B=B,A
      for y in range(A[1], B[1] + 1):
        pixels.append((A[0], y))
    elif A[1] == B[1]:
      if A[0] > B[0]:
          A,B=B,A
      for x in range(A[0], B[0] + 1):
        pixels.append((x, A[1]))
    else:
      if A[0] > B[0]:
          A,B=B,A
      dx = B[0] - A[0]
      dy = B[1] - A[1]
      if abs(dy/dx) > 1:
        for y in range(min(A[1], B[1]), max(A[1], B[1]) + 1):
          x = int((y - A[1] + (dy/dx) * A[0]) * (dx/dy))
          pixels.append((x, y))
      else:
        for x in range(min(A[0], B[0]), max(A[0], B[0]) + 1):
          y = int((B[1] - A[1])/(B[0] - A[0]) * (x - A[0]) + A[1])
          pixels.append((x, y))
    return pixels
  def line(im, A, B, color):
      def draw_pixel(x, y):
          if 0 <= x < im.width and 0 <= y < im.height:
              im.putpixel((x, y), color)

      if A[0] == B[0] and A[1] == B[1]:
          return
      else:
          if A[0] == B[0]:
              if A[1] > B[1]:
                  A, B = B, A
              for y in range(A[1], B[1] + 1):
                  draw_pixel(A[0], y)
          elif A[1] == B[1]:
              if A[0] > B[0]:
                  A, B = B, A
              for x in range(A[0], B[0] + 1):
                  draw_pixel(x, A[1])
          else:
              if A[0] > B[0]:
                  A, B = B, A
              dx = B[0] - A[0]
              dy = B[1] - A[1]
              if abs(dy / dx) > 1:
                  for y in range(min(A[1], B[1]), max(A[1], B[1]) + 1):
                      x = int((y - A[1] + (dy / dx) * A[0]) * (dx / dy))
                      draw_pixel(x, y)
              else:
                  for x in range(min(A[0], B[0]), max(A[0], B[0]) + 1):
                      y = int((B[1] - A[1]) / (B[0] - A[0]) * (x - A[0]) + A[1])
                      draw_pixel(x, y)

  def thick_line(im, A, B, thickness, color):
    pixels = linePixels(A, B)
    for X in pixels:
      filled_circle(im, X, thickness, color)

  def filled_circle(im, S, r, color):
      w, h = im.size

      for x in range(0, int(r/2**(1/2))+1):
          y = int((r**2-x**2)**(1/2))

          line(im, (y + S[0], x + S[1]), (y + S[0], -x + S[1]), color)
          line(im, (x + S[0], y + S[1]), (x + S[0], -y + S[1]), color)
          line(im, (-x + S[0], y + S[1]), (-x + S[0], -y + S[1]), color)
          line(im, (-y + S[0], x + S[1]), (-y + S[0], -x + S[1]), color)

  def circle(im, S, r, thickness, color):
    for x in range(0, int(r/2**(1/2))+1):
      y = int((r**2-x**2)**(1/2))

      filled_circle(im, (x + S[0], y + S[1]), thickness, color)
      filled_circle(im, (y + S[0], x + S[1]), thickness, color)
      filled_circle(im, (y + S[0], -x + S[1]), thickness, color)
      filled_circle(im, (x + S[0], -y + S[1]), thickness, color)
      filled_circle(im, (-x + S[0], -y + S[1]), thickness, color)
      filled_circle(im, (-y + S[0], -x + S[1]), thickness, color)
      filled_circle(im, (-y + S[0], x + S[1]), thickness, color)
      filled_circle(im, (-x + S[0], y + S[1]), thickness, color)

  def random_star(im, w, h):
      # Random position for the center of the star
      center_x = randint(50, w - 50)
      center_y = randint(50, h - 50)

      # Size of the star
      size = randint(20, min(center_x, center_y, w - center_x, h - center_y) - 1)

      # Generate three points for the first triangle
      x1 = center_x
      y1 = center_y - size
      x2 = center_x + size
      y2 = center_y
      x3 = center_x - size
      y3 = center_y

      # Draw the first triangle with a random yellow color
      star_color = (255, 255, 0)  # RGB values for yellow
      fill_triangle(im, (x1, y1), (x2, y2), (x3, y3), star_color)

      # Calculate points for the second triangle based on the first one
      multiplier = 1.8  # Adjust this multiplier for proportional division
      ys1 = int(y1 + (y3 - y1) / multiplier)
      ys2 = int(y3 - (y3 - y1) / multiplier)
      xs1, xs2, xs3 = x3, x1, x2

      # Draw the second triangle with the same color
      fill_triangle(im, (xs1, ys1), (xs2, ys2), (xs3, ys2), star_color)

  def hex_to_rgb(hex_color):
      hex_color = hex_color.lstrip('#')
      return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

  def getY(point):
    return point[1]

  def fill_triangle(im, A, B, C, color):
      V = sorted([A,B,C], key=getY)
      left = linePixels(V[0], V[1]) + linePixels(V[1], V[2])
      right = linePixels(V[0], V[2])

      Xmax = max(A[0], B[0], C[0])
      Xmin = min(A[0], B[0], C[0])

      if V[1][0] == Xmax:
        left, right = right, left

      for y in range(getY(V[0]), getY(V[2])+1):
        x1 = Xmax
        for X in left:
          if X[1] == y and X[0] < x1:
            x1 = X[0]

        x2 = Xmin
        for X in right:
          if X[1] == y and X[0] > x2:
            x2 = X[0]

        line(im, (x1,y), (x2,y), color)

  def triangle(im, A, B, C, thickness, color):
      thick_line(im, A, B, thickness, color)
      thick_line(im, B, C, thickness, color)
      thick_line(im, C, A, thickness, color)

  def rect(im, x1, y1, width, height, thickness, color):
      x2, y2 = x1 + width, y1
      x3, y3 = x1 + width, y1 + height
      x4, y4 = x1, y1 + height

      thick_line(im, (x1, y1), (x2, y2), thickness, color)
      thick_line(im, (x2, y2), (x3, y3), thickness, color)
      thick_line(im, (x3, y3), (x4, y4), thickness, color)
      thick_line(im, (x4, y4), (x1, y1), thickness, color)

  def fill_rect(im, x1, y1, width, height, color):
    x2, y2 = x1 + width, y1
    x3, y3 = x1 + width, y1 + height
    x4, y4 = x1, y1 + height

    for x in range(x1, min(x2, im.width)):
        for y in range(y1, min(y3, im.height)):
            im.putpixel((x, y), color)

  gs, inv = 0, 0

  from PIL import Image, ImageOps

  with open('input.txt','w') as wf:
      wf.write(f'VES v1.0 {int(width)} {int(int(width)*(3/4))}\n')
      wf.write(ves)
      wf.close()

  with open('input.txt', 'r') as f:
      first_riadok = f.readline().split()

      filetype = first_riadok[0]

      if filetype == 'VES':
        w = int(first_riadok[2])
        h = int(first_riadok[3])

        print(f"w: {w}, h: {h}")
        obr = Image.new('RGB',(w, h), (255,255,255))
        for riadok in f:
            parts = riadok.split()
            if len(parts) >= 2:
                cmd = parts[0]

                if cmd == 'LINE':       #line
                    x1, y1, x2, y2, thickness, color = parts[1:7]
                    x1, y1, x2, y2, thickness = map(int, [x1, y1, x2, y2, thickness])
                    #print(f"LINE: ({x1}, {y1}) -> ({x2}, {y2}), Thickness: {thickness}, Color: {color}")
                    color = hex_to_rgb(color)
                    thick_line(obr, (x1,y1), (x2,y2),thickness,color)
                elif cmd == 'CLEAR':    #clear
                    color = parts[1]
                    color = hex_to_rgb(color)
                    for x in range(0, w):
                        for y in range(0, h):
                          obr.putpixel((x,y), color)
                    #print(f"CLEAR Color: {color}")
                elif cmd == 'RECT':      #rectangle
                    x1, y1, width, height, thickness, color = parts[1:7]
                    x1, y1, width, height, thickness = map(int, [x1, y1, width, height, thickness])
                    color = hex_to_rgb(color)
                    rect(obr,x1,y1,width,height,thickness,color)
                    #print(f"RECT: ({x1}, {y1}), Width: {width}, Height: {height}, Thickness: {thickness}, Color: {color}")
                elif cmd == 'TRIANGLE':   #triangle
                    x1, y1, x2, y2, x3, y3, thickness, color = parts[1:9]
                    x1, y1, x2, y2, x3, y3, thickness = map(int, [x1, y1, x2, y2, x3, y3, thickness])
                    color = hex_to_rgb(color)
                    triangle(obr, (x1,y1),(x2,y2),(x3,y3),thickness,color)
                    #print(f"TRIANGLE: ({x1}, {y1}), ({x2}, {y2}), ({x3}, {y3}), Thickness: {thickness}, Color: {color}")
                elif cmd == 'CIRCLE':     #circle
                    sx, sy, r, thickness, color = parts[1:6]
                    sx, sy, r, thickness = map(int, [sx, sy, r, thickness])
                    color = hex_to_rgb(color)
                    circle(obr,(sx,sy),r,thickness,color)
                    #print(f"CIRCLE: Center: ({sx}, {sy}), Radius: {r}, Thickness: {thickness}, Color: {color}")
                elif cmd == 'FILL_CIRCLE':  #fillcircle
                    sx, sy, r, color = parts[1:5]
                    sx, sy, r = map(int, [sx, sy, r])
                    color = hex_to_rgb(color)
                    filled_circle(obr,(sx,sy),r,color)
                    #print(f"FILL_CIRCLE: Center: ({sx}, {sy}), Radius: {r}, Color: {color}")
                elif cmd == 'FILL_TRIANGLE':  #filltriangle
                    x1, y1, x2, y2, x3, y3, color = parts[1:8]
                    x1, y1, x2, y2, x3, y3 = map(int, [x1, y1, x2, y2, x3, y3])
                    color = hex_to_rgb(color)
                    fill_triangle(obr, (x1,y1),(x2,y2),(x3,y3),color)
                    #print(f"FILL_TRIANGLE: ({x1}, {y1}), ({x2}, {y2}), ({x3}, {y3}), Color: {color}")
                elif cmd == 'FILL_RECT':       #fillrectangle
                    x1, y1, width, height, color = parts[1:6]
                    x1, y1, width, height = map(int, [x1, y1, width, height])
                    color = hex_to_rgb(color)
                    fill_rect(obr,x1,y1,width,height,color)
                    #print(f"FILL_RECT: ({x1}, {y1}), Width: {width}, Height: {height}, Color: {color}")

  return obr