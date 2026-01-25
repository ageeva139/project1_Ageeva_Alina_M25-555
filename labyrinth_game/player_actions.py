from labyrinth_game import constants

# функция для показа инвентаря
def show_inventory(game_state):
    if game_state['player_inventory']:
        print ('Вам инвентарь:', *game_state['player_inventory'])
    else:
        print ('Ваш инвентарь пуст')

# функция для ввода команд пользователем
def get_input(prompt="> "):
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

# функция перемещения
def move_player(game_state, direction):
    from labyrinth_game.utils import (
        describe_current_room,
        pseudo_random,
        trigger_trap,
        random_event
    )
    # подключение описания текущей комнаты
    room = constants.ROOMS[game_state['current_room']]

    if direction in room['exits']:
        next_room_name = room['exits'][direction]  # получаем название следующей комнаты

        # проверка на вход в treasure_room
        if (next_room_name == 'treasure_room'
                and 'rusty_key' not in game_state['player_inventory']):
            print('Дверь заперта. Нужен ключ, чтобы пройти дальше')
            return  # прерываем перемещение

        game_state['current_room'] = next_room_name  # изменение текущей комнаты
        game_state['steps_taken'] += 1  # увеличение счетчика шагов

        # сообщение об использовании ключа для входа в treasure_room
        if (next_room_name == 'treasure_room'
                and 'rusty_key' in game_state['player_inventory']):
            msg = 'Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ'
            print(msg)

        # 10% шанс срабатывания ловушки при перемещении
        trap_chance = pseudo_random(game_state['steps_taken'], 10)
        if trap_chance == 0:
            trigger_trap(game_state)

        # если игра не закончилась из-за ловушки
        if not game_state['game_over']:
            random_event(game_state)  # случайное событие
            describe_current_room(game_state)  # описание комнаты

    else:
        print('Нельзя пойти в этом направлении.')


# функция пополнения инвентаря
def take_item(game_state, item_name):
    # подключение описания текущей комнаты
    room = constants.ROOMS[game_state['current_room']]

    # отдельно случай сундука, который нельзя взять в инвентарь
    if item_name == 'treasure_chest':
        print('Вы не можете поднять сундук, он слишком тяжелый')
        return

    if item_name in room['items']:
        game_state['player_inventory'].append(item_name) #добавляем в инвентарь
        room['items'].remove(item_name) # убираем из комнаты
        print(f'Вы подняли {item_name}!')
    else:
        print('Такого предмета здесь нет.')

# функция использования предмета из инвентаря
def use_item(game_state, item_name):
    inventory = game_state['player_inventory']

    if item_name not in inventory: # если предмета нет, произойдет прерывание функции
        print ('У вас нет такого предмета')
        return

    match item_name:
        case 'torch':
            print('Вы зажгли факел. Стало светлее и уютнее')

        case 'sword':
            print('Вы почувствовали уверенность, держа меч в руках')

        case 'bronze_box':
            print('Вы открыли бронзовую шкатулку')
            if 'rusty_key' not in inventory:
                game_state['player_inventory'].append('rusty_key')
                print('Внутри вы нашли rusty_key и добавили его в инвентарь!')
            else:
                print('Шкатулка пуста')

        case _:
            print(f'Вы не знаете, как использовать {item_name}.')
