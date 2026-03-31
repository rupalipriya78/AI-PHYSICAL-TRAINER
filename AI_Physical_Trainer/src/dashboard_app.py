# src/dashboard_app.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os

st.set_page_config(page_title="AI Trainer Dashboard", layout="wide")
st.title("AI Motion Trainer — Dashboard")

import os
SESSION_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "session_log.csv")


if not os.path.exists(SESSION_FILE):
    st.info("No session data found. Run a workout to generate session_log.csv.")
    st.stop()

df = pd.read_csv(SESSION_FILE, parse_dates=['timestamp'])
df['date'] = df['timestamp'].dt.date

st.sidebar.header("Filters")
exs = sorted(df['exercise'].unique())
selected = st.sidebar.multiselect("Exercise", options=exs, default=exs)
start = st.sidebar.date_input("Start date", value=df['timestamp'].dt.date.min())
end = st.sidebar.date_input("End date", value=df['timestamp'].dt.date.max())

mask = (df['exercise'].isin(selected)) & (df['timestamp'].dt.date >= start) & (df['timestamp'].dt.date <= end)
fdf = df[mask].copy()
if fdf.empty:
    st.warning("No sessions in selected range.")
    st.stop()

# Summary metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total sessions", fdf.shape[0])
col2.metric("Total reps", int(fdf['reps'].sum()))
col3.metric("Total calories (est.)", f"{fdf['calories'].sum():.1f} kcal")

st.markdown("---")
st.subheader("Reps over time")
agg = fdf.groupby('date').agg(total_reps=('reps','sum')).reset_index().sort_values('date')
st.line_chart(data=agg.set_index('date')['total_reps'])

st.subheader("Calories per session")
st.bar_chart(fdf.set_index('timestamp')['calories'])

st.subheader("Session details")
st.dataframe(fdf[['timestamp','exercise','reps','duration_seconds','calories']].sort_values('timestamp', ascending=False))

# Trend analysis
st.subheader("Performance Trend Analysis")
if fdf.shape[0] >= 2:
    x = np.array([d.toordinal() for d in fdf['timestamp'].dt.date])
    y = fdf['reps'].values
    m, b = np.polyfit(x, y, 1)
    slope_per_day = m
    st.write(f"Trend slope: **{slope_per_day:.3f} reps/day**")
    window = min(5, len(y))
    mov = pd.Series(y).rolling(window=window, min_periods=1).mean()
    trend_df = pd.DataFrame({'reps': y, 'moving_avg': mov}).set_index(fdf['timestamp'].dt.date)
    st.line_chart(trend_df)
    if slope_per_day > 0.05:
        st.success("Performance improving 🎉")
    elif slope_per_day < -0.05:
        st.error("Performance decreasing — consider rest")
    else:
        st.info("Stable performance")
else:
    st.info("Not enough sessions for trend analysis (need at least 2).")
