import re
from collections import Counter

import streamlit as st

# ----------------------------------------------------------------------------
# 기본 설정
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="소인수분해 학습 & 평가",
    page_icon="🔢",
    layout="centered",
)

QUIZ_NUMBERS = [12, 18, 24, 36, 45, 60, 72, 84, 90, 100]


# ----------------------------------------------------------------------------
# 소인수분해 유틸 함수
# ----------------------------------------------------------------------------
def get_correct_factors(n: int):
    """자연수 n을 소인수분해하여 소인수 리스트(중복 포함, 오름차순)를 반환."""
    factors = []
    d = 2
    temp = n
    while d * d <= temp:
        while temp % d == 0:
            factors.append(d)
            temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)
    return sorted(factors)


def format_factorization(factors, sep=" × "):
    """[2,2,3,5] -> '2^2 × 3 × 5' 형태의 문자열로 변환."""
    counter = Counter(factors)
    parts = []
    for p in sorted(counter):
        exp = counter[p]
        parts.append(f"{p}^{exp}" if exp > 1 else f"{p}")
    return sep.join(parts)


def parse_user_input(text: str):
    """
    사용자가 입력한 소인수분해 문자열을 파싱하여 소인수 리스트를 반환.
    지원 형식 예시: '2^2 x 3 x 5', '2*2*3*5', '2^2×3×5', '2 2 3 5'
    파싱에 실패하면 None을 반환.
    """
    if not text or not text.strip():
        return None

    cleaned = text.strip()
    # 다양한 곱셈 기호를 '*'로 통일
    for sym in ["×", "x", "X", "·", "ㆍ", "**"]:
        cleaned = cleaned.replace(sym, "*")

    # 공백만으로 구분한 경우('2 2 3 5')도 지원하기 위해 공백을 '*'로 치환
    # (단, '2^2' 같은 표현은 공백이 없다고 가정)
    if "*" not in cleaned and " " in cleaned:
        cleaned = re.sub(r"\s+", "*", cleaned.strip())

    terms = [t.strip() for t in cleaned.split("*") if t.strip() != ""]
    if not terms:
        return None

    factors = []
    for term in terms:
        m = re.match(r"^(\d+)(\^(\d+))?$", term)
        if not m:
            return None
        base = int(m.group(1))
        exp = int(m.group(3)) if m.group(3) else 1
        if base < 2 or exp < 1:
            return None
        factors.extend([base] * exp)

    return sorted(factors)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for d in range(2, int(n**0.5) + 1):
        if n % d == 0:
            return False
    return True


# ----------------------------------------------------------------------------
# 세션 상태 초기화 (퀴즈 진행 상황 저장)
# ----------------------------------------------------------------------------
def init_quiz_state():
    if "q_index" not in st.session_state:
        st.session_state.q_index = 0          # 현재 문제 번호(0~9)
        st.session_state.attempt = 1           # 현재 문제에서의 시도 횟수(1 또는 2)
        st.session_state.score = 0             # 맞힌 개수
        st.session_state.status = "answering"  # answering / correct / wrong_once / finished
        st.session_state.log = []              # 문제별 결과 기록


def reset_quiz():
    for key in ["q_index", "attempt", "score", "status", "log"]:
        if key in st.session_state:
            del st.session_state[key]
    init_quiz_state()


# ----------------------------------------------------------------------------
# 사이드바
# ----------------------------------------------------------------------------
st.sidebar.title("🔢 소인수분해 학습실")
menu = st.sidebar.radio("메뉴를 선택하세요", ["📘 학습하기", "📝 평가하기"])
st.sidebar.markdown("---")
st.sidebar.caption("중학교 1학년 수학 · 소인수분해 단원")


