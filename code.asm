JMP START
VALOR: org 000h
valor_12: DB 10
NBITS: DB 0
START: LDA VALOR    
        MOV B,A        
        MVI C,0        
        MVI D,1    
LOOP:    MOV A,D
        ANA B
        JZ PULA
        INR C
PULA:    MOV A,D
        RAL
        MOV D,A
JNC LOOP
        MOV A,C
        STA NBITS
        HLT

