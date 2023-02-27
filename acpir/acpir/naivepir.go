package main

// import "fmt"
import "strconv"

type NaivePIR struct{}

func (pi* NaivePIR) Name() string  {
	return "Naive PIR"
}

func (pi* NaivePIR) Setup(p Params, dataentries []string)  (ClientState, ServerState, *Database) {
	clst := ClientState{}
	svst := ServerState{}
	db := &Database{dataentries}
	return clst, svst, db
}

func (pi* NaivePIR) Query(i uint64, clstate ClientState) (ClientState, QueryMsg) {
	querymsg := make(map[string]string)
	querymsg["index"] = strconv.Itoa(int(i))
	query := QueryMsg{querymsg}
	return clstate, query
}

func (pi* NaivePIR) Answer(DB *Database, query QueryMsg, server ServerState) AnswerMsg {
	index, _ := strconv.Atoi(query.Msg["index"])
	answer := DB.DB[index]
	answermsg := make(map[string]string)
	answermsg["answer"] = answer
	response := AnswerMsg{answermsg}

	return response
}

func (pi* NaivePIR) Recover(i uint64, clstate ClientState, answer AnswerMsg) string {
	return answer.Msg["answer"]
}

func (pi* NaivePIR) EncryptDB(database *Database, enckeys EncParams) *Database{
	// TODO: Change
	return database
}

// func main()  {
// 	var index uint64
// 	index = 3

// 	test := &NaivePIR{}
// 	secparm := Params{20}
// 	temp1, temp2 := test.Setup(secparm)
// 	database := Database{[]string{"a","b","c","fuck you"}}
// 	_, q := test.Query(index, temp1)
// 	response := test.Answer(&database, q, temp2)
// 	fmt.Println(test.Name(), test.Recover(3, temp1, response))
// }