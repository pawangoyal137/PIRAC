#include <stdio.h>
#include <string.h>
#include <stdint.h>

typedef unsigned __int128 uint128_t;

uint128_t *encryptDatabase(uint128_t *database, uint128_t seed, uint64_t db_size, uint64_t elem_size);
