from labyrinth_game.utils import describe_current_room, show_help
from labyrinth_game.player_actions import (
    show_inventory,
    get_input,
    move_player,
    take_item,
    use_item
)

game_state = {
    'player_inventory': [], # Инвентарь игрока
    'current_room': 'entrance', # Текущая комната
    'game_over': False, # Значения окончания игры
    'steps_taken': 0 # Количество шагов
}

def process_command(game_state, command): # функция обработки команд
    # разбиваем команду на части для более простой обработки команд по типу "go north"
    parts = command.split()
    if not parts:
        return # если пользователь введет пустую строку, программа не прервется ошибкой
    main_command = parts[0]
    if len(parts) > 1:
        argument = parts[1]

    match main_command:
        case 'look': # осмотреться
            describe_current_room(game_state)

        case 'inventory': # проверить инвентарь
            show_inventory(game_state)

        case 'take': # взять предмет
            if argument:
                take_item(game_state, argument)
            else:
                print('Укажите предмет для взятия. Например: take torch')

        case 'go': # изменить команту
            if argument in ['north', 'south', 'east', 'west']:
                move_player(game_state, argument)
            else:
                print('Укажите направление. Например: go north')

        case 'use': # использовать предмет
            if argument:
                use_item(game_state, argument)
            else:
                print("Укажите предмет для использования. Например: use torch")

        case 'help': # список команд
            show_help()

        case 'quit' | 'exit': # выйти из игры
            print('Спасибо за игру!')
            game_state['game_over'] = True

        case _: # ошибка
            print('Неизвестная команда. Доступные: используйте help')

def main():
    print('Добро пожаловать в Лабиринт сокровищ!')
    describe_current_room(game_state)
    while not game_state['game_over']:
        print ('Что вы хотите сделать? Доступные команды: используйте help')
        command = get_input("> ")
        process_command(game_state, command)

if __name__ == "__main__":
    main()
