package main
import "fmt"

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
	DB *Database
	ClSt ClientState
	SvSt ServerState
	Pir PIR
	EncKeys EncParams
}

func (sympir *SymEncPIR) Init(pir PIR, p Params, enckeys EncParams, dataentries []string) {
	sympir.ClSt, sympir.SvSt, sympir.DB = pir.Setup(p, dataentries)
	sympir.Pir = pir
	sympir.EncKeys = enckeys
}

func (sympir *SymEncPIR) Query(i uint64, token string) QueryMsg {
	var query QueryMsg
	sympir.ClSt, query = sympir.Pir.Query(i, sympir.ClSt)
	return query
}

func (sympir *SymEncPIR) Answer(query QueryMsg) AnswerMsg {
	encDB := sympir.Pir.EncryptDB(sympir.DB, sympir.EncKeys)
	return sympir.Pir.Answer(encDB, query, sympir.SvSt)
}

func (sympir *SymEncPIR) Decrypt(token string, ciphertext string) string{
	// TODO: Change
	return ciphertext
}

func (sympir *SymEncPIR) Recover(i uint64, token string, answer AnswerMsg) string {
	ciphertext := sympir.Pir.Recover(i, sympir.ClSt, answer)
	return sympir.Decrypt(token, ciphertext)
}

func (sympir *SymEncPIR) Run(i uint64, token string) string {
	query := sympir.Query(i, token)
	answer := sympir.Answer(query)
	message := sympir.Recover(i, token, answer)
	return message
}

func main() {
	var index uint64
	index = 0

	pir := &NaivePIR{}
	secparm := Params{20}
	sympir := &SymEncPIR{}

	database := []string{"a","b","c","d"}
	sympir.Init(pir, secparm, EncParams{}, database)
	fmt.Println(sympir.Run(index, ""))
}

