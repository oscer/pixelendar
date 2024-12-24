from PIL import Image


class Font(dict):

    height: int = None

    def __init__(self, fp, charset: str):
        super().__init__()

        bitmap = Image.open(fp).convert('L')

        self.height = self.find_height(bitmap)
        if not self.height:
            raise ValueError('Invalid font image: can`t find height')

        charnum, first = 0, 1
        for x in range(first, bitmap.width):
            if not bitmap.getpixel((x, self.height)):
                continue

            glyph = bitmap.crop((first, 0, x, self.height))
            self[charset[charnum]] = glyph

            first = x + 1

            charnum += 1
            if charnum > len(charset):
                break

    @staticmethod
    def find_height(bitmap: Image) -> int:
        for y in range(bitmap.height):
            if bitmap.getpixel((0, y)):
                return y
        return 0

    def write(self, text: str) -> Image:
        width = sum([self[char].width for char in text]) + len(text) - 1
        bitmap = Image.new('L', (width, self.height))
        x = 0
        for char in text:
            bitmap.paste(self[char], (x, 0))
            x += self[char].width + 1
        return bitmap

    def write_color(self, text: str, color: tuple = (0, 0, 0, 255), background: tuple = (255, 255, 255, 0)):
        mask = self.write(text).convert('L')
        bitmap = Image.new('RGBA', mask.size, background)
        for y in range(mask.height):
            for x in range(mask.width):
                a = mask.getpixel((x, y))
                if a:
                    bitmap.putpixel((x, y), (color[0] * 255 // a, color[1] * 255 // a, color[2] * 255 // a, color[3]))
        return bitmap
