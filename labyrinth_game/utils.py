from labyrinth_game import constants

def describe_current_room(game_state):
    #подключение описания текущей комнаты
    room=constants.ROOMS[game_state['current_room']]

    #вывод описания комнаты
    print(f"=={game_state['current_room']}==")

    print(*room['description'])

    if room['items']: #проверка на непустой список items
        print('Заметные предметы:', ", ".join(room['items']))

    exits = list(room['exits'].keys()) #создание списка из ключей словаря выходов
    print('Выходы:', ', '.join(exits))

    if room['puzzle'] is not None: #проверка есть ли загадка
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
