"""과점시장 모형 시뮬레이터 (IO Ch.01). 브라우저의 Pyodide에서 실행됩니다."""
import io, json, base64
import numpy as np
import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt

QAX, PAX = 200, 150  # 고정 축 범위
C1, C2, C3, GR = "#2563eb", "#dc2626", "#16a34a", "#6b7280"
plt.rcParams.update({"axes.grid": True, "grid.alpha": .25, "axes.spines.top": False,
                     "axes.spines.right": False, "font.size": 9})


def _out(fig, rows, note=""):
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", dpi=110)
    plt.close(fig)
    return json.dumps({"img": base64.b64encode(buf.getvalue()).decode(),
                       "rows": rows, "note": note})


def _f(x, k=2):
    return f"{x:,.{k}f}"


# ---------------------------------------------------------------- 쿠르노
def cournot_eq(a, b, c1, c2):
    q1 = (a - 2 * c1 + c2) / (3 * b)
    q2 = (a - 2 * c2 + c1) / (3 * b)
    if q1 < 0:
        q1, q2 = 0.0, max((a - c2) / (2 * b), 0)
    elif q2 < 0:
        q2, q1 = 0.0, max((a - c1) / (2 * b), 0)
    return q1, q2


def cournot(a=100, b=1, c1=10, c2=10, start1=5, start2=60, rounds=8):
    br1 = lambda q2: np.maximum((a - c1) / (2 * b) - q2 / 2, 0)
    br2 = lambda q1: np.maximum((a - c2) / (2 * b) - q1 / 2, 0)
    q1e, q2e = cournot_eq(a, b, c1, c2)
    P = a - b * (q1e + q2e)
    pi1, pi2 = (P - c1) * q1e, (P - c2) * q2e
    # 담합(대칭 비용일 때의 균등 분할, 비용이 다르면 낮은 비용 기업이 독점 생산)
    cm = min(c1, c2)
    Qm = (a - cm) / (2 * b)
    if c1 == c2:
        qm1 = qm2 = Qm / 2
    elif c1 < c2:
        qm1, qm2 = Qm, 0
    else:
        qm1, qm2 = 0, Qm
    Pm = a - b * Qm
    pim1, pim2 = (Pm - c1) * qm1, (Pm - c2) * qm2

    fig, ax = plt.subplots(1, 3, figsize=(11, 4.4))
    qmax = (a - min(c1, c2)) / b
    g = np.linspace(0, QAX, 200)
    A = ax[0]
    A.plot(br1(g), g, color=C1, label="R1 (firm 1 best response)")
    A.plot(g, br2(g), color=C2, label="R2 (firm 2 best response)")
    # 반응 경로(순차 조정)
    x, y = start1, start2
    path = [(x, y)]
    for _ in range(int(rounds)):
        x = float(br1(y)); path.append((x, y))
        y = float(br2(x)); path.append((x, y))
    px, py_ = zip(*path)
    A.plot(px, py_, "-o", color=GR, ms=3, lw=1, label="adjustment path")
    A.plot([start1], [start2], "s", color="k", ms=5)
    A.plot(q1e, q2e, "o", color="k", ms=9, label="Cournot-Nash")
    A.plot(qm1, qm2, "*", color=C3, ms=13, label="cartel")
    A.set_xlim(0, QAX); A.set_ylim(0, QAX)
    A.set_xlabel("q1"); A.set_ylabel("q2"); A.set_title("Best responses & adjustment")
    A.legend(fontsize=7)

    # 담합 이탈
    B = ax[1]
    g1 = np.linspace(0, QAX, 200)
    dev = (a - b * (g1 + qm2) - c1) * g1
    B.plot(g1, dev, color=C1)
    qd = float(br1(qm2))
    B.plot(qm1, pim1, "*", color=C3, ms=13, label=f"cartel q1={_f(qm1)}")
    B.plot(qd, (a - b * (qd + qm2) - c1) * qd, "o", color=C2, ms=8,
           label=f"best deviation q1={_f(qd)}")
    B.set_xlim(0, QAX); B.set_ylim(-3000, 4000)
    B.set_xlabel("q1"); B.set_ylabel("profit of firm 1 (q2 at cartel level)")
    B.set_title("Why collusion collapses"); B.legend(fontsize=7)

    # 비교
    C = ax[2]
    Qc = (a - min(c1, c2)) / b
    labs = ["Competition", "Cournot", "Monopoly"]
    tot = [0, pi1 + pi2, Qm * (Pm - cm)]
    C.bar(labs, tot, color=[GR, C1, C3])
    for i, v in enumerate(tot):
        C.text(i, v, _f(v, 1), ha="center", va="bottom", fontsize=8)
    C.set_ylim(0, 8000); C.set_title("Total profit")

    dev_gain = (a - b * (qd + qm2) - c1) * qd - pim1
    rows = [("쿠르노 균형 생산량 $(q_1^*,q_2^*)$", f"{_f(q1e)}, {_f(q2e)}"),
            ("균형 가격 $P^*$", _f(P)),
            ("균형 이윤 $(\\pi_1^*,\\pi_2^*)$", f"{_f(pi1)}, {_f(pi2)}"),
            ("담합 생산량 $(q_1^m,q_2^m)$", f"{_f(qm1)}, {_f(qm2)}"),
            ("담합 가격", _f(Pm)),
            ("담합 이윤 $(\\pi_1^m,\\pi_2^m)$", f"{_f(pim1)}, {_f(pim2)}"),
            ("담합 이탈 시 기업 1의 추가 이득 $\\Delta\\pi_1$", _f(dev_gain))]
    return _out(fig, rows, r"담합점에서 $\partial\pi_1/\partial q_1 = b\,q_2^m > 0$ 이므로 기업 1은 항상 생산량을 늘릴 유인이 있습니다.")


