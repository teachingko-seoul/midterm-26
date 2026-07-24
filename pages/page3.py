import streamlit as st
from fractions import Fraction

# ────────────────────────────────────────────────────────────
# 기본 설정
# ────────────────────────────────────────────────────────────
st.set_page_config(page_title="정수와 유리수", page_icon="🔢", layout="wide")


# ────────────────────────────────────────────────────────────
# 답 확인용 함수
# ────────────────────────────────────────────────────────────
def parse_number(text: str) -> float:
    """'-3/4', '0.5', '-2' 같은 입력을 float으로 변환"""
    text = text.strip().replace(" ", "")
    if text == "":
        raise ValueError("빈 입력")
    if "/" in text:
        return float(Fraction(text))
    return float(text)


def is_correct(user_text: str, answer: float, tol: float = 1e-6) -> bool:
    try:
        val = parse_number(user_text)
    except Exception:
        return False
    return abs(val - answer) < tol


# ────────────────────────────────────────────────────────────
# 퀴즈 문제 데이터 (10문제, 그 중 8~10번은 정수·유리수 사칙연산 종합문제)
# ────────────────────────────────────────────────────────────
QUESTIONS = [
    {
        "category": "개념",
        "question": "정수가 아닌 유리수 $-\\dfrac{3}{4}$ 을(를) 소수로 나타내면 얼마입니까?",
        "hint": "분수를 소수로 바꿔보세요. (예: 1/2 = 0.5)",
        "answer": -0.75,
        "answer_display": "-0.75",
    },
    {
        "category": "개념",
        "question": "$|-9|$ (절댓값)의 값을 구하시오.",
        "hint": "절댓값은 수직선에서 원점(0)으로부터 떨어진 거리입니다.",
        "answer": 9,
        "answer_display": "9",
    },
    {
        "category": "대소관계",
        "question": "$-5$ 와 $-8$ 중 더 큰 수를 쓰시오.",
        "hint": "음수끼리는 절댓값이 작을수록 더 큰 수입니다.",
        "answer": -5,
        "answer_display": "-5",
    },
    {
        "category": "덧셈",
        "question": "$(-7) + (+12)$ 를 계산하시오.",
        "hint": "부호가 다른 두 수의 덧셈: 절댓값의 차에 절댓값이 큰 수의 부호를 붙입니다.",
        "answer": 5,
        "answer_display": "5",
    },
    {
        "category": "뺄셈",
        "question": "$(+5) - (-9)$ 를 계산하시오.",
        "hint": "빼는 수의 부호를 바꾸어 덧셈으로 고쳐보세요.",
        "answer": 14,
        "answer_display": "14",
    },
    {
        "category": "곱셈",
        "question": "$(-6) \\times (-3)$ 을 계산하시오.",
        "hint": "부호가 같은 두 수의 곱은 양수입니다.",
        "answer": 18,
        "answer_display": "18",
    },
    {
        "category": "나눗셈",
        "question": "$(-15) \\div 5$ 를 계산하시오.",
        "hint": "부호가 다른 두 수의 나눗셈은 음수입니다.",
        "answer": -3,
        "answer_display": "-3",
    },
    {
        "category": "사칙연산 종합 ①",
        "question": "$(-3) + 4 \\times (-2)$ 를 계산하시오.",
        "hint": "곱셈을 먼저 계산한 후 덧셈을 하세요.",
        "answer": -11,
        "answer_display": "-11",
    },
    {
        "category": "사칙연산 종합 ②",
        "question": "$\\dfrac{1}{2} + \\dfrac{1}{4} \\times 2$ 를 계산하시오. (소수 또는 분수로 입력, 예: 0.5 또는 1/2)",
        "hint": "곱셈을 먼저 계산한 후 분수의 덧셈을 하세요.",
        "answer": 1,
        "answer_display": "1",
    },
    {
        "category": "사칙연산 종합 ③",
        "question": "$8 \\div (-2) - (-3) \\times 2$ 를 계산하시오.",
        "hint": "곱셈과 나눗셈을 먼저 계산한 후 뺄셈을 하세요.",
        "answer": 2,
        "answer_display": "2",
    },
]

