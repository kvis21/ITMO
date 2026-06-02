import struct
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

from isa import Opcode, Instruction, Arg, ArgType, Register
from translator.tokenizer import Token, TokenType

@dataclass
class Program:
    """Представление скомпилированной программы."""
    instructions: List[Instruction] = field(default_factory=list)
    data_memory: List[int] = field(default_factory=list)  # Память данных (DMEM)
    
    # Таблицы символов для этапа трансляции
    labels: Dict[str, int] = field(default_factory=dict)     # Метка -> Адрес в IMEM
    variables: Dict[str, int] = field(default_factory=dict)  # Имя -> Адрес в DMEM

    def allocate_string(self, text: str) -> int:
        """
        Аллоцирует строку в памяти данных в формате Pascal-string (pstr).
        Каждый символ и длина занимают целое 32-битное слово.
        Возвращает базовый адрес строки.
        """
        address = len(self.data_memory)
        self.data_memory.append(len(text))  # Длина строки
        for char in text:
            self.data_memory.append(ord(char))  # Код символа
        return address

    def allocate_variable(self, initial_value: int) -> int:
        """Выделяет слово в DMEM под переменную и возвращает адрес."""
        address = len(self.data_memory)
        self.data_memory.append(initial_value)
        return address

    def to_machine_code(self) -> List[str]:
        """
        Преобразует список объектов Instruction в список 32-битных 
        бинарных строк (например, '010100...').
        """
        machine_code = []
        for instr in self.instructions:
            opcode_val = instr.opcode.value
            
            # Разбираем аргументы
            rd_val = 0
            rs1_val = 0
            rs2_val = 0
            imm_val = 0
            addr_val = 0
            
            # Вспомогательная функция для извлечения числового значения
            def get_val(arg: Arg) -> int:
                if arg.arg_type == ArgType.REG:
                    return arg.value.value
                elif arg.arg_type in (ArgType.IMM, ArgType.ADDR):
                    return int(arg.value)
                elif arg.arg_type == ArgType.LABEL:
                    # На этапе генерации маш. кода все метки уже должны быть разрешены
                    return self.labels.get(arg.value, 0)
                return 0

            # Классификация форматов на основе опкода
            if instr.opcode in (Opcode.ADD, Opcode.SUB, Opcode.MUL, Opcode.DIV, Opcode.MOD):
                # Формат R: [Opcode: 6] [Rd: 4] [Rs1: 4] [Rs2: 4] [Unused: 14]
                if len(instr.args) == 3:
                    rd_val = get_val(instr.args[0])
                    rs1_val = get_val(instr.args[1])
                    rs2_val = get_val(instr.args[2])
            elif instr.opcode == Opcode.CMP:
                if len(instr.args) == 2:
                    rs1_val = get_val(instr.args[0])
                    rs2_val = get_val(instr.args[1])
            elif instr.opcode in (Opcode.LDI, Opcode.LD, Opcode.ST, Opcode.IN, Opcode.OUT):
                # Формат I: [Opcode: 6] [Rd: 4] [Rs1: 4] [Immediate/Port: 18]
                if len(instr.args) == 2:
                    if instr.opcode in (Opcode.ST, Opcode.OUT):
                        rs1_val = get_val(instr.args[0]) # Источник
                        imm_val = get_val(instr.args[1]) # Адрес/Порт
                    else:
                        rd_val = get_val(instr.args[0])  # Приемник
                        if instr.args[1].arg_type == ArgType.REG:
                            rs1_val = get_val(instr.args[1])
                        else:
                            imm_val = get_val(instr.args[1])
            elif instr.opcode in (Opcode.JMP, Opcode.BEQ, Opcode.BNE, Opcode.BGT, Opcode.BLT, Opcode.CALL):
                # Формат J: [Opcode: 6] [Address: 26]
                if len(instr.args) == 1:
                    addr_val = get_val(instr.args[0])

            # Маски для ограничения разрядности (защита от переполнений и отрицательных чисел)
            imm_val = imm_val & 0x3FFFF      # 18 бит
            addr_val = addr_val & 0x3FFFFFF  # 26 бит
            
            # Сборка 32-битного слова сдвигами
            binary_word = 0
            if instr.opcode in (Opcode.JMP, Opcode.BEQ, Opcode.BNE, Opcode.BGT, Opcode.BLT, Opcode.CALL):
                binary_word = (opcode_val << 26) | addr_val
            elif instr.opcode in (Opcode.LDI, Opcode.LD, Opcode.ST, Opcode.IN, Opcode.OUT):
                binary_word = (opcode_val << 26) | (rd_val << 22) | (rs1_val << 18) | imm_val
            else:
                binary_word = (opcode_val << 26) | (rd_val << 22) | (rs1_val << 18) | (rs2_val << 14)
                
            # Форматируем в 32-битную строку из нулей и единиц
            machine_code.append(f"{binary_word:032b}")
            
        return machine_code