# ------------------------------------------------------------- 베르트랑
def bertrand(a=100, b=1, c1=10, c2=10, p1_0=80, p2_0=75, eps=2, rounds=80):
    cm = min(c1, c2)
    p1, p2 = float(p1_0), float(p2_0)
    h1, h2 = [p1], [p2]
    for t in range(int(rounds)):
        if t % 2 == 0:
            tgt = p2 - eps
            p1 = tgt if tgt >= c1 else (c1 if p2 > c1 else p1)
        else:
            tgt = p1 - eps
            p2 = tgt if tgt >= c2 else (c2 if p1 > c2 else p2)
        h1.append(p1); h2.append(p2)
    # 균형: 비용 낮은 기업이 상대 비용 바로 아래 가격(동일하면 c)
    if c1 == c2:
        pe, win = c1, "tie"
    else:
        pe, win = max(c1, c2), "firm 1" if c1 < c2 else "firm 2"
    Qe = max((a - pe) / b, 0)
    pr = (pe - cm) * Qe if c1 != c2 else 0

    fig, ax = plt.subplots(1, 2, figsize=(10.5, 4.2))
    ax[0].plot(h1, "-o", ms=3, color=C1, label="p1")
    ax[0].plot(h2, "-o", ms=3, color=C2, label="p2")
    ax[0].axhline(c1, color=C1, ls=":", lw=1); ax[0].axhline(c2, color=C2, ls=":", lw=1)
    ax[0].set_xlim(0, 150); ax[0].set_ylim(0, PAX)
    ax[0].set_xlabel("round"); ax[0].set_ylabel("price"); ax[0].legend()
    ax[0].set_title("Undercutting war (dotted = marginal cost)")
    # 기업 1의 이윤 함수 (p2 고정)
    pg = np.linspace(0, PAX, 600)
    p2f = p2
    D = np.maximum((a - pg) / b, 0)
    share = np.where(pg < p2f, 1.0, np.where(pg == p2f, .5, 0.0))
    ax[1].plot(pg, (pg - c1) * D * share, color=C1)
    ax[1].axvline(p2f, color=C2, ls="--", lw=1, label=f"rival price = {_f(p2f, 1)}")
    ax[1].set_xlim(0, PAX); ax[1].set_ylim(-2000, 4000)
    ax[1].set_xlabel("p1"); ax[1].set_ylabel("profit of firm 1")
    ax[1].set_title("Firm 1 profit given p2 (discontinuous)"); ax[1].legend(fontsize=8)
    rows = [("최종 가격 $(p_1,p_2)$", f"{_f(h1[-1])}, {_f(h2[-1])}"),
            ("이론적 균형 가격 $p^*$", _f(pe)),
            ("균형 이윤 합계", _f(pr)),
            ("시장 공급 기업", win)]
    return _out(fig, rows, "비용이 같으면 $p^* = c$, 이윤 0 (베르트랑 역설). 비용이 다르면 저비용 기업이 상대의 비용 바로 밑에서 시장 전체를 공급합니다.")


