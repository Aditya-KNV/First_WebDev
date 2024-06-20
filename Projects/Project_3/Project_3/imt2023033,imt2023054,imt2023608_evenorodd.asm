.data
n : .word 5
result : .word 0
.text
main:
	lw $t0, n
	addi $t1, $zero, 1
	and $t2, $t1, $t0
	sw $t2, result