"""
Консольное приложение для учета доходов и расходов
"""
import json
import os
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Optional


class FinanceRecord:
    """Класс для представления записи о доходе или расходе"""
    
    def __init__(self, amount: float, category: str, date: str, description: str, record_type: str):
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description
        self.record_type = record_type  # "income" или "expense"
    
    def to_dict(self) -> Dict:
        """Преобразует запись в словарь для сохранения"""
        return {
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description,
            "type": self.record_type
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'FinanceRecord':
        """Создает запись из словаря"""
        return cls(
            amount=data["amount"],
            category=data["category"],
            date=data["date"],
            description=data["description"],
            record_type=data["type"]
        )


class FinanceManager:
    """Класс для управления финансовыми записями"""
    
    def __init__(self, data_file: str = "finance_data.json"):
        self.data_file = data_file
        self.records: List[FinanceRecord] = []
        self.predefined_categories = {
            "expense": ["Еда", "Транспорт", "Развлечения", "Жилье", "Здоровье", "Одежда", "Образование"],
            "income": ["Зарплата", "Подарки", "Инвестиции", "Прочее"]
        }
        self.custom_categories = {
            "expense": [],
            "income": []
        }
        self.load_data()
    
    def load_data(self):
        """Загружает данные из файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.records = [FinanceRecord.from_dict(record) for record in data.get("records", [])]
                    self.custom_categories = data.get("custom_categories", {
                        "expense": [],
                        "income": []
                    })
            except Exception as e:
                print(f"Ошибка при загрузке данных: {e}")
                self.records = []
    
    def save_data(self):
        """Сохраняет данные в файл"""
        try:
            data = {
                "records": [record.to_dict() for record in self.records],
                "custom_categories": self.custom_categories
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")
    
    def add_record(self, amount: float, category: str, date: str, description: str, record_type: str):
        """Добавляет новую запись"""
        record = FinanceRecord(amount, category, date, description, record_type)
        self.records.append(record)
        
        # Добавляем категорию в пользовательские, если её нет в предустановленных
        if record_type in ["expense", "income"]:
            predefined = self.predefined_categories.get(record_type, [])
            if category not in predefined and category not in self.custom_categories[record_type]:
                self.custom_categories[record_type].append(category)
        
        self.save_data()
        print(f"\n✓ Запись успешно добавлена!")
    
    def get_balance(self) -> float:
        """Вычисляет итоговый баланс"""
        balance = 0.0
        for record in self.records:
            if record.record_type == "income":
                balance += record.amount
            else:
                balance -= record.amount
        return balance
    
    def get_records(self, start_date: Optional[str] = None, 
                   end_date: Optional[str] = None,
                   category: Optional[str] = None,
                   record_type: Optional[str] = None) -> List[FinanceRecord]:
        """Получает записи с фильтрацией"""
        filtered = self.records
        
        if start_date:
            filtered = [r for r in filtered if r.date >= start_date]
        if end_date:
            filtered = [r for r in filtered if r.date <= end_date]
        if category:
            filtered = [r for r in filtered if r.category == category]
        if record_type:
            filtered = [r for r in filtered if r.record_type == record_type]
        
        return sorted(filtered, key=lambda x: x.date, reverse=True)
    
    def get_expenses_by_category(self) -> Dict[str, float]:
        """Подсчитывает расходы по категориям"""
        expenses = defaultdict(float)
        for record in self.records:
            if record.record_type == "expense":
                expenses[record.category] += record.amount
        return dict(expenses)
    
    def get_top_expense_categories(self, top_n: int = 5) -> List[tuple]:
        """Возвращает топ категории расходов"""
        expenses = self.get_expenses_by_category()
        return sorted(expenses.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    def get_income_expense_ratio(self) -> Dict[str, float]:
        """Вычисляет соотношение доходов и расходов"""
        total_income = sum(r.amount for r in self.records if r.record_type == "income")
        total_expense = sum(r.amount for r in self.records if r.record_type == "expense")
        
        return {
            "income": total_income,
            "expense": total_expense,
            "balance": total_income - total_expense,
            "ratio": (total_expense / total_income * 100) if total_income > 0 else 0
        }
    
    def get_all_categories(self, record_type: str) -> List[str]:
        """Возвращает все категории (предустановленные + пользовательские)"""
        predefined = self.predefined_categories.get(record_type, [])
        custom = self.custom_categories.get(record_type, [])
        return predefined + custom


class FinanceApp:
    """Главный класс приложения"""
    
    def __init__(self):
        self.manager = FinanceManager()
    
    def display_menu(self):
        """Отображает главное меню"""
        print("\n" + "="*50)
        print("  УЧЕТ ДОХОДОВ И РАСХОДОВ")
        print("="*50)
        print("1. Добавить доход")
        print("2. Добавить расход")
        print("3. Просмотреть баланс")
        print("4. Просмотреть все записи")
        print("5. Фильтр записей")
        print("6. Анализ расходов по категориям")
        print("7. Топ категории расходов")
        print("8. Соотношение доходов и расходов")
        print("9. Добавить пользовательскую категорию")
        print("0. Выход")
        print("="*50)
    
    def input_date(self, prompt: str = "Дата (ГГГГ-ММ-ДД или Enter для сегодня): ") -> str:
        """Ввод даты с проверкой"""
        date_str = input(prompt).strip()
        if not date_str:
            return datetime.now().strftime("%Y-%m-%d")
        
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Неверный формат даты! Используется сегодняшняя дата.")
            return datetime.now().strftime("%Y-%m-%d")
    
    def input_amount(self, prompt: str = "Сумма: ") -> float:
        """Ввод суммы с проверкой"""
        while True:
            try:
                amount = float(input(prompt).strip())
                if amount <= 0:
                    print("Сумма должна быть положительным числом!")
                    continue
                return amount
            except ValueError:
                print("Неверный формат! Введите число.")
    
    def select_category(self, record_type: str) -> str:
        """Выбор категории"""
        categories = self.manager.get_all_categories(record_type)
        
        if not categories:
            print("Нет доступных категорий. Создайте новую.")
            return input("Введите название категории: ").strip()
        
        print(f"\nДоступные категории ({'доходы' if record_type == 'income' else 'расходы'}):")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        print(f"{len(categories) + 1}. Создать новую категорию")
        
        while True:
            try:
                choice = int(input("\nВыберите категорию: ").strip())
                if 1 <= choice <= len(categories):
                    return categories[choice - 1]
                elif choice == len(categories) + 1:
                    new_cat = input("Введите название новой категории: ").strip()
                    if new_cat:
                        return new_cat
                    print("Название категории не может быть пустым!")
                else:
                    print("Неверный выбор!")
            except ValueError:
                print("Введите число!")
    
    def add_income(self):
        """Добавление дохода"""
        print("\n--- ДОБАВЛЕНИЕ ДОХОДА ---")
        amount = self.input_amount("Сумма дохода: ")
        category = self.select_category("income")
        date = self.input_date("Дата (ГГГГ-ММ-ДД или Enter для сегодня): ")
        description = input("Описание (необязательно): ").strip()
        
        self.manager.add_record(amount, category, date, description, "income")
    
    def add_expense(self):
        """Добавление расхода"""
        print("\n--- ДОБАВЛЕНИЕ РАСХОДА ---")
        amount = self.input_amount("Сумма расхода: ")
        category = self.select_category("expense")
        date = self.input_date("Дата (ГГГГ-ММ-ДД или Enter для сегодня): ")
        description = input("Описание (необязательно): ").strip()
        
        self.manager.add_record(amount, category, date, description, "expense")
    
    def view_balance(self):
        """Просмотр баланса"""
        print("\n--- ИТОГОВЫЙ БАЛАНС ---")
        balance = self.manager.get_balance()
        
        ratio = self.manager.get_income_expense_ratio()
        
        print(f"Общий доход: {ratio['income']:.2f} ₽")
        print(f"Общий расход: {ratio['expense']:.2f} ₽")
        print(f"{'='*30}")
        print(f"ИТОГОВЫЙ БАЛАНС: {balance:.2f} ₽")
        
        if balance < 0:
            print("⚠ Внимание: отрицательный баланс!")
        elif balance == 0:
            print("Баланс равен нулю.")
        else:
            print("✓ Положительный баланс.")
    
    def view_all_records(self):
        """Просмотр всех записей"""
        print("\n--- ВСЕ ЗАПИСИ ---")
        records = self.manager.get_records()
        
        if not records:
            print("Нет записей.")
            return
        
        print(f"\nВсего записей: {len(records)}\n")
        print(f"{'Дата':<12} {'Тип':<10} {'Категория':<20} {'Сумма':<12} {'Описание':<30}")
        print("-" * 90)
        
        for record in records:
            record_type = "Доход" if record.record_type == "income" else "Расход"
            amount_str = f"{record.amount:.2f} ₽"
            print(f"{record.date:<12} {record_type:<10} {record.category:<20} {amount_str:<12} {record.description[:30]:<30}")
    
    def filter_records(self):
        """Фильтрация записей"""
        print("\n--- ФИЛЬТР ЗАПИСЕЙ ---")
        
        start_date = input("Начальная дата (ГГГГ-ММ-ДД или Enter для пропуска): ").strip() or None
        end_date = input("Конечная дата (ГГГГ-ММ-ДД или Enter для пропуска): ").strip() or None
        
        print("\nФильтр по категории:")
        print("1. Все категории")
        print("2. Только доходы")
        print("3. Только расходы")
        print("4. Конкретная категория")
        
        category = None
        record_type = None
        
        choice = input("Выбор: ").strip()
        if choice == "2":
            record_type = "income"
        elif choice == "3":
            record_type = "expense"
        elif choice == "4":
            cat_name = input("Введите название категории: ").strip()
            category = cat_name
        
        records = self.manager.get_records(start_date, end_date, category, record_type)
        
        if not records:
            print("\nЗаписей не найдено.")
            return
        
        print(f"\nНайдено записей: {len(records)}\n")
        print(f"{'Дата':<12} {'Тип':<10} {'Категория':<20} {'Сумма':<12} {'Описание':<30}")
        print("-" * 90)
        
        for record in records:
            record_type_str = "Доход" if record.record_type == "income" else "Расход"
            amount_str = f"{record.amount:.2f} ₽"
            print(f"{record.date:<12} {record_type_str:<10} {record.category:<20} {amount_str:<12} {record.description[:30]:<30}")
    
    def analyze_expenses_by_category(self):
        """Анализ расходов по категориям"""
        print("\n--- РАСХОДЫ ПО КАТЕГОРИЯМ ---")
        expenses = self.manager.get_expenses_by_category()
        
        if not expenses:
            print("Нет записей о расходах.")
            return
        
        total = sum(expenses.values())
        print(f"\nОбщая сумма расходов: {total:.2f} ₽\n")
        print(f"{'Категория':<25} {'Сумма':<15} {'% от общего':<15}")
        print("-" * 55)
        
        sorted_expenses = sorted(expenses.items(), key=lambda x: x[1], reverse=True)
        for category, amount in sorted_expenses:
            percentage = (amount / total * 100) if total > 0 else 0
            print(f"{category:<25} {amount:<15.2f} {percentage:<15.2f}%")
    
    def view_top_categories(self):
        """Просмотр топ категорий расходов"""
        print("\n--- ТОП КАТЕГОРИИ РАСХОДОВ ---")
        top_n = input("Сколько категорий показать (по умолчанию 5): ").strip()
        
        try:
            top_n = int(top_n) if top_n else 5
        except ValueError:
            top_n = 5
        
        top_categories = self.manager.get_top_expense_categories(top_n)
        
        if not top_categories:
            print("Нет записей о расходах.")
            return
        
        print(f"\nТоп-{len(top_categories)} категорий:\n")
        print(f"{'Место':<8} {'Категория':<25} {'Сумма':<15}")
        print("-" * 50)
        
        for i, (category, amount) in enumerate(top_categories, 1):
            print(f"{i:<8} {category:<25} {amount:<15.2f} ₽")
    
    def view_income_expense_ratio(self):
        """Просмотр соотношения доходов и расходов"""
        print("\n--- СООТНОШЕНИЕ ДОХОДОВ И РАСХОДОВ ---")
        ratio = self.manager.get_income_expense_ratio()
        
        print(f"\nОбщий доход: {ratio['income']:.2f} ₽")
        print(f"Общий расход: {ratio['expense']:.2f} ₽")
        print(f"Баланс: {ratio['balance']:.2f} ₽")
        
        if ratio['income'] > 0:
            print(f"\nРасходы составляют {ratio['ratio']:.2f}% от доходов")
            
            if ratio['ratio'] > 100:
                print("⚠ Внимание: расходы превышают доходы!")
            elif ratio['ratio'] > 80:
                print("⚠ Внимание: расходы близки к доходам!")
            else:
                print("✓ Расходы в пределах нормы.")
        else:
            print("\nНет записей о доходах.")
    
    def add_custom_category(self):
        """Добавление пользовательской категории"""
        print("\n--- ДОБАВЛЕНИЕ КАТЕГОРИИ ---")
        print("1. Категория для доходов")
        print("2. Категория для расходов")
        
        choice = input("Выбор: ").strip()
        
        if choice == "1":
            record_type = "income"
        elif choice == "2":
            record_type = "expense"
        else:
            print("Неверный выбор!")
            return
        
        category = input("Введите название категории: ").strip()
        
        if not category:
            print("Название категории не может быть пустым!")
            return
        
        if category in self.manager.predefined_categories.get(record_type, []):
            print("Эта категория уже есть в предустановленных!")
            return
        
        if category in self.manager.custom_categories[record_type]:
            print("Эта категория уже существует!")
            return
        
        self.manager.custom_categories[record_type].append(category)
        self.manager.save_data()
        print(f"✓ Категория '{category}' успешно добавлена!")
    
    def run(self):
        """Запуск приложения"""
        while True:
            self.display_menu()
            choice = input("\nВыберите действие: ").strip()
            
            if choice == "1":
                self.add_income()
            elif choice == "2":
                self.add_expense()
            elif choice == "3":
                self.view_balance()
            elif choice == "4":
                self.view_all_records()
            elif choice == "5":
                self.filter_records()
            elif choice == "6":
                self.analyze_expenses_by_category()
            elif choice == "7":
                self.view_top_categories()
            elif choice == "8":
                self.view_income_expense_ratio()
            elif choice == "9":
                self.add_custom_category()
            elif choice == "0":
                print("\nДо свидания!")
                break
            else:
                print("\nНеверный выбор! Попробуйте снова.")
            
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    app = FinanceApp()
    app.run()
