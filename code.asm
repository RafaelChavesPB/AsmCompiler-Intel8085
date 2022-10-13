jmp start
;data
data: db 0ffh, 0ffh, 0ffh
array: ds 3
;code
start: org 10
	mvi b, 3
	mov a, b
	adi 0
	jpo odd
	ani 127
	jmp fim
odd: 	xri 128
fim:	mov b,a
hlt

