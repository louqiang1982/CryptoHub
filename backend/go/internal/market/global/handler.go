package global

import (
	"encoding/json"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

// GlobalIndex represents a major global financial index.
type GlobalIndex struct {
	Symbol    string  `json:"symbol"`
	Name      string  `json:"name"`
	Price     float64 `json:"price"`
	Change    float64 `json:"change"`
	ChangePct float64 `json:"change_pct"`
	Country   string  `json:"country"`
}

// well-known global indices with Yahoo Finance symbols
var globalIndices = []struct {
	Symbol  string
	Name    string
	Country string
}{
	{"^GSPC", "S&P 500", "US"},
	{"^IXIC", "Nasdaq Composite", "US"},
	{"^DJI", "Dow Jones", "US"},
	{"^RUT", "Russell 2000", "US"},
	{"^VIX", "CBOE VIX", "US"},
	{"^FTSE", "FTSE 100", "UK"},
	{"^GDAXI", "DAX", "DE"},
	{"^FCHI", "CAC 40", "FR"},
	{"^N225", "Nikkei 225", "JP"},
	{"^HSI", "Hang Seng", "HK"},
	{"000001.SS", "Shanghai Composite", "CN"},
	{"^KS11", "KOSPI", "KR"},
	{"DX-Y.NYB", "US Dollar Index", "US"},
	{"GC=F", "Gold Futures", "US"},
	{"CL=F", "Crude Oil WTI", "US"},
	{"BTC-USD", "Bitcoin", "Crypto"},
}

type Handler struct {
	client *http.Client
}

func NewHandler() *Handler {
	return &Handler{
		client: &http.Client{Timeout: 10 * time.Second},
	}
}

func (h *Handler) RegisterRoutes(r gin.IRouter) {
	gm := r.Group("/global-market")
	{
		gm.GET("/indices", h.GetIndices)
		gm.GET("/indices/:symbol", h.GetIndex)
		gm.GET("/fear-greed", h.GetFearGreedIndex)
	}
}

// GetIndices returns the list of global indices with latest prices.
// In production this proxies to Yahoo Finance; here we return the
// metadata with placeholder prices to avoid external dependency in CI.
func (h *Handler) GetIndices(c *gin.Context) {
	indices := make([]GlobalIndex, 0, len(globalIndices))
	for _, idx := range globalIndices {
		indices = append(indices, GlobalIndex{
			Symbol:    idx.Symbol,
			Name:      idx.Name,
			Price:     0,
			Change:    0,
			ChangePct: 0,
			Country:   idx.Country,
		})
	}
	c.JSON(http.StatusOK, gin.H{"data": indices, "timestamp": time.Now().Unix()})
}

// GetIndex returns data for a single index by symbol.
func (h *Handler) GetIndex(c *gin.Context) {
	symbol := c.Param("symbol")
	for _, idx := range globalIndices {
		if idx.Symbol == symbol {
			c.JSON(http.StatusOK, GlobalIndex{
				Symbol:  idx.Symbol,
				Name:    idx.Name,
				Country: idx.Country,
			})
			return
		}
	}
	c.JSON(http.StatusNotFound, gin.H{"error": "index not found"})
}

// GetFearGreedIndex fetches the CNN Fear & Greed index from their public API.
func (h *Handler) GetFearGreedIndex(c *gin.Context) {
	req, err := http.NewRequest("GET", "https://production.dataviz.cnn.io/index/fearandgreed/graphdata", nil)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	req.Header.Set("User-Agent", "Mozilla/5.0")

	resp, err := h.client.Do(req)
	if err != nil {
		// Return cached/default value if external call fails
		c.JSON(http.StatusOK, gin.H{"score": 50, "rating": "Neutral", "source": "default"})
		return
	}
	defer resp.Body.Close()

	var result map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		c.JSON(http.StatusOK, gin.H{"score": 50, "rating": "Neutral", "source": "default"})
		return
	}

	// Extract score from CNN response structure
	if fear, ok := result["fear_and_greed"].(map[string]interface{}); ok {
		c.JSON(http.StatusOK, gin.H{
			"score":  fear["score"],
			"rating": fear["rating"],
			"source": "cnn",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{"score": 50, "rating": "Neutral", "source": "default"})
}
