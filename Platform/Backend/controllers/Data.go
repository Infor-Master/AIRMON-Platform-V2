package controllers

import (
	"airmon/model"
	"airmon/services"
	b64 "encoding/base64"
	"encoding/json"
	"log"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

func Parse(c *gin.Context) {
	var payload model.Payload
	var device model.Device
	var data model.Data
	var dataclaims model.DataClaims

	if err := c.ShouldBindJSON(&payload); err != nil {
		log.Println(err)
		c.JSON(http.StatusBadRequest, gin.H{"status": http.StatusBadRequest, "message": "Invalid structure"})
		return
	}

	payload_decoded, _ := b64.StdEncoding.DecodeString(payload.Msg)

	json.Unmarshal([]byte(payload_decoded), &dataclaims)

	log.Println(dataclaims)

	result := services.Db.First(&device, "key = ?", dataclaims.Keycode)
	if result.Error != nil {
		log.Println(result.Error)
		c.JSON(http.StatusNotFound, gin.H{"status": http.StatusNotFound, "message": "Device not found"})
		return
	}

	data.Device_ID = device.ID
	data.CO2_PPM = dataclaims.CO2
	data.O3_PPM = dataclaims.O3
	data.NO2_PPM = dataclaims.NO2
	data.CH2O_PPM = dataclaims.CH2O
	data.Temp_C = dataclaims.Temp
	data.Hum_100 = dataclaims.Humd

	services.Db.Create(&data)
	c.JSON(http.StatusCreated, gin.H{"status": http.StatusCreated, "message": "data created sucessfully"})
}

func AddData(c *gin.Context) {
	var data model.Data

	if err := c.ShouldBindJSON(&data); err != nil {
		log.Println(err)
		c.JSON(http.StatusBadRequest, gin.H{"status": http.StatusBadRequest, "message": "Invalid structure"})
		return
	}

	services.Db.Create(&data)
	c.JSON(http.StatusCreated, gin.H{"status": http.StatusCreated, "message": "data created sucessfully"})
}

func GetData(c *gin.Context) {
	var data []model.Data

	id := c.Param("id")
	limit, err := strconv.Atoi(c.Param("limit"))

	if err != nil {
		log.Println(err)
		c.JSON(http.StatusBadRequest, gin.H{"status": http.StatusBadRequest, "message": "Invalid request"})
		return
	}

	offset, err := strconv.Atoi(c.Param("offset"))

	if err != nil {
		log.Println(err)
		c.JSON(http.StatusBadRequest, gin.H{"status": http.StatusBadRequest, "message": "Invalid request"})
		return
	}

	services.Db.Order("created_at desc").Where("device_id = ?", id).Limit(limit).Offset(limit * offset).Find(&data)

	c.JSON(http.StatusOK, gin.H{"status": http.StatusOK, "data": data})
}
