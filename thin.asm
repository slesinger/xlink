/* -*- mode: kasm -*- */

.import source "server_h.asm"

// .pc = cmdLineVars.get("pc").asNumber()
	*= $0801 "Basic Upstart"
	BasicUpstart(startm)    // 10 sys$0810

	*= $0810 "Jump table"
	jmp install_thin_mode   // $0810
	jmp install_basic_mode  // $0813
        // *= $0810 "Program"
startm:
	lda #$03  // no key pressed keyboard matrix code
 	sta $2a

	lda #$ff  // set CIA2 port B to output
	sta $dd03

	lda $dd02 // set CIA2 Port A bit 2 to output 
	ora #$04  // this is our handshaking line to the PC
	sta $dd02
	lda #$3d
	:write()

//------------------------------------------------------------------------------

install: {
	lda #$00  // set CIA2 port B to input
	sta $dd03
  
	lda $dd02 // set CIA2 PA2 to output
	ora #$04
	sta $dd02

	lda $dd0d // clear stale handshake

	sei
	lda #<irq // setup irq
	ldx #>irq
	sta $0314
	stx $0315       
	cli

	lda #$4c   // install re-entry via "SYS1000"
	sta $03e8
	lda #<install
	sta $03e9
	lda #>install
	sta $03ea

	rts  // return to basic initially
}

install_thin_mode:
	lda #$0c
	sta $d020
	lda #$17
	sta $d018
thin_mode_loop:
	jmp thin_mode_loop


.const BASIC_warm_start = $a483
install_basic_mode:  // call from thin mode when thin app drawer sends signal to execute this logic
	lda #$15
	sta $d018
	lda #<BASIC_warm_start
	sta $0302
	lda #>BASIC_warm_start
	sta $0303
	lda #$18
	sta irq.mode_select
	lda #$00
	sta $c6  // clear keyboard buffer
	lda #$0e
	sta $d020
	jmp BASIC_warm_start

//------------------------------------------------------------------------------
	
uninstall: {
	lda #>sysirq
	ldx #<sysirq
	sta $0314
	stx $0315
	rts
}

//------------------------------------------------------------------------------
	
irq: {
	lda $dd0d // check for strobe from PC
	and #$10
	beq done  // no command

	ldy $dd01 // read command
	:ack()   

!next:
	cpy #Command.load  // dispatch command
	bne !next+
	jmp load

!next:
	cpy #Command.save
	bne !next+
	jmp save

!next:
	cpy #Command.peek
	bne !next+
	jmp peek
	
!next:
cpy #Command.poke
	bne !next+
	jmp poke
	
!next:
	cpy #Command.jump
	bne !next+
	jmp jump

!next:
	cpy #Command.run
	bne !next+
	jmp run

!next:
	cpy #Command.inject
	bne !next+
	jmp inject

!next:
	cpy #Command.identify
	bne !next+
	jmp identify
        
!next:	
done:
// read key
	lda #$0f   // initialize key to no key changed
	sta $02
	
	lda $2a    // previous key
	eor $cb    // current key
	and #%01111111
	beq thin_fin
	lda $cb    // previous key = current key
	sta $2a
	sta $02    // as key changed, it needs to be written to thin if enabled
	cmp #$40   // current key = no key pressed regardless modifiers
	beq no_modifiers
	// merge key and shift key somehow (and joys)
	// bit 0 shift,  bit 1 C=,  bit 2 CTRL
	lda $028D
	and #%00000001  // shift?
	beq no_shift
	lda $02
	ora #%11000000  // set shift key
	sta $02
	jmp no_modifiers
no_shift:
	lda $028D
	and #%00000010  // C=?
	beq no_commodore
	lda $02
	ora #%10000000  // set C= key
	and #%10111111  // set C= key
	sta $02
no_commodore:
no_modifiers:
// no_key_change:

// no_shift_key_change:  

	// branch for BASIC or thin mode?
mode_select:
	clc  // clc($18): BASIC,     sec($38): thin
	bcs thin_mode  // Branch if Carry is Set
basic_mode:  // check for C=+left arrow and exit IRQ
	// check if C=+left arrow is pressed
	lda $02  // contains blended key and shifts value, see. TODO
	cmp #$b9 // C= + left arrow
	bne basic_fin   // no change change to thin mode, exit
	// change mode from basic to thin
	lda #<thin_mode_loop
	sta $0302
	lda #>thin_mode_loop
	sta $0303
	lda #$38
	sta mode_select
	lda $02
	jsr write_to_thin
	lda #$00
	sta $d020  // indicate change start, it needs to complete by thin.py to execute JMP $thin_mode_loop
	// TODO all the below is here as a try to prevent <left arrow> to appear on screen but no luck. It is due
	// to the fact that at the moment of pressing the eft arrow key, processor is still looping in KERNAL wait key
	// routine and it is not possible to prevent the key to be written to screen.
	lda #$00
	sta $c6  // clear keyboard buffer
	jsr $ffea  // increment the real time clock
	lda $dc0d  // read VIA 1 ICR, clear the timer interrupt flag
	pla
	tay
	pla
	tax
	pla
	rti

basic_fin:
	jmp sysirq

thin_mode:  // send key to thin
	lda $02
	cmp #$0f  // no key pressed
	beq thin_fin
	jsr write_to_thin
thin_fin:
	jmp sysirq
}