# --------------------------------------------------------- 스타켈베르크
def stackelberg(a=100, b=1, c1=10, c2=10):
    q1c, q2c = cournot_eq(a, b, c1, c2)
    q1s = max((a - 2 * c1 + c2) / (2 * b), 0)
    q2s = max((a - c2) / (2 * b) - q1s / 2, 0)
    Pc, Ps = a - b * (q1c + q2c), a - b * (q1s + q2s)
    pic = ((Pc - c1) * q1c, (Pc - c2) * q2c)
    pis = ((Ps - c1) * q1s, (Ps - c2) * q2s)
    qmax = (a - min(c1, c2)) / b
    g = np.linspace(0.01, QAX, 600)
    fig, ax = plt.subplots(1, 2, figsize=(10.5, 4.4))
    A = ax[0]
    A.plot(np.maximum((a - c1) / (2 * b) - g / 2, 0), g, color=C1, label="R1")
    A.plot(g, np.maximum((a - c2) / (2 * b) - g / 2, 0), color=C2, label="R2 (follower)")
    for k, ls in ((pic[0], "--"), (pis[0], "-")):
        y = (a - c1) / b - g - k / (b * g)
        A.plot(g[y >= 0], y[y >= 0], color=C1, ls=ls, lw=1,
               label=f"iso-profit of 1 = {_f(k, 0)}")
    A.plot(q1c, q2c, "o", color="k", label="Cournot")
    A.plot(q1s, q2s, "*", color=C3, ms=13, label="Stackelberg")
    A.set_xlim(0, QAX); A.set_ylim(0, QAX); A.set_xlabel("q1 (leader)"); A.set_ylabel("q2")
    A.set_title("Leader picks the best point on R2"); A.legend(fontsize=7)
    B = ax[1]
    x = np.arange(2); w = .35
    B.bar(x - w / 2, pic, w, label="Cournot", color=GR)
    B.bar(x + w / 2, pis, w, label="Stackelberg", color=C3)
    B.set_xticks(x, ["leader (1)", "follower (2)"]); B.set_ylim(0, 4000); B.legend(); B.set_title("Profits")
    rows = [("스타켈베르크 $(q_1^S,q_2^S)$", f"{_f(q1s)}, {_f(q2s)}"),
            ("가격 $P^S$", _f(Ps)), ("이윤 $(\\pi_1^S,\\pi_2^S)$", f"{_f(pis[0])}, {_f(pis[1])}"),
            ("쿠르노 이윤 $(\\pi_1^C,\\pi_2^C)$", f"{_f(pic[0])}, {_f(pic[1])}"),
            ("선도자 이점 $\\pi_1^S-\\pi_1^C$", _f(pis[0] - pic[0]))]
    return _out(fig, rows, "선도자는 추종자의 반응함수 위에서 가장 높은 등이윤곡선에 닿는 점을 고릅니다. 수량은 전략적 대체재라서 먼저 움직이는 쪽이 유리합니다.")


# -------------------------------------------------------------- 차별화
def differentiated(alpha=100, beta=1.0, gamma=0.6, c=10):
    gamma = min(gamma, beta * 0.999)
    den = beta ** 2 - gamma ** 2
    a, b, d = alpha / (beta + gamma), beta / den, gamma / den
    pB = (a + b * c) / (2 * b - d)
    qB = a - (b - d) * pB
    piB = (pB - c) * qB
    qC = (alpha - c) / (2 * beta + gamma)
    pC = alpha - (beta + gamma) * qC
    piC = (pC - c) * qC
    # 순차 가격경쟁 (기업 1 선도)
    A_ = a - (b - d) * c
    m1g = np.linspace(0, A_ / b * 3, 3000)
    m2 = (A_ + d * m1g) / (2 * b)
    lead = m1g * (A_ - b * m1g + d * m2)
    k = int(np.argmax(lead))
    m1s, m2s = m1g[k], m2[k]
    p1s, p2s = c + m1s, c + m2s
    pi1s, pi2s = lead[k], m2s * (A_ - b * m2s + d * m1s)

    fig, ax = plt.subplots(1, 3, figsize=(11, 4.4))
    A = ax[0]
    pg = np.linspace(0, PAX, 100)
    A.plot((a + b * c) / (2 * b) + d / (2 * b) * pg, pg, color=C1, label="R1(p2)")
    A.plot(pg, (a + b * c) / (2 * b) + d / (2 * b) * pg, color=C2, label="R2(p1)")
    A.plot(pB, pB, "o", color="k", label="Bertrand-Nash")
    A.plot(p1s, p2s, "*", color=C3, ms=13, label="firm 1 moves first")
    A.set_xlim(0, PAX); A.set_ylim(0, PAX)
    A.set_xlabel("p1"); A.set_ylabel("p2"); A.set_title("Prices: strategic complements")
    A.legend(fontsize=7)
    gs = np.linspace(0, .98, 50) * beta
    pbs, pcs, ibs, ics = [], [], [], []
    for g_ in gs:
        dn = beta ** 2 - g_ ** 2
        a_, b_, d_ = alpha / (beta + g_), beta / dn, g_ / dn
        p_ = (a_ + b_ * c) / (2 * b_ - d_); q_ = a_ - (b_ - d_) * p_
        pbs.append(p_); ibs.append((p_ - c) * q_)
        q2_ = (alpha - c) / (2 * beta + g_); pp = alpha - (beta + g_) * q2_
        pcs.append(pp); ics.append((pp - c) * q2_)
    ax[1].plot(gs / beta, pbs, color=C1, label="Bertrand")
    ax[1].plot(gs / beta, pcs, color=C2, label="Cournot")
    ax[1].axvline(gamma / beta, color=GR, ls=":")
    ax[1].set_xlim(0, 1); ax[1].set_ylim(0, PAX)
    ax[1].set_xlabel("substitutability γ/β"); ax[1].set_ylabel("price"); ax[1].legend()
    ax[1].set_title("Price: Bertrand < Cournot")
    ax[2].plot(gs / beta, ibs, color=C1, label="Bertrand")
    ax[2].plot(gs / beta, ics, color=C2, label="Cournot")
    ax[2].axvline(gamma / beta, color=GR, ls=":")
    ax[2].set_xlim(0, 1); ax[2].set_ylim(0, 7000)
    ax[2].set_xlabel("substitutability γ/β"); ax[2].set_ylabel("profit per firm")
    ax[2].legend(); ax[2].set_title("Profit shrinks as goods get closer")
    rows = [("수요계수 $(a,b,d)$", f"{_f(a)}, {_f(b, 3)}, {_f(d, 3)}"),
            ("베르트랑 가격 / 기업당 이윤", f"{_f(pB)} / {_f(piB)}"),
            ("쿠르노 가격 / 기업당 이윤", f"{_f(pC)} / {_f(piC)}"),
            ("순차 가격: 선도자 $p_1$ / 후발자 $p_2$", f"{_f(p1s)} / {_f(p2s)}"),
            ("순차 가격 이윤 (선도자, 후발자)", f"{_f(pi1s)}, {_f(pi2s)}")]
    return _out(fig, rows, "같은 수요 구조(Singh–Vives)에서 가격경쟁이 수량경쟁보다 더 치열합니다. 가격은 전략적 보완재라서 후발자가 유리합니다.")


