import streamlit as st
import subprocess
import os

st.set_page_config(
    page_title="스프린트 대시보드",
    page_icon="📋",
    layout="wide",
)

st.title("📋 스프린트 대시보드")
st.caption("W1 (3/23~3/29) vs W2 (3/30~4/5) | 마케팅 주간 분석 허브")

st.markdown("---")

# ──────────────────────────────────────────────
# 대시보드 목록
# ──────────────────────────────────────────────
DASHBOARDS = [
    {
        "name": "앱그로스 주간 성과 분석",
        "desc": "Google · Facebook 캠페인 비교, 소재별 성과, 채널 비교",
        "path": "앱그로스-주간분석",
        "port": 8502,
        "icon": "📱",
    },
    {
        "name": "카카오 주간 마케팅 분석",
        "desc": "카카오 캠페인별 성과, W1 vs W2 비교, 인사이트",
        "path": "카카오-주간분석",
        "port": 8503,
        "icon": "💛",
    },
    {
        "name": "카카오 광고그룹 ROAS",
        "desc": "카카오 광고그룹별 ROAS 상세 분석",
        "path": "카카오-광고그룹-ROAS",
        "port": 8504,
        "icon": "📊",
    },
    {
        "name": "카카오 UA 확장 전략",
        "desc": "카카오 · 메타 · 구글 UA 확장 전략, 갭 분석, 액션 플랜",
        "path": "카카오-UA확장전략",
        "port": 8505,
        "icon": "🎯",
    },
]

GITHUB_PAGES = "https://jasonjjeon.github.io/jason-sprint/dashboard"

# ──────────────────────────────────────────────
# GitHub Pages 링크
# ──────────────────────────────────────────────
st.subheader("🌐 GitHub Pages (외부 공유용)")
gh_cols = st.columns(3)
gh_links = [
    ("앱그로스 주간 성과 분석", f"{GITHUB_PAGES}/appgrowth.html"),
    ("카카오 주간 마케팅 분석", "https://jasonjjeon.github.io/pbtd-kakao-report/"),
    ("UA 확장 전략", f"{GITHUB_PAGES}/ua-strategy.html"),
]
for col, (name, url) in zip(gh_cols, gh_links):
    with col:
        st.markdown(
            f"""<a href="{url}" target="_blank" style="
                display:block; padding:16px; border-radius:8px;
                border:1px solid #334155; background:#1e293b;
                text-decoration:none; color:#e2e8f0; text-align:center;
                transition: border-color 0.2s;">
                <div style="font-size:16px; font-weight:700; margin-bottom:4px;">{name}</div>
                <div style="font-size:12px; color:#94a3b8;">클릭하면 새 탭에서 열립니다</div>
            </a>""",
            unsafe_allow_html=True,
        )

st.markdown("---")

# ──────────────────────────────────────────────
# Streamlit 대시보드 카드
# ──────────────────────────────────────────────
st.subheader("📊 Streamlit 대시보드 (상세 분석용)")

cols = st.columns(2)

for i, db in enumerate(DASHBOARDS):
    with cols[i % 2]:
        with st.container(border=True):
            st.markdown(f"### {db['icon']} {db['name']}")
            st.caption(db["desc"])

            url = f"http://localhost:{db['port']}"
            c1, c2 = st.columns(2)
            with c1:
                st.link_button("열기", url, use_container_width=True)
            with c2:
                if st.button("실행", key=f"run_{db['path']}", use_container_width=True):
                    app_path = os.path.join(
                        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        db["path"],
                        "app.py",
                    )
                    subprocess.Popen(
                        ["streamlit", "run", app_path, "--server.port", str(db["port"])],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    st.success(f"실행됨 → localhost:{db['port']}")

st.markdown("---")
st.caption("데이터 소스: DATA_DB > marketing_cost")
