import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ──────────────────────────────────────────────
# 페이지 설정
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="앱그로스 주간 성과 대시보드",
    page_icon="📱",
    layout="wide",
)

st.title("📱 앱그로스 주간 성과 대시보드")
st.caption("W1 (3/23~3/29) vs W2 (3/30~4/5) | Google · Facebook 캠페인 비교")

# ──────────────────────────────────────────────
# 데이터 정의
# ──────────────────────────────────────────────
RAW = {
    "채널": [
        "Google", "Google",
        "Facebook", "Facebook",
    ],
    "캠페인": [
        "App promotion-AppInstall-ua-Purchase", "App promotion-AppInstall-ua-Purchase",
        "facebook_da_pr-ua-apppurchase-android-main", "facebook_da_pr-ua-apppurchase-android-main",
    ],
    "주차": ["W1", "W2", "W1", "W2"],
    "Impressions": [476_524, 936_527, 253_919, 266_449],
    "Clicks": [5_553, 5_484, 4_739, 9_554],
    "Cost": [2_172_050, 3_855_783, 2_144_070, 2_119_324],
    "회원가입": [452, 683, 357, 335],
    "구매완료": [261, 296, 92, 108],
    "구매액": [14_812_536, 16_691_660, 5_829_873, 7_800_822],
    "구매유저(App)": [201, 244, 81, 87],
    "구매유저(Web)": [0, 0, 0, 0],
    "CPI": [1_444, 2_171, 1_324, 1_407],
    "인앱구매유저수": [201, 244, 81, 87],
}

df = pd.DataFrame(RAW)
df["구매유저 합계"] = df["구매유저(App)"] + df["구매유저(Web)"]

# 성과 지표 계산
df["CTR"] = df["Clicks"] / df["Impressions"] * 100
df["CPC"] = df["Cost"] / df["Clicks"]
df["가입 CVR"] = df["회원가입"] / df["Clicks"] * 100
df["가입 CPA"] = df["Cost"] / df["회원가입"]
df["가입→구매 CVR"] = df["구매완료"] / df["회원가입"] * 100
df["구매 CVR"] = df["구매완료"] / df["Clicks"] * 100
df["구매 CPA"] = df["Cost"] / df["구매완료"]
df["ROAS"] = df["구매액"] / df["Cost"] * 100
df["ARPPU"] = df["구매액"] / df["구매유저 합계"].replace(0, 1)

CHANNELS = ["Google", "Facebook"]
COLORS = {"Google": "#4285F4", "Facebook": "#1877F2"}
WEEK_COLORS = {"W1": "#5B8FF9", "W2": "#FF6B6B"}

# ──────────────────────────────────────────────
# 메타 광고소재별 데이터 (Airbridge 전환 기준)
# ──────────────────────────────────────────────
CREATIVE_RAW = {
    "소재명": [
        "260226_carousel_workwear_vari_lastpage",
        "260226_carousel_workwear_vari_lastpage",
        "260321_carousel_springoutfits2_45",
        "260321_carousel_springoutfits2_45",
        "20260219-img-department store brand",
        "20260219-img-department store brand",
        "260321_carousel_blackandwhite_45",
        "260321_carousel_blackandwhite_45",
        "260313_carousel_springoutfits",
        "260313_carousel_springoutfits",
        "260330_carousel_springwear2_45",
        "260330_carousel_springwear2_45",
        "20260226-img-department store brand",
        "20260226-img-department store brand",
        "260403_img_ston-wappen",
        "260403_img_ston-wappen",
        "260403_img_ston-tshirt",
        "260403_img_ston-tshirt",
    ],
    "주차": ["W1", "W2"] * 9,
    "가입": [174, 155, 91, 121, 54, 3, 29, 23, 3, 3, 0, 6, 0, 2, 0, 2, 0, 1],
    "앱설치": [721, 652, 629, 516, 93, 0, 138, 125, 26, 26, 0, 65, 0, 7, 0, 60, 0, 40],
    "구매건": [40, 59, 23, 24, 24, 11, 2, 6, 3, 2, 0, 3, 0, 2, 0, 0, 0, 0],
    "구매유저": [35, 44, 23, 22, 19, 9, 2, 5, 2, 2, 0, 2, 0, 2, 0, 0, 0, 0],
    "구매액": [
        2_840_891, 4_473_639,
        1_450_626, 1_916_412,
        1_260_960, 439_331,
        163_800, 291_430,
        113_596, 0,
        0, 421_160,
        0, 144_540,
        0, 0,
        0, 0,
    ],
}

