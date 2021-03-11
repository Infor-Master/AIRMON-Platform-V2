package routes

import (
	"airmon/controllers"

	"github.com/gin-gonic/gin"
)

func DeleteUser(c *gin.Context) {
	controllers.DeleteUser(c)
}

func GetUsers(c *gin.Context) {
	controllers.GetUsers(c)
}