package services

import (
	"airmon/model"
	"net/http"

	"github.com/dgrijalva/jwt-go"
	"github.com/gin-gonic/gin"
)

func AuthorizationRequired() gin.HandlerFunc {

	return func(c *gin.Context) {
		if !ValidateTokenJWT(c) {
			c.JSON(http.StatusUnauthorized, gin.H{"status": http.StatusUnauthorized, "message": "Invalit Token"})
			c.Abort()
		} else {
			var tokenInput, _, _ = GetAuthorizationToken(c)
			token, _ := jwt.ParseWithClaims(tokenInput, &model.Claims{}, func(token *jwt.Token) (interface{}, error) {
				return JwtKey, nil
			})

			if claims, ok := token.Claims.(*model.Claims); ok && token.Valid {
				c.Set("username", claims.Username)
			}

			// before request
			c.Next()
		}
	}
}