# ---------------------------------------------------------------- 진입
def entry(a=100, b=1, c=10, e=40, nmax=40):
    n = np.arange(1, 41)
    qn = (a - c) / (b * (n + 1))
    Pn = (a + n * c) / (n + 1)
    pin = (a - c) ** 2 / (b * (n + 1) ** 2)
    ne = int(np.sum(pin >= e))
    Q = n * qn
    W = b * Q ** 2 / 2 + n * (pin - e)
    ns = int(n[np.argmax(W)])
    fig, ax = plt.subplots(1, 3, figsize=(11, 4.4))
    for A_ in ax: A_.set_xlim(0, 41)
    ax[0].plot(n, pin, "-o", ms=3, color=C1, label="π(n)")
    ax[0].axhline(e, color=C2, ls="--", label=f"entry cost e={_f(e, 0)}")
    ax[0].axvline(ne + .5, color=GR, ls=":")
    ax[0].set_ylim(0, 1500)
    ax[0].set_xlabel("number of firms n"); ax[0].set_title(f"Free entry: n^e = {ne}")
    ax[0].legend()
    ax[1].plot(n, Pn, "-o", ms=3, color=C1, label="P(n)")
    ax[1].axhline(c, color=GR, ls=":", label="marginal cost")
    ax[1].set_ylim(0, PAX)
    ax[1].set_xlabel("n"); ax[1].set_title("Price falls toward c"); ax[1].legend()
    ax[2].plot(n, W, "-o", ms=3, color=C3)
    ax[2].axvline(ns, color=C3, ls="--", label=f"social optimum n* = {ns}")
    ax[2].axvline(max(ne, 1), color=C2, ls="--", label=f"free entry = {ne}")
    ax[2].set_ylim(-2000, 8000)
    ax[2].set_xlabel("n"); ax[2].set_title("Welfare = CS + profits − entry cost"); ax[2].legend()
    rows = [("자유진입 균형 기업 수 $n^e$", ne),
            ("사회적 최적 기업 수 $n^*$", ns),
            ("$n^e$에서 기업당 이윤 $\\pi(n^e)$", _f(pin[ne - 1]) if ne else "-"),
            ("$n^e$에서 가격", _f(Pn[ne - 1]) if ne else "-")]
    return _out(fig, rows, "진입비용 e가 커지면 시장에 들어오는 기업 수가 줄어듭니다. 사업 빼앗기 효과 때문에 자유진입은 사회적 최적보다 기업이 많은 경우가 흔합니다.")


# ------------------------------------------------------------ 행태 모수
def conduct(a=100, b=1, c=20, lam=0.5):
    Q = lambda l: (a - c) / (b * (1 + l))
    q = Q(lam); p = a - b * q
    eta = p / (b * q)
    L = (p - c) / p
    fig, ax = plt.subplots(1, 2, figsize=(10.5, 4.2))
    g = np.linspace(0, QAX, 100)
    ax[0].plot(g, a - b * g, color=C1, label="demand P(Q)")
    ax[0].plot(g, a - b * (1 + lam) * g, color=C2, label=f"MR(λ={lam:.2f})")
    ax[0].axhline(c, color=GR, ls=":", label="MC")
    ax[0].plot(q, p, "o", color="k")
    ax[0].set_xlim(0, QAX); ax[0].set_ylim(0, PAX); ax[0].set_xlabel("Q"); ax[0].legend(); ax[0].set_title("Equilibrium p + λP′Q = c")
    ls_ = np.linspace(0, 1, 50)
    ax[1].plot(ls_, [(a - b * Q(l) - c) / (a - b * Q(l)) for l in ls_], color=C1)
    ax[1].plot(lam, L, "o", color="k")
    for l, t in ((0, "competition"), (.5, "n=2 Cournot"), (1, "monopoly")):
        ax[1].annotate(t, (l, (a - b * Q(l) - c) / (a - b * Q(l))), fontsize=7)
    ax[1].set_xlim(0, 1); ax[1].set_ylim(0, 1)
    ax[1].set_xlabel("conduct parameter λ"); ax[1].set_ylabel("Lerner index L")
    ax[1].set_title("L = λ/η")
    rows = [("시장 생산량 $Q$", _f(q)), ("가격 $P$", _f(p)),
            ("수요의 가격탄력성 $\\eta$", _f(eta)), ("러너지수 $L=(P-c)/P$", _f(L, 3)), ("$\\lambda/\\eta$ (검산)", _f(lam / eta, 3))]
    return _out(fig, rows, r"$\lambda=0$ 완전경쟁, $\lambda=1/n$ $n$기업 쿠르노, $\lambda=1$ 독점. 관측된 가격·수량만으로는 $\lambda$와 한계비용 기울기를 구별하기 어렵습니다(식별 문제).")


