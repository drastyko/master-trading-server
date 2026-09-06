import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

app = FastAPI()

# Récupération de la clé API depuis les variables d'environnement Render
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

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
    return {"status": "Server is active"}

@app.post("/analyze")
def analyze_market(data: MarketData):
    if not OPENAI_API_KEY:
        # Fallback de test si la clé n'est pas configurée
        return {
            "signal": "NEUTRAL",
            "confidence": 0,
            "sl": 0.0,
            "tp": 0.0,
            "reason": "OPENAI_API_KEY non configurée dans l'environnement Render."
        }

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    prompt = f"""
    Tu es un expert en trading algorithmique et en Smart Money Concepts (SMC).
    Analyse les données techniques suivantes pour l'actif {data.symbol} sur l'unité de temps {data.timeframe} :
    - Prix de clôture : {data.close}
    - RSI (14) : {data.rsi}
    - EMA 20 : {data.ema20}
    - EMA 50 : {data.ema50}
    - Structure du marché : {data.structure}

    Réponds UNIQUEMENT sous forme d'un objet JSON strict avec la structure suivante :
    {{
      "signal": "BUY" | "SELL" | "NEUTRAL",
      "confidence": nombre entre 0 et 100,
      "sl": prix_stop_loss,
      "tp": prix_take_profit,
      "reason": "Explication courte en 1 phrase"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.2
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
