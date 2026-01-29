import random
import os
import json
from datetime import datetime


class Character:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.exp = 0
        self.exp_to_level = 100
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.defense = 5
        self.charisma = 3
        self.inventory = {"healing_potion": 3, "strength_potion": 1}
        self.specialization = ""
        self.location = "Опушка леса"

    def display_stats(self):
        print(f"\n=== ХАРАКТЕРИСТИКИ {self.name.upper()} ===")
        print(f"Уровень: {self.level}")
        print(f"Опыт: {self.exp}/{self.exp_to_level}")
        print(f"Здоровье: {self.health}/{self.max_health}")
        print(f"Атака: {self.attack}")
        print(f"Защита: {self.defense}")
        print(f"Харизма:{self.charisma}")
        print(f"Раса: {self.specialization}")
        print("Инвентарь:", self.inventory)

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense // 2)
        self.health -= actual_damage
        return actual_damage

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
        return amount

    def add_exp(self, amount):
        self.exp += amount
        if self.exp >= self.exp_to_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_level
        self.exp_to_level = int(self.exp_to_level * 1.5)
        self.max_health += 20
        self.health = self.max_health
        self.attack += 5
        self.defense += 3

        print(f"\n🎉 Поздравляем! Вы достигли {self.level} уровня!")
        print("Ваши характеристики улучшены!")
        self.display_stats()

    def use_item(self, item):
        if item in self.inventory and self.inventory[item] > 0:
            self.inventory[item] -= 1
            if item == "healing_potion":
                healed = self.heal(30)
                print(f"Использовано пирожок с вишней. Восстановлено {healed} здоровья.")
            if item == "strength_potion":
                self.attack += 5
                print("Использовано пирожок с манго. Атака увеличена на 5 на этот бой.")
            return True
        return False


class Enemy:
    def __init__(self, name, health, attack, defense, exp_reward):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.exp_reward = exp_reward

    def display_stats(self):
        print(f"\n=== {self.name.upper()} ===")
        print(f"Здоровье: {self.health}/{self.max_health}")
        print(f"Атака: {self.attack}")
        print(f"Защита: {self.defense}")

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense // 2)
        self.health -= actual_damage
        return actual_damage


class Game:
    def __init__(self):
        self.player = None
        self.game_over = False
        self.locations = {
            "Опушка леса": {
                "description": "Вы находитесь на опушке леса. Вроде всё тихо.",
                "connections": ["Сумречный лес", "Заброщенный замок"],
                "events": ["rest", "find_item"]
            },
            "Сумречный лес": {
                "description": "Лес из в вечных сумраках. В воздухе витает странная энергия.",
                "connections": ["Опушка леса", "Вонючая пещера"],
                "events": ["enemy", "find_item"]
            },
            "Вонючая пещера": {
                "description": "Глубокая пещера, стены которой покрыты странной белой субстанцией.",
                "connections": ["Сумречный лес"],
                "events": ["boss", "treasure"]
            },
            "Заброщенный замок": {
                "description": "Заброшенный каменный замок. Кажется владелец за ним не очень хорошо следит.",
                "connections": ["Опушка леса", "Большая золотая комната"],
                "events": ["enemy", "find_item"]
            },
            "Большая золотая комната": {
                "description": "Огромная комната из золота. Здесь могут лежать всякие безделушки и не только.",
                "connections": ["Заброщенный замок"],
                "events": ["rest", "treasure"]
            }
        }

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def create_character(self):
        self.clear_screen()
        print("=== СОЗДАНИЕ ПЕРСОНАЖА ===")
        name = input("Введите имя вашего персонажа: ")

        print("\nВыберите расу:")
        print("1. Высший эльф (высокий интеллект, бонус к исследованиям)")
        print("2. Дварф (улучшенная техника, бонус к ремонту)")
        print("3. Тифлинг (харизма, бонус к взаимодействию с командой)")
        print("4. Гоблин (Гнусавость, низкий рост, бесполезность, никчемность, -харизма)")

        while True:
            choice = input("> ")
            if choice in ["1", "2", "3", "4"]:
                break
            print("Пожалуйста, выберите 1, 2, 3 или 4")