cr_df = pd.DataFrame(CREATIVE_RAW)
# 소재 유형 자동 분류
def classify_creative(name):
    if "carousel" in name:
        return "캐러셀"
    elif "img" in name:
        return "이미지"
    return "기타"

cr_df["소재유형"] = cr_df["소재명"].apply(classify_creative)
# 짧은 이름 생성
cr_df["소재(짧은이름)"] = cr_df["소재명"].str.replace(r"^(\d{6}_|20\d{6}-)", "", regex=True).str[:35]

# ──────────────────────────────────────────────
# 유틸리티
# ──────────────────────────────────────────────

def fmt_num(v, fmt_type="int"):
    if fmt_type == "int":
        return f"{v:,.0f}"
    if fmt_type == "won":
        return f"{v:,.0f}원"
    if fmt_type == "pct":
        return f"{v:.2f}%"
    return str(v)


def wow_pct(w1, w2):
    if w1 == 0:
        return "N/A"
    return (w2 - w1) / w1 * 100


# ──────────────────────────────────────────────
# 채널 선택 필터
# ──────────────────────────────────────────────
st.markdown("---")

view_mode = st.radio(
    "보기 모드",
    ["채널 비교 (Google vs Facebook)", "Google만 보기", "Facebook만 보기"],
    horizontal=True,
)

if view_mode == "Google만 보기":
    selected_channels = ["Google"]
elif view_mode == "Facebook만 보기":
    selected_channels = ["Facebook"]
else:
    selected_channels = CHANNELS

filtered_df = df[df["채널"].isin(selected_channels)]

# ──────────────────────────────────────────────
# 핵심 KPI 카드
# ──────────────────────────────────────────────
st.markdown("---")
st.subheader("핵심 KPI 요약")

if len(selected_channels) == 2:
    # 채널 비교 모드: 각 채널별 KPI
    for ch in selected_channels:
        ch_df = df[df["채널"] == ch]
        w1 = ch_df[ch_df["주차"] == "W1"].iloc[0]
        w2 = ch_df[ch_df["주차"] == "W2"].iloc[0]

        st.markdown(f"#### {ch}")
        kpi_cols = st.columns(6)
        kpis = [
            ("Cost", w1["Cost"], w2["Cost"], "won", True),
            ("구매완료", w1["구매완료"], w2["구매완료"], "int", False),
            ("구매액", w1["구매액"], w2["구매액"], "won", False),
            ("ROAS", w1["ROAS"], w2["ROAS"], "pct", False),
            ("구매 CPA", w1["구매 CPA"], w2["구매 CPA"], "won", True),
            ("ARPPU", w1["ARPPU"], w2["ARPPU"], "won", False),
        ]
        for col, (label, v1, v2, ft, inverse) in zip(kpi_cols, kpis):
            with col:
                st.metric(
                    label=label,
                    value=fmt_num(v2, ft),
                    delta=f"{wow_pct(v1, v2):+.1f}%" if v1 != 0 else "N/A",
                    delta_color="inverse" if inverse else "normal",
                )
else:
    ch = selected_channels[0]
    ch_df = df[df["채널"] == ch]
    w1 = ch_df[ch_df["주차"] == "W1"].iloc[0]
    w2 = ch_df[ch_df["주차"] == "W2"].iloc[0]

    kpi_cols = st.columns(6)
    kpis = [
        ("Cost", w1["Cost"], w2["Cost"], "won", True),
        ("구매완료", w1["구매완료"], w2["구매완료"], "int", False),
        ("구매액", w1["구매액"], w2["구매액"], "won", False),
        ("ROAS", w1["ROAS"], w2["ROAS"], "pct", False),
        ("구매 CPA", w1["구매 CPA"], w2["구매 CPA"], "won", True),
        ("ARPPU", w1["ARPPU"], w2["ARPPU"], "won", False),
    ]
    for col, (label, v1, v2, ft, inverse) in zip(kpi_cols, kpis):
        with col:
            st.metric(
                label=label,
                value=fmt_num(v2, ft),
                delta=f"{wow_pct(v1, v2):+.1f}%" if v1 != 0 else "N/A",
                delta_color="inverse" if inverse else "normal",
            )

# ──────────────────────────────────────────────
# 탭 구성
# ──────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab_cr, tab6, tab7 = st.tabs(
    ["📈 유입", "👤 가입", "🔄 가입→구매", "💰 구매", "📲 설치·앱구매", "🎨 메타 소재별", "📊 채널 비교", "📋 원본 데이터"]
)


