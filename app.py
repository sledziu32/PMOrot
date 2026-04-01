import streamlit as st
import pandas as pd
import random
import requests
import json

# Load custom CSS
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Konfiguracja strony
st.set_page_config(
    page_title="PMOrot - Biznesowy Tarot",
    page_icon="🃏",
    layout="wide"
)

# Mapowanie kategorii na emoji
CATEGORY_EMOJIS = {
    "Wielkie Arkana": "🃏",
    "Buławy (Ogień)": "🔥",
    "Kielichy (Woda)": "🍷",
    "Miecze (Powietrze)": "🗡️",
    "Monety (Ziemia)": "💰"
}

def load_cards():
    """Wczytaj talię kart z CSV"""
    try:
        df = pd.read_csv("pmorot.csv")
        return df
    except Exception as e:
        st.error(f"Błąd wczytywania talii kart: {e}")
        return None

def get_card_aspect(card_row, aspect_type, orientation):
    """
    Pobierz odpowiedni aspekt karty na podstawie typu i orientacji
    aspect_type: 'deadline', 'budget', 'team'
    orientation: 'prosta' lub 'odwrócona'
    """
    if orientation == "prosta":
        if aspect_type == "deadline":
            return card_row['Deadline_Prosta']
        elif aspect_type == "budget":
            return card_row['Budzet_Prosta']
        elif aspect_type == "team":
            return card_row['Zespol_Prosta']
    else:  # odwrócona
        if aspect_type == "deadline":
            return card_row['Deadline_Odwrócona']
        elif aspect_type == "budget":
            return card_row['Budzet_Odwrócona']
        elif aspect_type == "team":
            return card_row['Zespol_Odwrócona']
    return "Brak opisu"

def get_category_emoji(kategoria):
    """Zwróć emoji dla kategorii"""
    for key, emoji in CATEGORY_EMOJIS.items():
        if key in kategoria:
            return emoji
    return "❓"  # domyślne emoji

def get_ai_interpretation(question, card_readings):
    """
    Wysyła pytanie i odczyty kart do OpenRouter i zwraca interpretację AI
    
    Args:
        question (str): Pytanie użytkownika
        card_readings (list): Lista słowników z odczytami kart
    
    Returns:
        str: Interpretacja AI lub komunikat o błędzie
    """
    try:
        # Pobierz klucz API z secrets
        api_key = st.secrets["OPENROUTER_API_KEY"]
        
        # Przygotuj prompt
        prompt = f"""Jesteś wróżką specjalizującą się w biznesowych wróżbach tarota. 
Otrzymałaś następujące zapytanie: "{question}"

Wylosowano trzy karty:
"""
        
        for i, reading in enumerate(card_readings, 1):
            prompt += f"""
{i}. {reading['name']} ({reading['orientation']}):
   - Terminy: {reading['deadline']}
   - Zasoby: {reading['resources']}  
   - Zespół: {reading['team']}
"""
        
        prompt += """
Na podstawie tych informacji, podaj ostateczną, spójną interpretację tego wróżenia w kontekście biznesowym. 
Zachowaj humorystyczny, lekki ton odpowiedni na 1 kwietnia, ale z nutą mądrości. 
Nie przekraczaj 200 słów. Odpowiedz po polsku."""

        # Wywołanie API
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "nvidia/nemotron-3-super-120b-a12b:free",  # Darmowy model dobry na początek
                    
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 600,
                "temperature": 0.8
            })
        )
        
        # Sprawdź odpowiedź
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            return f"Błąd API: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Wystąpił błąd podczas komunikacji z AI: {str(e)}"

