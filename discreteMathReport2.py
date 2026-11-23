N = 5  # 집합 A = {1, 2, 3, 4, 5}


# [조건1] 5x5 관계행렬을 한 행씩 입력받아 2차원 리스트로 반환
# 한 행에 0 또는 1이 5개가 아니면 그 행을 다시 입력받는다
def inputMatrix():
    M = []
    print("5x5 관계행렬을 한 행씩 입력하세요 (예: 1 0 0 1 0)")
    while len(M) < N:
        row = input(f"{len(M) + 1}행: ").split()
        if len(row) == N and all(x in ("0", "1") for x in row):
            M.append([int(x) for x in row])
        else:
            print("  0 또는 1을 5개 입력해야 합니다. 다시 입력하세요.")
    return M

# 관계행렬을 제목과 함께 출력
def printMatrix(M, title):
    print(f"\n{title}")
    for row in M:
        print("  " + " ".join(map(str, row)))


# [조건2] 반사관계 판별: 모든 a에 대해 (a,a)∈R, 즉 대각원소가 모두 1인지 확인
def isReflexive(M):
    return all(M[i][i] == 1 for i in range(N))


# [조건2] 대칭관계 판별: (a,b)∈R이면 (b,a)∈R, 즉 M[i][j]와 M[j][i]가 모두 같은지 확인
def isSymmetric(M):
    return all(M[i][j] == M[j][i] for i in range(N) for j in range(N))


# [조건2] 추이관계 판별: (a,b)∈R이고 (b,c)∈R이면 (a,c)∈R인지 모든 a,b,c에 대해 확인
def isTransitive(M):
    return all(not (M[a][b] and M[b][c]) or M[a][c]
               for a in range(N) for b in range(N) for c in range(N))


# [조건2] 세 성질의 판별 결과를 출력하고, 판별 결과에 따라 동치관계 여부 메시지를 출력
# 동치관계이면 True, 아니면 False 반환
def isEquivalence(M):
    result = {"반사관계": isReflexive(M), "대칭관계": isSymmetric(M), "추이관계": isTransitive(M)}
    print("\n[관계의 성질 판별]")
    for name, ok in result.items():
        print(f"  {name} : {'O' if ok else 'X'}")

    failed = [name for name, ok in result.items() if not ok]
    if failed:
        print(f"→ {', '.join(failed)}를 만족하지 않으므로 R은 동치관계가 아닙니다.")
        return False
    print("→ 반사관계, 대칭관계, 추이관계를 모두 만족하므로 R은 동치관계입니다.")
    return True


# [조건3] 원소 a의 동치류 [a] = { x | (a,x)∈R }: a행에서 1인 열의 원소들을 모음
def equivalenceClass(M, a):
    return [x + 1 for x in range(N) if M[a - 1][x] == 1]


# [조건3] 집합 A의 각 원소 1~5에 대한 동치류를 각각 출력
def printClasses(M):
    print("\n[동치류]")
    for a in range(1, N + 1):
        print(f"  [{a}] = {{{', '.join(map(str, equivalenceClass(M, a)))}}}")


# [조건4] 반사폐포 S = R ∪ {(a,a) | a∈A}: 행렬을 복사한 뒤 대각원소를 모두 1로 만듦
def reflexiveClosure(M):
    S = [row[:] for row in M]
    for i in range(N):
        S[i][i] = 1
    return S


# [조건4] 대칭폐포 S = R ∪ R⁻¹: M[i][j] 또는 M[j][i]가 1이면 S[i][j]를 1로 만듦
def symmetricClosure(M):
    return [[M[i][j] | M[j][i] for j in range(N)] for i in range(N)]


# [조건4] 추이폐포 = 연결관계 R∞, 와샬 알고리즘으로 구함
# k = 1~n 단계마다 (i,k)와 (k,j)가 모두 1이면 (i,j)를 1로 만들어 W(k-1) → W(k) 계산
def transitiveClosure(M):
    W = [row[:] for row in M]
    for k in range(N):
        for i in range(N):
            for j in range(N):
                if W[i][k] and W[k][j]:
                    W[i][j] = 1
    return W


# 폐포 이름 → (해당 성질 판별 함수, 폐포 함수)
CLOSURES = {"반사": (isReflexive, reflexiveClosure),
            "대칭": (isSymmetric, symmetricClosure),
            "추이": (isTransitive, transitiveClosure)}

# 만족하지 않는 성질마다 원래 관계 R에 그 폐포만 각각 적용
# 각 폐포의 변환 전/후를 출력하고, 변환한 관계를 다시 판별해 동치관계이면 동치류 출력
def eachClosure(R):
    for name, (check, closure) in CLOSURES.items():
        if check(R):
            continue
        print(f"\n----- {name}폐포 -----")
        S = closure(R)
        printMatrix(R, f"[{name}폐포 변환 전]")
        printMatrix(S, f"[{name}폐포 변환 후]")
        if isEquivalence(S):
            printClasses(S)


# [추가기능] 폐포를 order 순서대로 누적 적용 (앞 폐포의 결과에 다음 폐포를 적용)
# 만족하지 않는 성질에 대해서만 적용하며 단계별 변환 전/후 출력 → 다시 판별 → 동치류 출력
# 대칭폐포를 추이폐포보다 먼저 적용하면 결과가 항상 동치관계가 됨
def cumulativeClosure(R, order):
    S = R
    for name in order:
        check, closure = CLOSURES[name]
        if not check(S):
            printMatrix(S, f"[{name}폐포 변환 전]")
            S = closure(S)
            printMatrix(S, f"[{name}폐포 변환 후]")
    if isEquivalence(S):
        printClasses(S)
    return S


# 전체 흐름: 입력 → 동치관계 판별 → (동치관계이면) 동치류 출력
#           → (아니면) [조건4] 각각의 폐포 적용 → [추가기능] 누적 적용
def main():
    R = inputMatrix()
    printMatrix(R, "[입력한 관계 R의 관계행렬]")

    if isEquivalence(R):
        printClasses(R)
        return

    print("\n========== [조건4] 각각의 폐포 적용 ==========")
    eachClosure(R)

    print("\n========== [추가기능] 반사 → 대칭 → 추이 순서로 누적 적용 ==========")
    cumulativeClosure(R, ["반사", "대칭", "추이"])


if __name__ == "__main__":
    main()