.pc = $9990

jmp rom.install
	
//------------------------------------------------------------------------------
	
.var start = $c1    // Transfer start address
.var end   = $c3    // Transfer end address

.var mem   = $fc    // Memory config
.var bank  = $fd    // bank config
.var low   = $fe    // $dd00 | #$04 (ack bit low)
.var high  = $ff    // $dd00 & #$fb /ack bit high);
	
.var insnewl  = $a659 // Insert new line into BASIC program
.var restxtpt = $a68e // Reset BASIC text pointer
.var warmst   = $a7ae // Basic warm start (e.g. RUN)

.namespace Command {
.label load  = $01
.label save  = $02
.label peek  = $03
.label poke  = $04
.label jump  = $05
.label run   = $06
}
	
.macro wait() { // Wait for handshake from PC (falling edge on FLAG <- Parport STROBE)
loop:	lda $dd0d
	and #$10
	beq loop
}

.macro ack() { // Send handshake to PC (rising edge on CIA2 PA2 -> Parport ACK) 
	ldx low
	stx $dd00
	ldx high
	stx $dd00
}

.macro fastack() { // assumes ($dd00 | $04) in X
	xaa #$fb
	sta $dd00
	stx $dd00
}
	
.macro strobe() { :ack() }
.macro faststrobe() { :fastack() }

.macro read() {
	:wait() lda $dd01 :ack()
}

.macro write() {
	sta $dd01 :strobe() :wait()
}

.macro fastwrite() {
	sta $dd01 :faststrobe() :wait()
}
	
.macro next() {
	inc start
	bne check
	inc start+1

check:	lda start+1
	cmp end+1
	bne !loop-

	lda start
	cmp end
	bne !loop-
}
	
.macro screenOff() {
	lda #$0b
	sta $d011
}

.macro screenOn() {
	lda #$1b
	sta $d011
}

readHeader: {
	jsr read sta mem
	jsr read sta bank
	jsr read sta start
	jsr read sta start+1
	jsr read sta end
	jsr read sta end+1
	rts
}

read: { :read() rts }
write: { :write() rts }

