package model

type DataClaims struct {
	Keycode string  `json:"keycode"`
	CO2     float32 `json:"CO2"`
	NO2     float32 `json:"NO2"`
	O3      float32 `json:"O3"`
	CH2O    float32 `json:"CH2O"`
	Temp    float32 `json:"Temp"`
	Humd    float32 `json:"Humd"`
}

type Payload struct {
	Msg string `json:"msg"`
}
