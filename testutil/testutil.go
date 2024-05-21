package testutil

import (
	"flag"
	"fmt"
	"os"
	"path"
	"runtime"
	"strings"
)

var _, filename, _, _ = runtime.Caller(0)

var output_path = path.Join(path.Dir(filename), "../../hotel_reservation/util/output.csv")
var Output = flag.String("output", output_path, "Location to put output CSV")

func WriteTestResults(service string, req any, res any) {
	input := fmt.Sprintf("%v", req)
	output := fmt.Sprintf("%v", res)

	output_csv, err := os.OpenFile(*Output, os.O_WRONLY|os.O_APPEND|os.O_CREATE, 0666)

	if err != nil {
		fmt.Printf("%x\n", err)
		os.Exit(1)
	}

	defer output_csv.Close()

	output_csv.Write([]byte(service + "," + input + "," + strings.Map(func(r rune) rune {
		if r == ',' {
			return ' '
		}
		return r
	}, output) + "\n"))

}
