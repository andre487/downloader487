package main

import (
	"io/ioutil"
	"log"
	"os"
	"strings"

	"github.com/loynoir/ExpandUser.go"
)

func GetSecretValue(envVar string, filePath *string) (string, error) {
	envVal := os.Getenv(envVar)
	if len(envVal) > 0 {
		return envVal, nil
	}

	fullFilePath, err := ExpandUser.ExpandUser(*filePath)
	if err != nil {
		return "", err
	}

	b, err := ioutil.ReadFile(fullFilePath)
	if err != nil {
		return "", err
	}

	Logger.Debug("Got secret", envVar)
	return strings.TrimSpace(string(b)), nil
}

func FatalOnErr(err error) {
	if err != nil {
		log.Fatal(err)
	}
}
