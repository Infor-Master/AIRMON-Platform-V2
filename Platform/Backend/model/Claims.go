package model

import (
	"github.com/dgrijalva/jwt-go"
)

// Create a struct that will be encoded to a JWT.
// We add jwt.StandardClaims as an embedded type, to provide fields like expiry time
type Claims struct {
	Username           string `json:"username"`
	Name               string `json:"name"`
	Admin              bool   `json:"admin"`
	Id                 uint   `json:"id"`
	jwt.StandardClaims `swaggerignore:"true"`
}
