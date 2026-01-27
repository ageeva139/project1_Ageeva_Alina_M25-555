import math
from labyrinth_game import constants
from labyrinth_game.player_actions import get_input

def describe_current_room(game_state):
    '''описание комнаты'''

    # подключение описания текущей комнаты
    room=constants.ROOMS[game_state['current_room']]

    # вывод описания комнаты
    print(f"=={game_state['current_room']}==")

    description_text = ' '.join(room['description'])
    print(description_text)

    if room['items']: # проверка на непустой список items
        print('Заметные предметы:', ", ".join(room['items']))

    exits = list(room['exits'].keys()) # создание списка из ключей словаря выходов
    print('Выходы:', ', '.join(exits))

    if room['puzzle'] is not None: # проверка есть ли загадка
        print('Кажется, здесь есть загадка (используйте команду solve).')

def show_help():
    '''вывод доступных команд'''

    print("\nДоступные команды:")
    for command, description in constants.COMMANDS.items():
        print(f"{command:<16} - {description}")

def solve_puzzle(game_state):
    '''разгадать загадку'''

    # подключение описания текущей комнаты
    room=constants.ROOMS[game_state['current_room']]

    if room['puzzle'] is None: # если загадки нет, произойдет прерывание функции
        print('Загадок здесь нет')
        return

    question = room['puzzle'][:-1]
    correct_answer = room['puzzle'][-1]

    print('Загадка:', *question)
    user_answer = get_input('Ваш ответ: ')

    # все варианты ответов
    alternative_answers = [correct_answer]
    if correct_answer == '10':
        alternative_answers.append('десять')
    elif correct_answer == 'шаг шаг шаг':
        alternative_answers.append('шагшагшаг')  # без пробелов

    if user_answer.strip().lower() in alternative_answers:
        print('Загадка решена!')
        room['puzzle'] = None
        current_room = game_state['current_room']
        if current_room == 'hall':
            print('Пьедестал открывается! Вы находите серебряную монету.')
            if 'silver_coin' not in room['items']:
                room['items'].append('silver_coin')
        elif current_room == 'trap_room':
            print('Система плит отключается. Вы в безопасности!')
        elif current_room == 'library':
            print('Вы находите скрытый отсек в книге с золотом!')
            if 'gold_nugget' not in game_state['player_inventory']:
                game_state['player_inventory'].append('gold_nugget')
        elif current_room == 'treasure_room':
            print('Код принят! Замок готов к открытию.')
        elif current_room == 'garden':
            print('Цветок расцветает, показывая драгоценный камень.')
            if 'precious_gem' not in room['items']:
                room['items'].append('precious_gem')
        elif current_room == 'secret_room':
            print('Стена открывается, показывая древний амулет!')
            if 'ancient_amulet' not in room['items']:
                room['items'].append('ancient_amulet')
        else:
            print('Вы получаете +10 к смекалке!')

    else:
         # в trap_room неверный ответ активирует ловушку
        if game_state['current_room'] == 'trap_room':
            print('Неверный ответ активирует ловушку!')
            from labyrinth_game.utils import trigger_trap
            trigger_trap(game_state)
        else:
            print('Неверно. Попробуйте снова')

def attempt_open_treasure(game_state):
    '''функция дляо ткрытия сундука'''

    # подключение описания текущей комнаты
    room=constants.ROOMS[game_state['current_room']]
    # проверяем, что мы в комнате с сокровищами и в ней есть сундук
    if (game_state['current_room'] != 'treasure_room'
        or 'treasure_chest' not in room['items']):
        print('Здесь нет сундука с сокровищами')
        return

    inventory = game_state['player_inventory']

    # проверка наличия ключа
    if 'treasure_key' in inventory:
        print('Вы применяете ключ, и замок щёлкает. Сундук открыт!')
        room['items'].remove('treasure_chest')
        print('В сундуке сокровище! Вы победили!')
        game_state['game_over'] = True
        return

    # если ключа нет, предлагаем ввести код
    print('Сундук заперт... Ввести код? (да/нет)')
    choice = get_input("> ").strip().lower()

    if room['puzzle'] is None: # если загадки уже нет, прерывание функции
        print("Не удалось найти код для взлома.")
        return

    if choice == 'да':
        question = room['puzzle'][:-1]
        correct_code = room['puzzle'][-1]
        print(*question) # выводим на экран загадку с кодом
        print("Введите код:")
        user_code = get_input()
        if user_code.strip() == correct_code.strip():
            room['items'].remove('treasure_chest')
            print('В сундуке сокровище! Вы победили!')
            game_state['game_over'] = True
            return
        else:
            print('Неверный код. Попробуйте еще раз или найдите ключ от сундука')
            return

    else:
        print("Вы отступаете от сундука.")
        return


def pseudo_random(seed, modulo):
    '''псевдослучайный генератор'''

    # используем формулу на основе синуса
    x = math.sin(seed * 12.9898) * 43758.5453

    # берем дробную часть
    fractional = x - math.floor(x)

    # приводим к нужному диапазону и возвращаем целое число
    return math.floor(fractional * modulo)


def trigger_trap(game_state):
    '''механика ловушек'''

    print('Ловушка активирована! Пол стал дрожать...')

    inventory = game_state['player_inventory']

    # если инвентарь не пуст - удаляется случайный предмет
    if inventory:
        # исключаем ключи, нужные для завершения игры
        losable_items = [
            item for item in inventory
            if item not in ['rusty_key', 'treasure_key', 'golden_key']
        ]

        if losable_items:
            item_index = pseudo_random(game_state['steps_taken'], len(losable_items))
            lost_item = losable_items[item_index]

            inventory.remove(lost_item)
            print(f'Вы потеряли {lost_item}')

            if not inventory:  # если после удаления инвентарь опустел
                print('Ваш инвентарь теперь пуст')

    # если инвентарь пуст - наносится урон
    else:
        damage_roll = pseudo_random(game_state['steps_taken'], constants.TRAP_DAMAGE_RANGE)

        if damage_roll < constants.TRAP_DAMAGE_THRESHOLD:
            print('Ловушка нанесла смертельный урон! Вы проиграли')
            game_state['game_over'] = True
        else:
            print('Вам удалось увернуться от ловушки!')

    # увеличиваем счетчик шагов
    game_state['steps_taken'] += 1


def random_event(game_state):
    '''случайные события при перемещении'''

    # проверяем, произойдет ли событие (10% шанс)
    event_chance = pseudo_random(game_state['steps_taken'], constants.EVENT_PROBABILITY10)
    if event_chance != 0:  # 90% что ничего не произойдет
        return

    # выбираем, какое именно событие произошло
    event_type = pseudo_random(game_state['steps_taken'] + 1, 3)  # 0, 1 или 2

    current_room_name = game_state['current_room']
    room = constants.ROOMS[current_room_name]
    inventory = game_state['player_inventory']

    match event_type:
        case 0:  # находка
            print('Находка: Вы нашли на полу блестящую монетку!')
            room['items'].append('coin')

        case 1:  # испуг
            print('Испуг: Вы слышите странный шорох в углу комнаты...')
            if 'sword' in inventory:
                print('Вы достаете меч, и звук мгновенно стихает')

        case 2:  # срабатывание ловушки (только в trap_room без факела)
            if (current_room_name == 'trap_room' and 'torch' not in inventory):
                print('В темноте вы наступили на подозрительную плитку!')
                trigger_trap(game_state)
            else:
                print('Ветер доносит чей-то шепот...')

    # увеличиваем счетчик шагов
    game_state['steps_taken'] += 1
