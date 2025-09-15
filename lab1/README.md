# Объяснение

## 1. Функция `create_board(size, num_colors)`

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

**Назначение**: Создание игрового поля со случайными цветами.

**Как работает**:
1. Создается пустой список `board`, который будет представлять игровое поле
2. Внешний цикл `for _ in range(size)` создает `size` строк
3. Внутренний цикл `for _ in range(size)` создает `size` столбцов в каждой строке
4. Для каждой клетки генерируется случайный индекс цвета от 0 до `num_colors - 1`
5. Каждая строка добавляется в игровое поле
6. Функция возвращает готовое игровое поле в виде двумерного списка

**Пример**: Для `size=3` и `num_colors=2` может вернуть:
```
[[0, 1, 0],
 [1, 0, 1],
 [0, 1, 0]]
```

## 2. Функция `draw_board(board, flood_set)`

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

**Назначение**: Отрисовка игрового поля на экране.

**Как работает**:
1. Двойной цикл проходит по всем клеткам игрового поля
2. Для каждой клетки вычисляется ее положение на экране с помощью `pygame.Rect`
3. Определяется цвет клетки из массива `Colors` по индексу
4. Если клетка находится в множестве `flood_set` (уже залита), она рисуется с серым контуром
5. Если клетка еще не залита, она рисуется без контура
6. Все отрисовки выполняются на глобальной поверхности `screen`

## 3. Функция `draw_sidebar(moves, max_moves, flood_set, total_cells)`

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

**Назначение**: Отрисовка правой панели с информацией и кнопками.

**Как работает**:
1. Рисует прямоугольник для боковой панели темно-серого цвета
2. Создает и отображает текст с количеством ходов
3. Вычисляет прогресс игры (процент залитых клеток) и отображает его
4. Для каждого цвета из палитры:
   - Рисует кнопку этого цвета
   - Добавляет белую рамку вокруг кнопки
   - Создает и отображает текст с номером цвета
5. Все элементы позиционируются относительно правого края игрового поля

## 4. Функция `get_flood_set(board, start_row=0, start_col=0)`

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


Функция `get_flood_set` - это ключевой алгоритм игры Flood It, который определяет, какие клетки на игровом поле входят в текущую "залитую" область. Давайте разберем ее работу пошагово:


### 1. Параметры функции

```python
def get_flood_set(board, start_row=0, start_col=0):
```
- `board` - игровое поле (двумерный список цветов)
- `start_row`, `start_col` - координаты начальной клетки (по умолчанию [0,0] - левый верхний угол)

### 2. Определение начального цвета

```python
start_color = board[start_row][start_col]
```
- Запоминаем цвет начальной клетки, с которой начинаем поиск

### 3. Инициализация структур данных

```python
flood_set = set()
stack = [(start_row, start_col)]
```
- `flood_set` - множество (set) для хранения координат всех клеток в залитой области
- `stack` - стек для реализации алгоритма DFS, начинаем с начальной клетки

### 4. Основной цикл алгоритма

```python
while stack:
    row, col = stack.pop()
    if (row, col) in flood_set:
        continue
        
    flood_set.add((row, col))
```
- Цикл выполняется, пока в стеке есть клетки для обработки
- Извлекаем клетку из стека (LIFO - последний пришел, первый ушел)
- Если клетка уже в множестве, пропускаем ее (избегаем повторной обработки)
- Добавляем клетку в множество залитых клеток

### 5. Проверка соседних клеток

```python
for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
    new_row, new_col = row + dr, col + dc
```
- Проверяем четырех соседей: вправо (0,1), вниз (1,0), влево (0,-1), вверх (-1,0)
- Вычисляем координаты соседней клетки

### 6. Условия добавления соседа в стек

```python
if (0 <= new_row < BoardSize and 
    0 <= new_col < BoardSize and 
    board[new_row][new_col] == start_color):
    stack.append((new_row, new_col))
```
- Проверяем, что соседняя клетка находится в пределах игрового поля
- Проверяем, что цвет соседней клетки совпадает с начальным цветом
- Если оба условия выполняются, добавляем соседнюю клетку в стек для дальнейшей обработки

### 7. Возврат результата

```python
return flood_set
```
- Возвращаем множество координат всех клеток, соединенных с начальной клеткой




## 5. Функция `flood_fill(board, flood_set, new_color)`

```python
def flood_fill(board, flood_set, new_color):
    for row, col in flood_set:
        board[row][col] = new_color
```

**Назначение**: Изменение цвета всех клеток в залитой области.

**Как работает**:
1. Принимает игровое поле, множество залитых клеток и новый цвет
2. Проходит по всем клеткам в множестве
3. Для каждой клетки устанавливает новый цвет

