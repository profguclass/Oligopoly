"""과점시장 모형 시뮬레이터 (IO Ch.01). 브라우저의 Pyodide에서 실행됩니다."""
import io, json, base64
import numpy as np
import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt

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
    g = np.linspace(0, qmax, 200)
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
    A.set_xlim(0, qmax); A.set_ylim(0, qmax)
    A.set_xlabel("q1"); A.set_ylabel("q2"); A.set_title("Best responses & adjustment")
    A.legend(fontsize=7)

    # 담합 이탈
    B = ax[1]
    g1 = np.linspace(0, qmax, 200)
    dev = (a - b * (g1 + qm2) - c1) * g1
    B.plot(g1, dev, color=C1)
    qd = float(br1(qm2))
    B.plot(qm1, pim1, "*", color=C3, ms=13, label=f"cartel q1={_f(qm1)}")
    B.plot(qd, (a - b * (qd + qm2) - c1) * qd, "o", color=C2, ms=8,
           label=f"best deviation q1={_f(qd)}")
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
    C.set_title("Total profit")

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
    ax[0].set_xlabel("round"); ax[0].set_ylabel("price"); ax[0].legend()
    ax[0].set_title("Undercutting war (dotted = marginal cost)")
    # 기업 1의 이윤 함수 (p2 고정)
    pg = np.linspace(0, a, 400)
    p2f = p2
    D = np.maximum((a - pg) / b, 0)
    share = np.where(pg < p2f, 1.0, np.where(pg == p2f, .5, 0.0))
    ax[1].plot(pg, (pg - c1) * D * share, color=C1)
    ax[1].axvline(p2f, color=C2, ls="--", lw=1, label=f"rival price = {_f(p2f, 1)}")
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
    g = np.linspace(0.01, qmax, 400)
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
    A.set_xlim(0, qmax); A.set_ylim(0, qmax); A.set_xlabel("q1 (leader)"); A.set_ylabel("q2")
    A.set_title("Leader picks the best point on R2"); A.legend(fontsize=7)
    B = ax[1]
    x = np.arange(2); w = .35
    B.bar(x - w / 2, pic, w, label="Cournot", color=GR)
    B.bar(x + w / 2, pis, w, label="Stackelberg", color=C3)
    B.set_xticks(x, ["leader (1)", "follower (2)"]); B.legend(); B.set_title("Profits")
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
    pg = np.linspace(0, pB * 1.8, 100)
    A.plot((a + b * c) / (2 * b) + d / (2 * b) * pg, pg, color=C1, label="R1(p2)")
    A.plot(pg, (a + b * c) / (2 * b) + d / (2 * b) * pg, color=C2, label="R2(p1)")
    A.plot(pB, pB, "o", color="k", label="Bertrand-Nash")
    A.plot(p1s, p2s, "*", color=C3, ms=13, label="firm 1 moves first")
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
    ax[1].set_xlabel("substitutability γ/β"); ax[1].set_ylabel("price"); ax[1].legend()
    ax[1].set_title("Price: Bertrand < Cournot")
    ax[2].plot(gs / beta, ibs, color=C1, label="Bertrand")
    ax[2].plot(gs / beta, ics, color=C2, label="Cournot")
    ax[2].axvline(gamma / beta, color=GR, ls=":")
    ax[2].set_xlabel("substitutability γ/β"); ax[2].set_ylabel("profit per firm")
    ax[2].legend(); ax[2].set_title("Profit shrinks as goods get closer")
    rows = [("수요계수 $(a,b,d)$", f"{_f(a)}, {_f(b, 3)}, {_f(d, 3)}"),
            ("베르트랑 가격 / 기업당 이윤", f"{_f(pB)} / {_f(piB)}"),
            ("쿠르노 가격 / 기업당 이윤", f"{_f(pC)} / {_f(piC)}"),
            ("순차 가격: 선도자 $p_1$ / 후발자 $p_2$", f"{_f(p1s)} / {_f(p2s)}"),
            ("순차 가격 이윤 (선도자, 후발자)", f"{_f(pi1s)}, {_f(pi2s)}")]
    return _out(fig, rows, "같은 수요 구조(Singh–Vives)에서 가격경쟁이 수량경쟁보다 더 치열합니다. 가격은 전략적 보완재라서 후발자가 유리합니다.")


# ---------------------------------------------------------------- 진입
def entry(a=100, b=1, c=10, e=40, nmax=15):
    n = np.arange(1, int(nmax) + 1)
    qn = (a - c) / (b * (n + 1))
    Pn = (a + n * c) / (n + 1)
    pin = (a - c) ** 2 / (b * (n + 1) ** 2)
    ne = int(np.sum(pin >= e))
    Q = n * qn
    W = b * Q ** 2 / 2 + n * (pin - e)
    ns = int(n[np.argmax(W)])
    fig, ax = plt.subplots(1, 3, figsize=(11, 4.4))
    ax[0].plot(n, pin, "-o", ms=3, color=C1, label="π(n)")
    ax[0].axhline(e, color=C2, ls="--", label=f"entry cost e={_f(e, 0)}")
    ax[0].axvline(ne + .5, color=GR, ls=":")
    ax[0].set_xlabel("number of firms n"); ax[0].set_title(f"Free entry: n^e = {ne}")
    ax[0].legend()
    ax[1].plot(n, Pn, "-o", ms=3, color=C1, label="P(n)")
    ax[1].axhline(c, color=GR, ls=":", label="marginal cost")
    ax[1].set_xlabel("n"); ax[1].set_title("Price falls toward c"); ax[1].legend()
    ax[2].plot(n, W, "-o", ms=3, color=C3)
    ax[2].axvline(ns, color=C3, ls="--", label=f"social optimum n* = {ns}")
    ax[2].axvline(max(ne, 1), color=C2, ls="--", label=f"free entry = {ne}")
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
    g = np.linspace(0, a / b, 100)
    ax[0].plot(g, a - b * g, color=C1, label="demand P(Q)")
    ax[0].plot(g, a - b * (1 + lam) * g, color=C2, label=f"MR(λ={lam:.2f})")
    ax[0].axhline(c, color=GR, ls=":", label="MC")
    ax[0].plot(q, p, "o", color="k")
    ax[0].set_ylim(0, a); ax[0].set_xlabel("Q"); ax[0].legend(); ax[0].set_title("Equilibrium p + λP′Q = c")
    ls_ = np.linspace(0, 1, 50)
    ax[1].plot(ls_, [(a - b * Q(l) - c) / (a - b * Q(l)) for l in ls_], color=C1)
    ax[1].plot(lam, L, "o", color="k")
    for l, t in ((0, "competition"), (.5, "n=2 Cournot"), (1, "monopoly")):
        ax[1].annotate(t, (l, (a - b * Q(l) - c) / (a - b * Q(l))), fontsize=7)
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
    for A, v, t in zip(ax, (P, prof, W), ("Price", "Industry profit", "Total welfare")):
        A.bar(range(4), v, color=cols); A.set_xticks(range(4), names, rotation=18, fontsize=8)
        A.set_title(t)
        for i, x in enumerate(v):
            A.text(i, x, _f(x, 1), ha="center", va="bottom", fontsize=8)
    rows = [(n_, f"Q={_f(q)}  P={_f(p)}  이윤={_f(pr)}  후생={_f(w)}")
            for n_, q, p, pr, w in zip(names, Q, P, prof, W)]
    return _out(fig, rows, "생산량: 완전경쟁 > 스타켈베르크 > 쿠르노 > 독점. 가격은 반대 순서입니다 (동질재, 대칭 비용).")
