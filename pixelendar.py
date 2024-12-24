import argparse
from datetime import datetime

from PIL import Image, ImageDraw

from typo import Font


WIDTH, HEIGHT = 71, 65
COLOR_BACK = (255, 255, 255, 0)
COLOR_MAIN = (0, 0, 0, 255)
COLOR_GRID = (192, 192, 192, 255)
FONT_FILE = 'assets/cal-fnt_ru.png'
FONT_CHARSET = '0123456789АБВГДЕИЙКЛМНОПРСТУФЧЬЮЯ'
MONTH_NAME = ['ЯНВАРЬ', 'ФЕВРАЛЬ', 'МАРТ', 'АПРЕЛЬ', 'МАЙ', 'ИЮНЬ',
              'ИЮЛЬ', 'АВГУСТ', 'СЕНТЯБРЬ', 'ОКТЯБРЬ', 'НОЯБРЬ', 'ДЕКАБРЬ']
DAY_NAME = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']


def calendar_bitmap(date):
    font = Font(FONT_FILE, FONT_CHARSET)
    image = Image.new(size=(WIDTH, HEIGHT), mode='RGBA', color=COLOR_BACK)
    draw = ImageDraw.Draw(image)

    year_img = font.write_color(str(date.year), COLOR_MAIN)
    image.paste(year_img, (WIDTH-2 - year_img.width, 1))
    image.paste(font.write_color(MONTH_NAME[date.month-1], COLOR_MAIN), (2, 1))

    for x in range(10, 70, 10):
        draw.line((x, 9, x, 63), COLOR_GRID)
    for y in range(16, 60, 8):
        draw.line((1, y, 69, y), COLOR_GRID)

    return image


if __name__ == '__main__':

    def valid_month_or_date(s):
        try:
            return datetime.strptime(s, '%Y-%m')
        except ValueError:
            try:
                return datetime.strptime(s, '%Y-%m-%d')
            except ValueError:
                msg = f'not a valid date: {s} (format YYYY-MM or YYYY-MM-DD)'
                raise argparse.ArgumentTypeError(msg)

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--date', type=valid_month_or_date, required=False,
                        help='month or day for produce calendar, format YYYY-MM or YYYY-MM-DD')
    args = parser.parse_args()

    date = args.date
    if date:
        date = date.date()
    else:
        date = datetime.today().date()
    print(date)

    calendar_bitmap(date).resize((WIDTH*5, HEIGHT*5), Image.Resampling.NEAREST).show()
