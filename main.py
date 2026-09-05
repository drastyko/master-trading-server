from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Structure des données envoyées par MT5
class MarketData(BaseModel):
    symbol: str
    timeframe: str
    close: float
    rsi: float
    ema20: float
    ema50: float
    structure: str

@app.get("/")
def home():
    return {"status": "ok", "message": "Serveur de test MT5 opérationnel"}

@app.post("/analyze")
def analyze(data: MarketData):
    print(f"Données reçues de MT5 pour {data.symbol} ({data.timeframe}) : Prix={data.close}, RSI={data.rsi}")
    
    # Simulation d'un signal fictif pour tester la réponse
    return {
        "signal": "BUY",
        "confidence": 85,
        "sl": round(data.close * 0.99, 5),
        "tp": round(data.close * 1.02, 5),
        "reason": "Test de connexion réussi entre MT5 et Render"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
