# Сравнение алгоритмов хэширования

Практическая работа по информационной безопасности

**Цель:**  
Практически оценить стойкость алгоритмов хэширования паролей при атаках:
- MD5
- SHA-1
- bcrypt
- Argon2

Сравниваются два подхода:
- Собственный инструмент на Python (CPU + словарная атака + bruteforce)
- Профессиональный Hashcat (GPU)

## Особенности проекта

- Словарная атака (rockyou.txt — 14 млн паролей)
- Многопоточная обработка
- Поддержка MD5, SHA-1, bcrypt, Argon2
- Переключение: словарь → маска → bruteforce

## Структура проекта

```text
├── main.py              ← запуск программы
├── worker.py            ← проверка пароля
├── config.py            ← хэши, алфавиты, пути к словарям
├── dictionaries/        ← скаченные словари (rockyou.txt)
├── result.md            ← итоговый отчёт с замерами
├── structure.md         ← разбор структуры проекта
└── requirements.txt
```

## Установка и запуск

```bash
git clone <url проекта>
cd <папка проекта>
python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt

# скачивание словаря
mkdir dictionaries
cd dictionaries
wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt
# или вручную: https://weakpass.com/wordlist/182

#запуск

python main.py
```