# ------------------------------------------------------------ 모형 비교
def compare(a=100, b=1, c=10):
    Qm = (a - c) / (2 * b); Qc = 2 * (a - c) / (3 * b); Qs = 3 * (a - c) / (4 * b); Qp = (a - c) / b
    Qs_ = {"Competition/Bertrand": Qp, "Stackelberg": Qs, "Cournot": Qc, "Monopoly": Qm}
    names = list(Qs_)
    Q = np.array([Qs_[k] for k in names])
    P = a - b * Q
    prof = (P - c) * Q
    cs = b * Q ** 2 / 2
    W = cs + prof
    fig, ax = plt.subplots(1, 3, figsize=(11, 4.2))
    cols = [GR, C3, C1, C2]
    for A, v, t, yl in zip(ax, (P, prof, W), ("Price", "Industry profit", "Total welfare"), (PAX, 8000, 15000)):
        A.set_ylim(0, yl)
        A.bar(range(4), v, color=cols); A.set_xticks(range(4), names, rotation=18, fontsize=8)
        A.set_title(t)
        for i, x in enumerate(v):
            A.text(i, x, _f(x, 1), ha="center", va="bottom", fontsize=8)
    rows = [(n_, f"Q={_f(q)}  P={_f(p)}  이윤={_f(pr)}  후생={_f(w)}")
            for n_, q, p, pr, w in zip(names, Q, P, prof, W)]
    return _out(fig, rows, "생산량: 완전경쟁 > 스타켈베르크 > 쿠르노 > 독점. 가격은 반대 순서입니다 (동질재, 대칭 비용).")


# ------------------------------------------- 그림 6-1: 부분게임완전균형
def spne(a=100, b=1, c=10):
    k = (a - c) / b
    pts = {"M": (k / 4, k / 4), "C": (k / 3, k / 3), "S1": (k / 2, k / 4),
           "S2": (k / 4, k / 2), "W": (k / 2, k / 2)}
    prof = {n: ((a - b * (x + y) - c) * x, (a - b * (x + y) - c) * y) for n, (x, y) in pts.items()}
    L = 110
    g = np.linspace(0, L, 200)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw={"width_ratios": [1.15, 1]})
    A = ax[0]
    r = np.where(g <= k, k / 2 - g / 2, np.nan)
    A.plot(r, g, color=C1, label="R1 (firm 1)")
    A.plot(g, r, color=C2, label="R2 (firm 2)")
    for n, (x, y) in pts.items():
        A.plot(x, y, "o", color="k", ms=7)
        A.annotate(n.replace("S1", "$S_1$").replace("S2", "$S_2$"), (x, y), xytext=(6, 6),
                   textcoords="offset points", fontsize=11, weight="bold")
        A.plot([x, x], [0, y], ":", color=GR, lw=1); A.plot([0, x], [y, y], ":", color=GR, lw=1)
    A.set_xlim(0, L); A.set_ylim(0, L)
    A.set_xlabel("q1 (firm 1 output)"); A.set_ylabel("q2 (firm 2 output)")
    A.set_title("Subgame-perfect outcomes"); A.legend(fontsize=8, loc="upper right")
    B = ax[1]
    names = list(pts)
    x = np.arange(len(names)); w = .38
    B.bar(x - w / 2, [prof[n][0] for n in names], w, color=C1, label="firm 1")
    B.bar(x + w / 2, [prof[n][1] for n in names], w, color=C2, label="firm 2")
    B.set_xticks(x, [n.replace("S1", "S1").replace("S2", "S2") for n in names])
    B.set_ylim(0, 4000); B.legend(fontsize=8); B.set_title("Profits at each point")
    desc = {"M": "담합 (각자 독점 생산량의 절반)", "C": "쿠르노–내시 (동시 선택)",
            "S1": "기업 1 선도, 기업 2 추종", "S2": "기업 2 선도, 기업 1 추종",
            "W": "둘 다 선도자로 행동 (스타켈베르크 전쟁)"}
    rows = [(f"{n} · {desc[n]}",
             f"q=({_f(pts[n][0])}, {_f(pts[n][1])})  π=({_f(prof[n][0], 1)}, {_f(prof[n][1], 1)})") for n in names]
    return _out(fig, rows, "S₁은 기업 1이 선도자 수량 (a−c)/2b를 정할 때 기업 2의 반응함수 위의 점, S₂는 그 반대입니다. 둘 다 선도자 수량을 고르면 W에서 가격이 한계비용까지 떨어집니다.".replace("S₁", "$S_1$").replace("S₂", "$S_2$").replace("(a−c)/2b", "$(a-c)/2b$"))


