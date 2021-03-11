package controllers

import (
	"airmon/model"
	"airmon/services"
	"net/http"

	"github.com/gin-gonic/gin"
)

func LoginHandler(c *gin.Context) {
	var user model.User
	var creds model.User

	if err := c.ShouldBindJSON(&creds); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": http.StatusBadRequest, "message": "Bad request"})
		return
	}

	result := services.Db.Find(&user, "username = ?", creds.Username)

	if result.Error != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"status": http.StatusUnauthorized, "message": "Invalid Credentials"})
		return
	}

	if !services.ComparePasswords(user.Password, []byte(creds.Password)) {
		c.JSON(http.StatusUnauthorized, gin.H{"status": http.StatusUnauthorized, "message": "Invalid Credentials"})
		return
	}

	token := services.GenerateTokenJWT(user)

	if token == "" {
		c.JSON(http.StatusUnauthorized, gin.H{"status": http.StatusUnauthorized, "message": "Invalid Credentials"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"status": http.StatusOK, "message": "Sucessfull authentication", "token": token})
}

func RegisterHandler(c *gin.Context) {

	type AuxInvite struct {
		Username string
		Password string
		Token     string
	}

	var auxUser AuxInvite
	var existUser model.User
	var creds model.Invite

	if err := c.ShouldBindJSON(&auxUser); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": http.StatusBadRequest, "message": "Check syntax!"})
		return
	}

	result := services.Db.Find(&creds, "token = ?", auxUser.Token)

	if result.Error != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"status": http.StatusUnauthorized, "message": "Invalid Credentials"})
		return
	}

	result = services.Db.Find(&existUser, "username = ?", auxUser.Username)

	if result.Error != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"status": http.StatusUnauthorized, "message": "Invalid Credentials"})
		return
	}

	if result.RowsAffected > 0 {
		c.JSON(http.StatusUnauthorized, gin.H{"status": http.StatusUnauthorized, "message": "User already invited"})
		return
	}

	hash := services.HashAndSalt([]byte(auxUser.Password))

	auxUser.Password = hash

	var user model.User

	user.Username= auxUser.Username
	user.Password= auxUser.Password

	services.Db.Save(&user)
	services.Db.Unscoped().Delete(&creds)

	c.JSON(http.StatusCreated, gin.H{"status": http.StatusCreated, "message": "Create successful!", "resourceId": user.Username})
}
