ORG 0x00
V0:     WORD    $DEFAULT,   0x180
V1:     WORD    $DEFAULT,      0x180
V2:     WORD    $INT2,   0x180
V3:     WORD    $INT3,      0x180
V4:     WORD    $DEFAULT,   0x180
V5:     WORD    $DEFAULT,   0x180
V6:     WORD    $DEFAULT,   0x180
V7:     WORD    $DEFAULT,   0x180
DEFAULT:IRET

ORG     0x01C
X:      WORD    ?
MIN:    WORD    0xFFE8	; -26
MAX:    WORD    0x0018	; 24

START:
        DI
        CLA
        OUT     0x1	; запрет прерываний для неисопльзуемых устройств
        OUT     0x3 
        OUT     0xB
        OUT     0xE
        OUT     0x12
        OUT     0x16
        OUT     0x1A
        OUT     0x1E

        LD      #0xA
        OUT     0x5

        LD      #0xB
        OUT     0x7
        EI

MAIN:
        DI
        LD      X
        INC
        CALL    CHECK
        ST      X
        EI
        JUMP    MAIN

CHECK:
CHECK_MIN:
        CMP     MIN
        BGE     CHECK_MAX
        LD      MIN
        ST      X
CHECK_MAX:
        CMP     MAX
        BLT     RETURN
        LD      MAX
        ST      X
RETURN:   RET

INT2:           	; NXOR = (A&X) | (~A & ~X)
        IN 0x4	; РД ВУ-2
        PUSH	; сохраняем число(A) из РД ВУ-2
        NOT
        PUSH	; сохраняем ~A	
        LD X	
        HLT
        NOT
        AND &0
        PUSH 	; сохраняем ~X & ~A
        LD &2	; загружаем A
        AND X	; A & X
        OR &0	; (A&X) | (~A & ~X)
        HLT

        CALL CHECK
        HLT
        ST X
        POP
        POP
        POP
        IRET

INT3:           	; 5X+6
        LD X
        HLT
        CALL CHECK
        ASL	; 2X	
        ASL	; 4X
        ADD X	; 5X
        ADD #0x6	; 5X + 6
        OUT 0x6
        HLT
        IRET

