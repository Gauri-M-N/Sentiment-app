import streamlit as st, requests, pandas as pd, altair as alt
API = st.secrets.get("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Sentiment Dashboard", layout="wide")
st.title("Sentiment Analysis Dashboard")

with st.sidebar:
    st.subheader("Add text")
    text = st.text_area("Input")
    if st.button("Analyze") and text.strip():
        r = requests.post(f"{API}/items", json={"text": text})
        st.success("Stored") if r.ok else st.error(r.text)

    st.subheader("Filters")
    q = st.text_input("Search")
    label = st.selectbox("Label", ["", "pos", "neu", "neg"], index=0)
    limit = st.slider("Rows", 10, 200, 50)

stats = requests.get(f"{API}/items/stats").json()
k1,k2,k3,k4 = st.columns(4)
k1.metric("Total", stats["total"]); k2.metric("Positive", stats["pos"])
k3.metric("Neutral", stats["neu"]); k4.metric("Negative", stats["neg"])
st.caption(f"Avg compound: {stats['avg_compound']:.3f}")

params = {"limit": limit}
if q: params["q"] = q
if label: params["label"] = label
rows = requests.get(f"{API}/items", params=params).json()
df = pd.DataFrame(rows)
st.subheader("Items")
st.dataframe(df[["id","created_at","sentiment_label","sentiment_score","text"]], use_container_width=True, height=420) if not df.empty else st.info("No data")

st.subheader("Distribution")
if not df.empty:
    chart_counts = df.groupby("sentiment_label").size().reset_index(name="count")
    st.altair_chart(alt.Chart(chart_counts).mark_bar().encode(x="sentiment_label:N", y="count:Q", tooltip=["sentiment_label","count"]), use_container_width=True)

    st.subheader("Scores over time")
    df["created_at"] = pd.to_datetime(df["created_at"])
    st.altair_chart(alt.Chart(df).mark_line(point=True).encode(x="created_at:T", y="sentiment_score:Q", tooltip=["id","sentiment_label","sentiment_score","text"]), use_container_width=True)

st.caption("Set API_URL in .streamlit/secrets.toml for remote API.")
