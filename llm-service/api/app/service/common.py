import torch
import ollama
import os
from openai import OpenAI
import argparse
import json
import re
import time 

# ANSI escape codes for colors
PINK = '\033[95m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

# Function to open a file and return its contents as a string
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
    
    
    
def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Запоминаем время начала
        result = func(*args, **kwargs)  # Вызываем оригинальную функцию
        end_time = time.time()  # Запоминаем время окончания
        execution_time = end_time - start_time  # Вычисляем время выполнения

        # Выводим имя функции и время её выполнения
        print(f"Функция '{func.__name__}' выполнялась {execution_time:.4f} секунд.")
        return result  # Возвращаем результат оригинальной функции
    
    return wrapper

@time_decorator
def clean_string(input_string):
    # Удаляем все символы, которые не являются буквами
    cleaned_string = re.sub(r'[^a-zA-Zа-яА-ЯёЁ\s]', '', input_string)
    # Удаляем лишние пробелы
    cleaned_string = re.sub(r'\s+', ' ', cleaned_string).strip()
    return cleaned_string.lower()