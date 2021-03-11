package model

import (
	"gorm.io/gorm"
)

type Invite struct {
	gorm.Model
	Username string `gorm:"unique;not null"`
	Token     string `gorm:"not null"`
}