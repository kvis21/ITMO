from io import BytesIO
from typing import List, Dict

from dataclasses import dataclass

@dataclass
class FileCallback:
    message: str
    status: bool
    data: Dict[str, int|float] = None

def _data_validator(data: List[str]) -> FileCallback:
    if len(data) != 3:
        return FileCallback("В файле должно быть 3 числа (a, b, eps), введенные через пробел.", False)
    try:
        a, b = int(data[0]), int(data[1])
        eps = float(data[2].replace(",", "."))
        if a < b:
            return FileCallback(f"Данные из файла успешно прочитаны: \na={a}, b={b}, eps={eps}", True, {"a": a, "b": b, "eps": eps})
        return FileCallback(f"Граница a >= b", False)
    except ValueError:
        return FileCallback("Не удалось преобразовать значения в нужный формат: \na, b - целочисленное \neps - с плавающей запятой", False)


def file_processor(file: BytesIO) -> FileCallback:
    data = file.read().decode()
    data = data.strip().split()

    callback = _data_validator(data)
    
    return callback


    