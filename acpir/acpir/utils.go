package main

type Params struct{
	SecParm uint64
}

type ClientState struct{}

type ServerState struct{}

type QueryMsg struct{
	Msg map[string]string
}

type AnswerMsg struct{
	Msg map[string]string
}

type Database struct{
	DB []string
}

type EncParams struct{}