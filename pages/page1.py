import streamlit as st
import random

# ----------------------------
# 기본 설정
# ----------------------------
st.set_page_config(
    page_title="소수와 합성수 배우기",
    page_icon="🔢",
    layout="wide"
)

# ----------------------------
# 소수 판별 함수
# ----------------------------
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def get_divisors(n: int):
    return [i for i in range(1, n + 1) if n % i == 0]


# ----------------------------
# 세션 상태 초기화
# ----------------------------
def init_quiz():
    # 1은 소수도 합성수도 아니므로 문제 출제 범위에서 제외 (2~100)
    pool = list(range(2, 101))
    numbers = random.sample(pool, 10)
    st.session_state.quiz_numbers = numbers
    st.session_state.answers = {}          # {문제번호: 사용자가 고른 답}
    st.session_state.submitted = {}        # {문제번호: True/False 제출 여부}


if "quiz_numbers" not in st.session_state:
    init_quiz()


# ----------------------------
# 사이드바 메뉴
# ----------------------------
st.sidebar.title("📚 메뉴")
menu = st.sidebar.radio("이동하기", ["🏠 학습 자료", "📝 퀴즈 풀기"])

st.sidebar.markdown("---")
st.sidebar.info("중학교 1학년 수학 · 소수와 합성수 단원")


# ============================================================
# 1. 학습 자료 페이지
# ============================================================
if menu == "🏠 학습 자료":
    st.title("🔢 소수와 합성수")
    st.markdown("중학교 1학년 수학에서 배우는 **소수(prime number)** 와 **합성수(composite number)** 를 함께 알아봅시다.")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.header("① 소수란?")
        st.markdown(
            """
**소수(素數, prime number)** 란

> **1보다 큰 자연수 중에서 1과 자기 자신만을 약수로 가지는 수**

를 말합니다.

즉, 어떤 자연수의 약수를 모두 찾았을 때 그 개수가 **딱 2개(1과 자기 자신)** 뿐이면 소수입니다.

**예시**
- 2의 약수: 1, 2 → 2개 → **소수 ✅**
- 3의 약수: 1, 3 → 2개 → **소수 ✅**
- 5의 약수: 1, 5 → 2개 → **소수 ✅**
- 7의 약수: 1, 7 → 2개 → **소수 ✅**

**소수의 특징**
- 소수는 무한히 많습니다.
- 2는 유일한 짝수 소수입니다. (2를 제외한 모든 소수는 홀수)
- 가장 작은 소수는 **2** 입니다.
            """
        )

    with col2:
        st.header("② 합성수란?")
        st.markdown(
            """
**합성수(合成數, composite number)** 란

> **1보다 큰 자연수 중에서 약수가 3개 이상인 수**

를 말합니다.

즉, 1과 자기 자신 이외에 다른 약수를 하나라도 더 가지면 합성수입니다.

**예시**
- 4의 약수: 1, 2, 4 → 3개 → **합성수 ✅**
- 6의 약수: 1, 2, 3, 6 → 4개 → **합성수 ✅**
- 9의 약수: 1, 3, 9 → 3개 → **합성수 ✅**
- 12의 약수: 1, 2, 3, 4, 6, 12 → 6개 → **합성수 ✅**

**합성수의 특징**
- 합성수는 소수들의 곱으로 표현할 수 있습니다. (소인수분해)
- 가장 작은 합성수는 **4** 입니다.
            """
        )

    st.markdown("---")
    st.header("③ 주의! 1은 소수도 합성수도 아니다")
    st.warning(
        "**1의 약수는 1 하나뿐**이기 때문에, 소수의 정의(약수 2개)와 합성수의 정의(약수 3개 이상) 어디에도 해당하지 않습니다.\n\n"
        "따라서 **1은 소수도 아니고 합성수도 아닙니다.**"
    )

    st.markdown("---")
    st.header("④ 소수와 합성수 판별 방법")
    st.markdown(
        """
어떤 자연수 **n**이 소수인지 확인하려면:

1. n이 1이면 → 소수도 합성수도 아님
2. n이 2이면 → 소수
3. n이 짝수이면(2 제외) → 합성수
4. 2부터 시작해서 어떤 수로도 나누어떨어지지 않으면 → 소수
5. 나누어떨어지는 수가 하나라도 있으면 → 합성수

이 방법을 표로 정리한 것이 유명한 **에라토스테네스의 체**입니다.
        """
    )

    with st.expander("🔍 1~100까지 소수 한눈에 보기 (에라토스테네스의 체)"):
        primes_1_100 = [n for n in range(1, 101) if is_prime(n)]
        st.write(f"1부터 100까지 소수는 총 **{len(primes_1_100)}개** 입니다.")

        # 10x10 표로 시각화
        rows = []
        for r in range(10):
            row = []
            for c in range(10):
                n = r * 10 + c + 1
                if n == 1:
                    row.append("1")
                elif is_prime(n):
                    row.append(f"**{n}**")
                else:
                    row.append(str(n))
            rows.append(row)

        st.table(rows)
        st.caption("굵게 표시된 숫자가 소수입니다. (1은 소수도 합성수도 아닙니다)")

    with st.expander("🧮 직접 약수 확인해보기"):
        num = st.number_input("확인하고 싶은 숫자를 입력하세요 (1~100)", min_value=1, max_value=100, value=12, step=1)
        divisors = get_divisors(int(num))
        st.write(f"**{num}의 약수**: {', '.join(map(str, divisors))} (총 {len(divisors)}개)")
        if num == 1:
            st.info("1은 소수도 합성수도 아닙니다.")
        elif is_prime(int(num)):
            st.success(f"{num}은(는) **소수**입니다! (약수가 2개)")
        else:
            st.error(f"{num}은(는) **합성수**입니다! (약수가 3개 이상)")

    st.markdown("---")
    st.success("학습 자료를 다 확인했다면, 왼쪽 메뉴에서 **📝 퀴즈 풀기**로 이동해서 실력을 확인해보세요!")


