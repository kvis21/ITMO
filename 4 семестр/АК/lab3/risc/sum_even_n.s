    .data

input_addr:      .word  0x80               
output_addr:     .word  0x84   
code_overflow:   .word  0xCCCCCCCC                    


    .text

_start:
    lui      a0, %hi(input_addr)             
    addi     a0, a0, %lo(input_addr)      
    lw       a0, 0(a0)                  ; input_addr = 0x80
    lw       t0, 0(a0)                  ; N 

    lui      a1, %hi(output_addr)             
    addi     a1, a1, %lo(output_addr)
    lw       a1, 0(a1)                  ; output_addr = 0x84

    addi     t6, t6, 2                  ; const 2

    div      t0, t0, t6                 ; n = N/2
    mv       t1, t0                      
    addi     t1, t1, 1                  ; t1 = n + 1
    mul      t4, t1, t0                 ; res = n * (n + 1)

check_overflow:
    beqz     t0, lower_zero          ; если t0 = 0 => lower_zero
    div      t5, t4, t0              ; Делим результат (t4) обратно на множитель (t0)
    bne      t5, t1, error_overflow  ; Если результат деления не равен второму множителю (t1) - переполнение


lower_zero:
    ble      t0, zero, error_lower


print_result:
    sw       t4, 0(a1)
    j        end_prog

error_overflow:
    lui      t2, %hi(code_overflow)
    addi     t2, t2, %lo(code_overflow)
    lw       t2, 0(t2)
    sw       t2, 0(a1)
    j        end_prog

error_lower:
    addi     t2, zero, -1                ;
    sw       t2, 0(a1)

end_prog:
    halt