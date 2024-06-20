.data
n: .word 5
result: .word 0
.text
lw $t0, n
addi $t1, , $zero, 0
addi $t2, $zero, 1

fibo:
	subi $t0, $t0, 1
	beq $t0,$zero, exit
	add $t3, $t2, $t1
	add $t1, $zero, $t2
	add $t2, $zero, $t3
	j fibo


exit:
	sw $t2, result