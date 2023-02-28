package main

import "fmt"

var _ = fmt.Println

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
	// TODO: Change
	return database
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
// 	fmt.Println(test.Name(), test.Run(index), test.EncryptAndRun(index, EncParams{}))
// }