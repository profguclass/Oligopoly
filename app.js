const COMMON = [["a","수요 절편 $a$",50,150,1,100],["b","수요 기울기 $b$",.75,2,.05,1]];
const MODELS = [
  { id:"cournot", fn:"cournot", extra:"isoprofit_cournot", name:"쿠르노", title:"쿠르노 모형: 수량 경쟁과 담합의 붕괴",
    theory:`<p>두 기업이 동시에 생산량을 선택한다. 역수요와 이윤은</p>
      $$P=a-b(q_1+q_2),\\qquad \\pi_1=\\bigl[a-b(q_1+q_2)-c_1\\bigr]q_1$$
      <p>1계 조건 $\\partial\\pi_1/\\partial q_1=0$에서 반응함수를 얻는다(전략적 대체재).</p>
      $$q_1^*(q_2)=\\frac{a-c_1}{2b}-\\frac{q_2}{2}$$
      <p>대칭 비용($c_1=c_2=c$)의 쿠르노–내시 균형:</p>
      $$q^*=\\frac{a-c}{3b},\\quad P^*=\\frac{a+2c}{3},\\quad \\pi^*=\\frac{(a-c)^2}{9b}$$
      <p>담합(독점) 생산량과 이윤:</p>
      $$Q^m=\\frac{a-c}{2b},\\quad \\pi_i^m=\\frac{(a-c)^2}{8b}>\\pi^*$$
      <p>등이윤곡선: 기업 1의 이윤이 같은 값 $k_1$인 점의 집합과 기업 2의 것은</p>
      $$\\pi_1=(a-c_1-bq_1-bq_2)\\,q_1=k_1\\;\\Rightarrow\\;q_2=\\frac{a-c_1}{b}-q_1-\\frac{k_1}{b\\,q_1}$$
      $$\\pi_2=(a-c_2-bq_1-bq_2)\\,q_2=k_2\\;\\Rightarrow\\;q_1=\\frac{a-c_2}{b}-q_2-\\frac{k_2}{b\\,q_2}$$
      <p>담합점에서의 한계이윤 $\\left.\\dfrac{\\partial\\pi_1}{\\partial q_1}\\right|_{q^m}=b\\,q_2^m>0$이므로 이탈 유인이 있다.</p>`,
    params:[...COMMON,["c1","기업 1 한계비용 $c_1$",0,50,1,10],["c2","기업 2 한계비용 $c_2$",0,50,1,10]] },
  { id:"bertrand", fn:"bertrand", name:"베르트랑", title:"베르트랑 모형: 가격 경쟁과 역설",
    theory:`<p>동질재, 두 기업이 가격을 동시에 선택한다. 더 싼 기업이 시장 전체를 가져간다.</p>
      $$D_1(p_1,p_2)=\\begin{cases}\\dfrac{a-p_1}{b}, & p_1<p_2\\\\[4pt] \\tfrac12\\,\\dfrac{a-p_1}{b}, & p_1=p_2\\\\[4pt] 0, & p_1>p_2\\end{cases}$$
      <p>$p_1>p_2>c$이면 $p_1=p_2-\\varepsilon$으로 낮출 유인이 있으므로 유일한 균형은</p>
      $$p_1^*=p_2^*=c,\\qquad \\pi_1^*=\\pi_2^*=0$$
      <p>(베르트랑 역설). 비용이 다르면($c_1<c_2$) 기업 1이 상대 비용 바로 아래의 가격으로 시장 전체를 공급한다.</p>`,
    params:[...COMMON,["c1","기업 1 한계비용 $c_1$",0,50,1,10],["c2","기업 2 한계비용 $c_2$",0,50,1,10],["p1_0","시작 가격 $p_1$",0,150,1,80],["p2_0","시작 가격 $p_2$",0,150,1,75],["eps","인하 폭 $\\varepsilon$",.5,10,.5,2],["rounds","라운드 수",2,150,2,80]] },
  { id:"stackelberg", fn:"stackelberg", extra:"isoprofit", name:"스타켈베르크", title:"스타켈베르크 모형: 선도자 이점",
    theory:`<p>기업 1(선도자)이 먼저 $q_1$을 정하고 기업 2(추종자)가 관찰 후 선택한다. 역진귀납법:</p>
      <p><b>2단계</b> 추종자의 최적화</p>
      $$\\max_{q_2}\\,[a-b(q_1+q_2)-c_2]\\,q_2\\;\\Rightarrow\\; q_2^*(q_1)=\\frac{a-c_2}{2b}-\\frac{q_1}{2}$$
      <p><b>1단계</b> 선도자는 $q_2^*(q_1)$을 이윤에 대입해 극대화한다.</p>
      $$q_1^S=\\frac{a-2c_1+c_2}{2b}$$
      <p>대칭 비용일 때:</p>
      $$q_1^S=\\frac{a-c}{2b},\\; q_2^S=\\frac{a-c}{4b},\\; P^S=\\frac{a+3c}{4}$$
      $$\\pi_1^S=\\frac{(a-c)^2}{8b},\\quad \\pi_2^S=\\frac{(a-c)^2}{16b}$$
      <p>기업 1의 등이윤곡선(이윤 $k$)은</p>
      $$\\pi_1(q_1,q_2)=(a-c_1-bq_1-bq_2)\\,q_1=k\\;\\Longleftrightarrow\\;q_2=\\frac{a-c_1}{b}-q_1-\\frac{k}{b\\,q_1}$$
      <p>꼭짓점은 $R_1$ 위에 있고 아래쪽 곡선일수록 이윤이 크다. 이 곡선이 추종자 반응함수에 접하는 점이 균형이다.</p>`,
    params:[...COMMON,["c1","선도자 한계비용 $c_1$",0,50,1,10],["c2","추종자 한계비용 $c_2$",0,50,1,10]] },
  { id:"spne", fn:"spne", name:"부분게임완전균형", title:"그림 6-1: 생산량결정 복점모형의 부분게임완전균형",
    theory:`<p>$k=(a-c)/b$로 두면 반응함수는 $q_i=\\dfrac{k}{2}-\\dfrac{q_j}{2}$이다. 그림의 다섯 점:</p>
      $$M=\\Bigl(\\tfrac k4,\\tfrac k4\\Bigr),\\; C=\\Bigl(\\tfrac k3,\\tfrac k3\\Bigr),\\; S_1=\\Bigl(\\tfrac k2,\\tfrac k4\\Bigr),\\; S_2=\\Bigl(\\tfrac k4,\\tfrac k2\\Bigr),\\; W=\\Bigl(\\tfrac k2,\\tfrac k2\\Bigr)$$
      <p>$S_1$은 기업 1이 선도자 수량 $\\tfrac{a-c}{2b}$를 정하고 기업 2가 반응함수 위에서 추종하는 점, $S_2$는 그 반대다. 둘 다 선도자 수량을 고르면 $W$에서 $P=c$가 되어 이윤은 0이다.</p>`,
    params:[...COMMON,["c","한계비용 $c$",0,50,1,10]] },
  { id:"timing", fn:"timing_game", name:"선도·추종 게임", title:"그림 6-2: 선도자와 추종자가 불명확한 스타켈베르크 복점모형",
    theory:`<p>누가 선도자가 될지 정해져 있지 않을 때 각 기업이 \"선도\"와 \"추종\" 중 하나를 고른다. 보수(단위 $(a-c)^2/b$):</p>
      $$\\begin{array}{c|cc} & \\text{2: 선도} & \\text{2: 추종}\\\\\\hline \\text{1: 선도} & 0,\\,0 & \\tfrac18,\\,\\tfrac1{16}\\\\ \\text{1: 추종} & \\tfrac1{16},\\,\\tfrac18 & \\tfrac19,\\,\\tfrac19\\end{array}$$
      <p>순수전략 내시균형은 (선도, 추종)과 (추종, 선도) 두 개이고, 대칭 혼합전략 균형도 있다. 오른쪽 그림은 복제자 동학으로 시작점에 따라 어느 균형에 수렴하는지 시뮬레이션한 것이다.</p>`,
    params:[...COMMON,["c","한계비용 $c$",0,50,1,10],["n_traj","시뮬레이션 횟수",1,40,1,16],["seed","난수 시드",1,50,1,3]] },
  { id:"differentiated", fn:"differentiated", name:"제품 차별화", title:"제품 차별화: 가격 경쟁 vs 수량 경쟁",
    theory:`<p>한계효용 $\\partial U/\\partial q_i=\\alpha-\\beta q_i-\\gamma q_j$ ($\\beta>\\gamma>0$)에서 역수요와 수요가 나온다.</p>
      $$P_i=\\alpha-\\beta q_i-\\gamma q_j,\\qquad D_i=a-b\\,p_i+d\\,p_j$$
      $$a=\\frac{\\alpha}{\\beta+\\gamma},\\quad b=\\frac{\\beta}{\\beta^2-\\gamma^2},\\quad d=\\frac{\\gamma}{\\beta^2-\\gamma^2}$$
      <p><b>베르트랑</b> (전략적 보완재)</p>
      $$p_1^*(p_2)=\\frac{a+bc}{2b}+\\frac{d}{2b}\\,p_2,\\qquad p^*=\\frac{a+bc}{2b-d}$$
      <p><b>쿠르노</b></p>
      $$q^*=\\frac{\\alpha-c}{2\\beta+\\gamma}$$
      <p><b>순차 가격</b>: 마크업 $m_i=p_i-c$, $A=a-(b-d)c$일 때 후발자는</p>
      $$m_2(m_1)=\\frac{A+d\\,m_1}{2b},\\qquad D_2=b\\,m_2$$
      <p>별 표시는 기업 1이 먼저 가격을 정하는 결과(후발자 이점).</p>`,
    params:[["alpha","최대 지불의사 $\\alpha$",50,150,1,100],["beta","자기효과 $\\beta$",.75,2,.05,1],["gamma","교차효과 $\\gamma$",0,2.9,.05,.6],["c","한계비용 $c$",0,50,1,10]] },
  { id:"entry", fn:"entry", name:"진입", title:"자유진입과 시장구조",
    theory:`<p>$n$개 대칭 기업의 쿠르노 균형:</p>
      $$q(n)=\\frac{a-c}{b(n+1)},\\quad P(n)=\\frac{a+nc}{n+1},\\quad \\pi(n)=\\frac{1}{b}\\left(\\frac{a-c}{n+1}\\right)^2$$
      <p>진입비용 $e$일 때 자유진입 균형 $n^e$는</p>
      $$\\pi(n^e)\\ge e\\quad\\text{이고}\\quad \\pi(n^e+1)<e$$
      <p>사회후생은 소비자잉여 + 이윤 − 진입비용이다.</p>
      $$W(n)=\\frac{b\\,Q^2}{2}+n\\bigl[\\pi(n)-e\\bigr],\\qquad Q=n\\,q(n)$$`,
    params:[...COMMON,["c","한계비용 $c$",0,50,1,10],["e","진입비용 $e$",1,1000,1,40]] },
  { id:"conduct", fn:"conduct", name:"시장지배력", title:"행태 모수 λ와 러너지수",
    theory:`<p>행태 모수 $\\lambda$를 둔 한계수입과 균형 조건:</p>
      $$MR(\\lambda)=P+\\lambda\\,P'(Q)\\,Q,\\qquad P+\\lambda P'(Q)\\,Q=c$$
      <p>$\\lambda=0$ 완전경쟁, $\\lambda=1/n$ 대칭 $n$기업 쿠르노, $\\lambda=1$ 독점.</p>
      <p>러너지수는 수요의 가격탄력성 $\\eta=-\\dfrac{\\partial Q}{\\partial P}\\dfrac{P}{Q}$로</p>
      $$L=\\frac{P-c}{P}=\\frac{\\lambda}{\\eta}$$`,
    params:[...COMMON,["c","한계비용 $c$",0,50,1,20],["lam","행태 모수 $\\lambda$",0,1,.01,.5]] },
  { id:"compare", fn:"compare", name:"모형 비교", title:"네 가지 모형 비교",
    theory:`<p>동질재·대칭 비용에서 시장 산출량:</p>
      $$Q^{PC}=\\frac{a-c}{b}>Q^{S}=\\frac{3(a-c)}{4b}>Q^{C}=\\frac{2(a-c)}{3b}>Q^{M}=\\frac{a-c}{2b}$$
      <p>가격은 반대 순서이고, 사회후생 $W=\\dfrac{bQ^2}{2}+(P-c)Q$는 산출량과 같은 방향으로 움직인다.</p>`,
    params:[...COMMON,["c","한계비용 $c$",0,50,1,10]] },
];