MAX_ATTEMPTS = 3  # 총 3번 입력 기회 (2번 재시도 후 3번째 오답 시 정답 공개)


# ────────────────────────────────────────────────────────────
# 세션 상태 초기화
# ────────────────────────────────────────────────────────────
if "quiz_state" not in st.session_state:
    st.session_state.quiz_state = {
        i: {"attempts": 0, "solved": False, "correct_on_first": None}
        for i in range(len(QUESTIONS))
    }


def reset_quiz():
    st.session_state.quiz_state = {
        i: {"attempts": 0, "solved": False, "correct_on_first": None}
        for i in range(len(QUESTIONS))
    }


# ────────────────────────────────────────────────────────────
# 탭 구성
# ────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📖 학습자료 - 정수와 유리수", "✏️ 평가 (퀴즈)"])

# ════════════════════════════════════════════════════════════
# TAB 1. 학습자료
# ════════════════════════════════════════════════════════════
with tab1:
    st.title("🔢 정수와 유리수")
    st.caption("중학교 1학년 · 수와 연산")

    with st.expander("📌 성취기준 안내", expanded=True):
        st.markdown(
            """
- 다양한 상황을 이용하여 **음수의 필요성**을 인식하고, **양수와 음수, 정수와 유리수**의 개념을 이해한다.
- **정수와 유리수의 대소 관계**를 판단할 수 있다.
- **정수와 유리수의 사칙계산의 원리**를 이해하고 그 계산을 할 수 있다.
"""
        )

    st.header("1️⃣ 음수는 왜 필요할까요?")
    st.markdown(
        """
우리 생활 속에는 서로 반대되는 성질을 가진 양들이 많이 있습니다. 양수(+)만으로는 이런 상황을
표현하기 어렵기 때문에 **음수(-)** 가 필요합니다.

| 상황 | 기준 | 양수(+)로 표현 | 음수(-)로 표현 |
|---|---|---|---|
| 기온 | 영상/영하 | 영상 5℃ → +5℃ | 영하 3℃ → -3℃ |
| 높이 | 해발/해저 | 해발 100m → +100m | 해저 50m → -50m |
| 경제 | 수입/지출 | 수입 3만원 → +3만원 | 지출 2만원 → -2만원 |
| 시간 | 기준 시각의 전/후 | 3분 후 → +3분 | 2분 전 → -2분 |

이처럼 서로 반대되는 성질을 가지는 양은 기준을 0으로 잡고, 한쪽은 **양의 부호(+)**, 다른 한쪽은
**음의 부호(-)** 를 사용하여 나타냅니다.
"""
    )

    st.header("2️⃣ 양수와 음수")
    st.markdown(
        """
- **양수**: 0보다 큰 수. 양의 부호 `+`를 붙여 나타냅니다. (예: +2, +3.5, +1/2)
- **음수**: 0보다 작은 수. 음의 부호 `-`를 붙여 나타냅니다. (예: -2, -3.5, -1/2)
- 0은 양수도 아니고 음수도 아닙니다.
- 양의 부호 `+`는 생략할 수 있지만, 음의 부호 `-`는 생략할 수 없습니다.
"""
    )

    st.header("3️⃣ 정수")
    st.markdown(
        """
**정수**는 다음 세 가지로 이루어져 있습니다.

- **양의 정수(자연수)**: +1, +2, +3, … (양의 부호를 생략하여 1, 2, 3, …으로도 씀)
- **0**
- **음의 정수**: -1, -2, -3, …

$$\\text{정수} = \\{\\, \\cdots, -3, -2, -1, 0, +1, +2, +3, \\cdots \\,\\}$$
"""
    )

    st.header("4️⃣ 유리수")
    st.markdown(
        """
**유리수**는 분수 $\\dfrac{b}{a}$ (단, $a$, $b$는 정수, $a \\neq 0$) 꼴로 나타낼 수 있는 수입니다.
정수도 분모가 1인 분수로 나타낼 수 있으므로 모든 정수는 유리수입니다.

- **양의 유리수**: 0보다 큰 유리수 (예: +1/2, +2.3)
- **음의 유리수**: 0보다 작은 유리수 (예: -1/2, -2.3)
- **정수가 아닌 유리수**: 분수 또는 유한소수·순환소수로 나타나지만 정수는 아닌 수 (예: 1/2, -0.75, 3.14)

$$\\text{유리수} = \\text{정수} \\;\\cup\\; \\text{정수가 아닌 유리수}$$

즉, 유리수는 **정수**와 **정수가 아닌 유리수**로 이루어져 있습니다.
"""
    )

    st.header("5️⃣ 수직선과 절댓값")
    st.markdown(
        """
- 정수와 유리수는 **수직선** 위의 점으로 나타낼 수 있습니다. 원점(0)을 기준으로 오른쪽은 양수,
  왼쪽은 음수를 나타냅니다.
- **절댓값**: 수직선에서 어떤 수를 나타내는 점과 원점 사이의 거리. 기호 $|\\;\\;|$ 로 나타냅니다.
    - $|+3| = 3$, $|-3| = 3$
    - 절댓값은 항상 0 또는 양수입니다.
    - 원점에서 멀수록 절댓값이 큽니다.
"""
    )

    st.header("6️⃣ 정수와 유리수의 대소 관계")
    st.markdown(
        """
1. (음수) < 0 < (양수)
2. 양수는 절댓값이 클수록 큽니다. → $+5 > +2$
3. 음수는 절댓값이 클수록 작습니다. (절댓값이 작을수록 큽니다.) → $-2 > -5$
4. 부등호 `<`, `>`, `≤`, `≥` 를 사용하여 대소 관계를 나타냅니다.

**예) $-4$, $+2$, $-1$ 을 작은 수부터 순서대로 나열하면?**
→ 음수는 절댓값이 클수록 작으므로 $-4 < -1$, 여기에 양수 $+2$가 가장 크므로
$$-4 < -1 < +2$$
"""
    )

    st.header("7️⃣ 정수와 유리수의 사칙계산")

    st.subheader("➕ 덧셈")
    st.markdown(
        """
- **부호가 같은 두 수의 덧셈**: 두 수의 절댓값의 합에 공통인 부호를 붙입니다.
    - $(+3) + (+2) = +5$,  $(-3) + (-2) = -5$
- **부호가 다른 두 수의 덧셈**: 두 수의 절댓값의 차에 절댓값이 큰 수의 부호를 붙입니다.
    - $(+5) + (-3) = +2$,  $(-5) + (+3) = -2$
"""
    )

    st.subheader("➖ 뺄셈")
    st.markdown(
        """
빼는 수의 부호를 바꾸어 덧셈으로 계산합니다.

$$a - b = a + (-b)$$

- $(+5) - (+2) = (+5) + (-2) = +3$
- $(-5) - (-2) = (-5) + (+2) = -3$
"""
    )

    st.subheader("✖️ 곱셈")
    st.markdown(
        """
- **부호가 같은 두 수의 곱**: 양수 → $(+) \\times (+) = (+)$,  $(-) \\times (-) = (+)$
- **부호가 다른 두 수의 곱**: 음수 → $(+) \\times (-) = (-)$,  $(-) \\times (+) = (-)$
- 세 개 이상의 수를 곱할 때는 곱해지는 음수의 개수가 **짝수**이면 결과는 양수, **홀수**이면 결과는 음수입니다.
"""
    )

    st.subheader("➗ 나눗셈")
    st.markdown(
        """
나눗셈은 나누는 수의 **역수**를 곱하는 것과 같습니다.

$$a \\div b = a \\times \\frac{1}{b} \\quad (b \\neq 0)$$

부호 규칙은 곱셈과 같습니다. (부호가 같으면 +, 다르면 -)
"""
    )

    st.subheader("🔢 사칙연산이 섞여 있는 혼합 계산의 순서")
    st.markdown(
        """
1. 거듭제곱이 있으면 먼저 계산합니다.
2. 괄호가 있으면 (소괄호) → (중괄호) → [대괄호] 순서로 먼저 계산합니다.
3. 곱셈과 나눗셈을 계산합니다.
4. 덧셈과 뺄셈을 계산합니다.

**예) $(-3) + 4 \\times (-2)$**
→ 곱셈 먼저: $4 \\times (-2) = -8$
→ 덧셈: $(-3) + (-8) = -11$
"""
    )

    st.info("💡 학습자료를 충분히 읽었다면 오른쪽 위 **✏️ 평가 (퀴즈)** 탭에서 문제를 풀어보세요!")


