package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
	"path/filepath"
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

	currentDir, err := os.Getwd()
	if err != nil {
		http.Error(w, "Failed to get current directory", http.StatusInternalServerError)
		return
	}

	filePath := filepath.Join(currentDir, req.FilePath)
	content, err := os.ReadFile(filePath)
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

func main() {
	http.HandleFunc("/navigate", navigate)
	http.HandleFunc("/filecontent", fileContent)

	log.Println("Server starting on :5000")
	if err := http.ListenAndServe(":5000", nil); err != nil {
		log.Fatal(err)
	}
}
