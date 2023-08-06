#!/bin/bash
go build -buildmode=c-shared -o _parser4mysql_$(python -c "import platform;print(platform.system())").so parser4mysql.go