# ════════════════════════════════════════════════════════════
# TAB 2. 퀴즈
# ════════════════════════════════════════════════════════════
with tab2:
    st.title("✏️ 정수와 유리수 평가 퀴즈")
    st.markdown(
        f"""
전체 **{len(QUESTIONS)}문제** 입니다. 각 문제마다 **최대 {MAX_ATTEMPTS}번**까지 입력할 수 있으며,
- 1, 2번째 오답 시 → "오답입니다. 다시 한번 입력해주세요."
- 3번째까지 틀리면 → 정답이 자동으로 공개됩니다.
"""
    )

    solved_count = sum(1 for s in st.session_state.quiz_state.values() if s["solved"])
    st.progress(solved_count / len(QUESTIONS))
    st.caption(f"진행 상황: {solved_count} / {len(QUESTIONS)} 문제 완료")

    st.divider()

    for i, q in enumerate(QUESTIONS):
        state = st.session_state.quiz_state[i]

        st.subheader(f"문제 {i + 1}. [{q['category']}]")
        st.markdown(q["question"])

        if state["solved"]:
            # 이미 종료된 문제 (정답 맞춤 또는 정답 공개됨)
            if state["correct_on_first"] is False and state["attempts"] >= MAX_ATTEMPTS:
                st.error(f"❌ 정답 공개: **{q['answer_display']}**  (최대 시도 횟수를 초과했습니다.)")
            else:
                st.success("✅ 정답입니다.")
        else:
            with st.form(key=f"form_{i}"):
                user_input = st.text_input(
                    "답을 입력하세요 (분수는 1/2 형태, 소수는 0.5 형태로 입력 가능)",
                    key=f"input_{i}",
                )
                submitted = st.form_submit_button("제출")

                if submitted:
                    if is_correct(user_input, q["answer"]):
                        state["solved"] = True
                        state["correct_on_first"] = (state["attempts"] == 0)
                        st.success("✅ 정답입니다.")
                    else:
                        state["attempts"] += 1
                        if state["attempts"] >= MAX_ATTEMPTS:
                            state["solved"] = True
                            state["correct_on_first"] = False
                            st.error(
                                f"❌ 오답입니다. 정답은 **{q['answer_display']}** 입니다."
                            )
                        else:
                            remaining = MAX_ATTEMPTS - state["attempts"]
                            st.warning(
                                f"⚠️ 오답입니다. 다시 한번 입력해주세요. (남은 기회: {remaining}번)"
                            )
                            st.caption(f"💡 힌트: {q['hint']}")

        st.divider()

    if solved_count == len(QUESTIONS):
        st.balloons()
        correct_first = sum(
            1 for s in st.session_state.quiz_state.values() if s["correct_on_first"]
        )
        st.success(
            f"🎉 모든 문제를 완료했습니다! 총 {len(QUESTIONS)}문제 중 "
            f"{correct_first}문제를 처음 시도에 맞혔습니다."
        )

    st.button("🔄 퀴즈 다시 풀기", on_click=reset_quiz)