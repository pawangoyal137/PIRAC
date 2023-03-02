#ifndef _ENCRYPTION
#define _ENCRYPTION

#include <stdio.h>
#include <string.h>
#include <stdint.h>

#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>

void encryptDatabase(uint64_t *database, uint64_t *encrpytedDB, uint64_t seed, uint64_t size, uint64_t elemsize);

#endif