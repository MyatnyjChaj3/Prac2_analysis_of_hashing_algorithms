import math
import multiprocessing
import os
import time
from itertools import product

import config
import worker
from colorama import Fore, Style, init

init(autoreset=True)


def dictionary_attack(algorithm, targets):
    print(f"{Fore.MAGENTA}Запуск словарной атаки на {algorithm}...{Style.RESET_ALL}")
    start_time = time.time()
    found = 0
    original_count = len(targets)
    
    try:
        dict_paths = config.DICTIONARIES
    except AttributeError:
        print(f"{Fore.RED}Внимание: config.DICTIONARIES не найден. Словарная атака пропущена.{Style.RESET_ALL}")
        return 0

    for dict_path in dict_paths:
        if not os.path.exists(dict_path):
            print(f"  Словарь не найден: {dict_path}")
            continue

        size_mb = os.path.getsize(dict_path) // 1024 // 1024
        print(f"  Используется словарь: {dict_path} ({size_mb} МБ)")

        with open(dict_path, "r", encoding="utf-8", errors="ignore") as f:
            with multiprocessing.Pool(processes=os.cpu_count()) as pool:
                # Передаёт ТРОЙКУ (password, algorithm, targets) как один элемент
                tasks = ((line.strip(), algorithm, targets) for line in f if line.strip())

                for result in pool.imap_unordered(worker.try_dictionary_word, tasks):
                    if result:
                        pwd, h = result
                        elapsed = time.time() - start_time
                        print(f"{Fore.GREEN}[+] Найдено: '{pwd}' → {h} ({elapsed:.2f} сек){Style.RESET_ALL}")
                        found += 1

                        # Удаляет найденный хэш
                        if isinstance(targets, set):
                            targets.discard(h)
                        else:
                            # Для list (bcrypt/Argon2)
                            targets[:] = [t for t in targets if t != h]

                        # Досрочный выход при нахождении всех паролей
                        if found >= original_count:
                            print(f"{Fore.CYAN}Все пароли для {algorithm} найдены! Останавливаем.{Style.RESET_ALL}")
                            pool.terminate()
                            return found

    print(f"Словарная атака завершена. Найдено: {found}/{original_count}\n")
    return found


def run_bruteforce(algorithm, targets, max_length):
    """
    Запускает Bruteforce атаку на оставшиеся хэши.
    """
    start_time = time.time()
    found_count = 0

    # Перебор по длине пароля (от 1 до max_length)
    for length in range(1, max_length + 1):
        if not targets:
            break

        total_combinations = len(config.CHARSET) ** length
        print(f"Проверка длины {length}... Комбинаций: {total_combinations}")

        num_workers = multiprocessing.cpu_count()
        chunk_size = math.ceil(total_combinations / num_workers)

        # Подготовка задач для воркеров
        tasks = []
        for i in range(num_workers):
            chunk_start = i * chunk_size
            # args: algo, targets, charset, length, start, size
            tasks.append((algorithm, targets, config.CHARSET, length, chunk_start, chunk_size))

        # Запуск пула процессов
        with multiprocessing.Pool(processes=num_workers) as pool:
            for result in pool.imap_unordered(worker.check_password, tasks):
                if result:
                    for password, h in result:
                        elapsed = time.time() - start_time
                        print(f"{Fore.GREEN}[SUCCESS] Пароль найден: '{password}' за {elapsed:.4f} сек.{Style.RESET_ALL}")
                        found_count += 1
                        
                        # Удаляет найденный хэш из targets
                        if isinstance(targets, set):
                            targets.discard(h)
                        else:
                            targets[:] = [t for t in targets if t != h]
                        
                        # Проверяет, остались ли цели
                        if not targets:
                             print(f"{Fore.CYAN}Все пароли для {algorithm} найдены! Останавливаем Bruteforce.{Style.RESET_ALL}")
                             pool.terminate()
                             return found_count 

  
        if algorithm in ["bcrypt", "Argon2"] and length >= max_length:
             print(f"{Fore.YELLOW}Достигнут предел длины ({max_length}) для медленного алгоритма. Пропускаем.{Style.RESET_ALL}")
             break
    
    total_time = time.time() - start_time
    print(f"Bruteforce завершен. Найдено: {found_count}. Время: {total_time:.4f} сек.")
    return found_count


def run_bruteforce_if_needed(algorithm, remaining_targets):
    if not remaining_targets:
        print(f"{Fore.CYAN}Все пароли уже найдены словарём! Bruteforce не нужен.{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}--- Запуск BRUTEFORCE атаки на алгоритм: {algorithm} ---{Style.RESET_ALL}")
    
    # Устанавливаем разумную максимальную длину для теста
    max_len = 6
    if algorithm in ["bcrypt", "Argon2"]:
 
        max_len = 6
        print(f"    Максимальная длина для {algorithm} ограничена {max_len} символами (защита от зависания на CPU).")
        
    run_bruteforce(algorithm, remaining_targets, max_len)


if __name__ == '__main__':
    print(f"{Fore.CYAN}Запуск крякера паролей{Style.RESET_ALL}\n")

    for algo, hashes in config.TARGETS.items():

        current_targets = set(hashes) if algo in ["SHA-1", "MD5"] else list(hashes)
        
        # 1. Словарная атака
        found_in_dict = dictionary_attack(algo, current_targets)

        # 2. Bruteforce, если остались ненайденные хэши
        if current_targets:
            run_bruteforce_if_needed(algo, current_targets)
        
    print(f"{Fore.CYAN}Работа завершена.{Style.RESET_ALL}")