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

	
	// // Test 'navigate' function
	// targetDir := "/home/user"
	// navigateRequest := NavigateRequest{Directory: targetDir}
	// navigateBody, _ := json.Marshal(navigateRequest)
	// navigateResp, err := http.Post(baseURL+"/navigate", "application/json", bytes.NewBuffer(navigateBody))
	// if err != nil {
	// 	t.Fatalf("Failed to send 'navigate' request: %v", err)
	// }
	// defer navigateResp.Body.Close()

	// // Check if we got a server error
	// if navigateResp.StatusCode != http.StatusOK {
	// 	t.Fatalf("Failed to navigate to directory: %s", navigateResp.Status)
	// }

	// var navigateResponse NavigateResponse
	// if err := json.NewDecoder(navigateResp.Body).Decode(&navigateResponse); err != nil {
	// 	t.Fatalf("Failed to decode 'navigate' response: %v", err)
	// }

	// // Test 'filecontent' function
	// fileContentRequest := FileContentRequest{FilePath: "/proc/version"}
	// fileContentBody, _ := json.Marshal(fileContentRequest)
	// fileContentResp, err := http.Post(baseURL+"/filecontent", "application/json", bytes.NewBuffer(fileContentBody))
	// if err != nil {
	// 	t.Fatalf("Failed to send 'filecontent' request: %v", err)
	// }
	// defer fileContentResp.Body.Close()

	// // Check if we got a server error
	// if fileContentResp.StatusCode != http.StatusOK {
	// 	t.Fatalf("Failed to get file content: %s", fileContentResp.Status)
	// }

	// var fileContentResponse FileContentResponse
	// if err := json.NewDecoder(fileContentResp.Body).Decode(&fileContentResponse); err != nil {
	// 	t.Fatalf("Failed to decode 'filecontent' response: %v", err)
	// }

	// fmt.Println("File Content:", fileContentResponse.Content)

	// Test 'find' function
	findRequest := FindRequest{Arguments: []string{"-name", "*.go"}}
	findBody, _ := json.Marshal(findRequest)
	findResp, err := http.Post(baseURL+"/find", "application/json", bytes.NewBuffer(findBody))
	if err != nil {
		t.Fatalf("Failed to send 'find' request: %v", err)
	}
	defer findResp.Body.Close()

	// Check if we got a server error
	if findResp.StatusCode != http.StatusOK {
		body := make([]byte, 1024)
		n, _ := findResp.Body.Read(body)
		t.Fatalf("Failed to find files: %s ; %s", findResp.Status, string(body[:n]))
	}

	var findResponse FindResponse
	if err := json.NewDecoder(findResp.Body).Decode(&findResponse); err != nil {
		t.Fatalf("Failed to decode 'find' response: %v", err)
	}

	fmt.Println("Find Response:", findResponse.Files)

}
