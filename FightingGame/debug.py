import colorama
from time import sleep as sp
import json
import random
import time
import keyboard
import pyperclip

# Load JSON data

with open('i2.json', 'r') as file:
    data = json.load(file)

bosses = data['Bosses']

def verify():
    return "VERIFY-CODE-"+"".join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))
def clear():
    print("\033[H\033[J", end="")  # Clear screen

def very_cool_print(text, speed=0.05):
    for char in text:
        print(char, end='', flush=True)
        sp(speed)

def very_cool_unprint(text, speed=0.05):
    t = text
    for i in range(len(text)+1):
        clear()
        print(t[:-i], end='', flush=True)
        sp(speed)

def startup():
    sp(2)
    very_cool_print("Moo Studios \n")
    sp(1)
    # Get the date
    very_cool_print(f"{time.strftime('%m-%d-%Y')}")
    sp(1)
    very_cool_unprint(f"Moo Studios \n{time.strftime('%m-%d-%Y')}", speed=0.05)
    sp(2)
    very_cool_print("Untitled Fighting Game \nCreated by Moo Studios\n")
    sp(0.5)
    very_cool_print("Click Space to start...")
    keyboard.wait('space')

def choose_boss(sm):
    # Get all keys from bosses dictionary
    bosses_got = list(bosses.keys())

    if not sm:
        very_cool_print("Choosing boss...")
        sp(0.2)
        very_cool_unprint("Choosing boss...")
        sp(0.5)
    current_boss = None
    for i in range(random.randint(1,10)):
        for boss in bosses_got:
            if not sm:
                very_cool_print(boss)
                sp(0.2*i)
                very_cool_unprint(boss)
            current_boss = boss
    very_cool_print(f"{current_boss} Chosen!")
    return current_boss

clear()

# Print loading message
print("Please wait while loading the data...")
sp(1)
sp(0.5)
clear()
code = input("Debug Code :>")
clear()
sm = False
if not code == "skip":
    startup()
else:
    sm = True
clear()
chosen_boss = choose_boss(sm)

colorama.init(autoreset=True)

health = 100
full_bar = "█"
blinker = True

# Swap helper function
def swap(x, a, b):
    return a if x == b else b

# Print health bar
def print_health_bar(hlth):
    bars = hlth // 10
    rbars = bars + 1
    health_bar = full_bar * rbars

    if bars < 4:
        color = colorama.Fore.RED
    elif bars < 8:
        color = colorama.Fore.YELLOW
    elif bars == 0:
        color = colorama.Fore.WHITE
    else:
        color = colorama.Fore.GREEN

    colored_bar = f"{color}{health_bar}{colorama.Fore.RESET}"
    if bars < 4:
        return f"[{colored_bar}{' ' * (10 - rbars)}]"
    elif bars >= 4:
        return f"[{colored_bar}{' ' * (10 - rbars)}]"
    
def choose_attack(boss:str):
    attacks = bosses[boss]
    attack = random.choice(list(attacks.keys())[:-1])
    return attack
level = 1
xpneeded = 100
xp = 0
player_attacks = {
    "punch": 10,
    "kick": 15,
}
original_attacks = {
    "punch": 10,
    "kick": 15,
}
def define_player_attacks():
    global player_attacks
    for item in player_attacks:
        player_attacks[item] = original_attacks[item] * level
    

# Main loop
while True:
    turn = "Boss"
    damage_done = 0
    boss_health = data["Bosses"][chosen_boss]["Stats"][0]
    while boss_health > 0 and health > 0:     
        clear()
        print("You:",print_health_bar(health))
        print(f"{chosen_boss}:", print_health_bar(boss_health))
        if turn == "Boss":
            chosen_attack = choose_attack(chosen_boss)
            print()
            damage = random.randint(1,bosses[chosen_boss][chosen_attack])
            very_cool_print(f"{chosen_boss} uses {chosen_attack}, You lose {damage} health.")         
            health -= damage
            sp(1)
        elif turn == "Player":
            very_cool_print("Choose your attack: \n")
            for i, attack in enumerate(player_attacks.keys()):
                very_cool_print(f"{i+1}. {attack} \n")
            c = input("Enter your choice:")
            supermode = False
            if c.strip().isdigit():
                choice = int(c) - 1
            else:
                if choice < 0 or choice >= len(player_attacks):
                    very_cool_print("Invalid choice.")
                    continue
            chosen_attack = list(player_attacks.keys())[choice]
            if not supermode:
                damage = random.randint(1,player_attacks[chosen_attack]+1)
            damage_done += damage
            boss_health -= damage
            very_cool_print(f"You use {chosen_attack}, Boss loses {damage} health. \n")
            if damage >= player_attacks[chosen_attack]:
                added_damage = random.randint(1, player_attacks[chosen_attack] * 2)
                damage_done += added_damage
                very_cool_print(f"Critical hit! Boss recieves {added_damage} more damage. \n")
                boss_health -= added_damage
            sp(2)
        
        turn = swap(turn, "Player", "Boss")
    if not health > 0:
        very_cool_print("You died! \n")
        sp(2)
        very_cool_print("Would you like to restart? \n")
        choice = input("Enter y/n: ")
        if choice.lower() == "y":
            health = 100
        else:
            break
    else:
        very_cool_print("\n Congrats, You defeated the boss.\n")
        sp(1)
        very_cool_print(f"You gained {damage_done} XP, As a total of all your hits.\n")
        xp += damage_done
        sp(2)
        very_cool_print(f"Your XP is now {xp}/{xpneeded}\n")
        sp(2)
        if xp >= xpneeded:
            while xp >= xpneeded:
                level += 1
                xp -= xpneeded
                xpneeded *= 2   
                define_player_attacks()  
                 
            very_cool_print(f"Congratulations, You leveled up! Your level is now {level}. \n")
            sp(1)
                
            very_cool_print(f"You can feel more strength inside of you.. \n")
            sp(2)
            very_cool_print(f"You feel like you can enter another round.. \n")
            sp(2)
            health = 100
        chosen_boss = choose_boss(sm)
            
        
                
        
