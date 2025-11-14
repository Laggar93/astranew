import pandas as pd
import random
from datetime import datetime

# Данные для заполнения
brands = ['Bosch', 'Makita', 'DeWalt', 'Hitachi', 'Stanley', 'Metabo', 'Einhell', 'AEG', 'Black+Decker', 'Skil']
countries = ['Германия', 'Япония', 'США', 'Китай', 'Тайвань', 'Швейцария', 'Италия']
categories = {
    'Электроинструменты': ['Дрели', 'Шуруповерты', 'Перфораторы', 'Шлифмашины', 'Пилы'],
    'Ручные инструменты': ['Молотки', 'Отвертки', 'Ключи', 'Плоскогубцы'],
    'Измерительные инструменты': ['Лазерные уровни', 'Рулетки', 'Угломеры']
}

# Генерация данных товаров
products_data = []

for i in range(1, 11):
    # Выбираем случайные категории
    main_category = random.choice(list(categories.keys()))
    subcategory = random.choice(categories[main_category])

    product = {
        'article': f'ART{1000 + i}',
        'product_title': f'Инструмент {i} Профессиональный',
        'product_price': round(random.uniform(1500, 25000), 2),
        'category': main_category,
        'subcategory': subcategory,
        'brand': random.choice(brands),
        'country': random.choice(countries),
        'instock': random.choice([True, False]),
        'leftovers': random.choice([True, False]),
        'pop_models': random.choice([True, False]),
        'order': i,

        # SEO поля
        'title': f'Купить {main_category} {subcategory} - цена, характеристики',
        'description': f'Профессиональный {subcategory.lower()} {random.choice(brands)}. Гарантия качества.',
        'keywords': f'{main_category}, {subcategory}, {random.choice(brands)}, инструмент',

        # Основное описание (HTML для CKEditor)
        'product_description': f'''
        <h3>Профессиональный {subcategory} {random.choice(brands)}</h3>
        <p>Высококачественный инструмент для профессионального использования.</p>
        <ul>
            <li>Мощный двигатель</li>
            <li>Эргономичный дизайн</li>
            <li>Долгий срок службы</li>
        </ul>
        <p><strong>Технические характеристики:</strong></p>
        <table border="1">
            <tr><td>Мощность</td><td>{random.randint(500, 2000)} Вт</td></tr>
            <tr><td>Вес</td><td>{random.uniform(1.5, 5.0):.1f} кг</td></tr>
        </table>
        ''',

        # Основное изображение (Яндекс.Диск)
        'main_image': f'https://disk.yandex.ru/d/example_folder/product_{i}_main.jpg',

        # SEO текст
        'seo_text': f'''
        <h2>О профессиональном инструменте {random.choice(brands)}</h2>
        <p>Этот {subcategory.lower()} предназначен для интенсивного использования в профессиональной сфере.</p>
        '''
    }

    products_data.append(product)

# Создаем DataFrame
df = pd.DataFrame(products_data)

# Добавляем колонки для слайдов (5 слайдов на товар)
for slide_num in range(1, 6):
    df[f'slide_{slide_num}_image'] = [f'https://disk.yandex.ru/d/example_folder/product_{i}_slide_{slide_num}.jpg' for i in range(1, 11)]
    df[f'slide_{slide_num}_alt'] = [f'Слайд {slide_num} - {row["product_title"]}' for _, row in df.iterrows()]

# Добавляем колонки для документов (7 документов на товар)
doc_types = ['Инструкция', 'Сертификат', 'Паспорт', 'Гарантия', 'Технические характеристики', 'Руководство', 'Схема']
for doc_num in range(1, 8):
    df[f'document_{doc_num}_file'] = [f'https://disk.yandex.ru/d/example_folder/product_{i}_{doc_types[doc_num - 1].lower()}.pdf' for i in range(1, 11)]
    df[f'document_{doc_num}_name'] = [f'{doc_types[doc_num - 1]} для {row["product_title"]}' for _, row in df.iterrows()]

# Добавляем колонки для параметров
param_names = ['Мощность', 'Напряжение', 'Частота', 'Скорость', 'Вес']
for param_num in range(1, 6):
    df[f'parameter_{param_num}_title'] = param_names[param_num - 1]
    df[f'parameter_{param_num}_value'] = [
        f'{random.randint(500, 2000)} Вт' if param_num == 1 else
        f'{random.choice(["220В", "110В", "380В"])}' if param_num == 2 else
        f'{random.randint(50, 60)} Гц' if param_num == 3 else
        f'{random.randint(1000, 3000)} об/мин' if param_num == 4 else
        f'{random.uniform(1.5, 5.0):.1f} кг'
        for _ in range(10)
    ]

# Добавляем колонки для характеристик
char_titles = ['Применение', 'Особенности', 'Комплектация', 'Безопасность', 'Гарантия']
for char_num in range(1, 6):
    df[f'characteristic_{char_num}_title'] = char_titles[char_num - 1]
    df[f'characteristic_{char_num}_value'] = [
        f'<p>{"Профессиональное использование на строительных площадках" if char_num == 1 else "Защита от перегрузки и система вентиляции" if char_num == 2 else "Инструмент, ключ, инструкция, кейс" if char_num == 3 else "Двойная изоляция, защита от случайного включения" if char_num == 4 else "24 месяца официальной гарантии"}</p>'
        for _ in range(10)
    ]

# Добавляем колонки для фильтров
filters_data = ['Мощность:Высокая', 'Тип:Профессиональный', 'Напряжение:220В', 'Страна:Германия', 'Бренд:Bosch']
df['filters'] = [','.join(random.sample(filters_data, 3)) for _ in range(10)]

# Переупорядочиваем колонки для лучшей читаемости
column_order = [
    'article', 'product_title', 'product_price', 'category', 'subcategory',
    'brand', 'country', 'instock', 'leftovers', 'pop_models', 'order',
    'title', 'description', 'keywords', 'product_description', 'main_image', 'seo_text'
]

# Добавляем остальные колонки
for slide_num in range(1, 6):
    column_order.extend([f'slide_{slide_num}_image', f'slide_{slide_num}_alt'])

for doc_num in range(1, 8):
    column_order.extend([f'document_{doc_num}_file', f'document_{doc_num}_name'])

for param_num in range(1, 6):
    column_order.extend([f'parameter_{param_num}_title', f'parameter_{param_num}_value'])

for char_num in range(1, 6):
    column_order.extend([f'characteristic_{char_num}_title', f'characteristic_{char_num}_value'])

column_order.append('filters')

# Применяем порядок колонок
df = df[column_order]

# Сохраняем в Excel
file_name = f'products_import_{datetime.now().strftime("%Y%m%d_%H%M")}.xlsx'
df.to_excel(file_name, index=False, engine='openpyxl')

print(f"Файл '{file_name}' успешно создан!")
print(f"Количество товаров: {len(df)}")
print(f"Колонки в файле: {len(df.columns)}")
print("\nПервые 3 товара:")
print(df[['article', 'product_title', 'brand', 'product_price']].head(3))