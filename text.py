import pygame, sys, random

def rotate():
    # 获取方块的初始位置
    y_drop, x_move = block_initial_position
    # 计算方块旋转后的位置
    rotating_position = [(-column, row) for row, column in select_block]

    # 检查旋转后的位置是否合法
    for row, column in rotating_position:
        row += y_drop
        column += x_move
        # 如果超出边界或和背景方块重叠，则跳出循环
        if column < 0 or column > 9 or background[row][column]:
            break
    else:
        # 如果旋转后的位置合法，则更新方块的位置
        select_block.clear()
        select_block.extend(rotating_position)

def block_move_down():
    # 获取方块的初始位置
    y_drop = block_initial_position[0]
    x_move = block_initial_position[1]
    y_drop -= 1

    # 检查方块下移后的位置是否合法
    for row, column in select_block:
        row += y_drop
        column += x_move

        # 如果下方有背景方块，则停止下移
        if background[row][column] == 1:
            break
    else:
        # 如果下移位置合法，则更新方块的位置
        block_initial_position.clear()
        block_initial_position.extend([y_drop, x_move])
        return

    # 如果方块无法下移，则将方块固定在背景上，并处理消除的行
    y_drop, x_move = block_initial_position
    for row, column in select_block:
        background[y_drop + row][x_move + column] = 1
    complete_row = []

    # 检查是否有行满了
    for row in range(1, 21):
        if 0 not in background[row]:
            complete_row.append(row)

    complete_row.sort(reverse=True)

    # 消除满行，并得分
    for row in complete_row:
        background.pop(row)
        background.append([0 for column in range(0, 10)])

    score[0] += len(complete_row)
    pygame.display.set_caption(str(score[0]) + '分')

    # 选择下一个方块并放置在顶部
    select_block.clear()
    select_block.extend(list(random.choice(all_block)))
    block_initial_position.clear()
    block_initial_position.extend([20, 5])
    y_drop, x_move = block_initial_position

    # 检查是否游戏结束
    for row, column in select_block:
        row += y_drop
        column += x_move
        if background[row][column]:
            game_over.append(1)


def new_draw():
    # 绘制方块
    y_drop, x_move = block_initial_position
    for row, column in select_block:
        row += y_drop
        column += x_move
        pygame.draw.rect(screen, (255, 165, 0), (column * 25, 500 - row * 25, 23, 23))

    # 绘制背景方块
    for row in range(0, 20):
        for column in range(0, 10):
            bottom_block = background[row][column]
            if bottom_block:
                pygame.draw.rect(screen, (0, 0, 255), (column * 25, 500 - row * 25, 23, 23))


def move_left_right(n):
    # 方块水平移动
    y_drop, x_move = block_initial_position
    x_move += n
    for row, column in select_block:
        row += y_drop
        column += x_move
        # 如果超出边界或和背景方块重叠，则跳出循环
        if column < 0 or column > 9 or background[row][column]:
            break
    else:
        # 如果移动位置合法，则更新方块的位置
        block_initial_position.clear()
        block_initial_position.extend([y_drop, x_move])


def event_logic():
    times = 0
    press = False
    while True:
        screen.fill((255, 255, 255))
        # 按键事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                move_left_right(-1)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                move_left_right(1)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                rotate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                press = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                press = False

        # 如果下箭头键被按下，则加快方块下落速度
        if press:
            times += 10

        # 达到时间阈值时让方块向下移动，并重置时间
        if times >= 100:
            block_move_down()
            times = 0
        else:
            times += 1

        # 如果游戏结束，则退出程序
        if game_over:
            sys.exit()

        new_draw()
        pygame.time.Clock().tick(200)
        pygame.display.flip()


if __name__ == '__main__':
    # 初始化游戏
    all_block = [[[0, 0], [0, -1], [0, 1], [0, 2]],
                 [[0, 0], [0, 1], [1, 1], [1, 0]],
                 [[0, 0], [0, -1], [-1, 0], [-1, 1]],
                 [[0, 0], [0, 1], [-1, -1], [-1, 0]],
                 [[0, 0], [0, 1], [1, 0], [0, -1]],
                 [[0, 0], [1, 0], [-1, 0], [1, -1]],
                 [[0, 0], [1, 0], [-1, 0], [1, 1]]]
    background = [[0 for column in range(0, 10)] for row in range(0, 22)]
    background[0] = [1 for column in range(0, 10)]

    select_block = list(random.choice(all_block))
    block_initial_position = [21, 5]
    score = [0]
    game_over = []

    pygame.init()
    screen = pygame.display.set_mode((250, 500))
    title = pygame.display.set_caption("俄罗斯方块")

    # 调用按键事件处理函数
    event_logic()
