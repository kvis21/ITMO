.data
input_addr:  .word  0x80         
output_addr: .word  0x84         

val:         .word  0x00         ; Исходное число
res:         .word  0x00         ; Накопленный результат
iterations:  .word  4            ; количество итераций 

c_1:         .word  1
c_8:         .word  8
mask_ff:     .word  0x000000FF   

.text
_start:
    load_addr    input_addr      ; acc = 0x80
    load_acc                     ; acc = mem[0x80] 
    store_addr   val             

iter:
    load_addr    res
    shiftl       c_8             ; acc = res << mem[c_8]
    store_addr   res

    load_addr    val
    and          mask_ff         ; acc = val & 0xFF
    
    add          res             ; acc = (val & 0xFF) + (res << 8)
    store_addr   res

    load_addr    val
    shiftr       c_8             ; acc = val >> 8
    store_addr   val

    load_addr    iterations
    sub          c_1             ; iterations--
    store_addr   iterations
    bgt          iter            ; iter if acc > 0 else _end

_end:
    load_addr    res             ; загружаем итоговое число
    store_ind    output_addr     ; mem[mem[output_addr]] = acc 
    halt