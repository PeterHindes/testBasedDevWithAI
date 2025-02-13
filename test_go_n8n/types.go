package go_n8n


type CommandRequest struct {
	Command string `json:"command"`
}

type CommandResponse struct {
	Stdout   string `json:"stdout"`
	Stderr   string `json:"stderr"`
	ExitCode int    `json:"exit_code"`
	Pwd      string `json:"pwd"`
}