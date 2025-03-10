package main

import (
	"context"
	"fmt"
	"os"
	"os/exec"
	"strings"

	openai "github.com/sashabaranov/go-openai"
)

func generatePatchFile() (string){
	res, err := exec.Command("git", "diff", "HEAD~1", "HEAD").Output()
	if err != nil {
		return ""
	}
	return string(res)
}

func fetchCode() (string){
	res := ">>main.go\n\n"
	output, err := exec.Command("cat", "code/main.go").Output()
	if err != nil {
		return ""
	}
	res += string(output)
	res += "\n\n>>index.html\n\n"
	output, err = exec.Command("cat", "code/index.html").Output()
	if err != nil {
		return ""
	}
	res += string(output)
	return res
}

func main() {
	// Get API key from environment variable
	apiKey := os.Getenv("GEMINI_API_KEY")
	if apiKey == "" {
		fmt.Println("api key environment variable is not set")
		return
	}

	// Create configuration with custom base URL
	config := openai.DefaultConfig(apiKey)
	config.BaseURL = "https://generativelanguage.googleapis.com/v1beta/openai/"

	// Create a new client with config
	client := openai.NewClientWithConfig(config)

	// Create message content with test output
	messageContent := fmt.Sprintf("the following patch was generated by a change to tests by the user. Please generate a matching patch for the actual api code\n\n%s\n\napi code currently:\n\n%s\n\nensure your patch is a valid patch file that can be applied with the patch command", generatePatchFile(), fetchCode())

	fmt.Println("Sending message to AI...")
	// then print it in teal
	fmt.Println("\033[36m", messageContent, "\033[0m")

	// Create a completion request
	resp, err := client.CreateChatCompletion(
		context.Background(),
		openai.ChatCompletionRequest{
			Model: "gemini-2.0-flash",
			Messages: []openai.ChatCompletionMessage{
				{
					Role:    openai.ChatMessageRoleSystem,
					Content: "You are a helpful assistant that analyzes test results and patch files to implement them with no other info.",
				},
				{
					Role:    openai.ChatMessageRoleUser,
					Content: messageContent,
				},
			},
		},
	)

	if err != nil {
		fmt.Printf("Error creating chat completion: %v\n", err)
		return
	}

	// Print the response
	fmt.Println(resp.Choices[0].Message.Content)


	// parse out only the diff code block
	diffCodeBlock := resp.Choices[0].Message.Content
	// remove the first line starting with ```
	diffCodeBlock = strings.Split(diffCodeBlock, "```")[1]
	// remove the first line starting with diff
	lines := strings.Split(diffCodeBlock, "\n")
	for i, line := range lines {
		if strings.HasPrefix(line, "diff") {
			diffCodeBlock = strings.Join(lines[i+1:], "\n")
			break
		}
	}

	fmt.Printf("\033[31mDiff code block: %s\033[0m", diffCodeBlock)
	// remove any trailing newlines
	diffCodeBlock = strings.TrimSuffix(diffCodeBlock, "\n")
	// Save the response to a file
	err = os.WriteFile("code/patch.patch", []byte(diffCodeBlock), 0644)
	if err != nil {
		fmt.Println("Error writing patch file: ", err)
		return
	}
	fmt.Println("Patch file written to patch.patch")
}