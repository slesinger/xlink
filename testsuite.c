#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

#include "range.h"

void check(bool condition, const char* message) {
  if(!condition) {
    fprintf(stderr, message);
    fprintf(stderr, "\n");
    exit(EXIT_FAILURE);
  }
}

void test_range() {
  
  Range* range = range_new(0x0801, 0x3000);
  Range* other = range_new(0x0801, 0x3000);
  
  check(range->start == 0x0801 && range->end == 0x3000, "Range not $0801-$3000");

  check(range_size(range) == 0x27ff, "Range size is not $27ff");

  check(range_equals(range, other), "Ranges are not equal");
  
  range_move(range, 0x1000);
  check(range->start == 0x1801 && range->end == 0x4000, "Range not moved to $1801-$4000");

  range_move(range, -0x1000);
  check(range->start == 0x0801 && range->end == 0x3000, "Range not moved back to $0801-$3000");

  range_move(range, -0x1000);
  check(range->start == 0x0000 && range->end == 0x27ff, "Range not moved to $0000-$27ff");

  range_move(range, 0x80000);
  check(range->start == 0xd801 && range->end == 0x10000, "Range not moved to $d801-$10000");  
  
  free(range);
  free(other);

  range = range_new(0x1000, 0x2000);
  other = range_new(0x1800, 0x2800);

  check(range_overlaps(range, other), "Ranges don't overlap");
  check(range_overlaps(other, range), "Ranges don't overlap");

  range_move(other, 0x4000);
  check(!range_overlaps(range, other), "Ranges overlap");
  check(!range_overlaps(other, range), "Ranges overlap");

  free(range);
  free(other);

  range = range_new(0x1000, 0x2000);
  other = range_new(0x0800, 0x2800);

  check(range_inside(range, other), "Range $1000-$2000 not within Range $0800-$2800");

  other->start = 0x1000;
  check(range_inside(range, other), "Range $1000-$2000 not within Range $1000-$2800");

  other->start = 0x0800;
  other->end = 0x2000;

  check(range_inside(range, other), "Range $1000-$2000 not within Range $0800-$2000");

  free(range);
  free(other);  
}

int main(int argc, char** argv) {
  test_range();
  
  exit(EXIT_SUCCESS);
}
