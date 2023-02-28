#include "../include/test.h"
#include <stdio.h>
#include <stdlib.h>

uint64_t *test(uint64_t *database, uint64_t seed, uint64_t size) {
    uint64_t *output = malloc(sizeof(uint64_t) *size);
    for (int i = 0; i < size; i++) {
        output[i] = database[i] + seed;
    }
    return output;
}