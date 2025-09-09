# Flood_It

## code
```python
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

def create_board(size, num_colors):
    board = []
    for _ in range(size):
        row = []
        for _ in range(size):
            color_index = random.randint(0, num_colors - 1)
            row.append(color_index)
        board.append(row)
    return board

def draw_board(board, flood_set):
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


def draw_sidebar(moves, max_moves, flood_set, total_cells): 
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

def get_flood_set(board, start_row=0, start_col=0):
    
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

def flood_fill(board, flood_set, new_color):
    for row, col in flood_set:
        board[row][col] = new_color

def check_win(flood_set, total_cells):
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
```


## Объяснение кода
### 1. Инициализация и константы
```python
import pygame
import random
import sys

pygame.init()
```
* Назначение: Импорт необходимых библиотек и инициализация движка Pygame.

* Объяснение:

    * `pygame` - библиотека для создания игр и графических приложений

    * `random` - для генерации случайных чисел (цветов клеток)

    * `sys` - для системных функций, в частности для закрытия игры

    * `pygame.init()` - инициализирует все модули Pygame

```python
BoardSize = 14
CellSize = 30
Colors = [       
    (255, 0, 0),    # Красный
    (0, 255, 0),    # Зеленый
    (0, 0, 255),    # Синий
    (255, 255, 0),  # Желтый
    (255, 0, 255),  # Пурпурный
]
SidebarWidth = 150
WindowWidth = BoardSize * CellSize + SidebarWidth
WindowHeight = BoardSize * CellSize
MaxMoves = 25
```

* Назначение: Определение констант игры.

* Объяснение:

    * `BoardSize` - размер игрового поля (14×14 клеток)

    * `CellSize` - размер одной клетки в пикселях

    * `Colors` - палитра цветов в формате RGB

    * `SidebarWidth` - ширина правой панели с кнопками

    * `WindowWidth`/`Height` - расчет размеров окна игры

    * `MaxMoves` - максимальное количество ходов для победы

### 2. Создание игрового поля
```python
def create_board(size, num_colors):
    board = []
    for _ in range(size):
        row = []
        for _ in range(size):
            color_index = random.randint(0, num_colors - 1)
            row.append(color_index)
        board.append(row)
    return board
```

* Назначение: Создание игрового поля со случайными цветами.

* Объяснение:

    * Функция создает двумерный список (матрицу)

    * Для каждой клетки генерируется случайный цвет от 0 до `num_colors`-1

    * Возвращает готовое игровое поле

### 3. Определение залитой области (ключевой алгоритм)
```python
def get_flood_set(board, start_row=0, start_col=0):
    start_color = board[start_row][start_col]
    flood_set = set()
    stack = [(start_row, start_col)]
    
    while stack:
        row, col = stack.pop()
        if (row, col) in flood_set:
            continue
            
        flood_set.add((row, col))
        
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < BoardSize and 
                0 <= new_col < BoardSize and 
                board[new_row][new_col] == start_color):
                stack.append((new_row, new_col))
                
    return flood_set
```

* Назначение: Нахождение всех клеток, соединенных с начальной клеткой.

* Объяснение:

    * Используется алгоритм поиска в глубину (DFS)

    * `start_color` - запоминаем цвет начальной клетки

    * `flood_set` - множество для хранения координат залитых клеток

    * `stack` - стек для реализации DFS

    * Проверяем четырех соседей (вправо, вниз, влево, вверх)

    * Если сосед существует и того же цвета, добавляем его в стек

    * Возвращаем множество всех соединенных клеток

### 4. Механика заливки
```python
def flood_fill(board, flood_set, new_color):
    for row, col in flood_set:
        board[row][col] = new_color
```

* Назначение: Изменение цвета всех клеток в залитой области.

* Объяснение:

    * Проходим по всем клеткам в `flood_set`

    * Устанавливаем им новый цвет

### 5. Отрисовка игрового поля
```python
def draw_board(board, flood_set):
    for row in range(BoardSize):
        for col in range(BoardSize):
            color_index = board[row][col]
            rect = pygame.Rect(col * CellSize, row * CellSize, CellSize, CellSize)
            
            if (row, col) in flood_set:
                pygame.draw.rect(screen, Colors[color_index], rect)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)
            else:
                pygame.draw.rect(screen, Colors[color_index], rect)
```

* Назначение: Визуализация игрового поля.

* Объяснение:

    * Для каждой клетки вычисляем ее положение на экране

    * Если клетка в залитой области - рисуем с серым контуром

    * Иначе - рисуем без контура

### 6. Отрисовка боковой панели
```python
def draw_sidebar(moves, max_moves, flood_set, total_cells):
    sidebar_rect = pygame.Rect(BoardSize * CellSize, 0, SidebarWidth, WindowHeight)
    pygame.draw.rect(screen, (50, 50, 50), sidebar_rect)
    
    moves_text = font.render(f"Ходы: {moves}/{max_moves}", True, (255, 255, 255))
    screen.blit(moves_text, (BoardSize * CellSize + 20, 20))
    
    progress = len(flood_set) / total_cells * 100
    progress_text = font.render(f"Прогресс: {progress:.1f}%", True, (255, 255, 255))
    screen.blit(progress_text, (BoardSize * CellSize + 20, 60))
    
    for i, color in enumerate(Colors):
        button_rect = pygame.Rect(BoardSize * CellSize + 20, 120 + i * 60, 110, 50)
        pygame.draw.rect(screen, color, button_rect)
        pygame.draw.rect(screen, (255, 255, 255), button_rect, 2)
        
        color_text = font.render(f"Цвет {i+1}", True, (255, 255, 255))
        screen.blit(color_text, (BoardSize * CellSize + 50, 135 + i * 60))
```

* Назначение: Отображение информации и кнопок управления.

* Объяснение:

    * Рисуем темно-серую панель справа

    * Выводим счетчик ходов и прогресс

    * Создаем кнопки для каждого цвета

    * Добавляем подписи к кнопкам

### 7. Проверка победы
```python
def check_win(flood_set, total_cells):
    return len(flood_set) == total_cells
```

* Назначение: Проверка условия победы.

* Объяснение:

    * Игрок побеждает, если количество залитых клеток равно общему количеству клеток

### 8. Главный игровой цикл
```python
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
```

* Назначение: Основная логика игры.

* Объяснение:

    * Инициализация игрового состояния

    * Бесконечный цикл обработки событий и отрисовки

    * Обработка кликов по кнопкам цветов

    * Проверка условий победы/поражения

    * Обработка рестарта игры (клавиша R)

    * Отрисовка затемнения и сообщения о результате игры

    * Обновление экрана

## Ключевые алгоритмические аспекты для защиты:

1. Алгоритм поиска связанной области:

    * Используется поиск в глубину (DFS) с использованием стека

    * Эффективно находит все клетки, соединенные с начальной

2. Структуры данных:

    * Множество (set) для хранения залитых клеток - обеспечивает быстрый поиск

    * Стек (stack) для реализации DFS

    * Двумерный список для представления игрового поля

3. Обработка пользовательского ввода:

    * Определение нажатой кнопки по координатам мыши

    * Обработка клавиатуры для рестарта игры

4. Визуализация:

    * Разделение логики и отрисовки

    * Использование относительных координат для элементов интерфейса

5. Архитектура игры:

    * Четкое разделение ответственности между функциями

    * Главный цикл игры, обрабатывающий события и обновляющий состояние