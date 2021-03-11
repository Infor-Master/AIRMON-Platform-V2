package model

import (
	"gorm.io/gorm"
)

type Device struct {
	gorm.Model
	Name string `gorm:"not null"`
	Key  string `gorm:"unique; not null"`
}
