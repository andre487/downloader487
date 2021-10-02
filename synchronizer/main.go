package main

import (
	"os"

	"github.com/akamensky/argparse"
)

func main() {
	SetupLogger()

	argParser := argparse.NewParser("synchronizer", "Sync files from S3")

	s3Endpoint := argParser.String("", "s3-endpoint", &argparse.Options{Default: "https://storage.yandexcloud.net"})
	s3Region := argParser.String("", "s3-region", &argparse.Options{Default: "ru-central1"})
	s3Bucket := argParser.String("", "s3-bucket", &argparse.Options{Default: "downloader487-files"})
	s3AccessFile := argParser.String("", "s3-access-file", &argparse.Options{Default: "~/.tokens/s3-access"})
	s3SecretFile := argParser.String("", "s3-secret-file", &argparse.Options{Default: "~/.tokens/s3-secret"})
	downloadDir := argParser.String("", "download-dir", &argparse.Options{Default: "/tmp/downloader487-sync"})
	noClearBucket := argParser.Flag("", "--no-clear-bucket", &argparse.Options{Default: false})

	err := argParser.Parse(os.Args)
	FatalOnErr(err)

	s3Access, err := GetSecretValue("S3_ACCESS_KEY", s3AccessFile)
	FatalOnErr(err)

	s3Secret, err := GetSecretValue("S3_SECRET_KEY", s3SecretFile)
	FatalOnErr(err)

	Logger.Info("Start to download objects")

	dwlErr := DownloadAll(DwlParams{
		S3Endpoint:    *s3Endpoint,
		S3Region:      *s3Region,
		S3Bucket:      *s3Bucket,
		S3Access:      s3Access,
		S3Secret:      s3Secret,
		DownloadDir:   *downloadDir,
		NoClearBucket: *noClearBucket,
	})
	FatalOnErr(dwlErr)
}
