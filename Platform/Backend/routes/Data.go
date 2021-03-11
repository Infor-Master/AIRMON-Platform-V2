package routes

import (
	"airmon/controllers"

	"github.com/gin-gonic/gin"
)

func AddData(c *gin.Context) {
	controllers.AddData(c)
}

func GetData(c *gin.Context) {
	controllers.GetData(c)
}

func Parse(c *gin.Context) {
	controllers.Parse(c)
}
