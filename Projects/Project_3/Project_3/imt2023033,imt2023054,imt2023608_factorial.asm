.data
n: .word 5
fac: .word 0
.text
main:
	lw $t0, n
	addi $t1, $zero, 1
	
loop: 
	beq $t0, $zero, store
	mul $t1, $t1, $t0
	subi $t0, $t0, 1
	j loop
store:
	sw $t1, fac