# ----------------------------------------------------------------------------
# 1. 학습하기 페이지
# ----------------------------------------------------------------------------
if menu == "📘 학습하기":
    st.title("📘 소인수분해 (素因數分解)")

    st.markdown(
        """
### 1. 소수와 합성수
- **소수(素數)**: 1과 자기 자신만을 약수로 가지는 1보다 큰 자연수입니다.
  예) 2, 3, 5, 7, 11, 13, 17, 19, 23, ...
- **합성수(合成數)**: 1과 자기 자신 이외의 약수를 가지는 1보다 큰 자연수입니다.
  예) 4, 6, 8, 9, 10, 12, ...
- 참고로 **1은 소수도 합성수도 아닙니다.**
"""
    )

    st.markdown(
        """
### 2. 인수와 소인수
- **인수(因數)**: 어떤 자연수를 두 자연수의 곱으로 나타낼 때, 곱해지는 각각의 수를 그 수의 인수라고 합니다.
  예) 12 = 3 × 4 이므로 3과 4는 12의 인수입니다.
- **소인수(素因數)**: 인수 중에서 소수인 것을 소인수라고 합니다.
  예) 12의 인수는 1, 2, 3, 4, 6, 12 이고, 이 중 소수는 2, 3이므로 12의 소인수는 **2와 3**입니다.
"""
    )

    st.markdown(
        """
### 3. 소인수분해란?
**소인수분해**란 1보다 큰 자연수를 그 수의 소인수만의 곱으로 나타내는 것입니다.

예를 들어 12를 소인수분해하면 다음과 같습니다.
"""
    )
    st.latex(r"12 = 2 \times 2 \times 3 = 2^2 \times 3")

    st.markdown(
        """
이때 같은 소인수의 곱은 **거듭제곱**을 사용하여 나타냅니다.
(2×2 는 2², 3×3×3 은 3³ 과 같이 표현합니다.)

> 📌 **소인수분해의 결과를 나타낼 때는 보통 소인수를 작은 수부터 크기순으로 쓰고, 거듭제곱을 사용합니다.**
"""
    )

    st.markdown("### 4. 소인수분해 하는 방법 — 나눗셈을 이용하는 방법")
    st.markdown(
        """
1. 주어진 자연수를 가장 작은 소수부터 차례로 나눕니다. (2, 3, 5, 7, 11, ...)
2. 더 이상 나누어지지 않으면 다음 소수로 넘어가서 나눕니다.
3. 몫이 1이 될 때까지 이 과정을 반복합니다.
4. 나눈 소수들을 모두 곱한 것이 소인수분해의 결과입니다.
"""
    )

    with st.expander("✏️ 예제: 60을 소인수분해 해봅시다"):
        st.markdown(
            """
```
2 ) 60
2 ) 30
3 ) 15
      5
```
왼쪽에 있는 나눈 소수들을 순서대로 곱하면:
"""
        )
        st.latex(r"60 = 2 \times 2 \times 3 \times 5 = 2^2 \times 3 \times 5")

    with st.expander("✏️ 예제: 84를 소인수분해 해봅시다"):
        st.markdown(
            """
```
2 ) 84
2 ) 42
3 ) 21
      7
```
"""
        )
        st.latex(r"84 = 2 \times 2 \times 3 \times 7 = 2^2 \times 3 \times 7")

    st.markdown("### 5. 소인수분해의 활용")
    st.markdown(
        """
- 소인수분해를 이용하면 어떤 수의 **약수를 모두 구할 수 있습니다.**
- 두 수 이상의 **최대공약수(GCD)**와 **최소공배수(LCM)**를 구할 때도 소인수분해를 활용합니다.
- 모든 합성수는 소인수분해 하는 방법이 (곱하는 순서를 제외하면) **오직 한 가지**뿐입니다. 이를 **산술의 기본정리**라고 합니다.
"""
    )

    st.info("💡 학습을 마쳤다면 왼쪽 메뉴에서 **📝 평가하기**를 눌러 문제를 풀어보세요!")

    st.markdown("### 🔍 직접 확인해보기")
    check_n = st.number_input(
        "자연수를 입력하면 소인수분해 결과를 바로 확인할 수 있어요 (연습용, 채점되지 않음)",
        min_value=2,
        max_value=100000,
        value=60,
        step=1,
    )
    if st.button("소인수분해 결과 보기"):
        f = get_correct_factors(int(check_n))
        if is_prime(int(check_n)):
            st.warning(f"{int(check_n)}은(는) 그 자체로 소수입니다. (소인수는 자기 자신뿐)")
        else:
            st.success(f"{int(check_n)} = {format_factorization(f)}")


