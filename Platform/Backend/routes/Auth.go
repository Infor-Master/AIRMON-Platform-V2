package routes

import (
	"airmon/controllers"

	"github.com/gin-gonic/gin"
)

func GenerateToken(c *gin.Context) {
	controllers.LoginHandler(c)
}

func Register(c *gin.Context) {
	controllers.RegisterHandler(c)
}