def main():
    # Load custom CSS
    load_css()
    
    # Initialize session state
    if 'cards_drawn' not in st.session_state:
        st.session_state.cards_drawn = False
    if 'card_readings' not in st.session_state:
        st.session_state.card_readings = None
    if 'card_roles' not in st.session_state:
        st.session_state.card_roles = None
    if 'question' not in st.session_state:
        st.session_state.question = ""
    if 'ai_result' not in st.session_state:
        st.session_state.ai_result = None
    
    hc1, hc2, hc3 = st.columns([1, 4, 1])
    with hc2:
        # Nagłówek aplikacji
        st.title("🃏 PMOrot - Biznesowy Tarot dla Zespołów Projektowych")
        st.markdown("*Parodia wróżb tarota w ujęciu biznesowym - tylko na 1 kwietnia!*")
        
        # Wczytaj talię kart
        cards_df = load_cards()
        if cards_df is None:
            st.stop()
        
        # Interfejs użytkownika - zawsze widoczny
        st.subheader("Zadaj swoje pytanie")
        question = st.text_input(
            "Co chcesz wiedzieć o swoim projekcie, zespole lub zasobach?",
            placeholder="np. Czy nasz projekt terminowy zostanie dostarczony na czas?",
            value=st.session_state.question
        )
        
        # Update question in session state when changed
        if question != st.session_state.question:
            st.session_state.question = question
        
        # Przycisk losowania - zawsze widoczny
        col1, col2 = st.columns([1, 4])
        with col1:
            draw_clicked = st.button("🔮 Wylosuj karty", type="primary", use_container_width=True)
        
        # OBSŁUGA LOSOWANIA KART - TYLKO TUTaj KARTY SĄ LOSOWANE
        if draw_clicked:
            if not question:
                st.warning("Proszę wpisać pytanie przed losowaniem kart!")
                return
            
            # Losuj trzy różne karty z talii
            selected_indices = random.sample(range(len(cards_df)), 3)
            selected_cards = cards_df.iloc[selected_indices]
            
            # Przypisz karty do kategorii: TimeLine, Resources, People
            card_roles = ["TimeLine (Terminy)", "Resources (Zasoby)", "People (Zespół)"]
            
            # Przygotuj dane dla AI (orientacje losowane raz dla spójności)
            card_readings = []
            orientations = [random.choice(["prosta", "odwrócona"]) for _ in range(3)]
            
            for i in range(len(selected_cards)):
                card_i = selected_cards.iloc[i]
                orientation = orientations[i]
                orientation_pl = "Prosta" if orientation == "prosta" else "Odwrócona"
                
                card_readings.append({
                    'name': f"{card_i['Karta_PL']} ({card_i['Karta_EN']})",
                    'emoji': get_category_emoji(card_i['Kategoria']),
                    'orientation': orientation_pl,
                    'deadline': get_card_aspect(card_i, 'deadline', orientation),
                    'resources': get_card_aspect(card_i, 'budget', orientation),
                    'team': get_card_aspect(card_i, 'team', orientation)
                })
            
            # Zapisz stan JAWNIE i wyraźnie
            st.session_state.selected_cards = selected_cards  # Keep for potential future use
            st.session_state.card_roles = card_roles
            st.session_state.question = question
            st.session_state.cards_drawn = True
            st.session_state.card_readings = card_readings  # Store for AI and display
            st.session_state.ai_result = None  # Reset AI result when new cards drawn
        
        # WYŚWIETLANIE WYNIKÓW - CZYTY TYLKO Z STANU SESJI
        # TYLKO JEŚLI KARTY ZOSTAŁY WYLOSOWANE
        if st.session_state.cards_drawn and st.session_state.card_readings is not None:
            # Pobierz dane ze stanu sesji (NIE MODYFIKUJ TUTAJ NIC!)
            selected_cards = st.session_state.selected_cards  # Keep for potential future use
            card_roles = st.session_state.card_roles if st.session_state.card_roles is not None else ["TimeLine (Terminy)", "Resources (Zasoby)", "People (Zespół)"]
            question = st.session_state.question if st.session_state.question is not None else ""
            card_readings = st.session_state.card_readings if st.session_state.card_readings is not None else []
            
            st.subheader("🎯 Twoje wróżenie biznesowe")
            st.markdown(f"*Pytanie: _{question}_*")
            st.markdown("---")
            
            # Wyświetl karty w trzech kolumnach - UŻYJ ZAPISANYCH ODCYTÓW DLA SPÓJNOŚCI
            col1, col2, col3 = st.columns(3)
            
            # Pobierz dane z session state raz na początku dla wydajności i spójności
            cr = st.session_state.card_readings
            cr_roles = st.session_state.card_roles
            
            # Pierwsza karta - TimeLine
            with col1:
                if cr is not None and len(cr) > 0:
                    reading = cr[0]
                    role = cr_roles[0] if cr_roles is not None and len(cr_roles) > 0 else "TimeLine (Terminy)"
                    
                    # Buduj HTML dla karty
                    card_html = f"""
                    <div class="card">
                        <h2>{reading['emoji']} {role}</h2>
                        <div class="interpretation">{reading['deadline']}</div>
                        <hr>
                        <div class="info">
                            <strong>{reading['name']}</strong><br>
                            <em>Orientacja: {reading['orientation']}</em>
                        </div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
                else:
                    # To nie powinno się zdarzyć, ale na wypadek
                    st.error("Błąd: Brak danych karty dla TimeLine")
            
            # Druga karta - Resources
            with col2:
                if cr is not None and len(cr) > 1:
                    reading = cr[1]
                    role = cr_roles[1] if cr_roles is not None and len(cr_roles) > 1 else "Resources (Zasoby)"
                    
                    # Buduj HTML dla karty
                    card_html = f"""
                    <div class="card">
                        <h2>{reading['emoji']} {role}</h2>
                        <div class="interpretation">{reading['resources']}</div>
                        <hr>
                        <div class="info">
                            <strong>{reading['name']}</strong><br>
                            <em>Orientacja: {reading['orientation']}</em>
                        </div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
                else:
                    # To nie powinno się zdarzyć, ale na wypadek
                    st.error("Błąd: Brak danych karty dla Resources")
            
            # Trzecia karta - People
            with col3:
                if cr is not None and len(cr) > 2:
                    reading = cr[2]
                    role = cr_roles[2] if cr_roles is not None and len(cr_roles) > 2 else "People (Zespół)"
                    
                    # Buduj HTML dla karty
                    card_html = f"""
                    <div class="card">
                        <h2>{reading['emoji']} {role}</h2>
                        <div class="interpretation">{reading['team']}</div>
                        <hr>
                        <div class="info">
                            <strong>{reading['name']}</strong><br>
                            <em>Orientacja: {reading['orientation']}</em>
                        </div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
                else:
                    # To nie powinno się zdarzyć, ale na wypadek
                    st.error("Błąd: Brak danych karty dla People")
            
            # Sekcja z interpretacją AI
            st.markdown("---")
            st.subheader("🔮 Ostatnie słowo od wróżki")
            
            # Przycisk do wygenerowania interpretacji
            if st.button("🧙‍♀️ Poproś wróżkę o ostateczną interpretację", type="secondary"):
                with st.spinner("Wróżka koncentruje się nad kartami..."):
                    # Użyj przechowywanych odczytów dla konsystencji
                    ai_interpretation = get_ai_interpretation(question, st.session_state.card_readings if st.session_state.card_readings is not None else [])
                    st.session_state.ai_result = ai_interpretation
            
            # Wyświetl wynik AI jeśli został wygenerowany
            if st.session_state.ai_result is not None:
                # Wyświetl wynik w wyróżnionym kontenere
                st.markdown(
                    f"""
                    <div style="
                        background-color: var(--secondary);
                        color: var(--text);
                        padding: 1.5rem;
                        border-radius: 10px;
                        border-left: 4px solid var(--accent);
                        font-size: 1.1em;
                        line-height: 1.6;
                    ">
                        {st.session_state.ai_result}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        # Dodaj żartobliwą stopkę (zawsze widoczna na dole)
        funny_footers = [
            "Nie traktuj tego poważnie - to tylko 1 kwietnia! 😄",
            "Pamiętaj: prawdziwe decyzje biznesowe podejmuje się na podstawie danych, nie kart! 📊",
            "Jeśli wróżenie nie pasuje - losuj ponownie! To tylko zabawa. 🎲",
            "Uwaga: nadmierne poleganie na wróżbach może prowadzić do złego zarządzania projektami. ⚠️",
            "Ten wynik jest ważny tylko do pierwszej kawy po spotkaniu. ☕"
        ]
        st.markdown(f"*{random.choice(funny_footers)}*")

if __name__ == "__main__":
    main()
