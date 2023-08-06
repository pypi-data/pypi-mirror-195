from time import sleep as _sleep;from os import system as _sys, name as _name, get_terminal_size as _size


class Utils:

    """
    functions -> 6:
        Init()       |      Initialize the command prompt to print colors
        Clear()      |      Clear the command prompt
        Title()      |      [!]Only for Windows systems: set the title of the command prompt
        Type()       |      Print slowly a string, it can use with :input(), Col.
        HideCursor() |      Hide the cursor (the white thing that blinking in the command prompt)
        ShowCursor() |      Show the cursor (the white thing that blinking in the command prompt)
    """

    def Init() -> None:
        _sys("")

    def Title(content: str) -> None:
        if _name == 'nt':
            return _sys(f"title {content}")
    def Clear() -> None:
        if _name == 'nt':
            return _sys("cls")
        else:
            return _sys("clear")

    def Type(text: str, cursor: bool = True, speed: float or int = 0.00004, new_line: bool = False) -> str:
        if cursor:
            Utils.HideCursor()
        
        for i in text:
            print(i, end="", flush=True)
            _sleep(speed)

        if new_line:
            print()

        return "" # to concatenate str 

    def HideCursor() -> str:
        print("\033[?25l", end='')
        
    def ShowCursor() -> str:
        print("\033[?25h", end='')


class Textspace:
    def getspace(text: str) -> int (1 or 0):
        return len(text) - len(text.lstrip())

class Dynamic:
    
    """
    variables -> 43:
        Dynamic Colors | All the colors to do gradient
        reset          | Reset the command prompt color with white
    """

    black_to_white = ["/;/;/"]
    black_to_red = ["/;0;0"]
    black_to_green = ["0;/;0"]
    black_to_blue = ["0;0;/"]
    black_to_cyan = ["0;/;/"]
    black_to_purple = ["/;0;/"]
    black_to_yellow = ["/;/;0"]

    blue_to_black = ["0;0;c"]
    blue_to_white = ["/;/;255"]
    blue_to_cyan = ["0;/;255"]
    blue_to_purple = ["/;0;255"]
    blue_to_red = ["c;0;/"]
    blue_to_green = ["0;/;c"]
    blue_to_yellow = ["/;/;c"]

    cyan_to_green = ["0;255;c"]
    cyan_to_blue = ["0;c;255"]
    cyan_to_white = ["/;255;255"]
    cyan_to_black = ["0;c;c"]
    cyan_to_purple = ["/;c;255"]
    cyan_to_yellow = ["/;255;c"]
    cyan_to_red = ["/;c;c"]

    green_to_black = ["0;c;0"]
    green_to_white = ["/;255;/"]
    green_to_yellow = ["/;255;0"]
    green_to_cyan = ["0;255;/"]
    green_to_purple = ["/;c;/"]
    green_to_red = ["/;c;0"]
    green_to_blue = ["0;c;/"]

    purple_to_red = ["255;0;c"]
    purple_to_blue = ["c;0;255"]
    purple_to_white = ["255;/;255"]
    purple_to_black = ["c;0:c"]
    purple_to_cyan = ["c;/;255"]
    purple_to_yellow = ["255;/;c"]
    purple_to_green = ["c;/;c"]
    purple_to_brown = ["105;60;c"]
    
    red_to_black = ["c;0;0"]
    red_to_white = ["255;/;/"]
    red_to_yellow = ["255;/;0"]
    red_to_purple = ["255;0;/"]
    red_to_blue = ["c;0;/"]
    red_to_green = ["c;/;0"]
    red_to_cyan = ["c;/;/"]

    white_to_black = ["c;c;c"]
    white_to_red = ["255;c;c"]
    white_to_green = ["c;255;c"]
    white_to_blue = ["c;c;255"]
    white_to_cyan = ["c;255;255"]
    white_to_purple = ["255;c;255"]
    white_to_yellow = ["255;255;c"]

    yellow_to_red = ["255;c;0"]
    yellow_to_green = ["c;255;0"]
    yellow_to_white = ["255;255;/"]
    yellow_to_black = ["c;c;0"]
    yellow_to_cyan = ["c;255;/"]
    yellow_to_purple = ["255;c;/"]
    yellow_to_blue = ["c;c;/"]
    yellow_to_pink = ["255;c;140"]

    pink_to_yellow = ["255;/;140"]

    brown_to_purple = ["105;60;/"]

    lightblue_to_lightgreen = ["191;215;c"]

    lightgreen_to_lightblue = ["191;215;/"]

    all_colors = [
        red_to_black, red_to_white, red_to_yellow, red_to_purple, red_to_blue, red_to_green, red_to_cyan,
        green_to_black, green_to_white, green_to_yellow, green_to_cyan, green_to_purple, green_to_red, green_to_blue,
        blue_to_black, blue_to_white, blue_to_cyan, blue_to_purple, blue_to_red, blue_to_green, blue_to_yellow,

        yellow_to_red, yellow_to_green, yellow_to_white, yellow_to_black, yellow_to_cyan, yellow_to_purple, yellow_to_blue, yellow_to_pink,
        purple_to_red, purple_to_blue, purple_to_white, purple_to_black, purple_to_cyan, purple_to_yellow, purple_to_green, purple_to_brown,
        cyan_to_green, cyan_to_blue, cyan_to_white, cyan_to_black, cyan_to_purple, cyan_to_yellow, cyan_to_red,

        black_to_white, black_to_red, black_to_green, black_to_blue, black_to_cyan, black_to_purple, black_to_yellow,
        white_to_black, white_to_red, white_to_green, white_to_blue, white_to_cyan, white_to_purple, white_to_yellow,

        pink_to_yellow,

        brown_to_purple,

        lightblue_to_lightgreen
    ]

    for color in all_colors:
        color_sub = 240
        color_add = 10

        content = color[0]
        color.pop(0)

        for _ in range(24):
            if ('c' and '/') in content:
                color.append(content.replace('c', str(color_sub)).replace('/', str(color_add)))
            else:
                if 'c' in content:
                    color.append(content.replace('c', str(color_sub)))

                elif '/' in content:
                    color.append(content.replace('/', str(color_add)))

            color_add += 10
            color_sub -= 10

        color.extend(color[::-1])

