package main

// #cgo CFLAGS: -g -Wall 
// #cgo LDFLAGS: -L /usr/local/Cellar//openssl@3/3.0.8/lib/ -lcrypto -lssl -lm
// #include <stdlib.h>
// #include "../include/encryption.h"
import "C"
import (
	"fmt"
	"unsafe"
	"math/rand"
	"reflect"
)
var _ = rand.Uint64
var _ = fmt.Println

func carray2slice(array *C.uint64_t, len int) []C.uint64_t {
	var list []C.uint64_t
	sliceHeader := (*reflect.SliceHeader)((unsafe.Pointer(&list)))
	sliceHeader.Cap = len
	sliceHeader.Len = len
	sliceHeader.Data = uintptr(unsafe.Pointer(array))
	return list
}

// func main()  {
// 	num_elements := 3
// 	database := [...]uint64{10, 20, 30}
// 	var encrpytedDB [3]uint64
// 	seed := rand.Uint64()
// 	C.encryptDatabase((*C.uint64_t)(&database[0]),(*C.uint64_t)(&encrpytedDB[0]), C.uint64_t(seed), C.uint64_t(num_elements), C.uint64_t(1))
// 	fmt.Println(encrpytedDB)
// }