## 6. Функция `check_win(flood_set, total_cells)`

```python
def check_win(flood_set, total_cells):
    return len(flood_set) == total_cells
```

**Назначение**: Проверка условия победы.

**Как работает**:
1. Сравнивает количество залитых клеток с общим количеством клеток на поле
2. Возвращает `True`, если все клетки залиты, иначе `False`





# Модуль `main()` 



## 1. Инициализация игрового состояния

```python
def main():
    # Инициализация игры
    board = create_board(BoardSize, len(Colors))  
    flood_set = get_flood_set(board)
    moves = 0
    total_cells = BoardSize * BoardSize
    game_over = False
    won = False
```

**Что здесь происходит:**
- `board = create_board(BoardSize, len(Colors))` - создается игровое поле размером 14×14 клеток с 5 цветами
- `flood_set = get_flood_set(board)` - определяется начальная область залитых клеток (все клетки, соединенные с левой верхней)
- `moves = 0` - счетчик ходов устанавливается в 0
- `total_cells = BoardSize * BoardSize` - вычисляется общее количество клеток (196)
- `game_over = False` - флаг, указывающий, что игра еще не закончена
- `won = False` - флаг, указывающий, что игрок еще не выиграл

## 2. Главный игровой цикл

```python
# Главный игровой цикл
while True:
    for event in pygame.event.get():
        # Обработка событий...
```

**Назначение**: Бесконечный цикл, который обеспечивает непрерывную работу игры до ее завершения.

**Как работает**:
- Цикл `while True` выполняется до тех пор, пока игра не будет закрыта
- На каждой итерации цикла обрабатываются все события, произошедшие с момента последней итерации
- После обработки событий происходит отрисовка игрового состояния

## 3. Обработка событий

### 3.1. Обработка выхода из игры

```python
if event.type == pygame.QUIT:
    pygame.quit()
    sys.exit()
```

**Назначение**: Корректное завершение игры при закрытии окна.

**Как работает**:
- При получении события `pygame.QUIT` (закрытие окна)
- Вызывается `pygame.quit()` для корректного завершения работы Pygame
- Вызывается `sys.exit()` для завершения работы программы

### 3.2. Обработка кликов мыши

```python
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
```

**Назначение**: Обработка выбора цвета игроком.

**Как работает**:
- Проверяется, что игра не закончена (`not game_over`)
- Определяются координаты клика (`x, y`)
- Проверяется, что клик был в области боковой панели (`x > BoardSize * CellSize`)
- Вычисляется, какая кнопка цвета была нажата: `button_index = (y - 120) // 60`
- Проверяется, что индекс кнопки соответствует существующему цвету
- Если выбран новый цвет (отличается от текущего):
  - Перекрашивается залитая область в новый цвет
  - Определяется новая залитая область
  - Увеличивается счетчик ходов
  - Проверяются условия победы или поражения

### 3.3. Обработка нажатий клавиш

```python
if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_r:
        board = create_board(BoardSize, len(Colors))
        flood_set = get_flood_set(board)
        moves = 0
        game_over = False
        won = False
```

**Назначение**: Перезапуск игры при нажатии клавиши R.

**Как работает**:
- При нажатии любой клавиши проверяется, является ли это клавишей R (`pygame.K_r`)
- Если да, игра перезапускается:
  - Создается новое игровое поле
  - Определяется новая залитая область
  - Сбрасывается счетчик ходов
  - Сбрасываются флаги окончания игры

## 4. Отрисовка игрового состояния

```python
# Отрисовка
screen.fill((0, 0, 0))
draw_board(board, flood_set)
draw_sidebar(moves, MaxMoves, flood_set, total_cells)
```

**Назначение**: Визуализация текущего состояния игры.

**Как работает**:
- `screen.fill((0, 0, 0))` - очистка экрана черным цветом
- `draw_board(board, flood_set)` - отрисовка игрового поля
- `draw_sidebar(moves, MaxMoves, flood_set, total_cells)` - отрисовка боковой панели

## 5. Обработка окончания игры

```python
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
```

**Назначение**: Отображение сообщения о результате игры.

**Как работает**:
- Если игра окончена (`game_over == True`):
  - Создается полупрозрачное затемнение поверх всего экрана
  - В зависимости от результата (победа или поражение) создается соответствующее сообщение
  - Сообщение размещается по центру экрана

## 6. Обновление экрана

```python
pygame.display.flip()
```

**Назначение**: Обновление содержимого экрана.

**Как работает**:
- `pygame.display.flip()` обновляет весь экран, показывая все изменения, сделанные с момента последнего обновления
- Это реализация двойной буферизации, которая предотвращает мерцание экрана