write_to_thin:
	lda #$ff   // set CIA2 port B to output
	sta $dd03
	lda $02
	:write()
	lda #$00   // set CIA2 port B to input
	sta $dd03
	rts

load: {
	jsr readHeader
	:screenOff()
	
	:checkBasic()
	
	ldy #$00
	
	lda mem         // check if specific memory config was requested
	and #$7f
	cmp #$37
	bne slow
	
fast:	
!loop:
	:wait()
	lda $dd01 
	sta (start),y   // write with normal memory config
	:ack()
	inc start
	bne !check+
	inc start+1

!check:	
	lda start+1
	cmp end+1
	bne !loop-

	lda start
	cmp end
	bne !loop-
	jmp done

slow:	
!loop:
	:wait()
	lda $dd01
	ldx #$33        // write to ram with io disabled
	stx $01
	sta (start),y
	lda #$37
	sta $01
	:ack()
	inc start
	bne !check+
	inc start+1

!check:	
	lda start+1
	cmp end+1
	bne !loop-

	lda start
	cmp end
	bne !loop-

done:
	:relinkBasic()
	:screenOn()
	jmp irq.done
}

//------------------------------------------------------------------------------
	
save: {
	jsr readHeader
	:screenOff()
	
        :output()
	ldy #$00

	lda mem        // check if specific memory config was requested
	cmp #$37
	beq fast
	jmp slow	

fast:	
!loop:
	lda (start),y  // read with normal memory config
	:write()
	inc start
	bne !check+
	inc start+1

!check:
	lda start+1
	cmp end+1
	bne !loop-

	lda start
	cmp end
	bne !loop-
	jmp done

slow:
!loop:
	lda mem        // read with requested memory config
	sta $01
	lda (start),y
	ldx #$37
	stx $01
	:write()
	inc start
	bne check
	inc start+1

check:	
	lda start+1
	cmp end+1
	bne !loop-

	lda start
	cmp end
	bne !loop-
	
done:	lda #$00   // reset CIA2 port B to input
	sta $dd03
	
	:screenOn()
	jmp irq.done
}

//------------------------------------------------------------------------------
	
poke: {
	jsr read
	stx mem
	jsr read
	stx bank
	jsr read
	stx start
	jsr read
	stx start+1

	ldy #$00	

	:wait()
	lda $dd01
	tax 
	:ack() 
	txa
	
	ldx mem
	stx $01
	sta (start),y
	lda #$37
	sta $01

	jmp irq.done
}

//------------------------------------------------------------------------------
	
peek: {
	jsr read
	stx mem
	jsr read
	stx bank
	jsr read
	stx start
	jsr read
	stx start+1

    :output()
	
	ldy #$00
	ldx mem
	stx $01
	lda (start),y
	ldx #$37
	stx $01

	jsr write

done:
	:input()
	
	jmp irq.done
}

//------------------------------------------------------------------------------
	
jump: {
	jsr read
	stx mem
	jsr read
	stx bank

	ldx #$ff
	txs // reset stack pointer

	lda #>repl
	pha // make sure the code jumped to can rts to basic
	lda #[<repl-1]
	pha   
  
	jsr read
	txa
	pha // push high byte of jump address
	jsr read
	txa
	pha // push low byte of jump address

	lda mem  // apply requested memory config
	sta $01
	
	lda #$00
	tax
	tay
	pha // clear registers & push clean flags 
	
	rti // jump via rti
}

//------------------------------------------------------------------------------
	
run: {
	jsr uninstall
	
	ldx #$ff
	txs        // reset stack pointer
	lda #$01
	sta cursor // cursor off

	jsr insnewl         // preprare run BASIC program
	jsr restxtpt

	lda #$00            // flag program mode
	sta mode  // TODO co je to tohle?
	
	jmp warmst
}

//------------------------------------------------------------------------------
	
inject:	{
	lda #>return
	pha
	lda #<return
	pha
	
	jsr read
	txa
	pha 
	jsr read
	txa
	pha
	
	rts
	
return: nop
	jmp irq.done
}

//------------------------------------------------------------------------------

identify: {
        :output()

        lda Server.size
        jsr write
  
        lda Server.id
        jsr write

        lda Server.id+1
        jsr write

        lda Server.id+2
        jsr write

        lda Server.id+3
        jsr write

        lda Server.id+4
        jsr write
  
        lda Server.version   
        jsr write

        lda Server.machine
        jsr write

        lda Server.type
        jsr write       

        lda Server.start
        jsr write

        lda Server.start+1
        jsr write

        lda Server.end
        jsr write

        lda Server.end+1
        jsr write

	lda memtop
	jsr write

	lda memtop+1
	jsr write
        
done:   :input()
        
        jmp irq.done
}
        
//------------------------------------------------------------------------------	
	
readHeader: {
	jsr read
	stx mem
	jsr read
	stx bank
	jsr read
	stx start
	jsr read
	stx start+1
	jsr read
	stx end
	jsr read
	stx end+1
	rts
}

//------------------------------------------------------------------------------
	
read: {
	:read()
	rts
}

//------------------------------------------------------------------------------	
	
write: {
	:write()
	rts
}

//------------------------------------------------------------------------------
	
Server:	{
size:    .byte $05
id:      .byte 'X', 'L', 'I', 'N', 'K'
start:	 .word install
version: .byte $10
type:	 .byte $00 // 0 = RAM, 1 = ROM
machine: .byte $00 // 0 = C64
end:	 .word *+2
}

//------------------------------------------------------------------------------	


