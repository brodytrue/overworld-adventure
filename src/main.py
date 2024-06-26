import os, sys, time, shutil

locations = {
    'Dark Forest': {'North': 'Giant Cliffs', 'South': 'The Caverns', 'East': 'The Ocean', 'West': 'Green Plains'},
    'Green Plains': {'East': 'Dark Forest', 'Potion': 'HP'},
    'Giant Cliffs': {'North': 'Heaven', 'South': 'Dark Forest', 'Enemy': 'Giant'},
    'Heaven': {'South': 'Giant Cliffs', 'Weapon': 'Heavenly Sword'},
    'The Ocean': {'West': 'Dark Forest', 'Weapon': 'Shark Tooth Hatchet'},
    'The Caverns': {'North': 'Dark Forest', 'South': 'Hell', 'Weapon': 'Wooden Slingshot'},
    'Hell': {'North': 'The Caverns', 'Enemy': 'Satan'}
}

enemies = {
    'Giant': {'HP': 80, "DMG": 5},
    'Satan': {'HP': 120, "DMG": 15}
}

game_items = {
    'Fists': {'DMG': 3},
    'Heavenly Sword': {'DMG': 35},
    'Shark Tooth Hatchet': {'DMG': 30},
    'Wooden Slingshot': {'DMG': 20}
}

potions = {
    'HP': 15
}

welcome_strings = [
    'Welcome to Overworld Adventure!',
    'Upon starting the game, you will be asked which way you would like to go.',
    'You can explore the world by typing \'north\', \'south\', \'east\', or \'west\'.',
    'Your goal is to defeat all the monsters in the world.',
    'Good luck!'
]

current_location = 'Dark Forest'
msg = 'You are in Dark Forest.'

inventory = ['Fists']
enemies_killed = []
found_potions = []
player_HP = 100
player_dead = 0

yellow = '\033[93m'
red = '\033[91m'
green = '\033[92m'
white = '\033[00m'

# Clear screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_center(s):
    print(s.center(shutil.get_terminal_size().columns))

# Character by character print
def slow_print(msg):
    for char in msg:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.1)

# Display welcome screen
def welcome():
    clear()
    for s in welcome_strings:
        print_center(s)
    print('Press ENTER to continue.')
    input('> ')

# Check if there is an item in the current location and handle appropriately
def handleItem(location):
    if 'Weapon' in location:
        item_name = location['Weapon']
        item_DMG = game_items[item_name]['DMG']
        if item_name not in inventory:
            print(f'You found {yellow}{item_name}{white}! It does {item_DMG} DMG!')
            inventory.append(item_name)
    if 'Potion' in location:
        global player_HP
        potion_name = location['Potion']
        potion_HP = potions[potion_name]
        if potion_name not in found_potions:
            if player_HP < 100:
                if player_HP <= 85:
                    print(f'You found {red}{potion_name} Potion{white}! Restored {potion_HP} HP.')
                    player_HP += 15
                else:
                    print(f'You found {red}{potion_name} Potion{white}! Restored {100 - player_HP} HP.')
                    player_HP += (100 - player_HP)
                found_potions.append(potion_name)
            else:
                print(f'You found {red}{potion_name} Potion{white}, but your health is full. You decide to leave it.')
            

# Check if there is an enemy in the current location and handle appropriately
def handleEnemy(location):
    if 'Enemy' in location:
        enemy_name = location['Enemy']
        enemy_HP = enemies[enemy_name]['HP']
        enemy_DMG = enemies[enemy_name]['DMG']
        if enemy_name not in enemies_killed:
            print(f'{enemy_name} lurks... HP: {enemy_HP} DMG: {enemy_DMG}')
            while True:
                print(f'Would you like to fight {enemy_name}? (Y/N)')
                choice = input('> ').upper()
                if choice == 'Y':
                    # Add logic for fighting the enemy here
                    handleBattle(enemy_name, enemy_HP, enemy_DMG)
                    break
                elif choice == 'N':
                    print('You choose to flee.')
                    break
                else:
                    print('Invalid choice. Please enter Y or N.')

def handleBattle(enemy_name, enemy_HP, enemy_DMG):
    global player_HP
    global player_dead
    enemy_HP = enemy_HP
    enemy_DMG = enemy_DMG
    battle_HP = player_HP
    player_DMG = 0
    selected_item = ''
    clear()
    print(f'You choose to fight {enemy_name}.')
    
    # Weapon choice
    print('Which weapon will you use?')
    item_choice_dict = {}
    i = 0
    for item in inventory:
        item_choice_dict[str(i)] = item
        item_DMG = game_items[item]['DMG']
        print(f'{i}.  {item} (DMG: {item_DMG})')
        i += 1
    while True:
        choice = input('> ')
        if choice in item_choice_dict:
            selected_item = item_choice_dict[choice]
            clear()
            print(f'You ready your {selected_item}.')
            player_DMG = game_items[selected_item]['DMG']
            break
        else:
            print('Invalid weapon choice.')

    battle_iterations = 0

    # Fight loop
    while enemy_HP > 0:
        if battle_HP <= 0:
            clear()
            print(f'{red}You died!{white}')
            player_HP = battle_HP
            player_dead = 1
            return
        if battle_iterations > 0:
            clear()
            print(f'Your {selected_item} did {player_DMG} DMG!')
            print(f'{enemy_name} dealt {enemy_DMG} DMG!')
        print(f'Your HP: {battle_HP}')
        print(f'Enemy HP: {enemy_HP}')
        print('Press enter to attack!')
        choice = input('> ').upper()
        enemy_HP -= player_DMG
        battle_HP -= enemy_DMG
        battle_iterations += 1
    clear()
    print(f'{green}You won!{white}')
    enemies_killed.append(enemy_name)
    player_HP = battle_HP

# Start Game
welcome()

while True:
    clear()
    print(msg)
    print('Inventory:')
    for item in inventory:
        item_DMG = game_items[item]['DMG']
        print(f'  - {item} (DMG: {item_DMG})')
    print(f'HP:', player_HP)

    handleItem(locations[current_location])

    handleEnemy(locations[current_location])

    # Check if all enemies have been killed
    if len(enemies_killed) == len(enemies):
        print('You have killed all the enemies!')
        print('Your items:', ', '.join(inventory))
        break

    # Check if player is dead
    if player_dead != 0:
        break

    # Player move
    print('Which way would you like to go?')
    choice = input('> ').title()
    try:
        current_location = locations[current_location][choice]
        msg = f'You are in {current_location}.'
    except:
        msg = f'Not a valid direction.\nYou are in {current_location}.'
    
print('Thanks for playing!')