def make_grouped_bar(data_df, metric, title, y_label, fmt=",.0f", suffix="", channels=None):
    """채널별 W1/W2 그룹 바 차트 생성"""
    if channels is None:
        channels = selected_channels
    fig = go.Figure()
    for ch in channels:
        ch_data = data_df[data_df["채널"] == ch]
        texts = []
        for v in ch_data[metric]:
            if suffix == "%":
                texts.append(f"{v:.2f}%")
            elif suffix == "원":
                texts.append(f"{v:,.0f}원")
            else:
                texts.append(f"{v:,.0f}")
        fig.add_trace(go.Bar(
            name=ch,
            x=ch_data["주차"],
            y=ch_data[metric],
            marker_color=COLORS[ch],
            text=texts,
            textposition="outside",
        ))
    fig.update_layout(
        title=title,
        yaxis_title=y_label,
        barmode="group",
        height=420,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def make_wow_bar(data_df, metric, title, channels=None):
    """채널별 WoW 변화율 바 차트"""
    if channels is None:
        channels = selected_channels
    ch_names = []
    changes = []
    colors = []
    for ch in channels:
        ch_data = data_df[data_df["채널"] == ch]
        w1_val = ch_data[ch_data["주차"] == "W1"][metric].values[0]
        w2_val = ch_data[ch_data["주차"] == "W2"][metric].values[0]
        pct = wow_pct(w1_val, w2_val)
        ch_names.append(ch)
        changes.append(pct if isinstance(pct, (int, float)) else 0)
        colors.append(COLORS[ch])

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=ch_names,
        y=changes,
        marker_color=colors,
        text=[f"{v:+.1f}%" for v in changes],
        textposition="outside",
    ))
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    fig.update_layout(title=title, yaxis_title="WoW %", height=350)
    return fig


# ──────────────── 유입 탭 ────────────────
with tab1:
    st.subheader("유입 지표")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            make_grouped_bar(filtered_df, "CTR", "CTR (클릭률)", "%", suffix="%"),
            use_container_width=True,
        )
    with col2:
        st.plotly_chart(
            make_grouped_bar(filtered_df, "CPC", "CPC (클릭당 비용)", "원", suffix="원"),
            use_container_width=True,
        )

    st.markdown("#### 노출 & 클릭 추이")
    col3, col4 = st.columns(2)
    with col3:
        fig = go.Figure()
        for ch in selected_channels:
            ch_data = filtered_df[filtered_df["채널"] == ch]
            fig.add_trace(go.Bar(
                name=ch, x=ch_data["주차"], y=ch_data["Impressions"],
                marker_color=COLORS[ch],
                text=[f"{v / 1_000:.0f}K" for v in ch_data["Impressions"]],
                textposition="outside",
            ))
        fig.update_layout(title="Impressions (노출수)", yaxis_title="회", barmode="group", height=420)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        fig = go.Figure()
        for ch in selected_channels:
            ch_data = filtered_df[filtered_df["채널"] == ch]
            fig.add_trace(go.Bar(
                name=ch, x=ch_data["주차"], y=ch_data["Clicks"],
                marker_color=COLORS[ch],
                text=[f"{v:,.0f}" for v in ch_data["Clicks"]],
                textposition="outside",
            ))
        fig.update_layout(title="Clicks (클릭수)", yaxis_title="회", barmode="group", height=420)
        st.plotly_chart(fig, use_container_width=True)

    # WoW 변화율
    st.markdown("#### WoW 변화율")
    col5, col6, col7 = st.columns(3)
    with col5:
        st.plotly_chart(make_wow_bar(df, "Impressions", "Impressions WoW"), use_container_width=True)
    with col6:
        st.plotly_chart(make_wow_bar(df, "Clicks", "Clicks WoW"), use_container_width=True)
    with col7:
        st.plotly_chart(make_wow_bar(df, "Cost", "Cost WoW"), use_container_width=True)


# ──────────────── 가입 탭 ────────────────
with tab2:
    st.subheader("가입 지표")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            make_grouped_bar(filtered_df, "가입 CVR", "가입 CVR (회원가입 / Clicks)", "%", suffix="%"),
            use_container_width=True,
        )
    with col2:
        st.plotly_chart(
            make_grouped_bar(filtered_df, "가입 CPA", "가입 CPA (Cost / 회원가입)", "원", suffix="원"),
            use_container_width=True,
        )

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(
            make_grouped_bar(filtered_df, "회원가입", "회원가입 수", "명"),
            use_container_width=True,
        )
    with col4:
        st.plotly_chart(make_wow_bar(df, "회원가입", "회원가입 WoW"), use_container_width=True)


