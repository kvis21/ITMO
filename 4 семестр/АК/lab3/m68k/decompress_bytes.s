    .data
    .org 0x100
input_addr:      .word  0x80               
output_addr:     .word  0x84 
temp_data_addr:  .word  0x400    ; указатель на ячейки для временного хранения декомпрессированных байт

    .text
    .org 0x200
_start:
    movea.l input_addr, A0
    move.l (A0), D0
    movea.l D0, A0              ; A0 - 0x80 (адрес ввода)

    movea.l output_addr, A2
    move.l (A2), D0
    movea.l D0, A2              ; A2 - 0x84 (адрес вывода)
    
    movea.l temp_data_addr, A1
    move.l (A1), D0
    movea.l D0, A1              ; A1 - 0x400 (адрес на времменные ячейки)

    move.l (A0), D0             ; D0 - длина (count + byte)
    
    cmp.l 0, D0                    
    blt handle_error            ; Проверка length < 0

    
    beq handle_zero             ; Проверка length == 0

    
    move.l D0, D1               
    and.l 1, D1                 
    bne handle_error            ; Проверка length % 2 != 0 (нечетность)        

    move.l 0x000000ff, D7
    
read_word:
    move.l (A0), D1             ; D1 - текущее слово

read_high_part:

    move.l D1, D2
    asr.l 24, D2
    and.l D7, D2               ; D2 - количество скомпрессированных байт

    move.l D1, D3
    asr.l 16, D3
    and.l D7, D3                ; D3 - скопрессированный байт

    move.b 1, D6

    jmp write_bytes

read_lowest_part:

    move.l D1, D2
    asr.l 8, D2
    and.l D7, D2               ; D2 - количество скомпрессированных байт

    move.l D1, D3
    and.l D7, D3                ; D3 - скопрессированный байт

    move.b 0, D6


write_bytes:
    add.l  D2, D4
write_bytes_loop:
    sub.b 1, D2

    move.b D3, (A1)+
    bne write_bytes_loop

    sub.b 2, D0
    beq output_bytes

    move.b D6, D6               ; устанaвливаем флаги для ветвления
    bne read_lowest_part        ; переход на чтение младшей части 

    jmp read_word

handle_error:
    move.l -1, (A2)             
    jmp end_prog                        

handle_zero:
    move.l 0, (A2)             
    jmp end_prog                         
    
output_bytes:
    movea.l temp_data_addr, A1
    move.l (A1), D0
    movea.l D0, A1              ; A1 снова указывает на 0x400

    move.l D4, (A2)             

    cmp.l 0, D4                 
    beq end_prog

    move.l D4, D0               ; Копируем общую длину байт для счетчика цикла

output_loop:
    move.l 0, D5                
    move.l 4, D6                ; Счетчик для сборки 4 байт в одно слово

pack_word_loop:
    move.l 0, D3                ; Очистка временного регистра для байта
    move.b (A1)+, D3            ; Читаем 1 байт из памяти (здесь инкремент нужен)
    and.l 0xFF, D3              ; Маскируем, оставляя только считанный байт

    lsl.l 8, D5                 ; Освобождаем место в младших 8 битах[cite: 1]
    or.l D3, D5                 ; Вставляем байт[cite: 1]

    sub.l 1, D6                 ; Уменьшаем счетчик заполнения текущего слова
    sub.l 1, D0                 ; Уменьшаем общий счетчик оставшихся байт
    beq finish_padding          ; Если байты в буфере кончились, идем на вывод

    cmp.l 0, D6                 ; Слово заполнено (4 байта)?
    bne pack_word_loop          ; Если нет, продолжаем собирать байты в D5

    move.l D5, (A2)             
    jmp output_loop             ; Возвращаемся к сборке следующего слова

finish_padding:
    cmp.l 0, D6                 
    beq send_final              ; Если D6=0, слово и так было полным
pad_loop:
    lsl.l 8, D5                 ; Додвигаем байты к старшим разрядам[cite: 1]
    sub.l 1, D6
    cmp.l 0, D6
    bne pad_loop

send_final:
    move.l D5, (A2)             ; Отправляем последнее (дополненное нулями) слово

end_prog:
    halt