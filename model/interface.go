package model

type Model interface {
	Train() error
	ToPmml() error
}
