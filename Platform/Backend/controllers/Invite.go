package controllers

import (
	"airmon/model"
	"airmon/services"
	"net/http"

	"github.com/gin-gonic/gin"
)

func AddInvite(c *gin.Context) {
	var invite model.Invite

	type Aux struct {
		Username string
	}

	var aux Aux

	if err := c.ShouldBindJSON(&aux); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": http.StatusBadRequest, "message": "Invalid structure"})
		return
	}

	invite.Token = services.HashAndSalt([]byte(aux.Username))
	invite.Username = aux.Username

	result := services.Db.Create(&invite)

	if result.Error != nil {
		c.JSON(http.StatusConflict, gin.H{"status": http.StatusConflict, "message": "Invite already exists"})
		return
	}

	c.JSON(http.StatusCreated, gin.H{"status": http.StatusCreated, "message": "Invite created sucessfully"})

	//services.SendInvite(invite.Username, invite.Token)
}

func DeleteInvite(c *gin.Context) {
	var invite model.Invite

	if err := c.ShouldBindJSON(&invite); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": http.StatusBadRequest, "message": "Invalid structure"})
		return
	}

	services.Db.Unscoped().Delete(&invite)

	c.JSON(http.StatusOK, gin.H{"status": http.StatusOK, "message": "Device deleted sucessfully"})
}

func GetInvites(c *gin.Context) {
	var invites []model.Invite

	services.Db.Find(&invites)

	c.JSON(http.StatusOK, gin.H{"status": http.StatusOK, "data": invites})
}
