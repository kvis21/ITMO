.data
    .org 0x100
input_ptr:   .word 0x80
output_ptr:  .word 0x84
mem_ptr:     .word 0x00

    .text
    .org 0x200
_start:
\ --- начало ---
    lit 1 >r             \ Флаг: 1 - начало строки или после пробела 
loop:
    @p input_ptr a! @    \ Читаем символ из порта 0x80  

    dup lit 10 xor                      \ Проверка на \n 
    if end                              
    
    dup lit 32 xor                      \ Проверка на пробел (код 32)   
    if handle_space                     
    
    r> if is_body           \ Если флаг 0 - это середина слова 
    
    \ --- Логика для ПЕРВОЙ буквы слова (флаг был 1) ---
    lit 0 >r             \ Сбрасываем флаг в 0  
    
    \ Проверяем, является ли символ строчной буквой ('a'-'z', 97-122)
    dup lit -97 +          
    -if check_z          \ Если char >= 97      
    write_char ;         \ Иначе это уже заглавная или спецсимвол, просто выводим
    
check_z:
    dup lit 122 over inv lit 1 + +  \ Вычисляем (122 - char) 
    -if make_upper       \ Если char <= 122     
    write_char ;         \ Иначе символ > 122, просто выводим

make_upper:
    lit -32 +            \ Вычитаем 32 для перевода в верхний регистр ('a' -> 'A')  277-278
    write_char ;         

handle_space:
    r> drop              \ Убираем старый флаг
    lit 1 >r             \ Ставим флаг 1, так как после пробела начнется новое слово
    write_char ;         

is_body:
    lit 0 >r             \ Возвращаем 0 в R-стек
    dup lit -65 +
    -if check_up
    write_char ;         

check_up:
    dup lit 96 over inv lit 1 + + \ Вычисляем (96 - char) 
    -if make_lower
    write_char ;
make_lower:
    lit 32 +
    write_char ;
overflow:
    lit -858993460 @p output_ptr a! !
    end_prog ;

write_char:
    
    \@p output_ptr a! dup !   \ Записываем символ в порт 0x84  29a-29d
    @p mem_ptr a! !+        \ Записываем символ в mem[0...31]  2a2-2a4
    a !p mem_ptr            \ запишем инкрементированный поинтер в mem_ptr   2a5-2aa
    loop ;               \ Безусловный переход в начало цикла

end:
    drop                 \ Убираем символ \n со стека
    r> drop              \ Очищаем R-стек

    \ --- Установка нуль-терминатора ---
    @p mem_ptr dup a! lit 0 !+ 
    a dup !p mem_ptr
    
    \ --- Вычисляем количество оставшихся ячеек ---
    inv lit 32 +         \ Считаем остаток. Если места не было, уйдет в минус
    
    \ --- Проверка на переполнение ---
    dup -if no_overflow  \ Если счетчик >= 0, переполнения нет, идем дальше
    drop                 \ Иначе (счетчик < 0): убираем мусор со стека
    overflow ;           \ Прыгаем в ваш обработчик переполнения

no_overflow:
    >r                   \ Устанавливаем валидный счетчик в R-стек
    @p mem_ptr a!        \ Начинаем с адреса mem[mem_ptr]

    a lit 32 xor         \ Проверяем: достигли ли мы конца буфера (A == 32?)
    if end_prog          \ Если xor дал 0 (то есть A равно 32), завершаем
fill_loop:
    lit 0x5f !+          \ Записываем '_' и инкрементируем A
    next fill_loop       \ Повторяем, пока R не станет 0
    
end_prog:
    halt