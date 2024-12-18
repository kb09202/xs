import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Téléchargement des données Yahoo Finance
data = yf.download("GC=F", start="2023-01-01", end="2024-06-30")  # Exemple pour l'or
if data.empty:
    raise ValueError("Les données téléchargées sont vides. Vérifiez le ticker ou la période.")

# Extraction des prix de clôture
prices = data['Close'].dropna()  # Supprime les valeurs manquantes
if prices.empty:
    raise ValueError("La colonne 'Close' est vide. Vérifiez les données téléchargées.")

# Appliquer la transformation FFT
fft = np.fft.fft(prices)
frequencies = np.fft.fftfreq(len(fft), d=1)  # d=1 pour des données journalières

# Affichage des fréquences et des amplitudes
plt.figure(figsize=(12, 6))
plt.plot(frequencies, np.abs(fft), label="Amplitudes FFT")
plt.xlabel('Fréquence')
plt.ylabel('Amplitude')
plt.title('Analyse spectrale avec FFT des prix de clôture de l\'or')
plt.grid()
plt.legend()
plt.show()