# ──────────────── 가입→구매 탭 ────────────────
with tab3:
    st.subheader("가입 → 구매 전환율")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            make_grouped_bar(filtered_df, "가입→구매 CVR", "가입→구매 CVR", "%", suffix="%"),
            use_container_width=True,
        )

    with col2:
        # 퍼널 시각화: 가입 → 구매 비교
        fig = go.Figure()
        for ch in selected_channels:
            ch_data = df[df["채널"] == ch]
            w2 = ch_data[ch_data["주차"] == "W2"].iloc[0]
            fig.add_trace(go.Funnel(
                name=ch,
                y=["클릭", "회원가입", "구매완료"],
                x=[int(w2["Clicks"]), int(w2["회원가입"]), int(w2["구매완료"])],
                marker_color=COLORS[ch],
                textinfo="value+percent previous",
            ))
        fig.update_layout(title="W2 전환 퍼널 (클릭→가입→구매)", height=420)
        st.plotly_chart(fig, use_container_width=True)

    # 채널별 가입→구매 비교 인사이트
    st.markdown("---")
    col_g, col_f = st.columns(2)
    g_df = df[df["채널"] == "Google"]
    f_df = df[df["채널"] == "Facebook"]
    with col_g:
        g_w1 = g_df[g_df["주차"] == "W1"].iloc[0]
        g_w2 = g_df[g_df["주차"] == "W2"].iloc[0]
        st.metric("Google 가입→구매 CVR", f"{g_w2['가입→구매 CVR']:.1f}%",
                  delta=f"{g_w2['가입→구매 CVR'] - g_w1['가입→구매 CVR']:+.1f}%p")
    with col_f:
        f_w1 = f_df[f_df["주차"] == "W1"].iloc[0]
        f_w2 = f_df[f_df["주차"] == "W2"].iloc[0]
        st.metric("Facebook 가입→구매 CVR", f"{f_w2['가입→구매 CVR']:.1f}%",
                  delta=f"{f_w2['가입→구매 CVR'] - f_w1['가입→구매 CVR']:+.1f}%p")


# ──────────────── 구매 탭 ────────────────
with tab4:
    st.subheader("구매 지표")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            make_grouped_bar(filtered_df, "구매 CVR", "구매 CVR (구매완료 / Clicks)", "%", suffix="%"),
            use_container_width=True,
        )
    with col2:
        st.plotly_chart(
            make_grouped_bar(filtered_df, "구매 CPA", "구매 CPA (Cost / 구매완료)", "원", suffix="원"),
            use_container_width=True,
        )

    col3, col4 = st.columns(2)
    with col3:
        # ROAS 비교 (손익분기선 포함)
        fig = make_grouped_bar(filtered_df, "ROAS", "ROAS (구매액 / Cost)", "%", suffix="%")
        fig.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="손익분기 100%")
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.plotly_chart(
            make_grouped_bar(filtered_df, "ARPPU", "ARPPU (구매액 / 구매유저수)", "원", suffix="원"),
            use_container_width=True,
        )

    # 구매액 vs Cost 비교
    st.markdown("#### 구매액 vs Cost 비교")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    for ch in selected_channels:
        ch_data = df[df["채널"] == ch]
        x_labels = [f"{ch}<br>{w}" for w in ch_data["주차"]]
        fig.add_trace(go.Bar(
            name=f"{ch} 구매액", x=x_labels,
            y=ch_data["구매액"].values, marker_color=COLORS[ch], opacity=0.8,
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            name=f"{ch} Cost", x=x_labels,
            y=ch_data["Cost"].values, mode="markers+lines",
            marker=dict(size=10, color=COLORS[ch]), line=dict(dash="dot"),
        ), secondary_y=True)
    fig.update_layout(title="채널별 구매액(막대) vs Cost(점선)", height=450, barmode="group")
    fig.update_yaxes(title_text="구매액 (원)", secondary_y=False)
    fig.update_yaxes(title_text="Cost (원)", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)

    # WoW 변화율
    st.markdown("#### 구매 지표 WoW 변화율")
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.plotly_chart(make_wow_bar(df, "구매완료", "구매완료 WoW"), use_container_width=True)
    with col6:
        st.plotly_chart(make_wow_bar(df, "구매액", "구매액 WoW"), use_container_width=True)
    with col7:
        st.plotly_chart(make_wow_bar(df, "ROAS", "ROAS WoW"), use_container_width=True)
    with col8:
        st.plotly_chart(make_wow_bar(df, "구매 CPA", "CPA WoW"), use_container_width=True)


