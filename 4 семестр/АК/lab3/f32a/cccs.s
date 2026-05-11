.data
    .org 0x100
input_ptr:     .word 0x80
output_ptr:    .word 0x84
mem_ptr:       .word 0x00

    .text
    .org 0x200
_start:
    lit 1 >r                        \ Флаг: 1 - начало строки или после пробела 
loop:
    @p mem_ptr lit 32 xor
    if overflow_detected

    @p input_ptr a! @               \ Читаем символ из порта 0x80  
    
    dup lit 10 xor                  \ Проверка на \n 
    if end                              
    
    dup lit 32 xor                  \ Проверка на пробел (код 32)   
    if handle_space                     
    
    r> if is_body                   \ Если флаг 0 - это середина слова 
  
    lit 0 >r                        \ Сбрасываем флаг в 0  
    
    \ Проверяем, является ли символ строчной буквой ('a'-'z', 97-122)
    dup lit -97 +          
    -if check_z                     \ Если char >= 97      
    write_char ;         
    
check_z:
    dup lit 122 over inv lit 1 + +  \ Вычисляем (122 - char) 
    -if make_upper                  \ Если char <= 122     
    write_char ;         

make_upper:
    lit -32 +                       \ Вычитаем 32 для перевода в верхний регистр ('a' -> 'A')
    write_char ;         

handle_space:
    r> drop                         \ Убираем старый флаг
    lit 1 >r                        \ Ставим флаг 1
    write_char ;         

is_body:
    lit 0 >r                        \ Возвращаем 0 в R-стек
    dup lit -65 +
    -if check_up
    write_char ;         

check_up:
    dup lit 96 over inv lit 1 + +   \ Вычисляем (96 - char) 
    -if make_lower
    write_char ;

make_lower:
    lit 32 +
    write_char ;

write_char:
    @p mem_ptr a! !+                \ Записываем символ в mem[0...31]  
    a !p mem_ptr                    \ запишем инкрементированный поинтер в mem_ptr  
    loop ;               

overflow_detected:
    lit 0xCCCCCCCC      
    @p output_ptr a! !
    end_prog ;

end:
    drop                            \ Убираем символ \n со стека
    r> drop                         \ Очищаем R-стек

    @p mem_ptr dup a! lit 0 !+ 
    a dup !p mem_ptr
    inv lit 32 +  >r                \ Устанавливаем счетчик на 32 - mem[mem_ptr] 
    @p mem_ptr a!             

    a lit 32 xor if start_printing     
fill_loop:
    lit 0x5f !+          
    next fill_loop                  \ Повторяем, пока R не станет 0

start_printing:
    lit 0 a!             
    lit 32 >r                       \ Устанавливаем счетчик цикла на 32

print_loop:
    @+ lit 0xff and             

    dup if end_prog

    @p output_ptr b! !b             
    next print_loop                 

end_prog:
    halt           