const STEPS = {
spne:[
 ["반응함수","$$R_1(q_2)=\\frac{a-c}{2b}-\\frac{q_2}{2},\\qquad R_2(q_1)=\\frac{a-c}{2b}-\\frac{q_1}{2}$$"],
 ["담합점 $M$","$$M=\\Bigl(\\frac{a-c}{4b},\\frac{a-c}{4b}\\Bigr)$$<p>독점 생산량 $\\tfrac{a-c}{2b}$를 반씩 나눈다.</p>"],
 ["쿠르노–내시 균형 $C$","$$C=\\Bigl(\\frac{a-c}{3b},\\frac{a-c}{3b}\\Bigr)$$<p>두 반응곡선의 교점이다.</p>"],
 ["기업 1이 선도: $S_1$","$$q_1=\\frac{a-c}{2b}\\;\\Rightarrow\\;q_2=R_2(q_1)=\\frac{a-c}{4b}$$"],
 ["기업 2가 선도: $S_2$","$$q_2=\\frac{a-c}{2b}\\;\\Rightarrow\\;q_1=R_1(q_2)=\\frac{a-c}{4b}$$"],
 ["둘 다 선도자처럼 행동: $W$","$$q_1=q_2=\\frac{a-c}{2b}\\;\\Rightarrow\\;P=a-bQ=c,\\quad \\pi_1=\\pi_2=0$$"]],
timing:[
 ["보수 계산 (선도–추종)","$$\\pi_L=\\frac{(a-c)^2}{8b},\\qquad \\pi_F=\\frac{(a-c)^2}{16b}$$"],
 ["보수 계산 (둘 다 추종 / 둘 다 선도)","$$\\pi^{FF}=\\frac{(a-c)^2}{9b},\\qquad \\pi^{LL}=0$$"],
 ["최적 반응","<p>상대가 선도이면 추종($\\tfrac1{16}>0$)이, 상대가 추종이면 선도($\\tfrac18>\\tfrac19$)가 최선이다.</p>"],
 ["순수전략 내시균형","$$(\\text{선도},\\text{추종}):\\ \\bigl(\\tfrac18,\\tfrac1{16}\\bigr),\\qquad (\\text{추종},\\text{선도}):\\ \\bigl(\\tfrac1{16},\\tfrac18\\bigr)$$<p>어느 쪽이 선도자가 될지는 게임만으로 정해지지 않는다(조정 문제).</p>"],
 ["혼합전략 균형","<p>상대가 선도할 확률을 $q$라 하면 기업 1이 무차별할 조건은</p>$$(1-q)\\tfrac18=q\\tfrac1{16}+(1-q)\\tfrac19\\;\\Rightarrow\\;q^*=\\tfrac{2}{11}$$<p>대칭이므로 기업 2도 같고, 기대보수는 $\\tfrac{9}{88}(a-c)^2/b$이다.</p>"]],
cournot:[
 ["이윤함수 전개","$$\\pi_1=[a-b(q_1+q_2)-c]\\,q_1=(a-c)\\,q_1-b\\,q_1^2-b\\,q_1q_2$$"],
 ["1계 조건 ($q_2$ 고정)","$$\\frac{\\partial\\pi_1}{\\partial q_1}=(a-c)-2b\\,q_1-b\\,q_2=0$$"],
 ["반응함수","$$q_1^*(q_2)=\\frac{a-c}{2b}-\\frac12\\,q_2,\\qquad q_2^*(q_1)=\\frac{a-c}{2b}-\\frac12\\,q_1$$<p>상대 생산량이 늘면 내 최적 생산량은 줄어든다(전략적 대체재).</p>"],
 ["두 반응함수를 연립","$$q_1=\\frac{a-c}{2b}-\\frac{q_2}{2},\\qquad q_2=\\frac{a-c}{2b}-\\frac{q_1}{2}$$"],
 ["대입하여 정리","$$q_1=\\frac{a-c}{2b}-\\frac12\\left(\\frac{a-c}{2b}-\\frac{q_1}{2}\\right)=\\frac{a-c}{4b}+\\frac{q_1}{4}\\;\\Rightarrow\\;\\frac34\\,q_1=\\frac{a-c}{4b}$$"],
 ["균형 확정","$$q_1^*=q_2^*=\\frac{a-c}{3b},\\quad Q^*=\\frac{2(a-c)}{3b},\\quad P^*=\\frac{a+2c}{3},\\quad \\pi^*=\\frac{(a-c)^2}{9b}$$"],
 ["담합: 합동이윤 극대화","$$\\max\\;\\Pi=[a-bQ-c]\\,Q\\;\\Rightarrow\\;Q^m=\\frac{a-c}{2b},\\quad q_i^m=\\frac{a-c}{4b},\\quad \\pi_i^m=\\frac{(a-c)^2}{8b}>\\frac{(a-c)^2}{9b}$$"],
 ["담합이 무너지는 이유","<p>담합 1계 조건 $\\partial\\pi_1/\\partial q_1=-\\partial\\pi_2/\\partial q_1$ 이고 $\\partial\\pi_2/\\partial q_1=-b\\,q_2<0$ 이므로</p>$$\\left.\\frac{\\partial\\pi_1}{\\partial q_1}\\right|_{q^m}=b\\,q_2^m>0$$<p>기업 1은 약속을 어기고 생산량을 늘릴 유인이 있다. 기업 2도 마찬가지이므로 담합은 균형이 아니다.</p>"],
 ["등이윤곡선: 기업 1","<p>이윤이 $k_1$로 같은 점의 집합이다.</p>$$\\pi_1=(a-c-bq_1-bq_2)\\,q_1=k_1\\;\\Rightarrow\\;q_2=\\frac{a-c}{b}-q_1-\\frac{k_1}{b\\,q_1}$$"],
 ["등이윤곡선: 기업 2","$$\\pi_2=(a-c-bq_1-bq_2)\\,q_2=k_2\\;\\Rightarrow\\;q_1=\\frac{a-c}{b}-q_2-\\frac{k_2}{b\\,q_2}$$"],
 ["꼭짓점은 반응곡선 위","$$\\frac{\\partial\\pi_1}{\\partial q_1}=0\\;\\Leftrightarrow\\;q_1=R_1(q_2),\\qquad \\frac{\\partial\\pi_2}{\\partial q_2}=0\\;\\Leftrightarrow\\;q_2=R_2(q_1)$$<p>기업 1의 곡선은 $R_1$ 위에서 수평 접선, 기업 2의 곡선은 $R_2$ 위에서 수직 접선을 갖는다. 쿠르노 점 $C$는 두 반응곡선의 교점이므로 두 곡선이 직각으로 만난다.</p>"],
 ["렌즈 영역","<p>$C$를 지나는 두 등이윤곡선 사이의 영역은 $\\pi_1>\\pi_1^C$이고 $\\pi_2>\\pi_2^C$인 점의 집합이다.</p>$$\\pi_i^M=\\frac{(a-c)^2}{8b}>\\pi_i^C=\\frac{(a-c)^2}{9b}$$<p>담합점 $M$은 렌즈 안에 있어 두 기업 모두 이득이지만, 반응곡선 위의 점이 아니므로 균형이 될 수 없다.</p>"]],
bertrand:[
 ["설정","<p>동질재, 두 기업이 가격을 동시에 설정하고 소비자는 더 낮은 가격의 기업에서만 산다.</p>"],
 ["높은 가격은 이탈 유인","$$p_1>p_2>c\\;\\Rightarrow\\;\\text{기업 1은 시장을 모두 잃음}\\;\\Rightarrow\\;p_1=p_2-\\varepsilon$$"],
 ["상대도 응수","$$p_2=p_1-\\varepsilon\\;\\to\\;\\text{가격 인하 경쟁이 반복}$$"],
 ["균형","$$p_1^*=p_2^*=c\\;\\Rightarrow\\;\\pi_1^*=\\pi_2^*=0$$<p>단 두 기업만 있어도 가격이 한계비용까지 내려간다(베르트랑 역설).</p>"],
 ["역설이 현실에 없는 이유","<p>(1) 생산용량 제약 (2) 제품 차별화 (3) 반복게임 (4) 규모의 비경제</p>"]],
stackelberg:[
 ["추종자의 최적화","$$\\max_{q_2}\\;\\pi_2=[a-b(q_1+q_2)-c]\\,q_2\\;\\Rightarrow\\;\\frac{\\partial\\pi_2}{\\partial q_2}=a-bq_1-2bq_2-c=0$$"],
 ["추종자의 반응함수","$$q_2^*(q_1)=\\frac{a-c}{2b}-\\frac{q_1}{2}$$<p>쿠르노와 같은 식이지만 추종자는 $q_1$을 확정된 값으로 관찰한다.</p>"],
 ["선도자: 반응을 이윤에 대입","$$\\pi_1=\\left[a-bq_1-b\\left(\\frac{a-c}{2b}-\\frac{q_1}{2}\\right)-c\\right]q_1=\\frac{(a-c)\\,q_1}{2}-\\frac{b\\,q_1^2}{2}$$"],
 ["선도자의 1계 조건","$$\\frac{d\\pi_1}{dq_1}=\\frac{a-c}{2}-b\\,q_1=0\\;\\Rightarrow\\;q_1^S=\\frac{a-c}{2b}$$"],
 ["균형 완성","$$q_2^S=\\frac{a-c}{4b},\\quad Q^S=\\frac{3(a-c)}{4b},\\quad P^S=\\frac{a+3c}{4}$$$$\\pi_1^S=\\frac{(a-c)^2}{8b},\\quad \\pi_2^S=\\frac{(a-c)^2}{16b}$$"],
 ["비용이 다른 경우","$$q_1^S=\\frac{a-2c_1+c_2}{2b},\\qquad q_2^S=\\frac{a+2c_1-3c_2}{4b}$$<p>$c_1=c_2$이면 위 대칭 결과로 돌아간다.</p>"],
 ["등이윤곡선의 정의","<p>기업 1의 이윤이 같은 값 $k$인 $(q_1,q_2)$의 집합이다.</p>$$\\pi_1(q_1,q_2)=(a-c_1-bq_1-bq_2)\\,q_1=k$$"],
 ["$q_2$에 대해 풀기","$$a-c_1-bq_1-bq_2=\\frac{k}{q_1}\\;\\Rightarrow\\;q_2=\\frac{a-c_1}{b}-q_1-\\frac{k}{b\\,q_1}$$<p>$k$가 클수록 곡선이 아래로 내려간다.</p>"],
 ["기울기","$$\\frac{dq_2}{dq_1}=-\\frac{\\partial\\pi_1/\\partial q_1}{\\partial\\pi_1/\\partial q_2}=\\frac{a-c_1-2bq_1-bq_2}{b\\,q_1}$$"],
 ["꼭짓점은 반응함수 위","<p>기울기가 0인 점에서는 $\\partial\\pi_1/\\partial q_1=0$이다. 이는 기업 1의 1계 조건과 같으므로</p>$$a-c_1-2bq_1-bq_2=0\\;\\Longleftrightarrow\\;q_1=R_1(q_2)$$<p>모든 등이윤곡선의 꼭짓점이 $R_1$ 위에 놓인다(쿠르노 균형은 이 위의 한 점).</p>"],
 ["이윤의 방향","$$\\frac{\\partial\\pi_1}{\\partial q_2}=-b\\,q_1<0$$<p>$q_2$가 작을수록 기업 1의 이윤이 크므로 아래쪽 곡선일수록 이윤이 높다.</p>"],
 ["선도자의 선택: 접점 조건","<p>추종자는 $R_2$ 위에서만 반응하므로, 선도자는 $R_2$와 접하는 가장 낮은 등이윤곡선을 고른다. 곡선의 기울기 = $R_2$의 기울기 $-\\tfrac12$:</p>$$\\frac{a-c-2bq_1-bq_2}{b\\,q_1}=-\\frac12,\\qquad q_2=\\frac{a-c}{2b}-\\frac{q_1}{2}$$"],
 ["접점 풀이","$$\\frac{a-c}{2}-\\frac32\\,b\\,q_1=-\\frac12\\,b\\,q_1\\;\\Rightarrow\\;q_1^S=\\frac{a-c}{2b}$$<p>앞의 역진귀납법 결과와 일치한다. 이 점의 등이윤곡선은 쿠르노 점을 지나는 곡선보다 아래에 있어 선도자가 더 높은 이윤을 얻는다.</p>"]],
differentiated:[
 ["역수요","$$P_1=\\alpha-\\beta q_1-\\gamma q_2,\\qquad P_2=\\alpha-\\beta q_2-\\gamma q_1\\qquad(\\beta>\\gamma>0)$$"],
 ["수요함수 (역함수)","$$q_1=\\underbrace{\\frac{\\alpha}{\\beta+\\gamma}}_{a}-\\underbrace{\\frac{\\beta}{\\beta^2-\\gamma^2}}_{b}\\,p_1+\\underbrace{\\frac{\\gamma}{\\beta^2-\\gamma^2}}_{d}\\,p_2$$"],
 ["베르트랑: 1계 조건","$$\\pi_1=(p_1-c)(a-bp_1+dp_2)\\;\\Rightarrow\\;\\frac{\\partial\\pi_1}{\\partial p_1}=a-2bp_1+dp_2+bc=0$$"],
 ["반응함수","$$p_1^*(p_2)=\\frac{a+bc}{2b}+\\frac{d}{2b}\\,p_2$$<p>$d>0$이므로 우상향 — 가격은 전략적 보완재.</p>"],
 ["대칭 균형","$$p_1\\!\\left(1-\\frac{d^2}{4b^2}\\right)=\\frac{(a+bc)(2b+d)}{4b^2}\\;\\Rightarrow\\;p^*=\\frac{a+bc}{2b-d}$$"],
 ["쿠르노 균형 (같은 수요)","$$q^*=\\frac{\\alpha-c}{2\\beta+\\gamma}$$<p>같은 수요에서 베르트랑 가격이 쿠르노 가격보다 낮다.</p>"],
 ["순차 가격: 후발자의 반응","<p>$m_i=p_i-c$, $A=a-(b-d)c$로 두면 $D_2=A-bm_2+dm_1$.</p>$$\\frac{\\partial\\pi_2}{\\partial m_2}=D_2-b\\,m_2=0\\;\\Rightarrow\\;m_2(m_1)=\\frac{A+d\\,m_1}{2b}$$"],
 ["순차 가격: 선도자","<p>선도자는 $m_2(m_1)$을 대입한 $\\pi_1=m_1\\,[A-bm_1+d\\,m_2(m_1)]$을 극대화한다. 가격은 보완재라 선도자가 높은 가격을 정하면 후발자도 높게 응수하므로 후발자가 더 높은 이윤을 얻는다.</p>"]],
entry:[
 ["$n$기업 쿠르노 1계 조건","$$a-2bq_i-bQ_{-i}-c=0,\\qquad Q_{-i}=(n-1)q$$"],
 ["대칭 균형","$$(n+1)\\,b\\,q=a-c\\;\\Rightarrow\\;q(n)=\\frac{a-c}{b(n+1)}$$$$P(n)=\\frac{a+nc}{n+1},\\qquad \\pi(n)=\\frac1b\\left(\\frac{a-c}{n+1}\\right)^2$$"],
 ["자유진입 균형","$$\\pi(n^e)-e=0\\;\\Longleftrightarrow\\;(n^e+1)^2=\\frac{(a-c)^2}{b\\,e}$$"],
 ["사회후생","$$Q(n)=\\frac{n(a-c)}{b(n+1)},\\quad CS=\\frac b2Q^2$$$$W(n)=\\frac{(a-c)^2}{2b}\\left[1-\\frac{1}{(n+1)^2}\\right]-n\\,e$$"],
 ["사회적 최적","$$W'(n^*)=\\frac{(a-c)^2}{b}\\frac{1}{(n^*+1)^3}-e=0\\;\\Longleftrightarrow\\;(n^*+1)^3=\\frac{(a-c)^2}{b\\,e}$$<p>$(n^e+1)^2=(n^*+1)^3$ 이므로 $n^e>n^*$ — 자유진입은 사회적 최적보다 기업이 많다(사업 빼앗기 효과).</p>"]],
conduct:[
 ["행태 모수를 넣은 한계수입","$$MR(\\lambda)=P+\\lambda\\,P'(Q)\\,Q$$<p>$\\lambda=0$ 완전경쟁, $\\lambda=1$ 독점, $\\lambda=1/n$ $n$기업 쿠르노.</p>"],
 ["균형 조건","$$P+\\lambda P'(Q)Q=c\\;\\Rightarrow\\;P-c=-\\lambda P'(Q)\\,Q$$"],
 ["러너지수","$$L=\\frac{P-c}{P}=-\\lambda\\frac{\\partial P}{\\partial Q}\\frac QP=\\frac{\\lambda}{\\eta}$$"],
 ["식별 문제","<p>선형 수요·비용을 대입하면 $p=\\beta_0+(\\beta_1+\\lambda\\alpha_1)\\,q+\\beta_2 w$. 수요가 평행이동만 하면 기울기 $\\beta_1+\\lambda\\alpha_1$만 추정되어 $\\beta_1$과 $\\lambda$를 구별할 수 없다.</p>"]],
compare:[
 ["완전경쟁","$$Q=\\frac{a-c}{b},\\quad P=c,\\quad \\Pi=0$$"],
 ["스타켈베르크","$$Q=\\frac{3(a-c)}{4b},\\quad P=\\frac{a+3c}{4},\\quad \\Pi=\\frac{3(a-c)^2}{16b}$$"],
 ["쿠르노","$$Q=\\frac{2(a-c)}{3b},\\quad P=\\frac{a+2c}{3},\\quad \\Pi=\\frac{2(a-c)^2}{9b}$$"],
 ["독점","$$Q=\\frac{a-c}{2b},\\quad P=\\frac{a+c}{2},\\quad \\Pi=\\frac{(a-c)^2}{4b}$$"]]
};
let shown = 0;
function renderSteps() {
  const st = STEPS[cur.id] || [];
  $("steps").innerHTML = st.slice(0, shown).map(([t, h], i) =>
    `<li><h3>Step ${i + 1}. ${t}</h3><div>${h}</div></li>`).join("");
  typeset($("steps"));
  $("next").disabled = shown >= st.length;
  $("next").textContent = shown >= st.length ? "마지막 단계예요" : (shown ? "다음 단계 보기" : "풀이 시작");
  $("stepcount").textContent = `${shown} / ${st.length}`;
}

