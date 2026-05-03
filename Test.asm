// Adds 2 + 3 and stores in RAM[0]

// D = 2
@2
D=A

// D = D + 3
@3
D=D+A

// RAM[0] = D
@0
M=D

// infinite loop to stop program
(END)
@END
0;JMP