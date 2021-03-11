package routes

import (
	"airmon/controllers"

	"github.com/gin-gonic/gin"
)

func AddDevice(c *gin.Context) {
	controllers.AddDevice(c)
}

func UpdateDevice(c *gin.Context) {
	controllers.UpdateDevice(c)
}

func DeleteDevice(c *gin.Context) {
	controllers.DeleteDevice(c)
}

func GetDevices(c *gin.Context) {
	controllers.GetDevices(c)
}

func GetDevice(c *gin.Context) {
	controllers.GetDevice(c)
}
