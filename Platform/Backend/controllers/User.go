package controllers

import (
	"airmon/model"
	"airmon/services"
	"net/http"
	"github.com/gin-gonic/gin"
)

func DeleteUser(c *gin.Context) {
	var user model.User

	if err := c.ShouldBindJSON(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": http.StatusBadRequest, "message": "Invalid structure"})
		return
	}

	services.Db.Unscoped().Delete(&user)

	c.JSON(http.StatusOK, gin.H{"status": http.StatusOK, "message": "User deleted sucessfully"})
}

func GetUsers(c *gin.Context) {
	var users []model.User

	services.Db.Find(&users)

	c.JSON(http.StatusOK, gin.H{"status": http.StatusOK, "data": users})
}