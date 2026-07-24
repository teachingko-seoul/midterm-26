import base64
from pathlib import Path

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['axes.unicode_minus'] = False

# 한글 폰트 직접 불러오기
FONT_PATH = Path(__file__).resolve().parent.parent / "fonts" / "NotoSansKR-Bold.ttf"
if FONT_PATH.exists():
    matplotlib.font_manager.fontManager.addfont(str(FONT_PATH))
    font_name = matplotlib.font_manager.FontProperties(fname=str(FONT_PATH)).get_name()
    matplotlib.rcParams['font.family'] = font_name
    matplotlib.rcParams['font.sans-serif'] = [font_name]
else:
    font_name = None

st.set_page_config(page_title="좌표평면과 그래프", page_icon="📈", layout="wide")

if FONT_PATH.exists():
    with open(FONT_PATH, "rb") as f:
        font_data = base64.b64encode(f.read()).decode("utf-8")
    st.markdown(
        f"""
        <style>
        @font-face {{
            font-family: 'Noto Sans KR';
            src: url("data:font/ttf;base64,{font_data}") format("truetype");
            font-weight: bold;
            font-style: normal;
        }}
        html, body, [class*="css"] {{
            font-family: 'Noto Sans KR', sans-serif !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# 사이드바 메뉴
# ---------------------------------------------------------
menu = st.sidebar.radio(
    "메뉴 선택",
    ["🏠 단원 소개", "📘 수업 자료", "📝 평가 퀴즈"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**중학교 1학년 수학**")
st.sidebar.markdown("좌표평면과 그래프 단원")
st.sidebar.markdown("""
- [9수02-05] 순서쌍과 좌표
- [9수02-06] 그래프 나타내기·해석
- [9수02-07] 정비례·반비례
""")

# ===========================================================
# 1. 단원 소개
# ===========================================================
if menu == "🏠 단원 소개":
    st.title("📈 좌표평면과 그래프")
    st.markdown("### 중학교 1학년 수학 · 함수 영역")

    st.info("""
    이 단원에서는 순서쌍과 좌표평면의 개념을 이해하고, 여러 가지 상황을 그래프로 표현·해석하며,
    정비례와 반비례 관계를 표·식·그래프로 나타내는 능력을 기릅니다.
    """)

    st.markdown("## 🎯 성취기준")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("**[9수02-05]**\n\n순서쌍과 좌표를 이해하고, 그 편리함을 인식할 수 있다.")
    with col2:
        st.success("**[9수02-06]**\n\n다양한 상황을 그래프로 나타내고, 주어진 그래프를 해석할 수 있다.")
    with col3:
        st.success("**[9수02-07]**\n\n정비례, 반비례 관계를 이해하고, 그 관계를 표, 식, 그래프로 나타낼 수 있다.")

    st.markdown("## 🗂️ 단원 구성")
    st.markdown("""
    | 차시 | 학습 내용 | 관련 성취기준 |
    |---|---|---|
    | 1차시 | 순서쌍과 좌표, 좌표평면 | 9수02-05 |
    | 2차시 | 사분면과 좌표축 위의 점 | 9수02-05 |
    | 3차시 | 그래프와 그 해석 | 9수02-06 |
    | 4차시 | 정비례 관계와 그 그래프 | 9수02-07 |
    | 5차시 | 반비례 관계와 그 그래프 | 9수02-07 |
    | 6차시 | 종합 평가(퀴즈) | 9수02-05~07 |
    """)

    st.markdown("왼쪽 메뉴에서 **📘 수업 자료**를 눌러 학습을 시작하거나, **📝 평가 퀴즈**로 이동해 실력을 확인해보세요!")

# ===========================================================
# 2. 수업 자료
# ===========================================================
elif menu == "📘 수업 자료":
    st.title("📘 수업 자료: 좌표평면과 그래프")

    tab1, tab2, tab3 = st.tabs([
        "① 순서쌍과 좌표 (9수02-05)",
        "② 그래프와 해석 (9수02-06)",
        "③ 정비례·반비례 (9수02-07)"
    ])

    # -------------------------------------------------
    # ① 순서쌍과 좌표
    # -------------------------------------------------
    with tab1:
        st.header("① 순서쌍과 좌표")

        st.subheader("1. 순서쌍")
        st.markdown("""
        두 수 $a$, $b$의 순서를 정하여 짝지어 나타낸 것을 **순서쌍**이라 하고, 기호로
        $(a,\\ b)$와 같이 나타냅니다.

        - 순서쌍은 **두 수의 나열 순서가 의미를 가집니다.** 즉, $a \\ne b$이면 $(a, b) \\ne (b, a)$입니다.
        - 예를 들어 지도에서 위치를 나타낼 때 (가로, 세로) 순서로 표현하는 것처럼, 순서쌍은 두 정보를 **하나로 압축하여 정확한 위치를 나타내는 편리함**이 있습니다.
        """)

        st.subheader("2. 좌표평면")
        st.markdown("""
        평면 위에 서로 수직으로 만나는 두 수직선을 그릴 때,
        - 가로의 수직선을 **$x$축**
        - 세로의 수직선을 **$y$축**
        - 두 축이 만나는 점을 **원점 $O$**

        라고 하며, $x$축과 $y$축을 통틀어 **좌표축**이라 하고, 좌표축이 그려진 평면을 **좌표평면**이라 합니다.
        """)

        st.subheader("3. 점의 좌표")
        st.markdown("""
        좌표평면 위의 점 P에서 $x$축, $y$축에 각각 수선을 내려 만나는 값을 $a$, $b$라 할 때,
        순서쌍 $(a, b)$를 점 P의 **좌표**라 하고 P$(a, b)$로 나타냅니다.
        - $a$:점 P의 **$x$좌표**
        - $b$:점 P의 **$y$좌표**

        > 좌표를 이용하면 평면 위의 모든 점의 위치를 **하나의 순서쌍만으로 정확하고 간단하게** 표현할 수 있다는 편리함이 있습니다.
        """)

        # 좌표평면 예시 그림
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        points = {"A(3,2)": (3, 2), "B(-2,4)": (-2, 4), "C(-3,-3)": (-3, -3), "D(4,-2)": (4, -2)}
        for label, (x, y) in points.items():
            ax.plot(x, y, 'o', color='crimson')
            ax.annotate(label, (x, y), textcoords="offset points", xytext=(8, 5))
        ax.set_xlim(-6, 6)
        ax.set_ylim(-6, 6)
        ax.set_xticks(range(-6, 7))
        ax.set_yticks(range(-6, 7))
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.set_title("좌표평면 위의 점")
        st.pyplot(fig)

        st.subheader("4. 사분면")
        st.markdown("""
        좌표축에 의하여 좌표평면은 네 부분으로 나누어지며, 이를 각각 제1사분면, 제2사분면, 제3사분면, 제4사분면이라 합니다.

        | 사분면 | $x$좌표 부호 | $y$좌표 부호 |
        |---|---|---|
        | 제1사분면 | + | + |
        | 제2사분면 | − | + |
        | 제3사분면 | − | − |
        | 제4사분면 | + | − |

        ⚠️ **주의:** 좌표축 위의 점(예: $(3, 0)$, $(0, -5)$, 원점 $(0,0)$)은 어느 사분면에도 속하지 않습니다.
        """)

    # -------------------------------------------------
    # ② 그래프와 해석
    # -------------------------------------------------
    with tab2:
        st.header("② 그래프와 그 해석")

        st.subheader("1. 그래프란?")
        st.markdown("""
        서로 관련 있는 두 양의 변화 관계를 좌표평면 위에 점, 직선, 곡선 등으로 나타낸 것을 **그래프**라 합니다.

        - 시간에 따른 온도, 속력, 물의 높이 변화 등 **실생활의 다양한 상황**을 그래프로 나타낼 수 있습니다.
        - 그래프를 이용하면 두 양 사이의 변화 상태(증가, 감소, 일정 등)를 **한눈에 파악**할 수 있는 편리함이 있습니다.
        """)

        st.subheader("2. 그래프 해석하기")
        st.markdown("""
        그래프를 해석할 때는 다음을 살펴봅니다.
        - **가로축과 세로축이 나타내는 양**이 무엇인지 확인한다.
        - 그래프가 **오른쪽 위로 향하면 증가**, **오른쪽 아래로 향하면 감소**, **수평이면 일정**함을 나타낸다.
        - 그래프의 **기울기가 가파를수록 변화가 빠르다**는 것을 의미한다.
        """)

        st.markdown("**예시: 컵에 일정한 속도로 물을 채울 때 시간에 따른 물의 높이**")
        t = np.linspace(0, 10, 100)
        h = 2 * t
        fig2, ax2 = plt.subplots(figsize=(5, 3.5))
        ax2.plot(t, h, color='royalblue', linewidth=2)
        ax2.set_xlabel("시간 (분)")
        ax2.set_ylabel("물의 높이 (cm)")
        ax2.set_title("시간에 따른 물의 높이 변화")
        ax2.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig2)

        st.markdown("""
        위 그래프는 시간이 지날수록 물의 높이가 **일정한 속도로 증가**하고 있음을 보여줍니다.
        만약 물을 채우다가 잠시 멈춘다면 그래프는 어떤 구간에서 **수평(일정)**이 되겠지요?
        이처럼 그래프의 모양을 통해 상황을 유추하는 것이 그래프 해석의 핵심입니다.
        """)

        st.subheader("3. 상황을 그래프로 나타내기")
        st.markdown("""
        반대로, 주어진 상황(이야기)을 보고 변화 양상을 그래프로 표현할 수도 있습니다.
        - 상황에서 **변하는 두 양**을 찾는다.
        - 각 양을 $x$축, $y$축으로 정한다.
        - 시간(상황)의 흐름에 따라 각 양이 **증가/감소/일정**하는지 파악하여 그래프의 개형을 그린다.
        """)

    # -------------------------------------------------
    # ③ 정비례·반비례
    # -------------------------------------------------
    with tab3:
        st.header("③ 정비례와 반비례")

        st.subheader("1. 정비례 관계")
        st.markdown("""
        두 변수 $x$, $y$에 대하여 $x$의 값이 2배, 3배, 4배, $\\cdots$ 로 변함에 따라
        $y$의 값도 2배, 3배, 4배, $\\cdots$ 로 변하는 관계를 **정비례 관계**라 합니다.

        - **식**: $y = ax$ (단, $a \\ne 0$인 상수)
        - **표**: $x$의 값이 커질수록 $y$의 값도 일정한 비율로 커집니다.
        - **그래프**: **원점을 지나는 직선**입니다.
          - $a > 0$이면 오른쪽 위로 향하는 직선 (제1, 3사분면 통과)
          - $a < 0$이면 오른쪽 아래로 향하는 직선 (제2, 4사분면 통과)
        """)

        colp1, colp2 = st.columns(2)
        with colp1:
            x = np.linspace(-5, 5, 100)
            fig3, ax3 = plt.subplots(figsize=(4.5, 4.5))
            ax3.axhline(0, color='black', linewidth=0.8)
            ax3.axvline(0, color='black', linewidth=0.8)
            ax3.plot(x, 2 * x, label="y = 2x", color='crimson')
            ax3.plot(x, -1.5 * x, label="y = -1.5x", color='seagreen')
            ax3.set_xlim(-5, 5)
            ax3.set_ylim(-8, 8)
            ax3.legend()
            ax3.grid(True, linestyle='--', alpha=0.5)
            ax3.set_title("정비례 그래프 (원점을 지나는 직선)")
            st.pyplot(fig3)

        st.subheader("2. 반비례 관계")
        st.markdown("""
        두 변수 $x$, $y$에 대하여 $x$의 값이 2배, 3배, 4배, $\\cdots$ 로 변함에 따라
        $y$의 값은 $\\dfrac{1}{2}$배, $\\dfrac{1}{3}$배, $\\dfrac{1}{4}$배, $\\cdots$ 로 변하는 관계를 **반비례 관계**라 합니다.

        - **식**: $y = \\dfrac{a}{x}$ (단, $a \\ne 0$인 상수, $x \\ne 0$)
        - **표**: $x$와 $y$의 곱 $xy$의 값이 항상 일정하게($=a$) 유지됩니다.
        - **그래프**: **원점을 지나지 않는 한 쌍의 매끄러운 곡선**입니다.
          - $a > 0$이면 제1사분면과 제3사분면 위에 그려집니다.
          - $a < 0$이면 제2사분면과 제4사분면 위에 그려집니다.
        """)

        with colp2:
            xp = np.linspace(0.4, 6, 100)
            xn = np.linspace(-6, -0.4, 100)
            fig4, ax4 = plt.subplots(figsize=(4.5, 4.5))
            ax4.axhline(0, color='black', linewidth=0.8)
            ax4.axvline(0, color='black', linewidth=0.8)
            ax4.plot(xp, 6 / xp, color='royalblue')
            ax4.plot(xn, 6 / xn, color='royalblue', label="y = 6/x")
            ax4.set_xlim(-6, 6)
            ax4.set_ylim(-15, 15)
            ax4.legend()
            ax4.grid(True, linestyle='--', alpha=0.5)
            ax4.set_title("반비례 그래프 (곡선)")
            st.pyplot(fig4)

        st.subheader("3. 정비례·반비례 비교")
        st.markdown("""
        | 구분 | 정비례 | 반비례 |
        |---|---|---|
        | 식 | $y = ax$ | $y = \\dfrac{a}{x}$ |
        | 그래프 모양 | 원점을 지나는 직선 | 원점을 지나지 않는 곡선 |
        | 특징 | $\\dfrac{y}{x} = a$ (일정) | $xy = a$ (일정) |
        """)

        st.info("💡 **상수 $a$ 구하는 법**: 그래프나 표에서 한 점 $(x_0, y_0)$을 알면, 정비례는 $a = \\dfrac{y_0}{x_0}$, 반비례는 $a = x_0 y_0$ 로 구할 수 있습니다.")

# ===========================================================
# 3. 평가 퀴즈
# ===========================================================
elif menu == "📝 평가 퀴즈":
    st.title("📝 평가 퀴즈: 좌표평면과 그래프")
    st.markdown("총 **10문제** (하 3문제 · 중 4문제 · 상 3문제)가 출제됩니다. 정답은 **숫자**로만 입력해주세요.")
    st.markdown("틀리면 **한 번 더** 도전할 수 있고, 두 번째도 틀리면 정답이 공개됩니다.")
    st.markdown("---")

    # 문제 목록: (난이도, 문제, 정답)
    questions = [
        ("하", "점 P(5, -3)의 y좌표는 얼마인가요?", -3),
        ("하", "점 Q(-2, -7)은 제 몇 사분면 위의 점인가요? (숫자만 입력, 예: 3)", 3),
        ("하", "정비례 관계 y = 4x에서 x = 3일 때, y의 값은 얼마인가요?", 12),
        ("중", "정비례 관계 y = -2x의 그래프가 점 (a, 8)을 지날 때, a의 값은 얼마인가요?", -4),
        ("중", "반비례 관계 y = 12/x 의 그래프가 점 (3, b)를 지날 때, b의 값은 얼마인가요?", 4),
        ("중", "정비례 관계 y = ax의 그래프가 점 (2, 10)을 지날 때, 상수 a의 값은 얼마인가요?", 5),
        ("중", "반비례 관계 y = a/x 의 그래프가 점 (4, 5)를 지날 때, 상수 a의 값은 얼마인가요?", 20),
        ("상", "정비례 관계 y = ax 와 반비례 관계 y = b/x 의 그래프가 모두 점 (2, 6)을 지날 때, a + b의 값은 얼마인가요?", 15),
        ("상", "반비례 관계 y = 36/x 의 그래프 위의 점 중 x좌표와 y좌표가 같은 자연수인 점이 있습니다. 이 점의 x좌표는 얼마인가요?", 6),
        ("상", "정비례 관계 y = 3x 와 반비례 관계 y = 12/x 의 그래프의 교점 중 x > 0인 점의 x좌표는 얼마인가요?", 2),
    ]

    # 세션 상태 초기화
    if "attempts" not in st.session_state:
        st.session_state.attempts = [0] * len(questions)
    if "solved" not in st.session_state:
        st.session_state.solved = [False] * len(questions)

    difficulty_color = {"하": "🟢", "중": "🟡", "상": "🔴"}

    for i, (level, q_text, answer) in enumerate(questions):
        st.markdown(f"### 문제 {i+1}. {difficulty_color[level]} 난이도: {level}")
        st.markdown(q_text)

        user_input = st.text_input(
            f"정답을 입력하세요 (문제 {i+1})",
            key=f"input_{i}",
            disabled=st.session_state.solved[i]
        )

        submit = st.button("제출", key=f"submit_{i}", disabled=st.session_state.solved[i])

        if submit and not st.session_state.solved[i]:
            if user_input.strip() == "":
                st.warning("답을 입력한 후 제출해주세요.")
            else:
                try:
                    user_val = float(user_input)
                    is_correct = (user_val == float(answer))
                except ValueError:
                    is_correct = False

                if is_correct:
                    st.session_state.solved[i] = True
                else:
                    st.session_state.attempts[i] += 1

        # 결과 메시지 출력 (제출 이후 상태 유지)
        if st.session_state.solved[i]:
            st.success("✅ 정답입니다.")
        elif st.session_state.attempts[i] == 1:
            st.error("❌ 오답입니다. 다시 한번 입력해주세요.")
        elif st.session_state.attempts[i] >= 2:
            st.warning(f"정답은 **{answer}** 입니다.")
            st.session_state.solved[i] = True  # 두 번째 오답 이후 문제 종료 처리

        st.markdown("---")

    # 전체 진행 상황
    solved_count = sum(st.session_state.solved)
    st.markdown(f"## 📊 진행 상황: {solved_count} / {len(questions)} 문제 완료")
    st.progress(solved_count / len(questions))

    if solved_count == len(questions):
        st.balloons()
        st.success("🎉 모든 문제를 완료했습니다! 수고하셨습니다.")

    if st.button("🔄 퀴즈 다시 시작하기"):
        st.session_state.attempts = [0] * len(questions)
        st.session_state.solved = [False] * len(questions)
        st.rerun()