# ──────────────── 설치·앱구매 탭 ────────────────
with tab5:
    st.subheader("설치 & 앱구매 지표")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            make_grouped_bar(filtered_df, "CPI", "CPI (설치당 비용)", "원", suffix="원"),
            use_container_width=True,
        )
    with col2:
        st.plotly_chart(
            make_grouped_bar(filtered_df, "인앱구매유저수", "인앱 구매 유저 수", "명"),
            use_container_width=True,
        )

    st.info("💡 첫 구매 완료(App) 데이터는 쿼리 타임아웃으로 이번 분석에서 제외되었습니다.")


# ──────────────── 메타 소재별 탭 ────────────────
with tab_cr:
    st.subheader("🎨 메타(Facebook) 광고소재별 성과")
    st.caption("Airbridge 전환 데이터 기준 | 노출·클릭·비용은 소재 단위 미적재")

    # W2 기준 소재별 구매액 순위
    cr_w2 = cr_df[cr_df["주차"] == "W2"].copy()
    cr_w1 = cr_df[cr_df["주차"] == "W1"].copy()

    # ── KPI 카드: 소재 수, 총 구매액, 상위 소재 점유율 ──
    total_rev_w2 = cr_w2["구매액"].sum()
    top_rev_w2 = cr_w2.sort_values("구매액", ascending=False).iloc[0]
    top_share = top_rev_w2["구매액"] / total_rev_w2 * 100 if total_rev_w2 > 0 else 0
    active_count = len(cr_w2[cr_w2["구매건"] > 0])

    kc1, kc2, kc3, kc4 = st.columns(4)
    with kc1:
        st.metric("활성 소재 수 (W2)", f"{active_count}개")
    with kc2:
        st.metric("총 구매액 (W2)", f"{total_rev_w2:,.0f}원")
    with kc3:
        st.metric("1위 소재", top_rev_w2["소재(짧은이름)"][:18])
    with kc4:
        st.metric("1위 점유율", f"{top_share:.1f}%")

    st.markdown("---")

    # ── 차트 1: 소재별 구매액 W1 vs W2 ──
    col1, col2 = st.columns(2)

    with col1:
        # 소재별 구매액 비교 (W1 vs W2)
        cr_pivot = cr_df.pivot_table(index="소재(짧은이름)", columns="주차", values="구매액", aggfunc="sum").fillna(0)
        cr_pivot = cr_pivot.sort_values("W2", ascending=True)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="W1", y=cr_pivot.index, x=cr_pivot.get("W1", 0),
            orientation="h", marker_color=WEEK_COLORS["W1"],
            text=[f"{v:,.0f}원" for v in cr_pivot.get("W1", [0] * len(cr_pivot))],
            textposition="outside",
        ))
        fig.add_trace(go.Bar(
            name="W2", y=cr_pivot.index, x=cr_pivot.get("W2", 0),
            orientation="h", marker_color=WEEK_COLORS["W2"],
            text=[f"{v:,.0f}원" for v in cr_pivot.get("W2", [0] * len(cr_pivot))],
            textposition="outside",
        ))
        fig.update_layout(
            title="소재별 구매액 (W1 vs W2)",
            xaxis_title="구매액 (원)",
            barmode="group", height=500,
            margin=dict(l=200),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # W2 구매액 점유율 파이 차트
        cr_w2_sorted = cr_w2[cr_w2["구매액"] > 0].sort_values("구매액", ascending=False)
        fig = go.Figure(data=[go.Pie(
            labels=cr_w2_sorted["소재(짧은이름)"],
            values=cr_w2_sorted["구매액"],
            textinfo="label+percent",
            marker_colors=["#FF6B6B", "#5B8FF9", "#61DDAA", "#F6BD16", "#7262FD", "#78D3F8"],
            hole=0.4,
        )])
        fig.update_layout(title="W2 소재별 구매액 점유율", height=500)
        st.plotly_chart(fig, use_container_width=True)

    # ── 차트 2: 소재별 구매건·구매유저·가입 비교 ──
    st.markdown("#### 소재별 전환 지표 비교 (W2)")
    col3, col4 = st.columns(2)

    with col3:
        cr_w2_chart = cr_w2.sort_values("구매건", ascending=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="구매건", y=cr_w2_chart["소재(짧은이름)"], x=cr_w2_chart["구매건"],
            orientation="h", marker_color="#FF6B6B",
            text=[f"{int(v)}건" for v in cr_w2_chart["구매건"]], textposition="outside",
        ))
        fig.add_trace(go.Bar(
            name="구매유저", y=cr_w2_chart["소재(짧은이름)"], x=cr_w2_chart["구매유저"],
            orientation="h", marker_color="#5B8FF9",
            text=[f"{int(v)}명" for v in cr_w2_chart["구매유저"]], textposition="outside",
        ))
        fig.update_layout(title="소재별 구매건 & 구매유저 (W2)", barmode="group", height=450, margin=dict(l=200))
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        cr_w2_chart2 = cr_w2.sort_values("가입", ascending=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="가입", y=cr_w2_chart2["소재(짧은이름)"], x=cr_w2_chart2["가입"],
            orientation="h", marker_color="#61DDAA",
            text=[f"{int(v)}명" for v in cr_w2_chart2["가입"]], textposition="outside",
        ))
        fig.add_trace(go.Bar(
            name="앱설치", y=cr_w2_chart2["소재(짧은이름)"], x=cr_w2_chart2["앱설치"],
            orientation="h", marker_color="#F6BD16",
            text=[f"{int(v)}건" for v in cr_w2_chart2["앱설치"]], textposition="outside",
        ))
        fig.update_layout(title="소재별 가입 & 앱설치 (W2)", barmode="group", height=450, margin=dict(l=200))
        st.plotly_chart(fig, use_container_width=True)

    # ── 차트 3: 소재유형별 비교 ──
    st.markdown("#### 소재유형별 성과 비교 (W2)")
    type_summary = cr_w2.groupby("소재유형").agg(
        구매건=("구매건", "sum"),
        구매액=("구매액", "sum"),
        가입=("가입", "sum"),
        앱설치=("앱설치", "sum"),
        구매유저=("구매유저", "sum"),
    ).reset_index()

    col5, col6 = st.columns(2)
    with col5:
        fig = go.Figure(data=[go.Bar(
            x=type_summary["소재유형"],
            y=type_summary["구매액"],
            marker_color=["#FF6B6B", "#5B8FF9"],
            text=[f"{v:,.0f}원" for v in type_summary["구매액"]],
            textposition="outside",
        )])
        fig.update_layout(title="소재유형별 구매액 (W2)", yaxis_title="원", height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col6:
        fig = go.Figure(data=[go.Bar(
            x=type_summary["소재유형"],
            y=type_summary["구매건"],
            marker_color=["#FF6B6B", "#5B8FF9"],
            text=[f"{int(v)}건" for v in type_summary["구매건"]],
            textposition="outside",
        )])
        fig.update_layout(title="소재유형별 구매건 (W2)", yaxis_title="건", height=350)
        st.plotly_chart(fig, use_container_width=True)

    # ── 소재별 WoW 변화 테이블 ──
    st.markdown("#### 소재별 W1 → W2 상세 데이터")
    creative_names = cr_df["소재명"].unique()
    wow_rows = []
    for name in creative_names:
        w1_data = cr_df[(cr_df["소재명"] == name) & (cr_df["주차"] == "W1")].iloc[0]
        w2_data = cr_df[(cr_df["소재명"] == name) & (cr_df["주차"] == "W2")].iloc[0]
        wow_rev = f"{wow_pct(w1_data['구매액'], w2_data['구매액']):+.1f}%" if w1_data["구매액"] > 0 else ("신규" if w2_data["구매액"] > 0 else "-")
        wow_rows.append({
            "소재명": name,
            "유형": w1_data["소재유형"],
            "W1 가입": int(w1_data["가입"]),
            "W2 가입": int(w2_data["가입"]),
            "W1 앱설치": int(w1_data["앱설치"]),
            "W2 앱설치": int(w2_data["앱설치"]),
            "W1 구매건": int(w1_data["구매건"]),
            "W2 구매건": int(w2_data["구매건"]),
            "W1 구매유저": int(w1_data["구매유저"]),
            "W2 구매유저": int(w2_data["구매유저"]),
            "W1 구매액": f"{w1_data['구매액']:,.0f}원",
            "W2 구매액": f"{w2_data['구매액']:,.0f}원",
            "구매액 WoW": wow_rev,
        })
    wow_cr_df = pd.DataFrame(wow_rows)
    st.dataframe(wow_cr_df, use_container_width=True, hide_index=True, height=400)

    st.info("💡 노출·클릭·비용 데이터는 현재 광고그룹(ad_group) 단위까지만 적재되어 있어 소재 단위 CTR·CPC·ROAS·CPA는 산출할 수 없습니다.")


# ──────────────── 채널 비교 탭 ────────────────
with tab6:
    st.subheader("Google vs Facebook 종합 비교 (W2 기준)")

    g_w2 = df[(df["채널"] == "Google") & (df["주차"] == "W2")].iloc[0]
    f_w2 = df[(df["채널"] == "Facebook") & (df["주차"] == "W2")].iloc[0]

    # 레이더 차트 (정규화)
    categories = ["CTR", "가입 CVR", "가입→구매 CVR", "구매 CVR", "ROAS (÷100)", "ARPPU (÷1000)"]
    g_vals = [g_w2["CTR"], g_w2["가입 CVR"], g_w2["가입→구매 CVR"],
              g_w2["구매 CVR"], g_w2["ROAS"] / 100, g_w2["ARPPU"] / 1000]
    f_vals = [f_w2["CTR"], f_w2["가입 CVR"], f_w2["가입→구매 CVR"],
              f_w2["구매 CVR"], f_w2["ROAS"] / 100, f_w2["ARPPU"] / 1000]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=g_vals + [g_vals[0]], theta=categories + [categories[0]],
        fill="toself", name="Google", line_color=COLORS["Google"], opacity=0.6,
    ))
    fig.add_trace(go.Scatterpolar(
        r=f_vals + [f_vals[0]], theta=categories + [categories[0]],
        fill="toself", name="Facebook", line_color=COLORS["Facebook"], opacity=0.6,
    ))
    fig.update_layout(
        title="W2 채널별 효율 비교 (레이더 차트)",
        polar=dict(radialaxis=dict(visible=True)),
        height=500,
    )
    st.plotly_chart(fig, use_container_width=True)

    # 비용 대비 성과 산점도
    st.markdown("#### 비용 대비 성과 (W1→W2 추이)")
    fig = go.Figure()
    for ch in CHANNELS:
        ch_data = df[df["채널"] == ch]
        for _, row in ch_data.iterrows():
            fig.add_trace(go.Scatter(
                x=[row["Cost"]],
                y=[row["ROAS"]],
                mode="markers+text",
                name=f"{ch} {row['주차']}",
                marker=dict(
                    size=row["구매액"] / 500_000 + 10,
                    color=COLORS[ch],
                    opacity=0.9 if row["주차"] == "W2" else 0.4,
                    line=dict(width=2, color="white"),
                ),
                text=f"{ch[:2]} {row['주차']}",
                textposition="top center",
            ))
    fig.update_layout(
        title="Cost vs ROAS (버블 크기 = 구매액)",
        xaxis_title="Cost (원)",
        yaxis_title="ROAS (%)",
        height=500,
        showlegend=True,
    )
    fig.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="손익분기")
    st.plotly_chart(fig, use_container_width=True)

    # 주요 비교표
    st.markdown("#### 핵심 지표 비교표 (W2)")
    compare_data = {
        "지표": ["Cost", "Impressions", "Clicks", "CTR", "CPC",
                 "회원가입", "가입 CVR", "가입 CPA",
                 "가입→구매 CVR",
                 "구매완료", "구매액", "구매 CVR", "구매 CPA", "ROAS", "ARPPU",
                 "CPI", "인앱구매유저수"],
        "Google": [
            f"{g_w2['Cost']:,.0f}원", f"{g_w2['Impressions']:,.0f}", f"{g_w2['Clicks']:,.0f}",
            f"{g_w2['CTR']:.2f}%", f"{g_w2['CPC']:,.0f}원",
            f"{int(g_w2['회원가입']):,}명", f"{g_w2['가입 CVR']:.2f}%", f"{g_w2['가입 CPA']:,.0f}원",
            f"{g_w2['가입→구매 CVR']:.2f}%",
            f"{int(g_w2['구매완료']):,}건", f"{g_w2['구매액']:,.0f}원",
            f"{g_w2['구매 CVR']:.2f}%", f"{g_w2['구매 CPA']:,.0f}원",
            f"{g_w2['ROAS']:.1f}%", f"{g_w2['ARPPU']:,.0f}원",
            f"{g_w2['CPI']:,.0f}원", f"{int(g_w2['인앱구매유저수']):,}명",
        ],
        "Facebook": [
            f"{f_w2['Cost']:,.0f}원", f"{f_w2['Impressions']:,.0f}", f"{f_w2['Clicks']:,.0f}",
            f"{f_w2['CTR']:.2f}%", f"{f_w2['CPC']:,.0f}원",
            f"{int(f_w2['회원가입']):,}명", f"{f_w2['가입 CVR']:.2f}%", f"{f_w2['가입 CPA']:,.0f}원",
            f"{f_w2['가입→구매 CVR']:.2f}%",
            f"{int(f_w2['구매완료']):,}건", f"{f_w2['구매액']:,.0f}원",
            f"{f_w2['구매 CVR']:.2f}%", f"{f_w2['구매 CPA']:,.0f}원",
            f"{f_w2['ROAS']:.1f}%", f"{f_w2['ARPPU']:,.0f}원",
            f"{f_w2['CPI']:,.0f}원", f"{int(f_w2['인앱구매유저수']):,}명",
        ],
    }
    st.dataframe(pd.DataFrame(compare_data), use_container_width=True, hide_index=True, height=650)


