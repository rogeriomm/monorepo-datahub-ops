package monitor

import (
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"log"
	"math/rand"
	"net/http"
	"runtime"
	"runtime/metrics"
	"time"
)

var PORT = ":9100"
var NAMESPACE = "golang_app_4"

var nGoroutines = prometheus.NewGauge(
	prometheus.GaugeOpts{
		Namespace: NAMESPACE,
		Name:      "n_goroutines",
		Help:      "Number of goroutines"})

var nMemory = prometheus.NewGauge(
	prometheus.GaugeOpts{
		Namespace: NAMESPACE,
		Name:      "n_memory",
		Help:      "Memory usage"})

func Start() {
	prometheus.MustRegister(nGoroutines)
	prometheus.MustRegister(nMemory)

	const (
		nGo  = "/sched/goroutines:goroutines"
		nMem = "/memory/classes/heap/free:bytes"
	)

	metricsList := []metrics.Sample{
		{Name: nGo},
		{Name: nMem},
	}

	// Launch metrics collection
	go func() {
		for {
			for i := 1; i < 4; i++ {
				go func() {
					_ = make([]int, 1_000_000)
					time.Sleep(time.Duration(rand.Intn(10)) * time.Second)
				}()
			}
			runtime.GC()
			metrics.Read(metricsList)
			nGoroutines.Set(float64(metricsList[0].Value.Uint64()))
			nMemory.Set(float64(metricsList[1].Value.Uint64()))
			time.Sleep(time.Duration(rand.Intn(15)) * time.Second)
		}
	}()

	// Launch metrics endpoint
	go func() {
		http.Handle("/metrics", promhttp.Handler())
		log.Println("Prometheus metrics listening on ", PORT, "/metrics")
		if err := http.ListenAndServe(PORT, nil); err != nil {
			log.Fatalf("Prometheus server failed: %v", err)
		}
	}()
}
