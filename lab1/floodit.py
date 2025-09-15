import pygame
import random
import sys


pygame.init()


BoardSize = 14  # Размер поля
CellSize = 30   # Размер одной клетки в пикселях
Colors = [       
    (255, 0, 0),    # red
    (0, 255, 0),    # green
    (0, 0, 255),    # blue
    (255, 255, 0),  # yellow
    (255, 0, 255),  # purple
]
SidebarWidth = 150  
WindowWidth = BoardSize * CellSize + SidebarWidth
WindowHeight = BoardSize * CellSize
MaxMoves = 25  

# Настройка окна
screen = pygame.display.set_mode((WindowWidth, WindowHeight))
pygame.display.set_caption("Flood It Game")


font = pygame.font.SysFont('Arial', 24)

def create_board(size, num_colors):  # Создает новое игровое поле, заполненное случайными цветами
    board = []
    for _ in range(size):
        row = []
        for _ in range(size):
            color_index = random.randint(0, num_colors - 1)
            row.append(color_index)
        board.append(row)
    return board

def draw_board(board, flood_set):  # Отрисовывает игровое поле на экране.
    for row in range(BoardSize):
        for col in range(BoardSize):
            color_index = board[row][col]
            rect = pygame.Rect(col * CellSize, row * CellSize, CellSize, CellSize)
            
            # Клетки, которые уже залиты
            if (row, col) in flood_set:
                pygame.draw.rect(screen, Colors[color_index], rect)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Серый контур
            else:
                pygame.draw.rect(screen, Colors[color_index], rect)


def draw_sidebar(moves, max_moves, flood_set, total_cells):  # Отрисовывает боковую панель с информацией и кнопками цветов.
    sidebar_rect = pygame.Rect(BoardSize * CellSize, 0, SidebarWidth, WindowHeight)
    pygame.draw.rect(screen, (50, 50, 50), sidebar_rect)
    
    # Отображение счетчика ходов
    moves_text = font.render(f"Ходы: {moves}/{max_moves}", True, (255, 255, 255))
    screen.blit(moves_text, (BoardSize * CellSize + 20, 20))
    
    # Отображение прогресса
    progress = len(flood_set) / total_cells * 100
    progress_text = font.render(f"Прогресс: {progress:.1f}%", True, (255, 255, 255))
    screen.blit(progress_text, (BoardSize * CellSize + 20, 60))
    
    # Кнопки цветов
    for i, color in enumerate(Colors):
        button_rect = pygame.Rect(BoardSize * CellSize + 20, 120 + i * 60, 110, 50)
        pygame.draw.rect(screen, color, button_rect)
        pygame.draw.rect(screen, (255, 255, 255), button_rect, 2)
        
        # Подписи для кнопок
        color_text = font.render(f"Цвет {i+1}", True, (255, 255, 255))
        screen.blit(color_text, (BoardSize * CellSize + 50, 135 + i * 60))

def get_flood_set(board, start_row=0, start_col=0):  # Возвращает множество координат всех клеток, соединенных с начальной областью.
    
    start_color = board[start_row][start_col]
    flood_set = set()
    stack = [(start_row, start_col)]
    
    while stack:
        row, col = stack.pop()
        if (row, col) in flood_set:
            continue
            
        flood_set.add((row, col))
        
        
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # right, down, left, up
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < BoardSize and 
                0 <= new_col < BoardSize and 
                board[new_row][new_col] == start_color):
                stack.append((new_row, new_col))
                
    return flood_set

def flood_fill(board, flood_set, new_color):  # Изменяет цвет всех клеток в flood_set на new_color.
    for row, col in flood_set:
        board[row][col] = new_color

def check_win(flood_set, total_cells):  # Проверяет залиты ли все клетки
    return len(flood_set) == total_cells

def main():
    # Инициализация игры
    board = create_board(BoardSize, len(Colors))  
    flood_set = get_flood_set(board)
    moves = 0
    total_cells = BoardSize * BoardSize
    game_over = False
    won = False
    
    # Главный игровой цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                
                
                if x > BoardSize * CellSize:
                    button_index = (y - 120) // 60
                    
                    if 0 <= button_index < len(Colors):
                        new_color = button_index
                        current_color = board[0][0]
                        
                        # Меняем цвет только если выбран другой цвет
                        if new_color != current_color:
                            flood_fill(board, flood_set, new_color)
                            flood_set = get_flood_set(board)
                            moves += 1
                            
                            
                            if check_win(flood_set, total_cells):
                                game_over = True
                                won = True
                            elif moves >= MaxMoves:
                                game_over = True
                                won = False
            
            # Рестарт игры по нажатию R
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = create_board(BoardSize, len(Colors))
                    flood_set = get_flood_set(board)
                    moves = 0
                    game_over = False
                    won = False
        
        # Отрисовка
        screen.fill((0, 0, 0))
        draw_board(board, flood_set)
        draw_sidebar(moves, MaxMoves, flood_set, total_cells)
        
        
        if game_over:
            overlay = pygame.Surface((WindowWidth, WindowHeight), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  
            screen.blit(overlay, (0, 0))
            
            if won:
                message = font.render("Вы выиграли! Нажмите R для рестарта", True, (0, 255, 0))
            else:
                message = font.render("Вы проиграли! Нажмите R для рестарта", True, (255, 0, 0))
            
            screen.blit(message, (WindowWidth // 2 - message.get_width() // 2, 
                                 WindowHeight // 2 - message.get_height() // 2))
        
        pygame.display.flip()

if __name__ == "__main__":
    main()