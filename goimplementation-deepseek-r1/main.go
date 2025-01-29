// main.go
package main

import (
	"database/sql"
	"fmt"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	_ "modernc.org/sqlite"
)

type Task struct {
	ID             string    `json:"id"`
	Name           string    `json:"name"`
	StartDate      time.Time `json:"start_date"`
	DueDate        time.Time `json:"due_date"`
	Priority       int       `json:"priority"`
	Status         string    `json:"status"`
	CreatedAt      time.Time `json:"created_at"`
	CompletedAt    *time.Time `json:"completed_at,omitempty"`
}

type AnalyticsResponse struct {
	DaysUntilDue        int     `json:"days_until_due"`
	CompletionHealth    string  `json:"completion_health"`
	PercentageComplete  float64 `json:"percentage_complete"`
	TimeToCompleteHours *float64 `json:"time_to_complete_hours,omitempty"`
}

type SystemStats struct {
	AvgCompletionHours *float64         `json:"avg_completion_hours"`
	CompletionRate     float64          `json:"completion_rate"`
	TasksByPriority    map[int]int      `json:"tasks_by_priority"`
}

var db *sql.DB

func main() {
	var err error
	db, err = sql.Open("sqlite", "./tasks.db")
	if err != nil {
		panic(err)
	}
	defer db.Close()

	createTable()

	r := gin.Default()

	r.POST("/tasks", createTask)
	r.GET("/tasks", listTasks)
	r.PUT("/tasks/:id/complete", completeTask)
	r.GET("/tasks/:id/analytics", getAnalytics)
	r.GET("/analytics", getSystemAnalytics)
	r.DELETE("/tasks/old", deleteOldTasks)

	r.Run(":8000")
}

func createTable() {
	query := `
	CREATE TABLE IF NOT EXISTS tasks (
		id TEXT PRIMARY KEY,
		name TEXT NOT NULL,
		start_date DATETIME NOT NULL,
		due_date DATETIME NOT NULL,
		priority INTEGER NOT NULL,
		status TEXT NOT NULL DEFAULT 'pending',
		created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
		completed_at DATETIME
	)`
	
	if _, err := db.Exec(query); err != nil {
		panic(err)
	}
}

// Handlers
func createTask(c *gin.Context) {
	var task struct {
		Name      string    `json:"name" binding:"required,min=3,max=50"`
		StartDate time.Time `json:"start_date" binding:"required"`
		DueDate   time.Time `json:"due_date" binding:"required"`
		Priority  int       `json:"priority" binding:"required,min=1,max=5"`
	}

	if err := c.ShouldBindJSON(&task); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if task.DueDate.Before(task.StartDate) {
		c.JSON(http.StatusBadRequest, gin.H{"error": "due_date must be after start_date"})
		return
	}

	if task.DueDate.Before(time.Now()) {
		c.JSON(http.StatusBadRequest, gin.H{"error": "due_date must be in the future"})
		return
	}

	id := generateUUID()
	_, err := db.Exec(`INSERT INTO tasks 
		(id, name, start_date, due_date, priority, status) 
		VALUES (?, ?, ?, ?, ?, 'pending')`,
		id, task.Name, task.StartDate, task.DueDate, task.Priority)

	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, gin.H{"id": id})
}

func listTasks(c *gin.Context) {
	rows, err := db.Query(`SELECT 
		id, name, start_date, due_date, priority, status, created_at, completed_at 
		FROM tasks`)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	defer rows.Close()

	tasks := []Task{}
	for rows.Next() {
		var task Task
		rows.Scan(&task.ID, &task.Name, &task.StartDate, &task.DueDate, &task.Priority, &task.Status, &task.CreatedAt, &task.CompletedAt)
		tasks = append(tasks, task)
	}

	c.JSON(http.StatusOK, gin.H{"tasks": tasks})
}

func completeTask(c *gin.Context) {
	id := c.Param("id")
	result, err := db.Exec(`UPDATE tasks 
		SET status = 'completed', completed_at = CURRENT_TIMESTAMP 
		WHERE id = ?`, id)
	
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	rowsAffected, _ := result.RowsAffected()
	if rowsAffected == 0 {
		c.JSON(http.StatusNotFound, gin.H{"error": "task not found"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"status": "completed"})
}

func getAnalytics(c *gin.Context) {
	var task Task
	id := c.Param("id")
	row := db.QueryRow(`SELECT 
		start_date, due_date, status, completed_at 
		FROM tasks WHERE id = ?`, id)

	err := row.Scan(&task.StartDate, &task.DueDate, &task.Status, &task.CompletedAt)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "task not found"})
		return
	}

	response := AnalyticsResponse{
		DaysUntilDue: int(task.DueDate.Sub(time.Now()).Hours() / 24),
	}

	// Calculate completion health
	if response.DaysUntilDue > 7 {
		response.CompletionHealth = "good"
	} else if response.DaysUntilDue >= 3 {
		response.CompletionHealth = "okay"
	} else {
		response.CompletionHealth = "critical"
	}

	// Calculate percentage complete
	if task.Status == "completed" {
		response.PercentageComplete = 100.0
	} else {
		total := task.DueDate.Sub(task.StartDate).Seconds()
		elapsed := time.Now().Sub(task.StartDate).Seconds()
		if total > 0 {
			response.PercentageComplete = (elapsed / total) * 100
			if response.PercentageComplete > 100 {
				response.PercentageComplete = 100
			}
		}
	}

	// Calculate time to complete
	if task.CompletedAt != nil {
		hours := task.CompletedAt.Sub(task.StartDate).Hours()
		response.TimeToCompleteHours = &hours
	}

	c.JSON(http.StatusOK, response)
}

func getSystemAnalytics(c *gin.Context) {
	stats := SystemStats{
		TasksByPriority: make(map[int]int),
	}

	// Calculate completion rate
	var total, completed int
	row := db.QueryRow(`SELECT 
		COUNT(*) as total,
		SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed 
		FROM tasks`)
	row.Scan(&total, &completed)

	if total > 0 {
		stats.CompletionRate = (float64(completed) / float64(total)) * 100
	}

	// Calculate average completion time
	var avgHours *float64
	row = db.QueryRow(`SELECT 
		AVG((julianday(completed_at) - julianday(start_date)) * 24) 
		FROM tasks WHERE status = 'completed'`)
	row.Scan(&avgHours)
	stats.AvgCompletionHours = avgHours

	// Get priority distribution
	rows, _ := db.Query(`SELECT priority, COUNT(*) 
		FROM tasks GROUP BY priority`)
	defer rows.Close()
	
	for rows.Next() {
		var p, count int
		rows.Scan(&p, &count)
		stats.TasksByPriority[p] = count
	}

	c.JSON(http.StatusOK, gin.H{"system_stats": stats})
}

func deleteOldTasks(c *gin.Context) {
	if c.Query("confirm") != "true" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "confirm parameter required"})
		return
	}

	result, err := db.Exec(`DELETE FROM tasks 
		WHERE status = 'completed' 
		AND completed_at < datetime('now', '-30 days')`)
	
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	count, _ := result.RowsAffected()
	c.JSON(http.StatusAccepted, gin.H{"deleted": count})
}

func generateUUID() string {
	// Implement proper UUID generation
	return fmt.Sprintf("%d", time.Now().UnixNano())
}