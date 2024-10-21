package main

                       import (
                           "fmt"
                           "log"
                           "net/http"

                           "github.com/gorilla/mux"
                       )

                       // RouteHandler handles incoming HTTP requests.
                       func routeHandler(w http.ResponseWriter, r *http.Request) {
                           // Get the user's IP address from the request.
                           ip := r.RemoteAddr

                           // Set the response content type to text/html.
                           w.Header().Set("Content-Type", "text/html")

                           // Write the response HTML.
                           html := fmt.Sprintf(`
                               <html>
                                   <body>
                                       <h1>Welcome!</h1>
                                       <p>Your IP address is: %s</p>
                                       <style>
                                           body {
                                               background-color: #f2f2f2;
                                               font-family: Arial, sans-serif;
                                           }
                                           h1 {
                                               color: #00698f;
                                           }
                                           p {
                                               color: #333333;
                                           }
                                       </style>
                                   </body>
                               </html>`, ip)

                           w.Write([]byte(html))
                       }

                       func main() {
                           // Create a new HTTP router.
                           router := mux.NewRouter()

                           // Define the route for handling incoming requests.
                           router.HandleFunc("/ip", routeHandler).Methods("GET")

                           // Start the server on port 8080.
                           fmt.Println("Server is running on port 8080")
                           log.Fatal(http.ListenAndServe(":8080", router))
                       }