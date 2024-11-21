FROM golang:1.22.0

WORKDIR /backend

COPY go.mod ./
COPY go.sum ./

RUN go mod download -x

ADD . .

# RUN go install github.com/swaggo/swag/cmd/swag@latest
# RUN export PATH=$(go env GOPATH)/bin:$PATH
# RUN swag init -g src/app/main.go

RUN cd cmd && go build -buildvcs=false -o /main

CMD ["/main"]