# ------------------------------------ 그림 6-2: 선도자·추종자 불명확
def timing_game(a=100, b=1, c=10, n_traj=16, seed=3):
    u = (a - c) ** 2 / b
    # A[i][j]: 기업 1 보수, i=0 선도/1 추종; j: 기업 2
    A = np.array([[0, u / 8], [u / 16, u / 9]])
    Bm = np.array([[0, u / 16], [u / 8, u / 9]])
    lab = ["Lead", "Follow"]
    ne = []
    for i in range(2):
        for j in range(2):
            if A[i, j] >= A[1 - i, j] and Bm[i, j] >= Bm[i, 1 - j]:
                ne.append((i, j))
    q = (A[1, 1] - A[0, 1]) / (A[0, 0] - A[0, 1] - A[1, 0] + A[1, 1])   # P(기업 2 선도)
    p = (Bm[1, 1] - Bm[1, 0]) / (Bm[0, 0] - Bm[1, 0] - Bm[0, 1] + Bm[1, 1])  # P(기업 1 선도)
    ev1 = q * A[0, 0] + (1 - q) * A[0, 1]
    ev2 = p * Bm[0, 0] + (1 - p) * Bm[1, 0]

    fig, ax = plt.subplots(1, 2, figsize=(11, 4.6))
    M = ax[0]; M.set_xlim(0, 3); M.set_ylim(-.6, 3); M.axis("off"); M.grid(False)
    M.set_title("Payoffs: (firm 1, firm 2)", fontsize=10)
    for j in range(2):
        M.text(1.5 + j, 2.75, f"Firm 2: {lab[j]}", ha="center", weight="bold", color=C2)
    for i in range(2):
        M.text(.45, 1.5 - i, f"Firm 1:\n{lab[i]}", ha="center", va="center", weight="bold", color=C1)
        for j in range(2):
            isne = (i, j) in ne
            M.add_patch(plt.Rectangle((1 + j, 1 - i + .0), 1, 1, fc="#dbeafe" if isne else "#f3f4f6",
                                      ec="k", lw=2 if isne else .8))
            M.text(1.5 + j, 1.5 - i, f"{A[i, j] / u:.4f}\n,\n{Bm[i, j] / u:.4f}".replace("\n,\n", ",  "),
                   ha="center", va="center", fontsize=9)
            M.text(1.5 + j, 1.12 - i, ["0,0", "1/8, 1/16", "1/16, 1/8", "1/9, 1/9"][2 * i + j],
                   ha="center", va="center", fontsize=8, color=GR)
    M.text(1.5, -.3, f"unit = (a−c)²/b = {u:,.0f};  blue = pure Nash equilibrium", ha="center", fontsize=8)

    P = ax[1]
    P.set_xlim(0, 1); P.set_ylim(0, 1)
    P.set_xlabel("x = P(firm 1 leads)"); P.set_ylabel("y = P(firm 2 leads)")
    P.set_title("Replicator dynamics (simulation)")
    rng = np.random.default_rng(int(seed))
    ends = {"LF": 0, "FL": 0, "other": 0}
    for _ in range(int(n_traj)):
        x, y = rng.uniform(.02, .98, 2)
        tx, ty = [x], [y]
        for _ in range(600):
            u1 = (y * A[0, 0] + (1 - y) * A[0, 1] - y * A[1, 0] - (1 - y) * A[1, 1]) / u
            u2 = (x * Bm[0, 0] + (1 - x) * Bm[1, 0] - x * Bm[0, 1] - (1 - x) * Bm[1, 1]) / u
            x = min(max(x + 4 * x * (1 - x) * u1, 0), 1)
            y = min(max(y + 4 * y * (1 - y) * u2, 0), 1)
            tx.append(x); ty.append(y)
        k = "LF" if x > .9 and y < .1 else "FL" if x < .1 and y > .9 else "other"
        ends[k] += 1
        col = C1 if k == "LF" else C2 if k == "FL" else GR
        P.plot(tx, ty, color=col, lw=1, alpha=.7); P.plot(tx[0], ty[0], ".", color=col)
    P.plot([1, 0], [0, 1], "o", color="k", ms=8)
    P.annotate("(Lead, Follow)", (1, 0), xytext=(-70, 8), textcoords="offset points", fontsize=8)
    P.annotate("(Follow, Lead)", (0, 1), xytext=(6, -14), textcoords="offset points", fontsize=8)
    P.plot(p, q, "s", color=C3, ms=8, label=f"mixed NE ({p:.3f}, {q:.3f})")
    P.legend(fontsize=8, loc="center right")

    nm = {(0, 1): "(선도, 추종)", (1, 0): "(추종, 선도)", (0, 0): "(선도, 선도)", (1, 1): "(추종, 추종)"}
    rows = [("순수전략 내시균형", ", ".join(nm[t] for t in ne) or "없음"),
            ("혼합전략 균형: 선도 확률 $(x^*, y^*)$", f"({p:.4f}, {q:.4f})"),
            ("혼합전략 균형의 기대보수 (단위 $(a-c)^2/b$)", f"{ev1 / u:.4f}, {ev2 / u:.4f}"),
            ("순수균형 보수 비교 (선도자 / 추종자)", f"{A[0, 1] / u:.4f} / {Bm[0, 1] / u:.4f}"),
            ("시뮬레이션 결과 (1이 선도 / 2가 선도 / 기타)", f"{ends['LF']} / {ends['FL']} / {ends['other']}")]
    return _out(fig, rows, "누가 선도자가 될지 정해져 있지 않으면 둘 다 선도(0,0)나 둘 다 추종(1/9,1/9)보다 한쪽만 선도하는 두 균형이 나옵니다. 어느 쪽이 될지는 게임만으로 정해지지 않아 조정 문제가 남습니다.")


