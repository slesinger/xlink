#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

#include "pp64.h"
#include "driver/driver.h"
#include "extension.h"
#include "extensions.c"
#include "util.h"

extern Driver* driver;

//------------------------------------------------------------------------------

bool pp64_set_device(char* path) {
  driver_setup(path);
  return pp64_has_device();
}  

//------------------------------------------------------------------------------

bool pp64_has_device() {
  return driver != NULL;
}

//------------------------------------------------------------------------------

bool pp64_ping() {
  
  bool result = false;

  if(driver->open()) {
    result = driver->ping();
    driver->close();
  }

  return result;
}

//------------------------------------------------------------------------------

bool pp64_reset(void) {

  if(driver->open()) {
    driver->reset();
    driver->close();
    return true;
  }
  return false;
};

//------------------------------------------------------------------------------

bool pp64_load(unsigned char memory, 
	       unsigned char bank, 
	       int start, 
	       int end, 
	       char* data, int size) {
  
  logger->enter("pp64_load");

  bool result = true;

  if(driver->open()) {
    
    if(!driver->ping()) {
      logger->error("no response from C64");
      result = false;
      goto done;
    }

    driver->output();    
    driver->send((char []) {PP64_COMMAND_LOAD, memory, bank, lo(start), hi(start), lo(end), hi(end)}, 7);
    driver->send(data, size);
    
    result = true;
  }

 done:
  driver->close();
  logger->leave();
  return result;
}

//------------------------------------------------------------------------------

bool pp64_save(unsigned char memory, 
	       unsigned char bank, 
	       int start, 
	       int end, 
	       char* data, int size) {

  if(driver->open()) {

    if(!driver->ping()) {
      logger->error("no response from C64");
      driver->close();
      return false;
    }

    driver->output();
    driver->send((char []) {PP64_COMMAND_SAVE, memory, bank, lo(start), hi(start), lo(end), hi(end)}, 7);

    driver->input();
    driver->strobe();

    driver->receive(data, size);

    driver->close();
    return true;
  }
  return false;
}

//------------------------------------------------------------------------------

bool pp64_peek(unsigned char memory, unsigned char bank, int address, unsigned char* value) {
  
  if(driver->open()) {
  
    if(!driver->ping()) {
      logger->error("no response from C64");
      driver->close();
      return false;
    }

    driver->output();
    driver->send((char []) {PP64_COMMAND_PEEK, memory, bank, lo(address), hi(address)}, 5);
    
    driver->input();
    driver->strobe();

    driver->receive((char *)value, 1);

    driver->close();
    return true;
  }
  return false;
}

//------------------------------------------------------------------------------

bool pp64_poke(unsigned char memory, unsigned char bank, int address, unsigned char value) {

  if(driver->open()) {
  
    if(!driver->ping()) {
      logger->error("no response from C64");
      driver->close();
      return false;
    }
    
    driver->output();
    driver->send((char []) {PP64_COMMAND_POKE, memory, bank, lo(address), hi(address), value}, 6);    

    driver->close();
    return true;
  }
  return false;
}

//------------------------------------------------------------------------------

bool pp64_jump(unsigned char memory, unsigned char bank, int address) {

    // jump address is send MSB first (big-endian)    

   if(driver->open()) {
  
    if(!driver->ping()) {
      logger->error("no response from C64");
      driver->close();
      return false;
    }

    driver->output();
    driver->send((char []) {PP64_COMMAND_JUMP, memory, bank, hi(address), lo(address)}, 5);    

    driver->close();
    return true;
  }
  return false;
}

//------------------------------------------------------------------------------

bool pp64_run(void) {

   if(driver->open()) {
  
    if(!driver->ping()) {
      logger->error("no response from C64");
      driver->close();
      return false;
    }

    driver->output();
    driver->send((char []) {PP64_COMMAND_RUN}, 1);

    driver->close();
    return true;
  }
  return false;
}

//------------------------------------------------------------------------------

bool pp64_extend(int address) {

  if(driver->open()) {
  
    if(!driver->ping()) {
      logger->error("no response from C64");
      driver->close();
      return false;
    }
  
    // send the address-1 high byte first, so the server can 
    // just push it on the stack and rts
    
    address--;

    driver->output();
    driver->send((char []) {PP64_COMMAND_EXTEND, hi(address), lo(address)}, 3);

    driver->close();
    return true;
  }
  return false;
}

//------------------------------------------------------------------------------

bool pp64_drive_status(char* status) {

  logger->enter("pp64_drive_status");

  unsigned char byte;
  bool result = false;

  Extension *lib = EXTENSION_LIB;
  Extension *drive_status = EXTENSION_DRIVE_STATUS;

  if (extension_load(lib) && extension_load(drive_status) && extension_init(drive_status)) {

    if (driver->open()) {
      
      driver->input();
      driver->strobe();

      int i = 0;

      // TODO: fixme: infinite loop, add another ack from server before entering?
      while(true) {

        driver->receive((char *) &byte, 1);

        if(byte == 0xff) break;

        status[i++] = byte;	
      }
      driver->wait(0);

      driver->close();
      result = true;
    }
  }

  extension_free(lib);
  extension_free(drive_status);
  logger->leave();

  return result;
}

