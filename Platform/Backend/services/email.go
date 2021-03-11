package services

import (
	"bytes"
	"fmt"
	"html/template"
	"log"
	"net/smtp"
	"os"
)

func SendInvite(emailTo string, token string) {

	to := []string{emailTo}
	from := os.Getenv("EMAIL_USER")
	password := os.Getenv("EMAIL_PASS")
	smtpHost := os.Getenv("SMTP_HOST")
	smtpPort := os.Getenv("SMTP_PORT")

	auth := smtp.PlainAuth("", from, password, smtpHost)

	t, _ := template.ParseFiles("invite3.html")

	var body bytes.Buffer

	headers := "MIME-version: 1.0;\nContent-Type: text/html;"
	body.Write([]byte(fmt.Sprintf("Subject: Invite to AIRMON platform \n%s\n\n", headers)))

	t.Execute(&body, struct {
		//Email string
		//Token string
		//Link  string
	}{
		//Email: emailTo,
		//Token: token,
		//Link:  os.Getenv("ADDRESS"),
	})

	err := smtp.SendMail(smtpHost+":"+smtpPort, auth, from, to, body.Bytes())
	if err != nil {
		log.Println(err)
		return
	}
}
