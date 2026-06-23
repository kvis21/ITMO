    .data

input_addr:      .word  0x80               
output_addr:     .word  0x84   
fnv32_prime:     .word  0x01000193                    
hash_value:      .word  0x811C9DC5

    .text
    .org 0x200
_start:
    lui t0, %hi(input_addr) / lui t1, %hi(output_addr) / nop / nop
    addi t0, t0, %lo(input_addr) / addi t1, t1, %lo(output_addr) / nop / nop

    lui s2, %hi(fnv32_prime) / lui t3, %hi(hash_value) / lw t0, 0(t0) / nop    
    addi s2, s2, %lo(fnv32_prime) / addi t3, t3, %lo(hash_value) / lw t1, 0(t1) / nop

    nop / nop / lw t3, 0(t3) / nop
    nop / nop / lw s2, 0(s2) / nop

loop:
    nop / nop / lw t4, 0(t0) / nop
    xor t3, t3, t4 / nop / nop / beqz t4, print_hash
    mul t3, s2, t3 / nop / nop / j loop

print_hash:
    nop / nop / sw t3, t1 / j end_prog

end_prog:
    nop / nop / nop / halt
   