# ------------------------------------------------ 스타켈베르크: 등이윤곡선
def isoprofit(a=100, b=1, c1=10, c2=10, **_):
    QZ = 120  # 고정 축
    q1c, q2c = cournot_eq(a, b, c1, c2)
    q1s = max((a - 2 * c1 + c2) / (2 * b), 0)
    q2s = max((a - c2) / (2 * b) - q1s / 2, 0)
    pi_s = (a - b * (q1s + q2s) - c1) * q1s
    pi_c = (a - b * (q1c + q2c) - c1) * q1c
    pi_m = (a - c1) ** 2 / (4 * b)
    g = np.linspace(0.05, QZ, 800)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.6))
    A = ax[0]
    levels = sorted(set([f * pi_m for f in (.1, .25, .45, .65, .85)] + [pi_c, pi_s]))
    for k in levels:
        y = (a - c1) / b - g - k / (b * g)
        m = y >= 0
        special = abs(k - pi_s) < 1e-9 or abs(k - pi_c) < 1e-9
        col = C3 if abs(k - pi_s) < 1e-9 else "k" if abs(k - pi_c) < 1e-9 else C1
        A.plot(g[m], y[m], color=col, lw=2.2 if special else 1, alpha=1 if special else .6)
        if m.any():
            i = int(np.argmax(y)); A.plot(g[i], y[i], ".", color=col, ms=5)
            A.annotate(f"{k:,.0f}", (g[i], y[i]), xytext=(0, 4), textcoords="offset points",
                       fontsize=7, ha="center", color=col)
    A.plot(np.where(g <= (a - c1) / b, (a - c1) / (2 * b) - g / 2, np.nan), g, "--", color=C1, lw=1, label="R1 = peaks of iso-profit curves")
    A.plot(g, np.where(g <= (a - c2) / b, (a - c2) / (2 * b) - g / 2, np.nan), color=C2, label="R2 (follower)")
    A.plot(q1c, q2c, "o", color="k", label="Cournot")
    A.plot(q1s, q2s, "*", color=C3, ms=14, label="Stackelberg (tangency)")
    A.set_xlim(0, QZ); A.set_ylim(0, QZ)
    A.set_xlabel("q1 (leader)"); A.set_ylabel("q2")
    A.set_title("Iso-profit curves of firm 1 (labels = profit)"); A.legend(fontsize=7)
    B = ax[1]
    q1g = np.linspace(0, QZ, 400)
    q2r = np.maximum((a - c2) / (2 * b) - q1g / 2, 0)
    lead = (a - b * (q1g + q2r) - c1) * q1g
    B.plot(q1g, lead, color=C1)
    B.axhline(pi_c, color="k", ls=":", lw=1, label=f"Cournot profit {pi_c:,.0f}")
    B.plot(q1s, pi_s, "*", color=C3, ms=14, label=f"leader's optimum q1 = {q1s:,.1f}")
    B.set_xlim(0, QZ); B.set_ylim(-1000, 4000)
    B.set_xlabel("q1"); B.set_ylabel("π1 along follower's R2")
    B.set_title("Leader's problem: π1(q1, R2(q1))"); B.legend(fontsize=8)
    rows = [("꼭짓점 위치 (반응함수 $R_1$ 위)", "$q_1=\\sqrt{k/b}$"),
            ("스타켈베르크 접점 $(q_1^S,q_2^S)$", f"{_f(q1s)}, {_f(q2s)}"),
            ("접점의 등이윤 수준 $\\pi_1^S$", _f(pi_s)),
            ("쿠르노 점의 등이윤 수준 $\\pi_1^C$", _f(pi_c)),
            ("접점에서 $R_2$의 기울기", "$-1/2$")]
    return _out(fig, rows, "등이윤곡선은 아래쪽일수록 기업 1의 이윤이 큽니다. 선도자는 추종자의 반응함수 R2와 접하는 가장 아래쪽 곡선(초록)을 고릅니다. 쿠르노 점은 R2 위에서 더 위쪽 곡선(검정)이라 이윤이 낮습니다.")