//------------------------------------------------------------------------------

bool pp64_dos(char* cmd) {

  logger->enter("pp64_dos");

  bool result = false;

  Extension *lib = EXTENSION_LIB;
  Extension *dos_command = EXTENSION_DOS_COMMAND;

  char *command = (char *) calloc(strlen(cmd)+1, sizeof(char));
  
  for(int i=0; i<strlen(cmd); i++) {
    command[i] = toupper(cmd[i]);
  }      

  logger->debug("loading & initialising extensions");

  if(extension_load(lib) && extension_load(dos_command) && extension_init(dos_command)) {
    
    if(driver->open()) {   

      driver->output();
      driver->send((char []) {strlen(command)}, 1);
      driver->send(command, strlen(command));

      driver->wait(0);

      driver->close();
      result = true;
    }
  }
  
  free(command);
  extension_free(lib);
  extension_free(dos_command);
  logger->leave();

  return result;
}

//------------------------------------------------------------------------------

bool pp64_sector_read(unsigned char track, unsigned char sector, unsigned char* data) {
  
  bool result = false;
  char U1[13];

  Extension *lib = EXTENSION_LIB;
  Extension *sector_read = EXTENSION_SECTOR_READ;

  if (extension_load(lib) && extension_load(sector_read) && extension_init(sector_read)) {

    if (driver->open()) {
      
      sprintf(U1, "U1 2 0 %02d %02d", track, sector);

      driver->output();
      driver->send(U1, strlen(U1));

      driver->input();
      driver->strobe();

      driver->receive((char *) data, 256);
      driver->wait(0);
      
      driver->close();      
      result = true;
    }
  }

  extension_free(lib);
  extension_free(sector_read);

  return result;
}

//------------------------------------------------------------------------------

bool pp64_sector_write(unsigned char track, unsigned char sector, unsigned char *data) {

  int result = false;
  char U2[13];

  Extension *lib = EXTENSION_LIB;
  Extension *sector_write = EXTENSION_SECTOR_WRITE;

  if (extension_load(lib) && extension_load(sector_write) && extension_init(sector_write)) {

    if (driver->open()) {
      sprintf(U2, "U2 2 0 %02d %02d", track, sector);

      driver->output();
      driver->send((char *) data, 256);
      driver->send(U2, strlen(U2));

      driver->wait(0);
      
      driver->close();
      result = true;
    }
  }
  
  extension_free(lib);
  extension_free(sector_write);
  return result;
}

//------------------------------------------------------------------------------

bool pp64_test(char* path, char *test) {

  Driver *driver = driver_setup(path);
  Watch* watch = watch_new();
  bool result = false;

  if(driver == NULL) {
    goto done;
  }

  logger->enter("testsuite");

  if(driver->open()) {

    logger->info("running test \"%s\"", test);

    if(strcmp(test, "FLASH") == 0) {
      driver->flash();
      goto done;
    }

    if(strcmp(test, "PING") == 0) {
      
      watch_start(watch);

      if(driver->ping()) {
        logger->info("received ping reply after %.2fms", watch_elapsed(watch));
      } 
      else {
        logger->error("no response from C64");
        result = false;
      }
      goto done;
    }

    if(strcmp(test, "RESET") == 0) {
      driver->reset();
      goto done;
    }

    if(strcmp(test, "TRANSFER") == 0) {

      if(!driver->ping()) {
        logger->error("no response from C64");
        result = false;
        goto done;
      }

      char payload[0x8000];
      char roundtrip[sizeof(payload)];
      
      int start = 0x1000;
      int end = start + sizeof(payload);
      
      logger->info("sending %d bytes...", sizeof(payload));
      
      watch_start(watch);

      driver->output();
      driver->send((char []) {PP64_COMMAND_LOAD, 0x37, 0x10, lo(start), hi(start), lo(end), hi(end)}, 7);
      driver->send(payload, sizeof(payload));
      
      float seconds = (watch_elapsed(watch) / 1000.0);
      float kbs = sizeof(payload)/seconds/1024;
      
      logger->info("%.2f seconds at %.2f kb/s", seconds, kbs);       
      
      logger->info("receiving %d bytes...", sizeof(payload));

      watch_start(watch);
      
      driver->send((char []) {PP64_COMMAND_SAVE, 0x37, 0x10, lo(start), hi(start), lo(end), hi(end)}, 7);
      
      driver->input();
      driver->strobe();
      
      driver->receive(roundtrip, sizeof(payload));
      
      seconds = (watch_elapsed(watch) / 1000.0);
      kbs = sizeof(payload)/seconds/1024;

      logger->info("%.2f seconds at %.2f kb/s", seconds, kbs);
      
      logger->info("verifying...");
      
      for(int i=0; i<sizeof(payload); i++) {
        if(payload[i] != roundtrip[i]) {
          logger->error("roundtrip error at byte %d: %d != %d", i, payload[i], roundtrip[i]);
          result = false;
          goto done;
        }
      }
      logger->info("test completed successfully");

      result = true;
    }
  }
  
 done:
  if(driver != NULL) {
    driver->close();
    driver->free();
  }
  watch_free(watch);

  logger->leave();
  return result;
}
