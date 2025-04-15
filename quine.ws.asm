    ; Push rest of program (P)
    push    33677979231883625366339880199817361448324292608720810793833615453798990824199845066086716622329279289043809935949178154863258
    ; mem[0] = space
    push    0
    push    ' '
    store
    ; mem[1] = tab
    push    1
    push    '\t'
    store
    ; mem[2] = linefeed
    push    2
    push    '\n'
    store
    ; Output PUSH opcode (space, space) and sign bit (space)
    push    ' '
    dup
    dup
    outc
    outc
    outc

    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ; Output rest of program (P) encoded in base 2, most-significant    ;
    ; bit first, where:                                                 ;
    ; - 0 = space                                                       ;
    ; - 1 = tab                                                         ;

    ; Initialize divisor (D) = 1
    push    1       ; stack = P, D = 1
label 0
    ; Do D = D * 2
    dup             ; stack = P, D, D
    add             ; stack = P, D, D = D * 2
    dup             ; stack = P, D, D
    copy    2       ; stack = P, D, D, P
    sub             ; stack = P, D, D - P
    ; While D < P
    jumpn   0       ; stack = P, D
                    ; If D < P, loop
label 1
    ; While (D = D // 2) != 0
    push    2       ; stack = P, D, 2
    div             ; stack = P, D = D // 2
    dup             ; stack = P, D, D
    jumpz   00      ; stack = P, D
                    ; If D = 0, exit loop
    ; N = P // D
    copy    1       ; stack = P, D, P
    copy    1       ; stack = P, D, P, D
    div             ; stack = P, D, N = P // D
    ; Output mem[N % 2]
    push    2       ; stack = P, D, N, 2
    mod             ; stack = P, D, N % 2
    retr            ; stack = P, D, mem[N % 2]
    outc            ; stack = P, D
                    ; Output mem[N % 2]
    jump    1

label 00
    ; Clean up stack
    pop             ; stack = P
    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

    ; Output end of PUSH instruction (linefeed)
    push    '\n'
    outc

    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ; Output P encoded in base 3, least-significant value first,        ;
    ; where:                                                            ;
    ; - 0 = space                                                       ;
    ; - 1 = tab                                                         ;
    ; - 2 = linefeed                                                    ;

label 01
    ; Do output mem[P % 3]
    dup             ; stack = P, P
    push    3       ; stack = P, P, 3
    mod             ; stack = P, P % 3
    retr            ; stack = P, mem[P % 3]
    outc            ; stack = P
                    ; Output mem[Q % 3]
    ; P = P // 3
    push    3       ; stack = P, 3
    div             ; stack = P = P // 3
    ; While P != 0
    dup             ; stack = P, P
    jumpz   11      ; stack = P
                    ; If P == 0, exit
    jump    01      ; Otherwise, loop
    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

label 11
    ; Clean up stack
    pop
    end
