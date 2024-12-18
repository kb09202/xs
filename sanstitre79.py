from deep_translator import GoogleTranslator
from textblob import TextBlob

# Fonction pour corriger le texte
def correct_text(text):
    # Créer un objet TextBlob avec le texte
    blob = TextBlob(text)

    # Corriger le texte
    corrected_text = str(blob.correct())
    return corrected_text

# Fonction pour traduire le texte dans les trois langues
def translate_text(text):
    # Corriger le texte
    corrected_text = correct_text(text)

    # Traduire en hébreu (utiliser 'iw' au lieu de 'he')
    translated_hebrew = GoogleTranslator(source='auto', target='iw').translate(corrected_text)
    
    # Traduire en arabe
    translated_arabic = GoogleTranslator(source='auto', target='ar').translate(corrected_text)
    
    # Traduire en français
    translated_french = GoogleTranslator(source='auto', target='fr').translate(corrected_text)

    return corrected_text, translated_hebrew, translated_arabic, translated_french

# Exemple d'utilisation
if __name__ == '__main__':
    # Exemple de texte à traduire
    text_to_translate = "Je suis un sharingan* This is an example text for translation."

    # Traduire le texte
    corrected_text, hebrew, arabic, french = translate_text(text_to_translate)

    print("Texte Corrigé:")
    print(corrected_text)
    print("\nTexte Hébreu Traduit:")
    print(hebrew)
    print("\nTexte Arabe Traduit:")
    print(arabic)
    print("\nTexte Français Traduit:")
    print(french)
