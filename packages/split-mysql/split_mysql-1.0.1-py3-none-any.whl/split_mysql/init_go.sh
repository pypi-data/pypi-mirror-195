#!/bin/bash
go mod init split-mysql
go mod edit -require github.com/pingcap/tidb/parser@master
go mod tidy
