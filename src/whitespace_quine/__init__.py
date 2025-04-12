import sys
from pathlib import Path
from typing import NoReturn

from whitespace_asm import asm

WHITESPACE_CHARS = {
    " ": "0",
    "\t": "1",
    "\n": "2",
}
REST_OF_PROGRAM = """\
    ; mem[0] = ' '
    push    0
    push    ' '
    store
    ; mem[1] = '\\t'
    push    1
    push    '\\t'
    store
    ; mem[2] = '\\n'
    push    2
    push    '\\n'
    store
    ; Output PUSH opcode (space, space) and sign bit (space)
    push    ' '
    outc
    push    ' '
    outc
    push    ' '
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
    push    2       ; stack = P, D, 2
    mult            ; stack = P, D = D * 2
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

    ; Output end of PUSH instruction (newline)
    push    '\\n'
    outc

    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ; Output P encoded in base 3, least-significant value first,        ;
    ; where:                                                            ;
    ; - 0 = space                                                       ;
    ; - 1 = tab                                                         ;
    ; - 2 = newline                                                     ;

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
"""

ASSEMBLED_FILENAME = "quine.ws"
ASSEMBLY_CODE_FILENAME = "quine.ws.asm"


def assemble(program: str) -> str | NoReturn:
    output, errors = asm.assemble(program, "raw")
    if errors:
        for error in errors:
            print(error, file=sys.stderr)

        sys.exit(1)

    return output


def main():
    # Assemble rest of program (P)
    assembly_code = REST_OF_PROGRAM
    rest_of_program = assemble(assembly_code)

    # Convert P to base 3
    s = "".join(WHITESPACE_CHARS[c] for c in rest_of_program)[::-1]
    p = int(s, 3)

    # Program = 'PUSH P' plus P
    push = f"""\
    ; Push rest of program (P)
    push    {p}
"""
    assembly_code = f"{push}{assembly_code}"
    assembled_code = assemble(push) + rest_of_program

    # Write assembly code to file
    Path(ASSEMBLY_CODE_FILENAME).write_text(assembly_code, encoding="utf-8")

    # Write assembled code to file
    Path(ASSEMBLED_FILENAME).write_text(assembled_code, encoding="utf-8")
    return 0


if __name__ == "__main__":
    main()