def translate_program(tokens: List[Token], result: Program) -> None:
    """
    Анализирует токены Forth-подобного языка и заполняет объект Program.
    Включает базовую логику линковки и управления стеком.
    """
    i = 0
    
    # Стартовый код: Инициализация SP и RP (если нужно), прыжок к началу программы
    # Если начало программы - это метка _start (как в C)
    result.instructions.append(Instruction(Opcode.JMP, [Arg("_start", ArgType.LABEL)], "Jump to entry point"))
    
    while i < len(tokens):
        token = tokens[i]
        
        if token.type == TokenType.NUMBER:
            # В Forth число кладет само себя на стек данных
            val = int(token.value)
            # LDI R10, #val
            result.instructions.append(Instruction(
                Opcode.LDI, [Arg(Register.R10, ArgType.REG), Arg(val, ArgType.IMM)], f"Load {val}"
            ))
            # ST R10, SP (Push to Data Stack)
            result.instructions.append(Instruction(
                Opcode.ST, [Arg(Register.R10, ArgType.REG), Arg(Register.SP, ArgType.REG)], "Push to stack"
            ))
            # ADD SP, SP, 1 (Увеличиваем указатель) - здесь потребуется LDI для 1, или если ISA позволяет
            # Для упрощения предполагаем наличие инструкции инкремента или используем свободный регистр
            pass 

        elif token.type == TokenType.STRING:
            # Размещение строки в памяти и пуш ее адреса на стек
            addr = result.allocate_string(token.value)
            result.instructions.append(Instruction(
                Opcode.LDI, [Arg(Register.R10, ArgType.REG), Arg(addr, ArgType.ADDR)], f"Load str address '{token.value}'"
            ))
            result.instructions.append(Instruction(
                Opcode.ST, [Arg(Register.R10, ArgType.REG), Arg(Register.SP, ArgType.REG)], "Push str addr"
            ))

        elif token.type == TokenType.WORD:
            word = token.value.upper()
            
            # --- Обработка переменных (Пример: 10 VARIABLE X) ---
            if word == "VARIABLE":
                var_name = tokens[i+1].value
                # Берем начальное значение, если оно было перед VARIABLE
                # (В реальном компиляторе тут сложнее, но для примера сойдет 0)
                var_addr = result.allocate_variable(0)
                result.variables[var_name] = var_addr
                i += 1 # Пропускаем имя переменной
            
            # --- Обработка определения функций ( : SQUAR DUP * ; ) ---
            elif word == ":":
                func_name = tokens[i+1].value
                # Запоминаем текущий адрес в памяти команд как адрес функции
                result.labels[func_name] = len(result.instructions)
                i += 1
                
            elif word == ";":
                result.instructions.append(Instruction(Opcode.RET, [], "Return from proc"))

            # --- Базовые арифметические операции ---
            elif word == "+":
                # POP R2 (NOS), POP R1 (TOS), ADD R3, R1, R2, PUSH R3
                result.instructions.append(Instruction(Opcode.ADD, 
                    [Arg(Register.R3, ArgType.REG), Arg(Register.R1, ArgType.REG), Arg(Register.R2, ArgType.REG)], "+ operation"))

            # Входная точка программы
            elif word == "MAIN" or word == "_START":
                result.labels["_start"] = len(result.instructions)
            # --- Встроенный Ассемблер ---
            elif hasattr(Opcode, word):
                opcode = Opcode[word]
                inst_args = []
                
                # Парсим аргументы (читаем токены вперед, пока не упремся в следующую команду)
                while i + 1 < len(tokens):
                    next_tok = tokens[i+1]
                    next_val = next_tok.value.upper()
                    
                    if hasattr(Register, next_val):
                        # Это регистр (например, R1)
                        inst_args.append(Arg(Register[next_val], ArgType.REG))
                    elif next_val.isdigit() or (next_val.startswith("-") and next_val[1:].isdigit()):
                        # Это число (например, 4000000)
                        inst_args.append(Arg(int(next_tok.value), ArgType.IMM))
                    elif next_tok.type == TokenType.WORD and not hasattr(Opcode, next_val) and next_val not in ("VARIABLE", ":", ";"):
                        # Это метка перехода или имя переменной (например, CURR или LOOP_START)
                        inst_args.append(Arg(next_tok.value, ArgType.LABEL))
                    else:
                        break # Началась следующая инструкция или системное слово
                    i += 1
                
                result.instructions.append(Instruction(opcode, inst_args))
            else:
                # Если слово неизвестно, но есть в метках - это вызов функции (CALL)
                result.instructions.append(Instruction(
                    Opcode.CALL, [Arg(word, ArgType.LABEL)], f"Call {word}"
                ))

        i += 1

    # --- Pass 2: Линковка (разрешение меток и переменных) ---
    # Транслятор проходит по всем инструкциям и заменяет ArgType.LABEL на реальные адреса
    for instr in result.instructions:
        for arg in instr.args:
            if arg.arg_type == ArgType.LABEL:
                # 1. Сначала проверяем, не переменная ли это
                if arg.value in result.variables:
                    arg.arg_type = ArgType.ADDR
                    arg.value = result.variables[arg.value]
                
                # 2. Если нет, проверяем, не метка ли это перехода
                elif arg.value in result.labels:
                    arg.arg_type = ArgType.ADDR
                    arg.value = result.labels[arg.value]
                
                else:
                    raise Exception(f"Линковщик: Неразрешенная метка или переменная '{arg.value}'")
