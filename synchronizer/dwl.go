package main

import (
	"os"
	"path/filepath"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
	"github.com/aws/aws-sdk-go/service/s3/s3manager"
)

type DwlParams struct {
	S3Endpoint  string
	S3Region    string
	S3Bucket    string
	S3Access    string
	S3Secret    string
	DownloadDir string
}

func DownloadAll(params DwlParams) error {
	s3Session := session.Must(session.NewSession(&aws.Config{
		Endpoint:    aws.String(params.S3Endpoint),
		Region:      aws.String(params.S3Region),
		Credentials: credentials.NewStaticCredentials(params.S3Access, params.S3Secret, ""),
	}))
	client := s3.New(s3Session)

	result, err := client.ListObjects(&s3.ListObjectsInput{
		Bucket: aws.String(params.S3Bucket),
	})
	if err != nil {
		return err
	}

	Logger.Info("Got", len(result.Contents), "objects")
	downloader := s3manager.NewDownloader(s3Session)

	for _, x := range result.Contents {
		destPath := filepath.Join(params.DownloadDir, *x.Key)
		destDir := filepath.Dir(destPath)
		Logger.Info("Download start:", destPath)

		if err := ensureDir(destDir); err != nil {
			return err
		}

		f, err := os.Create(destPath)
		if err != nil {
			return err
		}

		n, err := downloader.Download(f, &s3.GetObjectInput{
			Bucket: aws.String(params.S3Bucket),
			Key:    aws.String(*x.Key),
		})
		if err != nil {
			return err
		}

		Logger.Info("Download finished:", destPath)
		Logger.Debug("Downloaded", n, "bytes")
	}

	return nil
}

func doesFileExist(filePath string) (bool, error) {
	_, err := os.Stat(filePath)
	if err == nil {
		return true, nil
	}

	if os.IsNotExist(err) {
		return false, nil
	}

	return false, err
}

func ensureDir(dir string) error {
	ok, err := doesFileExist(dir)
	if err != nil {
		return err
	}
	if ok {
		return nil
	}

	Logger.Debug("Create directory", dir)
	mkdirErr := os.MkdirAll(dir, os.ModePerm)
	if mkdirErr != nil {
		return mkdirErr
	}

	return nil
}
