# filename: song_recommender_oop_artist.py

import streamlit as st

# ---------------------------
# Song-klasse
# --------------------------- 
class Song:
    def __init__(self, title, artist, pop, rap, indie, RnB, energi, glad, trist, tidsperiode):
        self.title = title
        self.artist = artist
        self.pop = pop
        self.rap = rap
        self.indie = indie
        self.RnB = RnB
        self.energi = energi
        self.glad = glad
        self.trist = trist
        self.tidsperiode = tidsperiode
        self.tidsperiode_norm = 0  # bliver sat senere

    def features(self):
        return [self.pop, self.rap, self.indie, self.RnB, self.energi, self.glad, self.trist, self.tidsperiode_norm]

# ---------------------------
# Recommender-klasse
# ---------------------------
class Recommender:
    def __init__(self, songs, weights=None):
        self.songs = songs
        self.normalize_time()
        self.weights = weights if weights else [1]*8

    def normalize_time(self):
        min_year = min(song.tidsperiode for song in self.songs)
        max_year = max(song.tidsperiode for song in self.songs)
        for song in self.songs:
            song.tidsperiode_norm = (song.tidsperiode - min_year) / (max_year - min_year)

    def euclidean_distance(self, song1, song2):
        f1 = song1.features()
        f2 = song2.features()
        dist = sum(w*(a-b)**2 for w, a, b in zip(self.weights, f1, f2))**0.5
        return dist

    def recommend(self, selected_song, n=5):
        distances = []
        for song in self.songs:
            if song.title != selected_song.title:
                dist = self.euclidean_distance(selected_song, song)
                distances.append((dist, song))
        distances.sort(key=lambda x: x[0])
        return [song for _, song in distances[:n]]

# ---------------------------
# Datasæt
# ---------------------------
songs = [
Song("Blinding Lights", "The Weeknd", 0.9, 0.0, 0.1, 0.4, 0.8, 0.9, 0.1, 2019),
Song("Shape of You", "Ed Sheeran", 0.8, 0.2, 0.0, 0.6, 0.7, 0.8, 0.2, 2017),
Song("Lose Yourself", "Eminem", 0.2, 0.95, 0.0, 0.2, 0.9, 0.6, 0.3, 2002),
Song("Bad Guy", "Billie Eilish", 0.7, 0.2, 0.3, 0.4, 0.6, 0.7, 0.2, 2019),
Song("Redbone", "Childish Gambino", 0.2, 0.0, 0.6, 0.8, 0.4, 0.5, 0.5, 2016),
Song("HUMBLE.", "Kendrick Lamar", 0.2, 1.0, 0.0, 0.2, 0.85, 0.6, 0.2, 2017),
Song("Man I Need", "Olivia Dean", 0.7, 0.0, 0.3, 0.6, 0.65, 0.7, 0.3, 2021),
Song("The Hardest Part", "Olivia Dean", 0.65, 0.0, 0.3, 0.55, 0.6, 0.65, 0.35, 2021),
Song("Show Me", "Olivia Dean", 0.7, 0.0, 0.25, 0.6, 0.65, 0.7, 0.3, 2020),
Song("God's Plan", "Drake", 0.6, 0.9, 0.0, 0.5, 0.8, 0.7, 0.2, 2018),
Song("In My Feelings", "Drake", 0.7, 0.85, 0.0, 0.55, 0.75, 0.8, 0.2, 2018),
Song("Hotline Bling", "Drake", 0.8, 0.6, 0.0, 0.5, 0.7, 0.8, 0.2, 2015),
Song("Take Care", "Drake", 0.4, 0.5, 0.1, 0.8, 0.5, 0.6, 0.3, 2011),
Song("One Dance", "Drake", 0.75, 0.5, 0.0, 0.6, 0.7, 0.8, 0.2, 2016),
Song("Thinkin Bout You", "Frank Ocean", 0.3, 0.0, 0.2, 0.9, 0.5, 0.7, 0.3, 2012),
Song("Pink + White", "Frank Ocean", 0.4, 0.0, 0.3, 0.85, 0.55, 0.7, 0.3, 2016),
Song("Nights", "Frank Ocean", 0.2, 0.0, 0.3, 0.9, 0.5, 0.6, 0.4, 2016),
Song("Pyramids", "Frank Ocean", 0.3, 0.0, 0.4, 0.85, 0.55, 0.65, 0.35, 2012),
Song("Lost", "Frank Ocean", 0.35, 0.0, 0.25, 0.9, 0.6, 0.7, 0.3, 2012),
Song("I Love Lucy", "Khamari", 0.5, 0.2, 0.2, 0.7, 0.65, 0.7, 0.3, 2020),
Song("Drifting", "Khamari", 0.55, 0.15, 0.25, 0.7, 0.6, 0.65, 0.35, 2020),
Song("Late Night", "Khamari", 0.6, 0.25, 0.2, 0.7, 0.65, 0.7, 0.3, 2021),
Song("Luv", "Tory Lanez", 0.5, 0.6, 0.1, 0.8, 0.7, 0.75, 0.2, 2016),
Song("Say It", "Tory Lanez", 0.4, 0.5, 0.0, 0.85, 0.65, 0.7, 0.3, 2015),
Song("Controlla", "Tory Lanez", 0.5, 0.5, 0.0, 0.8, 0.7, 0.7, 0.25, 2016),
Song("Temperature Rising", "Tory Lanez", 0.45, 0.4, 0.0, 0.8, 0.65, 0.7, 0.25, 2015),
Song("Talk To Me", "Tory Lanez", 0.5, 0.5, 0.0, 0.75, 0.65, 0.7, 0.25, 2015),

]

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("Song Recommender")
st.write("Vælg enten en sang eller juster parametre for at få anbefalinger.")

recommender = Recommender(
    songs,
    weights=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5]
)

mode = st.radio("Vælg metode:", ["Vælg sang", "Vælg parametre"])

# ---------------------------
# MODE 1: Vælg sang
# ---------------------------
if mode == "Vælg sang":
    song_options = [f"{song.title} - {song.artist}" for song in songs]
    song_choice_str = st.selectbox("Vælg en sang:", song_options)

    selected_title = song_choice_str.split(" - ")[0]
    selected_song = next(song for song in songs if song.title == selected_title)

    recommended_songs = recommender.recommend(selected_song)

    st.subheader("Anbefalede sange:")
    for song in recommended_songs:
        st.write(f"{song.title} af {song.artist}")

# ---------------------------
# MODE 2: Vælg parametre
# ---------------------------
elif mode == "Vælg parametre":
    st.subheader("Indstil dine præferencer")

    pop = st.slider("Pop", 0.0, 1.0, 0.5)
    rap = st.slider("Rap", 0.0, 1.0, 0.5)
    indie = st.slider("Indie", 0.0, 1.0, 0.5)
    RnB = st.slider("R&B", 0.0, 1.0, 0.5)
    energi = st.slider("Energi", 0.0, 1.0, 0.5)
    glad = st.slider("Glad", 0.0, 1.0, 0.5)
    trist = st.slider("Trist", 0.0, 1.0, 0.5)
    tidsperiode = st.slider("År", 2000, 2023, 2018)

    if st.button("Find anbefalinger", key="param_button"):
        selected_song = Song(
            "Din smag", "Dig",
            pop, rap, indie, RnB,
            energi, glad, trist,
            tidsperiode
        )

        recommender.normalize_time()
        recommended_songs = recommender.recommend(selected_song)

        st.subheader("Anbefalede sange:")
        for song in recommended_songs:
            st.write(f"{song.title} af {song.artist}")