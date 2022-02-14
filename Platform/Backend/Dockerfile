FROM golang:latest

RUN set -eux; \
	export GOROOT="$(go env GOROOT)";

RUN apk update && \
    apk upgrade && \
    apk add --no-cache bash git

RUN go get -u github.com/gin-gonic/gin
RUN go get -u gorm.io/gorm
RUN go get -u gorm.io/driver/postgres
RUN go get -u github.com/dgrijalva/jwt-go
# HOT RELOAD
RUN go get -u github.com/githubnemo/CompileDaemon

# Set the Current Working Directory inside the container
WORKDIR /go/src/airmon

# Copy everything from the current directory to the Working Directory inside the container
COPY . .

# Build the Go app
RUN go build -o main .

# Expose port 8081 to the outside world
EXPOSE 8081

# Run the executable DEPLOYMENT
# CMD ./main

# HOT RELOAD
ENTRYPOINT CompileDaemon -log-prefix=false -build="go build ./main.go" -command="./main"