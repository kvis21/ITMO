from enum import Enum
from dataclasses import dataclass, field
from typing import List, Union, Any

class Opcode(int, Enum):
    """Список опкодов команд процессора."""
    # Память и константы
    LDI  = 0x00
    LD   = 0x01
    ST   = 0x02
    
    # Арифметика и логика
    ADD  = 0x11
    SUB  = 0x12
    MUL  = 0x13
    DIV  = 0x14
    MOD  = 0x15
    CMP  = 0x16
    
    # Ветвления
    JMP  = 0x20
    BEQ  = 0x21
    BNE  = 0x22
    BGT  = 0x23
    BLT  = 0x24
    
    # Процедуры
    CALL = 0x30
    RET  = 0x31
    
    # Ввод-вывод и прерывания
    IN   = 0x40
    OUT  = 0x41
    EI   = 0x42
    DI   = 0x43
    IRET = 0x44

class Register(int, Enum):
    """Список регистров процессора."""
    R0   = 0  # Hardwired Zero
    R1   = 1
    R2   = 2
    R3   = 3
    R4   = 4
    R5   = 5
    R6   = 6
    R7   = 7
    R8   = 8
    R9   = 9
    R10  = 10 # TOS (Top of Stack)
    R11  = 11 # NOS (Next of Stack)
    SP   = 12 # Data Stack Pointer
    RP   = 13 # Return Stack Pointer
    SR   = 14 # Status Register
    PC   = 15 # Program Counter

class ArgType(str, Enum):
    """Типы аргументов (способы адресации/интерпретации)."""
    REG   = "REG"   # Регистр (значение - число от 0 до 15)
    IMM   = "IMM"   # Непосредственное значение (константа)
    ADDR  = "ADDR"  # Адрес в памяти или номер порта
    LABEL = "LABEL" # Строковая метка (используется транслятором до линковки)

@dataclass
class Arg:
    """Аргумент инструкции."""
    value: Union[int, str, Register]
    arg_type: ArgType

    def to_dict(self) -> dict:
        """Сериализация аргумента (например, для сохранения в JSON)."""
        val = self.value.value if isinstance(self.value, Register) else self.value
        return {
            "value": val,
            "type": self.arg_type.value
        }

@dataclass
class Instruction:
    """Представление одной машинной инструкции."""
    opcode: Opcode
    args: List[Arg] = field(default_factory=list)
    comment: str = ""

    def to_dict(self) -> dict:
        """Сериализация инструкции для вывода."""
        return {
            "opcode": self.opcode.name,
            "args": [arg.to_dict() for arg in self.args],
            "comment": self.comment
        }

    def __str__(self) -> str:
        """Текстовое представление для отладки (disassembly)."""
        args_str = ", ".join(
            f"{'R' + str(a.value.value) if isinstance(a.value, Register) else ('#' if a.arg_type == ArgType.IMM else '')}{a.value}"
            for a in self.args
        )
        base = f"{self.opcode.name:<5} {args_str}"
        if self.comment:
            # Выравниваем комментарии для красоты
            return f"{base:<20} ; {self.comment}"
        return base