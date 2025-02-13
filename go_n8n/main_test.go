package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"testing"
)

func TestNavigateAndFileContent(t *testing.T) {
	baseURL := "http://localhost:5000"

	targetDir := "../.vscode"

	// Test 'navigate' function
	navigateRequest := NavigateRequest{Directory: targetDir}
	navigateBody, _ := json.Marshal(navigateRequest)
	navigateResp, err := http.Post(baseURL+"/navigate", "application/json", bytes.NewBuffer(navigateBody))
	if err != nil {
		t.Fatalf("Failed to send 'navigate' request: %v", err)
	}
	defer navigateResp.Body.Close()

	var navigateResponse NavigateResponse
	if err := json.NewDecoder(navigateResp.Body).Decode(&navigateResponse); err != nil {
		t.Fatalf("Failed to decode 'navigate' response: %v", err)
	}

	// if navigateResponse.CurrentDir != targetDir {
	// 	t.Fatalf("Failed to navigate to directory: %s got to %s", targetDir, navigateResponse.CurrentDir)
	// }

	// Test 'filecontent' function
	fileContentRequest := FileContentRequest{FilePath: "settings.json"}
	fileContentBody, _ := json.Marshal(fileContentRequest)
	fileContentResp, err := http.Post(baseURL+"/filecontent", "application/json", bytes.NewBuffer(fileContentBody))
	if err != nil {
		t.Fatalf("Failed to send 'filecontent' request: %v", err)
	}
	defer fileContentResp.Body.Close()

	var fileContentResponse FileContentResponse
	if err := json.NewDecoder(fileContentResp.Body).Decode(&fileContentResponse); err != nil {
		t.Fatalf("Failed to decode 'filecontent' response: %v", err)
	}

	fmt.Println("File Content:", fileContentResponse.Content)
}
