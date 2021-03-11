package controllers

import (
	"airmon/model"
	"airmon/services"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
)

func AddDevice(c *gin.Context) {
	var device model.Device

	if err := c.ShouldBindJSON(&device); err != nil {
		log.Println(err)
		c.JSON(http.StatusBadRequest, gin.H{"status": http.StatusBadRequest, "message": "Invalid structure"})
		return
	}

	result := services.Db.Create(&device)
	if result.Error != nil {
		log.Println(result.Error)
		c.JSON(http.StatusConflict, gin.H{"status": http.StatusConflict, "message": "Device already exists"})
		return
	}

	c.JSON(http.StatusCreated, gin.H{"status": http.StatusCreated, "message": "Device created sucessfully"})
}

func UpdateDevice(c *gin.Context) {
	var device model.Device
	var auxdevice model.Device

	if err := c.ShouldBindJSON(&device); err != nil {
		log.Println(err)
		c.JSON(http.StatusBadRequest, gin.H{"status": http.StatusBadRequest, "message": "Invalid structure"})
		return
	}

	result := services.Db.First(&auxdevice, "id = ?", device.ID)
	if result.Error != nil {
		log.Println(result.Error)
		c.JSON(http.StatusNotFound, gin.H{"status": http.StatusNotFound, "message": "Device not found"})
		return
	}

	auxdevice.Name = device.Name
	auxdevice.Key = device.Key

	services.Db.Save(&auxdevice)

	c.JSON(http.StatusOK, gin.H{"status": http.StatusOK, "message": "Device updated sucessfully"})
}

func DeleteDevice(c *gin.Context) {
	var device model.Device

	if err := c.ShouldBindJSON(&device); err != nil {
		log.Println(err)
		c.JSON(http.StatusBadRequest, gin.H{"status": http.StatusBadRequest, "message": "Invalid structure"})
		return
	}

	services.Db.Unscoped().Delete(&device)

	c.JSON(http.StatusOK, gin.H{"status": http.StatusOK, "message": "Device deleted sucessfully"})
}

func GetDevices(c *gin.Context) {
	var devices []model.Device

	services.Db.Find(&devices)

	c.JSON(http.StatusOK, gin.H{"status": http.StatusOK, "data": devices})
}

func GetDevice(c *gin.Context) {
	var device model.Device

	id := c.Param("id")
	result := services.Db.First(&device, "id = ?", id)
	if result.Error != nil {
		log.Println(result.Error)
		c.JSON(http.StatusNotFound, gin.H{"status": http.StatusNotFound, "message": "Device not found"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"status": http.StatusOK, "data": device})
}