# ------------------------------------------- 쿠르노: 두 기업의 등이윤곡선
def isoprofit_cournot(a=100, b=1, c1=10, c2=10, **_):
    QZ = 120
    q1c, q2c = cournot_eq(a, b, c1, c2)
    pi1 = lambda x, y: (a - b * (x + y) - c1) * x
    pi2 = lambda x, y: (a - b * (x + y) - c2) * y
    k1, k2 = pi1(q1c, q2c), pi2(q1c, q2c)
    cm = min(c1, c2)
    qm = (a - cm) / (2 * b)
    mx, my = ((qm / 2, qm / 2) if c1 == c2 else (qm, 0) if c1 < c2 else (0, qm))
    g = np.linspace(0.05, QZ, 800)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.6))
    A = ax[0]
    for f in (.1, .25, .45, .65, .85):
        k = f * (a - c1) ** 2 / (4 * b)
        y = (a - c1) / b - g - k / (b * g); m = y >= 0
        A.plot(g[m], y[m], color=C1, lw=.9, alpha=.55)
        k = f * (a - c2) ** 2 / (4 * b)
        x = (a - c2) / b - g - k / (b * g); m = x >= 0
        A.plot(x[m], g[m], color=C2, lw=.9, alpha=.55)
    y = (a - c1) / b - g - k1 / (b * g); m = y >= 0
    A.plot(g[m], y[m], color=C1, lw=2.4, label=f"firm 1: $\\pi_1$ = {k1:,.0f}")
    x = (a - c2) / b - g - k2 / (b * g); m = x >= 0
    A.plot(x[m], g[m], color=C2, lw=2.4, label=f"firm 2: $\\pi_2$ = {k2:,.0f}")
    r = np.where(g <= (a - c1) / b, (a - c1) / (2 * b) - g / 2, np.nan)
    A.plot(r, g, "--", color=C1, lw=1, label="R1 (peaks of firm 1 curves)")
    r = np.where(g <= (a - c2) / b, (a - c2) / (2 * b) - g / 2, np.nan)
    A.plot(g, r, "--", color=C2, lw=1, label="R2 (peaks of firm 2 curves)")
    A.plot(q1c, q2c, "o", color="k", ms=8, label="Cournot")
    A.set_xlim(0, QZ); A.set_ylim(0, QZ); A.set_xlabel("q1"); A.set_ylabel("q2")
    A.set_title("Iso-profit curves of both firms"); A.legend(fontsize=7)
    B = ax[1]
    X, Y = np.meshgrid(np.linspace(0, QZ, 400), np.linspace(0, QZ, 400))
    lens = (pi1(X, Y) > k1) & (pi2(X, Y) > k2) & (X + Y < a / b)
    B.contourf(X, Y, lens.astype(float), levels=[.5, 1.5], colors=[C3], alpha=.35)
    for kk, col in ((k1, C1), (k2, C2)):
        if col == C1:
            y = (a - c1) / b - g - kk / (b * g); m = y >= 0; B.plot(g[m], y[m], color=col, lw=2)
        else:
            x = (a - c2) / b - g - kk / (b * g); m = x >= 0; B.plot(x[m], g[m], color=col, lw=2)
    B.plot(q1c, q2c, "o", color="k", ms=8); B.annotate("C", (q1c, q2c), xytext=(6, 6), textcoords="offset points", weight="bold")
    B.plot(mx, my, "*", color=C3, ms=14); B.annotate("M", (mx, my), xytext=(6, 6), textcoords="offset points", weight="bold")
    B.set_xlim(0, QZ); B.set_ylim(0, QZ); B.set_xlabel("q1"); B.set_ylabel("q2")
    B.set_title("Green lens: both firms earn more than at C")
    in_lens = bool(pi1(mx, my) > k1 and pi2(mx, my) > k2)
    rows = [("쿠르노 점 $C$의 이윤 $(\\pi_1^C,\\pi_2^C)$", f"{_f(k1)}, {_f(k2)}"),
            ("$C$에서 기업 1 곡선의 접선", "수평 (꼭짓점)"),
            ("$C$에서 기업 2 곡선의 접선", "수직 (꼭짓점)"),
            ("담합점 $M$ 이윤", f"{_f(pi1(mx, my))}, {_f(pi2(mx, my))}"),
            ("$M$이 렌즈 안에 있는가", "예" if in_lens else "아니오")]
    return _out(fig, rows, "쿠르노 점에서 두 기업의 등이윤곡선은 직각으로 만나 렌즈 모양의 영역을 만듭니다. 이 영역 안에서는 두 기업 모두 쿠르노보다 이윤이 높아 담합이 유인되지만, 담합점은 반응곡선 위가 아니므로 균형이 아닙니다.")
