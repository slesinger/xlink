# Ideation

## Immediate Goals
zprovoznit barevny buffer
partial screen update changes
Renderovat Button a BigButton, viz https://petscii.krissz.hu
map CTRL like TAB? and SH_CTRL as SHIFT_TAB?
mapovat joystick, nevesel by se do undefined vcetne modifieru? Pak by se nachal udelat CTRL jako modifier 01
mapping function keyboard codes > ascii  https://www.c64-wiki.com/wiki/Keyboard_code
mapping ascii to screen codes  https://sta.c64.org/cbm64scr.html
cursor set
input widet
screen scroll
screen partial updates
design drawer app

## High Level Goals

- input field na zadani URI
- nacteni MTextu
- list server directory
- search the web
- talk to AI
- SSH
- read emails

## Controls

```text
￩ enable thin client
```

## Mapping
c64 keyboard codes to unicode key codes
unicode to screencodes incl reverse

## Widgets

### Input

### Button

### Hotkey

Does not render. May have automatic help later

## Next widgets
viewport, content, mdtext_browser, textbox, layout


# Dal ladit
1	1  obe bezi      OK  (C64 se vypne a pak zapne)  (PC se vypne a pak zapne)
bylo v c64 rezimu
bylo v xthin rezimu

v xthin rezimu, pc restart FAIL, C64 se nusi restartovat. C64 musi detekovat, ze je diconnected, tzn na left arrow se prepnout do basicu a pak eventuelne cekat na pripojeni.
po nastartovani c64 musi detekovat pripojeni v irq a nezablokovat se