from labyrinth_game.utils import describe_current_room
from labyrinth_game.player_actions import show_inventory, get_input

game_state = {
    'player_inventory': [], # Инвентарь игрока
    'current_room': 'entrance', # Текущая комната
    'game_over': False, # Значения окончания игры
    'steps_taken': 0 # Количество шагов
}

def main():
    print('Добро пожаловать в Лабиринт сокровищ!')
    describe_current_room(game_state)
    while not game_state['game_over']:
        print ('Что вы хотите сделать? Доступные команды: look, inventory, quit')
        command = get_input("> ")

        if command == 'look':
            describe_current_room(game_state)
        elif command == 'inventory':
            show_inventory(game_state)
        elif command == 'quit':
            print('Спасибо за игру!')
            game_state['game_over'] = True
        else:
            print('Неизвестная команда. Доступные команды: look, inventory, quit')

        game_state['steps_taken'] += 1



if __name__ == "__main__":
    main()
