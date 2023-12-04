#include <stdint.h>
#include <stdlib.h>
#include "../include/encryption.h"
#include "../include/aes.h"

uint128_t *encryptDatabase(uint128_t *database, uint128_t seed, uint64_t db_size, uint64_t elem_size)
{
    struct AES *aes_keys = initAESkeys((uint8_t *)&seed, db_size);
    uint128_t *encrpyted_dB = malloc(sizeof(uint128_t) * db_size * elem_size);

    if (encrpyted_dB == NULL)
    {
        printf("failed to allocate space");
        exit(0);
    }

    reEncrypt(aes_keys, db_size, elem_size, database, encrpyted_db);

    return encrpyted_db;
}