class Colors:
    reset = '\033[38;2;255;255;255m'

    white = "\033[38;2;255;255;255m"
    black = "\033[38;2;0;0;0m"

    red = "\033[38;2;255;0;0m"
    green = "\033[38;2;0;255;0m"
    blue = "\033[38;2;0;0;255m"

    purple = "\033[38;2;255;0;255m"
    cyan = "\033[38;2;0;255;255m"
    yellow = "\033[38;2;255;255;0m"
    orange = "\033[38;2;255;130;0m"
    pink= "\033[38;2;255;138;239m"

    light_orange = "\033[38;2;255;170;0m"
    light_green = "\033[38;2;187;255;0m"
    light_yellow = "\033[38;2;251;255;133m"
    light_pink = "\033[38;2;255;199;248m"

    dark_orange = "\033[38;2;255;90;0m"
    dark_green = "\033[38;2;18;82;0m"
    dark_yellow = "\033[38;2;212;219;0m"
    dark_pink = "\033[38;2;194;0;168m"

colors = Dynamic


class Animation():
    terminal_size = _size().columns
    
    def Come_Back(text: str, sleep: int = 0.03, repeat: int = 1, mode: int = 1) -> (str or None):
        if mode == 1:
            for _ in range(repeat):

                for i in range(Animation.terminal_size - len(text)):
                    print(" " * i + text, end= "\r")
                    _sleep(sleep)

                for j in range(Animation.terminal_size - len(text)):
                    print(" " * (Animation.terminal_size - len(text)- j - 1) + text + " " * j , end= "\r")
                    _sleep(sleep)

            print("\n")

        elif mode == 2:
            for _ in range(repeat):

                for i in range(Animation.terminal_size - len(text)):
                    print(" " * i + text, end= "\r")
                    _sleep(sleep)

                for j in range(Animation.terminal_size - len(text)):
                    print(" " * (Animation.terminal_size - len(text)- j - 1) + text + " " * j , end= "\r")
                    _sleep(sleep)

            return input(text)

    def Left_to_Right(text: str, sleep: int = 0.03, columns: str = 10, mode: int = 1) -> None:
        
        if mode == 1:
            for spaces in range(columns):
                print(" " * spaces + text, end= "\r")
                _sleep(sleep)
            print("\n")

        elif mode == 2:
            for spaces in range(columns):
                print(" " * spaces + text, end= "\r")
                _sleep(sleep)

            return input(" " * spaces + text)

    def Right_to_Left(text: str, sleep: int = 0.03, columns: str = 10) -> None:

        for spaces in range(columns):
            print(" " * (Animation.terminal_size - len(text)- spaces - 1) + text + " " * spaces, end= "\r")
            _sleep(sleep)

        print("\n")

    def Blink(text: str, sleep: int = 0.1, repeat: int = 30, columns: int = -1):
        size = Animation.terminal_size
        if columns == -1:
            print(" "* len(text))
            



