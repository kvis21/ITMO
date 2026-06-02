\ Project Euler: Problem 2
\ Найти сумму четных чисел Фибоначчи, не превышающих 4 000 000.

\ Инициализация переменных в памяти данных (DMEM)
0 VARIABLE SUM
1 VARIABLE PREV
2 VARIABLE CURR

MAIN
: LOOP_START
  \ 1. Условие: CURR < 4 000 000
  LD R1 CURR       \ Загружаем CURR в R1
  LDI R2 4000000   \ Загружаем лимит в R2
  CMP R1 R2        \ Сравниваем
  BGT END_LOOP     \ Если R1 > R2, выходим из цикла

  \ 2. Проверка на четность: CURR % 2 == 0
  LDI R3 2
  MOD R4 R1 R3     \ R4 = R1 % 2
  LDI R5 0
  CMP R4 R5
  BNE SKIP_ADD     \ Если остаток не равен 0, перепрыгиваем сложение

  \ 3. Добавляем к сумме: SUM = SUM + CURR
  LD R6 SUM        \ Загружаем текущую сумму
  ADD R6 R6 R1     \ R6 = SUM + CURR
  ST R6 SUM        \ Сохраняем обратно в память

: SKIP_ADD
  \ 4. Вычисляем следующее число Фибоначчи: NEXT = PREV + CURR
  LD R7 PREV       \ Загружаем PREV
  ADD R8 R7 R1     \ R8 = PREV + CURR
  
  \ Сдвигаем окно переменных
  ST R1 PREV       \ PREV = старый CURR
  ST R8 CURR       \ CURR = NEXT (R8)

  JMP LOOP_START   \ Возврат в начало цикла

: END_LOOP
  RET              \ Конец программы