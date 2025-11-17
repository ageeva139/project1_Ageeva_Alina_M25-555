from labyrinth_game import constants
from labyrinth_game.player_actions import get_input

def describe_current_room(game_state): # описание комнаты
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
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")

def solve_puzzle(game_state): # разгадать загадку
    # подключение описания текущей комнаты
    room=constants.ROOMS[game_state['current_room']]

    if room['puzzle'] is None: # если загадки нет, произойдет прерывание функции
        print('Загадок здесь нет')
        return

    question = room['puzzle'][:-1]
    correct_answer = room['puzzle'][-1]

    print('Загадка:', *question)
    user_answer = get_input('Ваш ответ: ')

    if user_answer.strip().lower() == correct_answer.strip().lower():
        print('Загадка решена!')
        room['puzzle'] = None
        print('Вы получаете +10 к смекалке!')

    else:
        print('Неверно. Попробуйте снова')

def attempt_open_treasure(game_state): # функция дляо ткрытия сундука

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
