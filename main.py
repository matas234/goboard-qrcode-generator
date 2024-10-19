from PIL import Image, ImageDraw, ImageOps
import qrcode


def create_go_board(
    board_size=19,
    grid_size=40,
    line_color=(0, 0, 0),
    border_size=0,
    background="color",
    bg_color=(255, 255, 255),
):
    board_pixel_size = ((board_size - 1) * grid_size) + 2 * border_size

    if background == "color":
        board_image = Image.new("RGB", (board_pixel_size, board_pixel_size), color=bg_color)

    elif background == "texture":
        texture = Image.open("assets/wood_texture.jpg").resize((board_pixel_size, board_pixel_size))
        board_image = Image.new("RGB", (board_pixel_size, board_pixel_size))
        board_image.paste(texture, (0, 0))

    elif background == "transparent":
        board_image = Image.new("RGBA", (board_pixel_size, board_pixel_size), (0, 0, 0, 0))

    else:
        raise ValueError("Unsupported background type")

    draw = ImageDraw.Draw(board_image)

    for i in range(board_size):
        draw.line((
                border_size + i * grid_size,
                border_size,
                border_size + i * grid_size,
                board_pixel_size - border_size),
            fill=line_color)

        draw.line((
                border_size,
                border_size + i * grid_size,
                board_pixel_size - border_size,
                border_size + i * grid_size),
            fill=line_color)

    return board_image


def generate_qr_matrix(data):
    qr = qrcode.QRCode(box_size=1, border=0, error_correction=qrcode.constants.ERROR_CORRECT_L)  ## change this for error correcting (currently on the lowest)
    qr.add_data(data)
    qr.make(fit=True)

    qr_matrix = qr.get_matrix()

    return qr_matrix


def create_go_board_with_qr(
    data,
    grid_size=40,
    stone_scaling=1,
    border_size=0,
    background="color",
    bg_color=(255, 255, 255),
    bg_texture=None,
):

    stone_size = int(grid_size * stone_scaling)

    black_stone = Image.open(f"assets/b16.png").resize((stone_size, stone_size)).convert("RGBA")
    white_stone = Image.open(f"assets/w16.png").resize((stone_size, stone_size)).convert("RGBA")
    
    qr_matrix = generate_qr_matrix(data)
    qr_size = len(qr_matrix)

    board_image = create_go_board(
        board_size=qr_size,
        grid_size=grid_size,
        border_size=border_size,
        background=background,
        bg_color=bg_color,
    )

    for x in range(qr_size):
        for y in range(qr_size):
            cx = border_size + x * grid_size + (grid_size - stone_size) // 2 - grid_size // 2
            cy = border_size + y * grid_size + (grid_size - stone_size) // 2 - grid_size // 2

            board_image.paste(black_stone if qr_matrix[x][y] else white_stone, (cx, cy), black_stone)

    board_image.save("go_qrcode.png", format="PNG")
    print(f"Image saved | board size: {qr_size}")


data_string = "warwicksu.com/societies-sports/societies/gosociety/"

create_go_board_with_qr(
    data_string,
    grid_size=90,
    stone_scaling=0.95,
    border_size=200,
    background="texture", # "color", "texture", or "transparent"
    bg_color=(0,0,0,0)
)