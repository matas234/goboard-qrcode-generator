from PIL import Image, ImageDraw
import qrcode


def create_go_board(board_size=19, grid_size=40, line_color=(0, 0, 0), border_size = 0):
    board_pixel_size = ((board_size - 1) * grid_size) + 2*border_size
   
    texture = Image.open("assets/wood_texture.jpg").resize((board_pixel_size, board_pixel_size))

    board_image = Image.new("RGB", (board_pixel_size, board_pixel_size))
    board_image.paste(texture, (0, 0))
    draw = ImageDraw.Draw(board_image)

    for i in range(board_size):
        draw.line((border_size + i * grid_size, border_size, 
                    border_size + i * grid_size, board_pixel_size - border_size), 
                   fill=line_color)
        
        draw.line((border_size, border_size + i*grid_size, 
                    board_pixel_size - border_size, border_size + i*grid_size), 
                   fill=line_color)
    
    return board_image


def generate_qr_matrix(data):
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)

    qr_matrix = qr.get_matrix()  
    
    return qr_matrix

def create_go_board_with_qr(data, grid_size=40, stone_scaling=1, border_size = 0,):
    
    stone_size = int(grid_size * stone_scaling)

    black_stone = Image.open(f"assets/b16.png").resize((stone_size, stone_size))
    white_stone = Image.open(f"assets/w16.png").resize((stone_size, stone_size))

    qr_matrix = generate_qr_matrix(data)
    qr_size = len(qr_matrix)

    board_image = create_go_board(board_size = qr_size, 
                                  grid_size = grid_size, 
                                  border_size = border_size)

    for x in range(qr_size):
        for y in range(qr_size):
            cx = border_size + x * grid_size + (grid_size - stone_size) // 2 - grid_size//2
            cy = border_size + y * grid_size + (grid_size - stone_size) // 2 - grid_size//2

            board_image.paste(black_stone if qr_matrix[x][y] else white_stone, (cx, cy), black_stone)

    board_image.save("go_qrcode.png")


data_string = "wikipedia.com"

create_go_board_with_qr(data_string, 
                        stone_scaling=0.9, 
                        border_size=50)