# ============================================================
# 2. 퀴즈 페이지
# ============================================================
else:
    st.title("📝 소수·합성수 판별 퀴즈")
    st.markdown("아래 숫자가 **소수**인지 **합성수**인지 버튼을 눌러 선택해보세요! (총 10문제)")

    if st.button("🔄 새로운 문제 10개로 다시 시작하기"):
        init_quiz()
        st.rerun()

    st.markdown("---")

    numbers = st.session_state.quiz_numbers
    answers = st.session_state.answers

    for idx, number in enumerate(numbers, start=1):
        st.subheader(f"문제 {idx}. 숫자 **{number}** 은(는) 소수일까요, 합성수일까요?")

        c1, c2, c3 = st.columns([1, 1, 3])

        with c1:
            if st.button("소수", key=f"prime_btn_{idx}"):
                answers[idx] = "소수"

        with c2:
            if st.button("합성수", key=f"composite_btn_{idx}"):
                answers[idx] = "합성수"

        with c3:
            if idx in answers:
                user_choice = answers[idx]
                correct_choice = "소수" if is_prime(number) else "합성수"

                if user_choice == correct_choice:
                    st.success("✅ 정답입니다!")
                else:
                    st.error("❌ 소수가 아니고 합성수 입니다." if correct_choice == "합성수" else "❌ 소수입니다. 다시 생각해보세요.")

        st.markdown("---")

    # 채점 결과
    answered_count = len(answers)
    correct_count = 0
    for idx, number in enumerate(numbers, start=1):
        if idx in answers:
            correct_choice = "소수" if is_prime(number) else "합성수"
            if answers[idx] == correct_choice:
                correct_count += 1

    st.header("📊 채점 결과")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("푼 문제 수", f"{answered_count} / 10")
    col_b.metric("맞은 개수", f"{correct_count}")
    col_c.metric("점수", f"{correct_count * 10}점")

    if answered_count == 10:
        if correct_count == 10:
            st.balloons()
            st.success("🎉 만점입니다! 소수와 합성수를 완벽하게 이해했네요!")
        elif correct_count >= 7:
            st.info("👍 잘했어요! 조금만 더 연습하면 완벽해질 거예요.")
        else:
            st.warning("💪 학습 자료를 다시 한번 읽어보고 도전해보세요!")