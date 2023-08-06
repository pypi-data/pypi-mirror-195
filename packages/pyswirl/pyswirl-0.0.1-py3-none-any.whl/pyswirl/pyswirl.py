import turtle
import random
import time
import datetime
import io
from PIL import Image

class swirl:
    def __init__(self):
        self.default_color_palette = ['#537c78', '#7ba591', '#cc222b', '#f15b4c', '#faa41b', '#ffd45b']
        self.color_palette = self.default_color_palette
        self.spiral = turtle.Turtle()
        self.cursor_speed = 100
        self.spiral.speed(self.cursor_speed)
        self.spiral.hideturtle()
        self.shuffle_style = False
        self.width_bias = 0
    def get_random_colors(self):
        k = random.randint(1,2)
        if k == 1:
            return self.random_hex_colors(random.randint(4,30))
        if k == 2:
            return self.generate_pastel_colors(random.randint(4,30))
    def set_random_bg(self):
        bg_clr = self.get_random_colors()[0]
        self.spiral.screen.bgcolor(bg_clr)
    def set_style(self, style=None, color_style=None, num_colors=None, bg_style=None):
        if style == "random":
            self.color_palette = self.get_random_colors()
            self.set_random_bg()
        elif style == "shuffle":
            self.shuffle_style = True
        elif style == "default":
            self.color_palette = self.default_color_palette
            self.spiral.screen.bgcolor("#ffffff")
        else:
            self.shuffle_style = False
            if color_style == "random":
                k = random.randint(1,2)
                if k == 1:
                    if num_colors:
                        self.color_palette = self.random_hex_colors(num_colors)
                    else:
                        self.color_palette = self.random_hex_colors(random.randint(4,30))
                if k == 2:
                    if num_colors:
                        self.color_palette = self.generate_pastel_colors(num_colors)
                    else:
                        self.color_palette = self.generate_pastel_colors(random.randint(4,30))
            elif color_style == "all colors":
                if num_colors:
                    self.color_palette = self.random_hex_colors(num_colors)
                else:
                    self.color_palette = self.random_hex_colors(random.randint(4,30))
            elif color_style == "pastel":
                if num_colors:
                    self.color_palette = self.generate_pastel_colors(num_colors)
                else:
                    self.color_palette = self.generate_pastel_colors(random.randint(4,30))
            elif color_style == "default":
                self.color_palette = self.default_color_palette
            else:
                if color_style:
                    if color_style[0][0] == "#":
                        self.color_palette = color_style
                    else:
                        raise("Invalid color style. Please supply a list of Hex color codes.")
            if bg_style == "random":
                self.set_random_bg()
            else:
                if bg_style:
                    if bg_style[0] == "#":
                        self.spiral.screen.bgcolor(bg_style)
    def reset(self):
        self.spiral.home()
        self.spiral.clear()
        self.spiral.pencolor("black")
        self.spiral.width(1 / 100 + 1)
        self.dist = 1
        self.width_bias = 0
    def change_width(self, width_speed = None):
        if width_speed:
            self.spiral.width((self.dist / 100 + 1))
        else:
            self.spiral.width((self.dist / 200 + 1))
        self.width_bias+=1
    def draw(self, angle, width_speed = None, iterations = 500, random_moves = False, change_colors = False, change_width = False, circles = False, rhombus= False):
        self.reset()
        if self.shuffle_style:
            self.set_style(style="random")
        for iter in range(iterations):
            # print(angle, iter)
            if change_colors:
                self.spiral.pencolor(self.color_palette[self.dist % len(self.color_palette)])
            if change_width:
                if width_speed:
                    self.change_width(width_speed)
                else:
                    self.change_width()
            if circles:
                self.spiral.circle(self.dist)
            if rhombus:
                for _ in range(4):
                    self.spiral.forward(self.dist)
                    self.spiral.right(60)
                    if change_width:
                        self.change_width()
            if random_moves:
                seed = random.randint(1,3)
                for _ in range(seed):
                    self.spiral.forward(self.dist)
                    self.spiral.right(60)
                    if change_width:
                        self.change_width()
                if self.dist%2 == 0:
                    self.dist+=10
            self.spiral.forward(self.dist)
            self.spiral.right(angle)
            self.dist+=1
            self.cursor_speed+=2000
            self.spiral.speed(self.cursor_speed)
    def save_result(self, File_name = None, png = False, eps = True):
            ts = self.spiral.getscreen().getcanvas().postscript(colormode="color")
            if not File_name:
                File_name = f"Untitled - {str(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))}"
            if png:
                im = Image.open(io.BytesIO(ts.encode("utf-8")))
                im.save(f"{File_name}.png", format="PNG")
            if eps:
                self.spiral.getscreen().getcanvas().postscript(file=f"{File_name}.eps")
    def clear(self):
        time.sleep(3)
        self.spiral.clear()
    def random_hex_colors(self, num_colors):
        hex_digits = "0123456789ABCDEF"
        colors = []
        for i in range(num_colors):
            color = "#" + "".join(random.choice(hex_digits) for _ in range(6))
            colors.append(color)
        return colors
    def generate_pastel_colors(self, n):
        """Generate a list of n random pastel colors in hexadecimal format"""
        pastel_colors = []
        for i in range(n):
            red = random.randint(128, 255)
            green = random.randint(128, 255)
            blue = random.randint(128, 255)
            pastel_colors.append('#{:02x}{:02x}{:02x}'.format(red, green, blue))
        return pastel_colors
    def play_demo(self):
        k_vals = list(range(1, 25))
        random.shuffle(k_vals)
        for k in k_vals:
            if k == 1:
                self.set_style(style="shuffle")
                self.set_style(color_style=["#7b4b8b", "#828b4b"], bg_style="#ffffff")
                self.draw(185, iterations=127, circles=True, change_colors=True)
                self.clear()
            if k == 2:
                self.draw(270, iterations=200, circles=True, change_width=True, change_colors=True)
                self.clear()
            if k == 3:
                self.set_style(style="shuffle")
                self.draw(245, iterations=200, change_colors=True)
                self.clear()
            if k == 4:
                self.set_style(color_style=["#556B2F", "#6B8E23", "#808000", "#8FBC8F", "#9ACD32"], bg_style="#ffffff")
                self.draw(150, iterations=200, circles=True, change_width=True, change_colors=True)
                self.clear()
            if k == 5:
                self.set_style(color_style=["#BDB76B", "#DAA520", "#CD853F", "#8B4513", "#006400"], bg_style="#ffffff")
                self.draw(103, iterations=200, circles=True, change_width=True, change_colors=True)
                self.clear()
            if k == 6:
                self.set_style(color_style="default", bg_style="#ffffff")
                self.draw(119, iterations=200, change_colors=True)
                self.clear()
            if k == 7:
                self.draw(64, iterations=200, change_colors=True)
                self.clear()
            if k == 8:
                self.draw(61, iterations=200, change_colors=True)
                self.clear()
            if k == 9:
                self.draw(59, iterations=200, change_colors=True)
                self.clear()
            if k == 10:
                self.set_style(color_style="all colors", bg_style="#FFFFFF", num_colors=2)
                self.draw(48, iterations=200, change_colors=True)
                self.clear()
            if k == 11:
                self.set_style(color_style="pastel", bg_style="#000000", num_colors=2)
                self.draw(118, iterations=200, change_colors=True)
                self.clear()
            if k == 12:
                self.set_style(style="default")
                self.draw(103, iterations=200, change_colors=False)
                self.clear()
            if k == 13:
                self.draw(103, iterations=200, change_colors=False)
                self.clear()
            if k == 14:
                self.draw(91, iterations=200, change_colors=False)
                self.clear()
            if k == 15:
                self.draw(165, iterations=200, change_colors=False)
                self.clear()
            if k == 16:
                self.draw(121, iterations=200, change_colors=False)
                self.clear()
            if k == 17:
                self.draw(123, iterations=200, change_colors=False)
                self.clear()
            if k == 18:
                self.draw(120, iterations=200, change_colors=False)
                self.clear()
            if k == 19:
                self.draw(108, iterations=200, change_colors=False)
                self.clear()
            if k == 20:
                self.draw(108, iterations=200, change_colors=False)
                self.clear()
            if k == 21:
                self.draw(60, iterations=200, change_colors=False, circles=True)
                self.clear()
            if k == 22:
                self.draw(80, iterations=200, change_colors=False, circles=True)
                self.clear()
            if k == 23:
                self.draw(182, iterations=200, change_colors=False, circles=True)
                self.clear()
            if k == 24:
                self.set_style(color_style="default", bg_style="#ffffff", num_colors=5)
                self.draw(144, iterations=200, circles=True, change_colors=True)
                self.clear()