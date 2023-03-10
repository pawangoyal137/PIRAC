package main

// import "fmt"


// Defines the interface for a blackbox PIR
type PIR interface {
	Name() string

	// sets up the client and server states, setup the database
	// Only database is passed around as reference, else all other objects are
	// passed by value
	Setup(p Params, dataentries []DatabaseEntry)
	
	Run(i uint64) DatabaseEntry

	EncryptAndRun(i uint64, enckeys EncParams) DatabaseEntry
}
