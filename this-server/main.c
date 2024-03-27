#include <stdio.h>
#include <stdlib.h>
#include <xlink.h>

int main(int argc, char **argv)
{

    // memory config to use
    uchar memory = 0x37;

    // bank value (reserverd, always use 0x00)
    uchar bank = 0x00;

    // start of screen ram
    unsigned short address = 0x0400;

    // "HONDANI!" in C64 Screencode
    // char data[12] = {0x08, 0x0F, 0x0E, 0x04, 0x01, 0x0E, 0x09, 0x21};
    // if (!xlink_load(memory, bank, address, data, sizeof(data)))
    // {
    //     fprintf(stderr, "error: %s\n", xlink_error->message);
    // }

    printf("start loop\n");
    uchar key_input = 'm';

    uchar *backup_screen = (uchar*)malloc(40 * 25 * sizeof(uchar));
    if (backup_screen == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }

    // Dispatch key inputs in an infinite loop
    while(true) {
        do
        {
            xlink_begin();
        } while (!xlink_receive(&key_input, 1));  // wait for key input

        // $40 - all keys up, continue
        if (key_input == 0x40)
        {
            xlink_end();
            continue;
        }

        fprintf(stderr, "%d\n", (int)key_input);

        if (key_input == 0x39)  // left arrow enter thin mode
        {
            fprintf(stdout, "enter ");
            xlink_end();
            int rc = xlink_poke(memory, bank, 0xd020, 0x00);
            fprintf(stdout, "%d\n", rc);
            rc = xlink_save(memory, bank, address, backup_screen, 40*25);  // save screen memory (40x25, 1 byte per character, 1 byte per color)
            fprintf(stdout, "saved %d\n", rc);
            continue;
        }

        if (key_input == 0x3f)  // Run/Stop exit thin mode
        {
            xlink_end();
            int rc = xlink_load(memory, bank, address, backup_screen, 40*25);  // load screen memory (40x25, 1 byte per character, 1 byte per color)
            fprintf(stdout, "restored %d\n", rc);
            rc = xlink_poke(memory, bank, 0xd020, 0x0e);
            fprintf(stdout, "exited %d\n", rc);
            continue;
            // return 0;
        }

        xlink_end();
    }
}
