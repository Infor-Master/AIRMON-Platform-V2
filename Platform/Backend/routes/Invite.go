package routes

import (
	"airmon/controllers"

	"github.com/gin-gonic/gin"
)

func AddInvite(c *gin.Context) {
	controllers.AddInvite(c)
}

func DeleteInvite(c *gin.Context) {
	controllers.DeleteInvite(c)
}

func GetInvites(c *gin.Context) {
	controllers.GetInvites(c)
}