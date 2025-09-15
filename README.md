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

**Назначение**: Нахождение всех клеток, соединенных с начальной клеткой.

**Как работает**:
1. Запоминает цвет начальной клетки (по умолчанию левой верхней)
2. Создает пустое множество `flood_set` для хранения залитых клеток
3. Создает стек `stack` и добавляет в него начальную клетку
4. Пока стек не пуст:
   - Извлекает клетку из стека
   - Если клетка уже в множестве, пропускает ее
   - Добавляет клетку в множество
   - Проверяет четырех соседей (вправо, вниз, влево, вверх)
   - Если сосед существует и имеет тот же цвет, добавляет его в стек
5. Возвращает множество всех соединенных клеток

**Алгоритм**: Поиск в глубину (DFS) с использованием стека

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

## 7. Функция `main()`

**Назначение**: Главная функция игры, содержащая основной игровой цикл.

**Как работает**:
1. Инициализирует игровое состояние:
   - Создает игровое поле
   - Определяет начальную залитую область
   - Устанавливает счетчик ходов в 0
   - Устанавливает флаги окончания игры

2. Запускает бесконечный игровой цикл:
   - Обрабатывает события (выход, клики мыши, нажатия клавиш)
   - При клике на кнопку цвета:
     - Определяет, какая кнопка была нажата
     - Если выбран новый цвет, перекрашивает область
     - Обновляет залитую область
     - Увеличивает счетчик ходов
     - Проверяет условия победы/поражения
   - При нажатии клавиши R перезапускает игру
   - Отрисовывает игровое поле и боковую панель
   - Если игра окончена, отображает сообщение о результате
   - Обновляет экран

## Общая архитектура программы

1. **Инициализация**: Настройка констант, создание окна, загрузка шрифтов
2. **Создание игрового состояния**: Генерация поля, определение начальной области
3. **Игровой цикл**:
   - Обработка входных данных
   - Обновление состояния игры
   - Отрисовка графики
4. **Завершение**: Выход из игры при закрытии окна

Каждая функция имеет четко определенную ответственность, что делает код модульным и легко понимаемым.