label: db 10 ,10,10
;<Program title>
jmp start
;data
;code
start:  nop
	mvi b, 3
	mov a, b
	adi 0
	jpo odd
	ani 127
	jmp fim
org 0
odd: 	xri 128
fim:	mov b,a
hlt

