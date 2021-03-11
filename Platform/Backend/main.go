package main

import (
	"airmon/model"
	"airmon/routes"
	"airmon/services"

	"github.com/gin-gonic/gin"
)

func init() {
	services.OpenDatabase()
	services.Db.AutoMigrate(&model.Device{})
	services.Db.AutoMigrate(&model.Data{})
	services.Db.AutoMigrate(&model.User{})
	services.Db.AutoMigrate(&model.Invite{})

	var admin model.User
	admin.Username = "Admin"
	admin.Name = "Test Admin Account"
	admin.Password = services.HashAndSalt([]byte("admin123"))
	admin.Admin = true
	services.Db.Create(&admin)
}

func main() {

	router := gin.New()
	router.Use(gin.Logger())
	router.Use(gin.Recovery())

	router.NoRoute(func(c *gin.Context) {
		c.JSON(404, gin.H{"code": "PAGE_NOT_FOUND", "message": "Page not found"})
	})

	user := router.Group("/api/user")
	user.Use(services.AuthorizationRequired())
	{
		user.DELETE("/", routes.DeleteUser)
		user.GET("/", routes.GetUsers)
	}

	invite := router.Group("/api/invite")
	invite.Use(services.AuthorizationRequired())
	{
		invite.POST("/", routes.AddInvite)
		invite.DELETE("/", routes.DeleteInvite)
		invite.GET("/", routes.GetInvites)
	}

	device := router.Group("/api/device")
	device.Use(services.AuthorizationRequired())
	{
		device.POST("/", routes.AddDevice)
		device.PUT("/", routes.UpdateDevice)
		device.DELETE("/", routes.DeleteDevice)
		device.GET("/", routes.GetDevices)
		device.GET("/:id", routes.GetDevice)
	}

	data := router.Group("/api/data")
	data.Use(services.AuthorizationRequired())
	{
		data.POST("/", routes.AddData)
		data.GET("/:id/:limit/:offset", routes.GetData)
	}

	auth := router.Group("/api")
	{
		auth.POST("/login", routes.GenerateToken)
		auth.POST("/register", routes.Register)
		auth.POST("/parse", routes.Parse)
	}

	router.Run(":8081")
}
