        *= $0801 "Basic Upstart"
        BasicUpstart(startm)    // 10 sys$0810

        *= $0810 "Program"
startm:
jmp startm
    // install thin loop
.break
	lda #<thin_loop_start
	sta $0302
	lda #>thin_loop_start
	sta $0303
    jmp thin_loop_start

	// loop over BASIC input
basic_loop_start:
	inc $d021
    jmp startm // resintall thin
	jsr $A560
	stx $7A
	sty $7B
	jsr $0073
	tax
	beq basic_loop_start
	jmp $a490  // jmp to where normally BASIC input is handled


thin_loop_start:
    inc $d020
    lda $cb
    // jsr $e5b4
    cmp #$3f
    bne thin_loop_start
    // reinstall BASIC warm start
	lda #<basic_loop_start
	sta $0302
	lda #>basic_loop_start
	sta $0303
    jmp basic_loop_start



//loopuje se v e5cd
// FFCF	6C 24 03	JMP ($0324)	do input character from channel >$f157
// F170	4C 32 E6	JMP $E632	input from screen or keyboard
// E638	F0 93	BEQ $E5CD	if keyboard go wait for key

// start2:
// 	lda #<key_loop_start
// 	sta $0324
// 	lda #>key_loop_start
// 	sta $0325

// key_loop_start:
//     // $f157
//     lda $99
//     beq !+   // if not the keyboard continue to $f166
//     jmp $f166
// vyrkcinik:  lda $d3
//     sta $ca
//     lda $d6
//     sta $c9
//     jmp e632 // my routine: input from screen or keyboard

// e5cd:
// 	inc $d021  // decide here about mode execution
//     lda $c6
//     sta $cc
//     sta $0292
//     beq e5cd
//     jmp $e5db  // jump to normal BASIC routine
// e632:
//     tya
//     pha
//     txa
//     pha
//     lda $d0
//     beq e5cd  //$e5cd
