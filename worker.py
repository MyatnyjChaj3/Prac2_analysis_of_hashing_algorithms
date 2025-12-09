import hashlib
from itertools import product

import argon2
import bcrypt

# Инициализация Argon2 hasher, чтобы не создавать его в каждом потоке
ph = argon2.PasswordHasher()


#1. Функция для атаки полным перебором (Bruteforce)

def check_password(args):

    algorithm, targets, charset, length, chunk_start, chunk_size = args
    # Генератор комбинаций
    iterator = product(charset, repeat=length)
    from itertools import islice
    subset = islice(iterator, chunk_start, chunk_start + chunk_size)

    results = []

    for p_tuple in subset:
        password = "".join(p_tuple)
        p_bytes = password.encode('utf-8')

        try:
            if algorithm == "SHA-1":
                h = hashlib.sha1(p_bytes).hexdigest()
                if h in targets:
                    results.append((password, h))
            
            elif algorithm == "MD5":
                h = hashlib.md5(p_bytes).hexdigest()
                if h in targets:
                    results.append((password, h))

            elif algorithm == "bcrypt":
                for target_hash in targets:
                    if bcrypt.checkpw(p_bytes, target_hash):
                         results.append((password, target_hash))
            
            elif algorithm == "Argon2":
                for target_hash in targets:
                    try:
                        if ph.verify(target_hash, password):
                            results.append((password, target_hash))
                    except:
                        pass
        except Exception as e:
            continue
            
        # Если нашли что-то, возвращаем сразу
        if results:
            return results
            
    return None


#2. Функция для словарной атаки (Dictionary Attack)

def try_dictionary_word(args):

    password, algorithm, targets = args
    
    p_bytes = password.encode('utf-8')
    results = []
    
    try:
        if algorithm == "SHA-1":
            h = hashlib.sha1(p_bytes).hexdigest()
            if h in targets:
                return (password, h)
        
        elif algorithm == "MD5":
            h = hashlib.md5(p_bytes).hexdigest()
            if h in targets:
                return (password, h)

        elif algorithm == "bcrypt":
            for target_hash in targets:
                target_hash_bytes = target_hash if isinstance(target_hash, bytes) else target_hash.encode('utf-8')
                if bcrypt.checkpw(p_bytes, target_hash_bytes):
                     return (password, target_hash)
        
        elif algorithm == "Argon2":
            for target_hash in targets:
                try:
                    if ph.verify(target_hash, password):
                        return (password, target_hash)
                except:
                    pass
    except Exception:
        pass
        
    return None