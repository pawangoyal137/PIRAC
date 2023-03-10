package main

// #cgo CFLAGS: -g -Wall 
// #cgo LDFLAGS: -L /usr/local/Cellar//openssl@3/3.0.8/lib/ -lcrypto -lssl -lm
// #include <stdlib.h>
// #include "../include/encryption.h"
import "C"
import "fmt"
import "math/rand"

var _ = fmt.Println
var _ = rand.Uint64

type NPClientState struct{}

type NPServerState struct{}

type NPQueryMsg struct{
	index uint64 
}

type NPAnswerMsg struct{
	response DatabaseEntry
}

type NPDatabase struct{
	DB []DatabaseEntry
}


// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

type NaivePIR struct{
	DB NPDatabase
	ClSt NPClientState
	SvSt NPServerState
}

func (pi* NaivePIR) Name() string  {
	return "Naive PIR"
}

func (pi* NaivePIR) Setup(p Params, dataentries []DatabaseEntry) {
	pi.ClSt = NPClientState{}
	pi.SvSt = NPServerState{}
	pi.DB = NPDatabase{dataentries}
}

func (pi* NaivePIR) Query(i uint64) NPQueryMsg{
	return NPQueryMsg{i}
}

func (pi* NaivePIR) Answer(query NPQueryMsg, database *NPDatabase) NPAnswerMsg{
	return NPAnswerMsg{database.DB[query.index]}
}

func (pi* NaivePIR) Recover(i uint64, answer NPAnswerMsg) DatabaseEntry {
	return answer.response
}

func (pi* NaivePIR) _run(i uint64, database *NPDatabase) DatabaseEntry {
	query := pi.Query(i)
	response := pi.Answer(query, database)
	message := pi.Recover(i, response)
	return message
}

func (pi* NaivePIR) Run(i uint64) DatabaseEntry {
	return pi._run(i, &pi.DB)
}

func (pi* NaivePIR) EncryptDB(database *NPDatabase, enckeys EncParams) *NPDatabase{
	num_elements := len(pi.DB.DB)
	encDB := make([]DatabaseEntry, num_elements)
	C.encryptDatabase((*C.uint64_t)(&pi.DB.DB[0]), (*C.uint64_t)(&encDB[0]), C.uint64_t(enckeys.seed), C.uint64_t(num_elements), C.uint64_t(1))
	return &NPDatabase{encDB}
}

func (pi* NaivePIR) EncryptAndRun(i uint64, enckeys EncParams) DatabaseEntry {
	encDatabase := pi.EncryptDB(&pi.DB, enckeys)
	return pi._run(i, encDatabase)
}

// func main()  {
// 	var index uint64
// 	index = 2

// 	test := &NaivePIR{}
// 	test.Setup(Params{20}, []DatabaseEntry{1,2,3,4})
// 	fmt.Println(test.Name(), test.Run(index), test.EncryptAndRun(index, EncParams{rand.Uint64()}))
// }