package main

import (
	"encoding/json"
	"fmt"
	_ "io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/exec"
	_ "path/filepath"
	_ "sync"
)

type NavigateRequest struct {
	Directory string `json:"directory"`
}

type NavigateResponse struct {
	CurrentDir string   `json:"current_dir"`
	Files      string   `json:"files"`
}

type FileContentRequest struct {
	FilePath string `json:"file_path"`
}

type FileContentResponse struct {
	Content string `json:"content"`
}

type FindRequest struct {
	Arguments []string `json:"arguments"`
}

type FindResponse struct {
	Files string `json:"files"`
}

func navigate(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req NavigateRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	os.Chdir(req.Directory)

	dirs, err := os.ReadDir(".")
	if err != nil {
		http.Error(w, "Failed to read directory", http.StatusInternalServerError)
		return
	}

	dirsAsString := ""
	for _, dir := range dirs {
		dirsAsString += dir.Name() + "\n"
	}

	currentDir, err := os.Getwd()
	if err != nil {
		http.Error(w, "Failed to get current directory", http.StatusInternalServerError)
		return
	}

	response := NavigateResponse{
		CurrentDir: currentDir,
		Files:      dirsAsString,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func fileContent(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req FileContentRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	content, err := os.ReadFile(req.FilePath)
	if err != nil {
		http.Error(w, "Failed to read file", http.StatusInternalServerError)
		return
	}


	response := FileContentResponse{
		Content: string(content),
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

// this method will use the find command and alow the user to pass all the arguments to it
func find(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		fmt.Println("Method not allowed")
		return
	}

	// print out the whole request
	bodyBytes, err := ioutil.ReadAll(r.Body)
	if err != nil {
		fmt.Printf("Error reading body: %v\n", err)
	} else {
		fmt.Printf("Received task: %s\n", string(bodyBytes))
	}

	var req FindRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		fmt.Println("Invalid request body: ", err)
		return
	}

	pwd, err := os.Getwd()
	if err != nil {
		http.Error(w, "Failed to get current directory", http.StatusInternalServerError)
		fmt.Println("Failed to get current directory")
		return
	}
	// cmd := exec.Command("find", pwd, req.Arguments[0], req.Arguments[1])
	cmd := exec.Command("find", append([]string{pwd}, req.Arguments...)...)
	// cmd := exec.Command("find", "--version")
	out, err := cmd.CombinedOutput()
	if err != nil {
		http.Error(w, "Failed to execute command", http.StatusBadRequest)
		fmt.Println("Failed to execute command")
		return
	}

	fmt.Printf("Command input: %s\n", cmd.String())
	fmt.Printf("Command output: %s\n", out)

	response := FindResponse{
		Files: string(out),
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func main() {
	http.HandleFunc("/navigate", navigate)
	http.HandleFunc("/filecontent", fileContent)
	http.HandleFunc("/find", find)

	log.Println("Server starting on :5000")
	if err := http.ListenAndServe(":5000", nil); err != nil {
		log.Fatal(err)
	}
}
