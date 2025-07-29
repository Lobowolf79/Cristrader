import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.title("Análisis Técnico: RSI + MACD para Trading")

# Entrada de símbolo
symbol = st.text_input("Introduce el símbolo de la acción (ej: AAPL, TSLA, AMZN):", "AAPL")

# Descarga datos
data = yf.download(symbol, period="6mo", interval="1d")

if data.empty:
    st.error("No se encontraron datos para ese símbolo.")
else:
    # Cálculo RSI y MACD
    data["RSI"] = ta.rsi(data["Close"], length=14)
    macd = ta.macd(data["Close"])
    data = pd.concat([data, macd], axis=1)

    st.subheader(f"Gráficos para {symbol}")
    st.line_chart(data[["Close", "RSI", "MACD_12_26_9", "MACDh_12_26_9"]].dropna())

    # Señales básicas
    last_rsi = data["RSI"].iloc[-1]
    last_macd = data["MACD_12_26_9"].iloc[-1]
    last_signal = data["MACDs_12_26_9"].iloc[-1]

    # Señal de cruce MACD
    macd_cross = last_macd > last_signal
    macd_cross_prev = data["MACD_12_26_9"].iloc[-2] < data["MACDs_12_26_9"].iloc[-2]

    signal = "Mantener"
    if last_rsi < 30 and macd_cross and macd_cross_prev:
        signal = "Comprar"
    elif last_rsi > 70 and not macd_cross and not macd_cross_prev:
        signal = "Vender"

    st.markdown(f"**RSI actual:** {last_rsi:.2f}")
    st.markdown(f"**Última señal MACD:** {'Cruce alcista' if macd_cross else 'Cruce bajista'}")
    st.markdown(f"### Señal recomendada: {signal}")
