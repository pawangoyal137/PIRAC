package main
import "fmt"

var _ = fmt.Println

// type Database struct{
// 	DB []string
// }

// decided by the sym
// Params
// Encparams

// decided by the underlying pir
// ClientState
// ServerState
// Database

type SymEncPIR struct{
	Pir PIR
	EncKeys EncParams
}

func (sympir *SymEncPIR) Init(pir PIR, p Params, enckeys EncParams, dataentries []DatabaseEntry) {
	pir.Setup(p, dataentries)
	sympir.Pir = pir
	sympir.EncKeys = enckeys
}

// func (sympir *SymEncPIR) Query(i uint64, token string) QueryMsg {
// 	var query QueryMsg
// 	sympir.ClSt, query = sympir.Pir.Query(i, sympir.ClSt)
// 	return query
// }

// func (sympir *SymEncPIR) Recover(i uint64, token string, answer AnswerMsg) string {
// 	ciphertext := sympir.Pir.Recover(i, sympir.ClSt, answer)
// 	return sympir.Decrypt(token, ciphertext)
// }

// func (sympir *SymEncPIR) Answer(query QueryMsg) AnswerMsg {
// 	encDB := sympir.Pir.EncryptDB(sympir.DB, sympir.EncKeys)
// 	return sympir.Pir.Answer(encDB, query, sympir.SvSt)
// }

func (sympir *SymEncPIR) Decrypt(token string, ciphertext DatabaseEntry) DatabaseEntry{
	// TODO: Change
	return ciphertext
}

func (sympir *SymEncPIR) Run(i uint64, token string) DatabaseEntry {
	ciphertext := sympir.Pir.EncryptAndRun(i, sympir.EncKeys)
	return sympir.Decrypt(token, ciphertext)
}

func main() {
	var index uint64
	index = 2

	pir := &NaivePIR{}
	secparm := Params{20}
	sympir := &SymEncPIR{}

	database := []DatabaseEntry{1,2,3,4}
	sympir.Init(pir, secparm, EncParams{}, database)
	fmt.Println(sympir.Run(index, ""))
}

