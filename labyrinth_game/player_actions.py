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
    # подключение описания текущей комнаты
    room = constants.ROOMS[game_state['current_room']]

    if direction in room['exits']:
        game_state['current_room'] = room['exits'][direction] #изменение текущей комнаты
        game_state['steps_taken'] += 1 # увеличение счетчика шагов
        from labyrinth_game.utils import describe_current_room
        describe_current_room(game_state) # вывод описания текущей комнаты
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