const $ = id => document.getElementById(id);
const DELIMS = [{left:"$$",right:"$$",display:true},{left:"$",right:"$",display:false}];
function typeset(...els) {
  if (window.renderMathInElement) els.forEach(e => renderMathInElement(e, {delimiters: DELIMS, throwOnError:false}));
}
let py, cur, vals = {}, timer, src = "";

function selectModel(m) {
  cur = m;
  document.querySelectorAll("#tabs button").forEach(b => b.setAttribute("aria-selected", b.dataset.id === m.id));
  $("title").textContent = m.title;
  $("theory").innerHTML = m.theory;
  const f = $("controls"); f.innerHTML = "";
  vals = {};
  m.params.forEach(([k, label, min, max, step, def]) => {
    vals[k] = def;
    const d = document.createElement("div"); d.className = "ctl";
    d.innerHTML = `<label for="p_${k}"><span>${label}</span><output id="o_${k}">${def}</output></label>
      <input id="p_${k}" type="range" min="${min}" max="${max}" step="${step}" value="${def}">`;
    d.querySelector("input").addEventListener("input", e => {
      vals[k] = parseFloat(e.target.value); $("o_" + k).textContent = vals[k];
      clearTimeout(timer); timer = setTimeout(run, 120);
    });
    f.appendChild(d);
  });
  typeset($("theory"), $("controls"));
  const cut = fn => { const a = src.search(new RegExp(`^def ${fn}\\(`, "m")); const e = src.slice(a + 1).search(/^(def |# -{5,})/m); return src.slice(a, e < 0 ? undefined : a + 1 + e).trim(); };
  $("code").textContent = cut(m.fn) + (m.extra ? "\n\n\n" + cut(m.extra) : "");
  shown = 0; renderSteps();
  run();
}

async function run() {
  document.body.classList.add("busy");
  py.globals.set("_args", py.toPy(vals));
  const out = JSON.parse(await py.runPythonAsync(`import models\nmodels.${cur.fn}(**_args)`));
  if (cur.extra) out.img2 = JSON.parse(await py.runPythonAsync(`models.${cur.extra}(**_args)`)).img;
  $("plot").src = "data:image/png;base64," + out.img;
  $("note").textContent = out.note;
  $("plot2wrap").hidden = !out.img2; if (out.img2) $("plot2").src = "data:image/png;base64," + out.img2;
  $("rows").innerHTML = out.rows.map(([k, v]) => `<tr><td>${k}</td><td>${v}</td></tr>`).join("");
  typeset($("note"), $("rows"));
  document.body.classList.remove("busy");
}

async function main() {
  MODELS.forEach(m => {
    const b = document.createElement("button");
    b.textContent = m.name; b.dataset.id = m.id; b.setAttribute("role", "tab");
    b.onclick = () => py && selectModel(m);
    $("tabs").appendChild(b);
  });
  py = await loadPyodide();
  await py.loadPackage(["numpy", "matplotlib"]);
  src = await (await fetch("py/models.py")).text();
  py.FS.writeFile("models.py", src);
  $("loading").hidden = true; $("panel").hidden = false;
  selectModel(MODELS[0]);
}
main().catch(e => { $("loading").textContent = "불러오지 못했어요. 새로고침해 주세요. (" + e.message + ")"; });
$("reset").onclick = () => cur && selectModel(cur);
$("next").onclick = () => { shown++; renderSteps(); $("steps").lastElementChild?.scrollIntoView({block:"nearest", behavior:"smooth"}); };
$("all").onclick = () => { shown = (STEPS[cur.id] || []).length; renderSteps(); };
$("fold").onclick = () => { shown = 0; renderSteps(); };
