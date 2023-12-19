package main

import (
        "log"
        "net/http"
)

func main() {
        file := http.FileServer(http.Dir("public"))
        http.Handle("/static/", http.StripPrefix("/static/", file))
        err := http.ListenAndServe(":5999", nil)
        if err != nil {
                log.Println(err)
        }
}
