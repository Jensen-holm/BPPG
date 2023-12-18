package nn

import (
	"fmt"
	"strings"

	"github.com/go-gota/gota/dataframe"
	"github.com/gofiber/fiber/v2"
)

type NN struct {
	CSVData        string   `json:"csv_data"`
	Features       []string `json:"features"`
	Target         string   `json:"target"`
	Epochs         int      `json:"epochs"`
	HiddenSize     int      `json:"hidden_size"`
	LearningRate   float64  `json:"learning_rate"`
	ActivationFunc string   `json:"activation"`
	Df             *dataframe.DataFrame
}

func NewNN(c *fiber.Ctx) (*NN, error) {
	newNN := new(NN)
	err := c.BodyParser(newNN)
	if err != nil {
		return nil, fmt.Errorf("invalid JSON request: %v", err)
	}

	csvReader := strings.NewReader(newNN.CSVData)
	df := dataframe.ReadCSV(csvReader)

	if df.Nrow() == 0 || df.Ncol() == 0 {
		return nil, fmt.Errorf("empty csv_data sent: %v", err)
	}

	newNN.Df = &df
	return newNN, nil
}
