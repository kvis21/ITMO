from enum import Enum, auto
from dataclasses import dataclass
import re
from typing import List

class TokenType(Enum):
    """Типы токенов для Forth-подобного языка."""
    WORD   = auto()  # Любое Forth-слово, определение или имя (например: +, DUP, VARIABLE, :, ;, SET-ISR)
    NUMBER = auto()  # Целочисленный литерал (например: 42, -10)
    STRING = auto()  # Строковый литерал в формате P" ... "

@dataclass
class Token:
    """Класс представления токена."""
    type: TokenType
    value: str
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, '{self.value}', line={self.line}, col={self.column})"

class Tokenizer:
    """Лексический анализатор (сканер текста программы)."""
    
    def tokenize(self, text: str) -> List[Token]:
        """Преобразует исходный текст программы в список токенов."""
        tokens: List[Token] = []
        length = len(text)
        i = 0
        line = 1
        col = 1

        while i < length:
            ch = text[i]

            # 1. Пропуск пробельных символов с подсчетом строк
            if ch.isspace():
                if ch == '\n':
                    line += 1
                    col = 1
                else:
                    col += 1
                i += 1
                continue

            # 2. Обработка комментариев (В Forth комментарий строки начинается с символа '\')
            if ch == '\\':
                while i < length and text[i] != '\n':
                    i += 1
                # Перенос строки обработается на следующей итерации цикла
                continue

            # 3. Обработка Pascal-строк вида P" ... "
            if i + 1 < length and text[i:i+2] == 'P"':
                start_line = line
                start_col = col
                
                i += 2
                col += 2
                string_chars = []
                
                while i < length and text[i] != '"':
                    if text[i] == '\n':
                        line += 1
                        col = 1
                    else:
                        col += 1
                    string_chars.append(text[i])
                    i += 1
                
                if i >= length:
                    raise SyntaxError(f"Ошибка транслятора: Незакрытая строка, начатая на строке {start_line}, поз. {start_col}")
                
                # Пропускаем закрывающую кавычку
                i += 1
                col += 1
                
                tokens.append(Token(TokenType.STRING, "".join(string_chars), start_line, start_col))
                continue

            # 4. Обработка обычных слов и числовых литералов (все, что разделено пробелами)
            start_line = line
            start_col = col
            word_chars = []
            
            while i < length and not text[i].isspace():
                word_chars.append(text[i])
                i += 1
                col += 1
            
            word = "".join(word_chars)
            
            # Проверяем, является ли слово числом (включая отрицательные числа)
            if re.match(r'^-?\d+$', word):
                tokens.append(Token(TokenType.NUMBER, word, start_line, start_col))
            else:
                tokens.append(Token(TokenType.WORD, word, start_line, start_col))

        return tokens