function_add:
    push BP          ; Save the previous BP
    mov BP, SP       ; Set up a new base pointer
    sub SP, 4       ; Allocate space for a local variable
    mov [BP-4], 0   ; Initialize the local variable
    mov AX, [BP+8]  ; Get the first parameter 'a'
    mov BX, [BP+12] ; Get the second parameter 'b'
    add AX, BX      ; Compute the sum
    mov [BP-4], AX  ; Store the result in the local variable
    mov AX, [BP-4]  ; Load the result
    mov SP, BP       ; Restore the stack pointer
    pop BP           ; Restore the base pointer
    ret