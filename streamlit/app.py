"""
BIND AI 데이터 시각화 대시보드

사용법:
  1. 터미널에서: streamlit run app.py
  2. CSV 또는 엑셀 파일을 업로드
  3. AI가 생성한 분석 결과를 시각화
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import glob

st.set_page_config(
    page_title="BIND AI 대시보드",
    page_icon="📊",
    layout="wide",
)

st.title("📊 BIND AI 데이터 대시보드")


# --- 사이드바: 데이터 소스 선택 ---
st.sidebar.header("데이터 소스")
source = st.sidebar.radio(
    "데이터를 어디서 가져올까요?",
    ["파일 업로드", "프로젝트 폴더에서 찾기"],
)

df = None

if source == "파일 업로드":
    uploaded = st.sidebar.file_uploader(
        "CSV 또는 엑셀 파일",
        type=["csv", "xlsx", "xls"],
    )
    if uploaded:
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)

elif source == "프로젝트 폴더에서 찾기":
    data_files = sorted(
        glob.glob("projects/**/data/*.csv", recursive=True)
        + glob.glob("projects/**/data/*.xlsx", recursive=True)
        + glob.glob("projects/**/*.csv", recursive=True)
    )
    if data_files:
        selected = st.sidebar.selectbox("파일 선택", data_files)
        if selected.endswith(".csv"):
            df = pd.read_csv(selected)
        else:
            df = pd.read_excel(selected)
    else:
        st.sidebar.info("projects/ 폴더에 데이터 파일이 없습니다.")


# --- 데이터 없으면 안내 ---
if df is None:
    st.info("👈 왼쪽에서 데이터를 선택하거나 업로드하세요.")
    st.markdown("""
    ### 사용 예시
    - 광고 성과 CSV 업로드 → 채널별 ROAS 비교 차트
    - 매출 데이터 업로드 → 기간별 추이 그래프
    - 상품 데이터 업로드 → 카테고리별 분포

    ### AI와 함께 사용하기
    Claude에게 "이 데이터 시각화해줘"라고 말하면,
    이 대시보드에서 볼 수 있는 차트 코드를 생성해줍니다.
    """)
    st.stop()


# --- 데이터 미리보기 ---
st.subheader("📋 데이터 미리보기")
col1, col2, col3 = st.columns(3)
col1.metric("행 수", f"{len(df):,}")
col2.metric("열 수", f"{len(df.columns):,}")
col3.metric("결측치", f"{df.isnull().sum().sum():,}")

with st.expander("전체 데이터 보기", expanded=False):
    st.dataframe(df, use_container_width=True)


# --- 자동 차트 ---
st.subheader("📈 자동 시각화")

numeric_cols = df.select_dtypes(include="number").columns.tolist()
category_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
date_cols = [c for c in df.columns if "date" in c.lower() or "날짜" in c.lower() or "일자" in c.lower()]

tab1, tab2, tab3 = st.tabs(["추이 차트", "비교 차트", "분포 차트"])

with tab1:
    if date_cols and numeric_cols:
        x_col = st.selectbox("X축 (날짜)", date_cols, key="trend_x")
        y_col = st.selectbox("Y축 (수치)", numeric_cols, key="trend_y")
        fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} 추이")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("날짜 열과 숫자 열이 있으면 추이 차트가 자동 생성됩니다.")

with tab2:
    if category_cols and numeric_cols:
        cat_col = st.selectbox("그룹", category_cols, key="bar_cat")
        val_col = st.selectbox("값", numeric_cols, key="bar_val")
        agg = st.selectbox("집계", ["합계", "평균", "개수"], key="bar_agg")
        agg_map = {"합계": "sum", "평균": "mean", "개수": "count"}
        grouped = df.groupby(cat_col)[val_col].agg(agg_map[agg]).reset_index()
        grouped = grouped.sort_values(val_col, ascending=False)
        fig = px.bar(grouped, x=cat_col, y=val_col, title=f"{cat_col}별 {val_col} ({agg})")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("범주형 열과 숫자 열이 있으면 비교 차트가 자동 생성됩니다.")

with tab3:
    if numeric_cols:
        dist_col = st.selectbox("분포 확인", numeric_cols, key="dist")
        fig = px.histogram(df, x=dist_col, title=f"{dist_col} 분포", nbins=30)
        st.plotly_chart(fig, use_container_width=True)


# --- 커스텀 차트 영역 ---
st.subheader("🎨 커스텀 시각화")
st.markdown("""
Claude에게 아래처럼 요청하면 여기에 표시할 차트 코드를 생성해줍니다:
```
이 CSV 데이터로 채널별 ROAS 비교 차트 만들어줘.
streamlit + plotly로 만들어줘.
```
생성된 `.py` 파일을 `streamlit/pages/` 폴더에 넣으면 사이드바에 새 페이지로 나타납니다.
""")
