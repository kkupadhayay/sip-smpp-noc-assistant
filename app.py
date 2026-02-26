import streamlit as st
import os
import plotly.express as px
from db import init_db, insert_capture, insert_calls, get_recent
from parser import parse_pcap
from rules import apply_rules
from ai_chat import ask_grok

st.set_page_config(layout="wide")
init_db()

st.title("SIP NOC Assistant")

tab1, tab2, tab3 = st.tabs(["Upload", "Dashboard", "AI"])

with tab1:
    uploaded = st.file_uploader("Upload PCAP", type=["pcap","pcapng"])
    if uploaded:
        temp = uploaded.name
        with open(temp, "wb") as f:
            f.write(uploaded.getvalue())

        cid = insert_capture(uploaded.name)
        calls = parse_pcap(temp)
        insert_calls(cid, calls)
        alerts = apply_rules(cid, calls)

        st.success(f"Processed {len(calls)} calls")
        for a in alerts:
            st.warning(a["message"])

        os.remove(temp)

with tab2:
    calls_df, alerts_df, cap_df = get_recent()
    st.metric("Total Calls", len(calls_df))

    if not calls_df.empty:
        fig = px.histogram(calls_df, x="final_status")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Alerts")
    st.dataframe(alerts_df)

with tab3:
    calls_df, _, _ = get_recent()
    q = st.chat_input("Ask about traffic")
    if q:
        st.write(ask_grok(q, calls_df))