# ──────────────── 원본 데이터 탭 ────────────────
with tab7:
    st.subheader("원본 데이터")

    display_df = filtered_df.copy()
    won_cols = ["Cost", "구매액", "가입 CPA", "구매 CPA", "ARPPU", "CPC", "CPI"]
    pct_cols = ["CTR", "가입 CVR", "가입→구매 CVR", "구매 CVR", "ROAS"]

    for c in won_cols:
        if c in display_df.columns:
            display_df[c] = display_df[c].apply(lambda x: f"{x:,.0f}원")
    for c in pct_cols:
        if c in display_df.columns:
            display_df[c] = display_df[c].apply(lambda x: f"{x:.2f}%")
    for c in ["Impressions", "Clicks", "회원가입", "구매완료", "구매유저(App)", "구매유저(Web)", "구매유저 합계", "인앱구매유저수"]:
        if c in display_df.columns:
            display_df[c] = display_df[c].apply(lambda x: f"{x:,.0f}")

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # WoW 증감률 테이블
    st.markdown("#### W1 → W2 증감률")
    change_data = []
    metrics = [
        ("Impressions", "int"), ("Clicks", "int"), ("Cost", "won"),
        ("회원가입", "int"), ("구매완료", "int"), ("구매액", "won"),
        ("CTR", "pct"), ("CPC", "won"), ("가입 CVR", "pct"), ("가입 CPA", "won"),
        ("가입→구매 CVR", "pct"), ("구매 CVR", "pct"), ("구매 CPA", "won"),
        ("ROAS", "pct"), ("ARPPU", "won"), ("CPI", "won"),
    ]
    for ch in CHANNELS:
        row = {"채널": ch}
        ch_data = df[df["채널"] == ch]
        w1_row = ch_data[ch_data["주차"] == "W1"].iloc[0]
        w2_row = ch_data[ch_data["주차"] == "W2"].iloc[0]
        for metric, _ in metrics:
            v1, v2 = w1_row[metric], w2_row[metric]
            pct = wow_pct(v1, v2)
            row[metric] = f"{pct:+.1f}%" if isinstance(pct, (int, float)) else "N/A"
        change_data.append(row)

    change_df = pd.DataFrame(change_data)
    st.dataframe(change_df, use_container_width=True, hide_index=True)


