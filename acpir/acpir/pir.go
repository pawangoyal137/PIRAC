package main

// import "fmt"


// Defines the interface for a blackbox PIR
type PIR interface {
	Name() string

	// sets up the client and server states, setup the database
	Setup(p Params, dataentries []string)  (ClientState, ServerState, *Database)
	
	Query(i uint64, clstate ClientState) (ClientState, QueryMsg)

	Answer(DB *Database, query QueryMsg, server ServerState) AnswerMsg

	Recover(i uint64, clstate ClientState, answer AnswerMsg) string

	// Return a new database encrypted under the provided keys
	EncryptDB(database *Database, enckeys EncParams) *Database
}
