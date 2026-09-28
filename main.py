import streamlit as st
import random
import plotly.graph_objects as go
import base64

st.set_page_config(page_title="Wavelength", page_icon="🏄", layout="centered")

def set_background(image_path):
    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* DARK OVERLAY (this fixes your issue) */
        .stApp::before {{
            content: "";
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.7);  /* <-- change strength here */
            z-index: 0;
        }}

        /* KEEP CONTENT ABOVE OVERLAY */
        .main {{
            position: relative;
            z-index: 1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# CALL THIS AT THE TOP
set_background(r"images/bg.png")

st.title("Wavelength", text_alignment="center")

st.image(r"images/header.png", use_container_width=False)

LOW, HIGH = 0, 100

SCORE_TIERS = [
    (2, 4, "#4B97B7"),   # bullseye
    (5, 3, "#FE4902"),
    (8, 2, "#FFB40B")
]

OUTER_COLOR = "#DFE3D4"
HIDDEN_COLOR = "#78DECA"

CONCEPT_PAIRS = [
    ("Cold", "Hot"), ("Cheap", "Expensive"), ("Underrated", "Overrated"),
    ("Bad Movie", "Great Movie"), ("Small", "Huge"), ("Boring Job", "Exciting Job"),
    ("Rare", "Common"), ("Simple", "Complicated"), ("Quiet", "Loud"),
    ("Early", "Late"), ("Ugly", "Beautiful"), ("Weak", "Strong"),
    ("Safe", "Dangerous"), ("Slow", "Fast"), ("Soft", "Hard"),
    ("Sad Song", "Happy Song"), ("Low Effort", "High Effort"),
    ("Bad Superpower", "Amazing Superpower"), ("Useless Gift", "Perfect Gift"),
    ("Normal Pet", "Weird Pet"), ("Casual Restaurant", "Fancy Restaurant"),
    ("Introvert Activity", "Extrovert Activity"), ("Predictable", "Surprising"),
    ("Old-Fashioned", "Futuristic"), ("Light Snack", "Heavy Meal"),
    ("Guilty Pleasure", "Respectable Taste"), ("Niche", "Mainstream"),
    ("Amateur", "Professional"), ("Cheap Wine", "Expensive Wine"),
    ("Bad Superhero Name", "Great Superhero Name"), ("Forgettable", "Iconic"),
]

if "random_number" not in st.session_state:
    st.session_state.random_number = 0
if "words" not in st.session_state:
    random_word_num = random.randint(0,len(CONCEPT_PAIRS))
    st.session_state.words = CONCEPT_PAIRS[random_word_num]
if "reveal" not in st.session_state:
    st.session_state.reveal = False
if "guess" not in st.session_state:
    st.session_state.guess = False
if "help" not in st.session_state:
    st.session_state.help = ""
if "phase" not in st.session_state:
    st.session_state.phase = "idle"  
    # idle → reveal → guessing → result

def create_random():
    return random.randint(LOW+2, HIGH-2)

col1, col2 = st.columns(2)

col1.subheader(f"⬅️ {st.session_state.words[0]}", text_alignment="left", width="stretch", )
col2.subheader(f"{st.session_state.words[1]} ➡️", text_alignment="right", width="stretch")


col3, col4 = st.columns([3,1])
if col3.button("Play", use_container_width=True):
    st.session_state.random_number = create_random()
    st.session_state.guess = False
    st.session_state.reveal = False
    st.session_state.help = ""
    st.session_state.last_score = ""
    help = ""

if col4.button("Shuffle words", use_container_width=True):
    random.shuffle(CONCEPT_PAIRS)
    st.session_state.words = CONCEPT_PAIRS[0]
    st.rerun()

if st.button("Reveal", use_container_width=True):
    st.session_state.reveal = True
    st.session_state.phase = "reveal"
#elif st.button("Hide", use_container_width=True):
#    st.session_state.reveal= False
        
if st.session_state.phase == "reveal":
    clue = st.text_input("Enter clue", value=st.session_state.help)

    if clue != "":
        st.session_state.help = clue
        st.session_state.reveal = False   # hide target again
        st.session_state.phase = "guessing"
        st.rerun()

if st.session_state.reveal:
    steps = [
        {'range': [st.session_state.random_number - SCORE_TIERS[2][0], st.session_state.random_number + SCORE_TIERS[2][0]], 'color': SCORE_TIERS[2][2]},
        {'range': [st.session_state.random_number - SCORE_TIERS[1][0], st.session_state.random_number + SCORE_TIERS[1][0]], 'color': SCORE_TIERS[1][2]},
        {'range': [st.session_state.random_number - SCORE_TIERS[0][0], st.session_state.random_number + SCORE_TIERS[0][0]], 'color': SCORE_TIERS[0][2]}
        ]
else:
    steps = [
        {'range': [LOW,HIGH], 'color': HIDDEN_COLOR},

    ]

if st.button("Guess", use_container_width=True):
    st.session_state.guess= True

if st.session_state.guess:
    st.session_state.guess_num = st.slider("Guess", LOW, HIGH, 0, 1)
    threshold ={
        "line": {"color": "#D70B3C", "width": 5},
        "thickness": 0.85,
        "value": st.session_state.guess_num}
else:
    threshold = {"line": {"color": "#D70B3C", "width": 0}}

fig = go.Figure(
        go.Indicator(
            mode="gauge",
            value=st.session_state.random_number,
            gauge={
                "axis": {"range": [LOW, HIGH], "tickwidth": 1, "tickcolor": "#333"},
                'bar': {'color': "rgba(0,0,0,0)"},
                'bgcolor': OUTER_COLOR,
                "threshold": threshold,
                'steps': steps
                }
    )
)

left_label = st.session_state.words[0]
right_label = st.session_state.words[1]

fig.add_annotation(
    x=0.5,
    y=0.2,
    text=st.session_state.help,
    showarrow=False,
    font=dict(size=50, color="#afaca2")
)
st.plotly_chart(fig)

if st.button("Check answer", use_container_width=True):
    st.session_state.reveal = True
    st.session_state.phase = "result"
    evaluation = abs(st.session_state.random_number - st.session_state.guess_num)

    if evaluation < SCORE_TIERS[0][0]:
        score = SCORE_TIERS[0][1]
    elif evaluation < SCORE_TIERS[1][0]:
        score = SCORE_TIERS[1][1]
    elif evaluation < SCORE_TIERS[2][0]:
        score = SCORE_TIERS[2][1]
    else:
        score = 0

    st.session_state.last_score = score

    st.rerun()

if st.session_state.phase == "result":
    if st.session_state.last_score == "":
        pass
    elif st.session_state.last_score == 4:
        st.success(f"Your score is: {st.session_state.last_score}")
    elif st.session_state.last_score > 0:
        st.warning(f"Your score is: {st.session_state.last_score}")
    else:
        st.error(f"Your score is: {st.session_state.last_score}")