# ----------------------------------------------------------------------------
# 2. 평가하기 페이지 (퀴즈)
# ----------------------------------------------------------------------------
else:
    st.title("📝 소인수분해 평가")
    st.caption("아래 자연수를 소인수분해한 결과를 입력하세요. 총 10문제입니다.")
    st.markdown(
        "**입력 형식 안내**: `2^2 x 3`, `2*2*3`, `2^2×3` 처럼 입력할 수 있어요. "
        "거듭제곱은 `^`, 곱셈은 `x`, `*`, `×` 모두 사용 가능합니다."
    )

    init_quiz_state()

    total = len(QUIZ_NUMBERS)

    # 퀴즈가 모두 끝난 경우 -> 결과 화면
    if st.session_state.q_index >= total:
        st.balloons()
        st.header("🎉 평가가 끝났습니다!")
        st.subheader(f"점수: {st.session_state.score} / {total}")

        st.markdown("### 문제별 결과")
        for item in st.session_state.log:
            icon = "✅" if item["correct"] else "❌"
            st.write(
                f"{icon} 문제 {item['idx']+1}. **{item['number']}** → "
                f"정답: {item['answer_str']}  (제출: {item['tries']}회)"
            )

        if st.button("🔄 다시 풀어보기"):
            reset_quiz()
            st.rerun()

    else:
        idx = st.session_state.q_index
        n = QUIZ_NUMBERS[idx]
        correct_factors = get_correct_factors(n)
        correct_str = format_factorization(correct_factors)

        st.progress(idx / total, text=f"문제 {idx + 1} / {total}")
        st.markdown(f"## 문제 {idx + 1}. **{n}** 을(를) 소인수분해 하세요.")

        input_key = f"input_{idx}_{st.session_state.attempt}"
        user_input = st.text_input(
            "소인수분해 결과를 입력하세요 (예: 2^2 x 3)",
            key=input_key,
        )

        # ---- 아직 정답을 맞히지 못한 상태(첫 시도 또는 재시도 전) ----
        if st.session_state.status in ("answering", "wrong_once"):
            if st.session_state.status == "wrong_once":
                st.warning("❗ 틀렸습니다. 한 번 더 입력해보세요! (마지막 기회)")

            submit_label = "제출하기" if st.session_state.attempt == 1 else "다시 제출하기"

            if st.button(submit_label, key=f"submit_{idx}_{st.session_state.attempt}"):
                parsed = parse_user_input(user_input)

                if parsed is None:
                    st.error(
                        "입력 형식을 확인해주세요. 예: `2^2 x 3` 처럼 소수와 거듭제곱, "
                        "곱셈 기호(x, *, ×)를 사용해 입력해주세요."
                    )
                elif parsed == correct_factors:
                    st.session_state.status = "correct"
                    st.session_state.score += 1
                    st.session_state.log.append(
                        {
                            "idx": idx,
                            "number": n,
                            "correct": True,
                            "answer_str": correct_str,
                            "tries": st.session_state.attempt,
                        }
                    )
                    st.rerun()
                else:
                    if st.session_state.attempt == 1:
                        st.session_state.attempt = 2
                        st.session_state.status = "wrong_once"
                        st.rerun()
                    else:
                        st.session_state.status = "finished_wrong"
                        st.session_state.log.append(
                            {
                                "idx": idx,
                                "number": n,
                                "correct": False,
                                "answer_str": correct_str,
                                "tries": 2,
                            }
                        )
                        st.rerun()

        # ---- 정답을 맞힌 경우 ----
        elif st.session_state.status == "correct":
            st.success("정답입니다! 🎉")
            latex_expr = format_factorization(correct_factors, sep=' \\times ')
            st.latex(f"{n} = {latex_expr}")
            if st.button("다음 문제 ▶", key=f"next_correct_{idx}"):
                st.session_state.q_index += 1
                st.session_state.attempt = 1
                st.session_state.status = "answering"
                st.rerun()

        # ---- 두 번 다 틀린 경우 ----
        elif st.session_state.status == "finished_wrong":
            st.error("틀렸습니다.")
            st.markdown(f"**정답:** {n} = {correct_str}")
            latex_expr = format_factorization(correct_factors, sep=' \\times ')
            st.latex(f"{n} = {latex_expr}")
            if st.button("다음 문제 ▶", key=f"next_wrong_{idx}"):
                st.session_state.q_index += 1
                st.session_state.attempt = 1
                st.session_state.status = "answering"
                st.rerun()

        st.markdown("---")
        st.caption(f"현재까지 점수: {st.session_state.score} / {idx if st.session_state.status != 'answering' else idx}")