# ──────────────────────────────────────────────
# 인사이트 섹션
# ──────────────────────────────────────────────
st.markdown("---")
st.subheader("💡 핵심 인사이트")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Google")
    st.markdown("""
    **볼륨 ↑ 효율 ↓**
    - 예산 +77.5% 증액 → 노출·클릭 약 2배
    - ROAS 682% → 433% (**-36.5%**)
    - 구매 CPA 8,322원 → 13,026원 (**+56.5%**)
    - 구매 CVR 5.51% → 3.10% (**-43.7%**)
    - 확장된 트래픽의 품질이 낮았음을 시사
    """)
    st.warning("⚠️ 효율이 낮은 광고그룹 OFF 또는 W1 수준 예산으로 조정 필요")

with col2:
    st.markdown("#### Facebook")
    st.markdown("""
    **비용 유지, 효율 개선**
    - 비용 -1.2% (거의 동일)
    - ROAS 272% → 368% (**+35.4%**)
    - 구매 CPA 23,305원 → 19,623원 (**-15.8%**)
    - 가입→구매 CVR 25.8% → 32.2% (**+25.1%**)
    - ARPPU 71,974원 → 89,665원 (**+24.6%**)
    """)
    st.success("✅ 현 소재/타겟 유지 + 소폭 예산 증액 테스트 권장")

st.markdown("---")
st.subheader("📌 다음 스프린트 제안")
st.markdown("""
1. **Google 광고그룹 최적화** — W1/W2 광고그룹별 ROAS 비교 → 효율 낮은 그룹 OFF
2. **Facebook 예산 증액 테스트** — 현 효율 유지 여부 확인하며 10~20% 단계적 증액
3. **Google ARPPU 하락 원인** — 구매 상품 카테고리/할인율 변화 추가 분석
4. **Facebook 소재 분석** — W2에 잘 작동한 소재 식별 → 유사 소재 추가 제작
""")
