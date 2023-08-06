package main

import (
	"C"
	"encoding/json"
	"github.com/pingcap/tidb/parser"
	_ "github.com/pingcap/tidb/parser/test_driver"
)
//export splitMySQL
func splitMySQL(statementC *C.char) *C.char {
	ret := ""

	p := parser.New()
	stmtNodes, _, err := p.Parse(
		C.GoString(statementC),
		"", "")
	if err != nil {
		ret = err.Error()
	} else {
		var mapStatement []string
		for i := 0; i < len(stmtNodes); i++ {
			mapStatement = append(mapStatement, stmtNodes[i].Text())
		}
		mapByte, _ := json.Marshal(mapStatement)
		ret = string(mapByte)
	}
	return C.CString(ret)
}

func main() {}