class Mode:
    """
    functions -> 2:
        Horizontal() |      Put the color gradient in honrizontal
        Vertical()   |      Put the color gradient in vertical
        OneLine()    |      Put the color gradient in one line (without reset color for each line)
    """
    def Colored_Text(text: str, r: int, g: int, b: int) -> str:
        return f"\033[38;2;{r};{g};{b}m{text}\033[38;2;255;255;255m"
        
    def Center(text: str, width: int = -1) -> str:
        result = ""
        lines = text.split('\n')
        for line in lines:            
            result += "\n"+line.center(width)
        return result
    
    def OneLine(color: list, text: str, mode: int = 1, col_reset: bool = True, cursor: bool = False) -> str:
        result = ""
        selector = 0

        if cursor:
                Utils.HideCursor()
                    
        for carac in text:

            if (len(color) - 1) == selector:
                selector = 0

            if col_reset:

                if type(selector) != int:
                    result += f"\033[38;2;{color[int(selector - 0.5)]}m{carac}\033[38;2;255;255;255"

            elif not col_reset:

                if type(selector) != int:
                    result += f"\033[38;2;{color[int(selector - 0.5)]}m{carac}"

            selector += 0.5

        if mode == 1:
            print(result.rstrip())

        elif mode == 2:
            res = input(result.rstrip())
            return res

        elif mode == 3:
            Utils.Type(result.rstrip())

        elif mode == 4:
            res = input(Utils.Type(result.rstrip()))
            return res
        elif mode == 5:
            print(result.rstrip(), end= "\r")

    def Horizontal(color: list, text: str, mode: int = 1, col_reset: bool = True, cursor: bool = False) -> str:
        lines = text.split("\n")
        result = ""    
        num_colors = len(color) - 1
            
        if cursor:
            Utils.HideCursor()
                
        for line in lines:
            selector = 0
            characters = [*line]

            for letter in characters:

                if num_colors == selector:
                    selector = 0

                dyna_color = color[selector]

                if col_reset:
                    result += " " * Textspace.getspace(letter) + f"\033[38;2;{dyna_color}m{letter.strip()}{Colors.reset}"
                elif not col_reset:
                    result += " " * Textspace.getspace(letter) + f"\033[38;2;{dyna_color}m{letter.strip()}"

                selector += 1


            result += "\n"
                
        if mode == 1:
            return result.rstrip()

        elif mode == 2:
            res = input(result.rstrip())
            return res

        elif mode == 3:
            Utils.Type(result.rstrip())

        elif mode == 4:
            res = input(Utils.Type(result.rstrip()))
            return res

        elif mode == 5:
            print(result.rstrip(), end= "\r")
        
        return ""
        
    def Vertical(color: list, text: str, mode: int = 1, col_reset: bool = True, cursor: bool = False) -> str:
        lines = text.split("\n")
        result = ""
        num_colors = len(color) - 1
        selector = 0
        if cursor: 
            Utils.HideCursor()
        for line in lines:

            if num_colors == selector:
                selector = 0

            dyna_color = color[selector]

            result += " " * Textspace.getspace(line) + "".join(f"\033[38;2;{dyna_color}m"+ x for x in line.strip() +"\n")

            selector += 1

        if col_reset:
            if mode == 1:
                print(result.rstrip()+Colors.reset)

            elif mode == 2:
                res = input(result.rstrip()+Colors.reset)
                return res

            elif mode == 3:
                Utils.Type(result.rstrip()+Colors.reset)

            elif mode == 4:
                res = input(Utils.Type(result.rstrip())+Colors.reset)
                return res
            elif mode == 5:
                print(result.rstrip(), end= "\r")

        elif not col_reset:
            if mode == 1:
                print(result.rstrip())

            elif mode == 2:
                res  = input(result.rstrip())
                return res

            elif mode == 3:
                Utils.Type(result.rstrip())

            elif mode == 4:
                res = input(Utils.Type(result.rstrip()))
                return res
            elif mode == 5:
                print(result.rstrip(), end= "\r")
        return ""

Utils.Init()