//------------------------------------------------------------------------------
rom: {
install: {
	
	lda $0314    // check if already installed
	cmp #<ram.irq
	bne install
	lda $0315
	cmp #>ram.irq
	bne install

	jsr uninstall // is installed -> uninstall
	jmp done
	
install:
	lda #$00  // set CIA2 port B to input
	sta $dd03
	
	lda $dd02 // set CIA2 PA2 to output
	ora #$04
	sta $dd02

	lda $dd0d // clear stale handshake

	sei
	lda #<ram.irq // setup irq
	ldx #>ram.irq
	sta $0314
	stx $0315	
	cli

	ldx #eof-ram-1 // install ramcode
copy:	lda ram,x
	sta $02a7,x
	dex
	bpl copy

done:	jmp ram.dorts
}

uninstall: {
	jsr hidemsg
	lda #$31
	ldx #$ea
	sta $0314
	stx $0315
	rts
}
	
irq: {
	jsr showmsg
	
	lda $dd0d // check for strobe from PC
	and #$10
	beq done  // no command

	ldy $dd01 // read command

	lda $dd00 // prepare ack values
	and #$fb sta low   
	ora #$04 sta high

	:ack()   // ack command 

!next:	cpy #Command.load  // dispatch command
	bne !next+
	jmp load

!next:	cpy #Command.save
	bne !next+
	jmp save

!next:	cpy #Command.peek
	bne !next+
	jmp peek
	
!next:	cpy #Command.poke
	bne !next+
	jmp poke
	
!next:	cpy #Command.jump
	bne !next+
	jmp jump

!next:	cpy #Command.run
	bne done
	jmp run
	
done:	jmp ram.dorti
}

load: {
	:screenOff()
	jsr readHeader
	
	lda mem         // check if specific memory config was requested
	cmp #$37
	beq fast
	jmp slow
	
fast:	ldy #$00
	ldx high        // prepare fastack

!loop:  :wait()
	lda $dd01 
	sta (start),y   // write with normal memory config
	:fastack()
	:next()
	jmp done

slow:	ldx high        // prepare fastack
!loop:  :wait()
	ldy mem         // write with requested memory config
	sty $01
	ldy #$00
	sta (start),y
	lda #$37
	sta $01
	:fastack()
	:next()

done:   :screenOn()
	jmp irq.done
}

save: {
	:screenOff()
	jsr readHeader

	:wait()        // wait until PC has set its port to input
	lda #$ff       // and set CIA2 port B to output
	sta $dd03

	ldy #$00

	lda mem        // check if specific memory config was requested
	cmp #$37
	beq fast
	jmp slow	

fast:	ldx high       // prepare fastwrite
!loop:  jsr ram.read
	:fastwrite()
	:next()
	jmp done

slow:
!loop:  lda mem        // read with requested memory config
	sta $01
	jsr ram.read
	ldx #$37
	stx $01
	:write()
	:next()
	
done:	lda #$00   // reset CIA2 port B to input
	sta $dd03
	
	:screenOn()
	jmp irq.done
}

peek: {
	jsr read sta mem
	jsr read sta bank
	jsr read sta start
	jsr read sta start+1

	:wait()        // wait until PC has set its port to input
	lda #$ff       // and set CIA2 port B to output
	sta $dd03
	
	ldy #$00
	ldx mem
	stx $01
	jsr ram.read
	ldx #$37
	stx $01

	jsr write

done:	lda #$00   // reset CIA2 port B to input
	sta $dd03
	
	jmp irq.done
}
	
poke: {
	jsr read sta mem
	jsr read sta bank
	jsr read sta start
	jsr read sta start+1
	jsr read

	ldy #$00
	ldx mem
	stx $01
	sta (start),y
	lda #$37
	sta $01

	jmp irq.done
}
	
jump: {
	jsr uninstall	

	jsr read sta mem
	jsr read sta bank

	ldx #$ff txs // reset stack pointer
	
	jsr read pha // push high byte of jump address
	jsr read pha // push low byte of jump address

	lda mem  // apply requested memory config
	sta $01

	lda #$00 tax tay pha // clear registers & push clean flags 
	
	jmp ram.jump
}

run: {
	jsr uninstall
	jmp ram.run
}

showmsg: {
	ldx #$27
loop:	lda msg,x
	sta $0400,x
	lda #$07
	sta $d800,x
	dex
	bpl loop
	rts	

msg: .byte $A0, $A0, $A0, $A0, $A0, $A0, $83, $B6, $B4, $8C
     .byte $89, $8E, $8B, $A0, $93, $85, $92, $96, $85, $92
     .byte $A0, $B1, $AE, $B0, $A0, $89, $8E, $93, $94, $81
     .byte $8C, $8C, $85, $84, $A0, $A0, $A0, $A0, $A0, $A0
}

hidemsg: {
	ldx #$27
	lda #$20
loop:	sta $0400,x
	dex
	bpl loop
	rts
}
	
} // end rom
	
ram: { // copied to $02a7
.pseudopc $02a7 {
irq:
	lda #$18   // enable rr bank 3
	sta $de00	  	
	jmp rom.irq // jump to service irq routine in rom

dorti:	lda #$48   // reset rr bank
	sta $de00
	jmp $ea31  // jump to system irq

dorts:	lda #$48   // enable rr bank 0
	sta $de00
	lda #$00
	rts

read:	lda #$1a       // disable rr
	sta $de00
	lda (start),y  // read from ram
	ldy #$18       // enable rr
	sty $de00
	ldy #$00
	rts	
	
jump:   lda #$48   // enable rr bank 0
	sta $de00
	rti
	
run:    lda #$48   // enable rr bank 0
	sta $de00

	ldx #$ff txs     // reset stack pointer
	lda #$01 sta $cc // cursor off

	jsr insnewl     // run BASIC program
	jsr restxtpt
	jmp warmst
}
}
eof:



	
