const COMMON = [["a","수요 절편 $a$",50,200,1,100],["b","수요 기울기 $b$",.5,3,.1,1]];
const MODELS = [
  { id:"cournot", fn:"cournot", name:"쿠르노", title:"쿠르노 모형: 수량 경쟁과 담합의 붕괴",
    theory:`<p>두 기업이 동시에 생산량을 선택한다. 역수요와 이윤은</p>
      $$P=a-b(q_1+q_2),\\qquad \\pi_1=\\bigl[a-b(q_1+q_2)-c_1\\bigr]q_1$$
      <p>1계 조건 $\\partial\\pi_1/\\partial q_1=0$에서 반응함수를 얻는다(전략적 대체재).</p>
      $$q_1^*(q_2)=\\frac{a-c_1}{2b}-\\frac{q_2}{2}$$
      <p>대칭 비용($c_1=c_2=c$)의 쿠르노–내시 균형:</p>
      $$q^*=\\frac{a-c}{3b},\\quad P^*=\\frac{a+2c}{3},\\quad \\pi^*=\\frac{(a-c)^2}{9b}$$
      <p>담합(독점) 생산량과 이윤:</p>
      $$Q^m=\\frac{a-c}{2b},\\quad \\pi_i^m=\\frac{(a-c)^2}{8b}>\\pi^*$$
      <p>담합점에서의 한계이윤 $\\left.\\dfrac{\\partial\\pi_1}{\\partial q_1}\\right|_{q^m}=b\\,q_2^m>0$이므로 이탈 유인이 있다. 회색 선은 번갈아 최적 반응하며 균형에 수렴하는 경로다.</p>`,
    params:[...COMMON,["c1","기업 1 한계비용 $c_1$",0,60,1,10],["c2","기업 2 한계비용 $c_2$",0,60,1,10],["start1","시작점 $q_1$",0,100,1,5],["start2","시작점 $q_2$",0,100,1,60],["rounds","조정 횟수",1,20,1,8]] },
  { id:"bertrand", fn:"bertrand", name:"베르트랑", title:"베르트랑 모형: 가격 경쟁과 역설",
    theory:`<p>동질재, 두 기업이 가격을 동시에 선택한다. 더 싼 기업이 시장 전체를 가져간다.</p>
      $$D_1(p_1,p_2)=\\begin{cases}\\dfrac{a-p_1}{b}, & p_1<p_2\\\\[4pt] \\tfrac12\\,\\dfrac{a-p_1}{b}, & p_1=p_2\\\\[4pt] 0, & p_1>p_2\\end{cases}$$
      <p>$p_1>p_2>c$이면 $p_1=p_2-\\varepsilon$으로 낮출 유인이 있으므로 유일한 균형은</p>
      $$p_1^*=p_2^*=c,\\qquad \\pi_1^*=\\pi_2^*=0$$
      <p>(베르트랑 역설). 비용이 다르면($c_1<c_2$) 기업 1이 상대 비용 바로 아래의 가격으로 시장 전체를 공급한다.</p>`,
    params:[...COMMON,["c1","기업 1 한계비용 $c_1$",0,60,1,10],["c2","기업 2 한계비용 $c_2$",0,60,1,10],["p1_0","시작 가격 $p_1$",0,150,1,80],["p2_0","시작 가격 $p_2$",0,150,1,75],["eps","인하 폭 $\\varepsilon$",.5,10,.5,2],["rounds","라운드 수",2,150,2,80]] },
  { id:"stackelberg", fn:"stackelberg", name:"스타켈베르크", title:"스타켈베르크 모형: 선도자 이점",
    theory:`<p>기업 1(선도자)이 먼저 $q_1$을 정하고 기업 2(추종자)가 관찰 후 선택한다. 역진귀납법:</p>
      <p><b>2단계</b> 추종자의 최적화</p>
      $$\\max_{q_2}\\,[a-b(q_1+q_2)-c_2]\\,q_2\\;\\Rightarrow\\; q_2^*(q_1)=\\frac{a-c_2}{2b}-\\frac{q_1}{2}$$
      <p><b>1단계</b> 선도자는 $q_2^*(q_1)$을 이윤에 대입해 극대화한다.</p>
      $$q_1^S=\\frac{a-2c_1+c_2}{2b}$$
      <p>대칭 비용일 때:</p>
      $$q_1^S=\\frac{a-c}{2b},\\; q_2^S=\\frac{a-c}{4b},\\; P^S=\\frac{a+3c}{4}$$
      $$\\pi_1^S=\\frac{(a-c)^2}{8b},\\quad \\pi_2^S=\\frac{(a-c)^2}{16b}$$
      <p>파란 등이윤곡선이 추종자 반응함수에 접하는 점이 균형이다.</p>`,
    params:[...COMMON,["c1","선도자 한계비용 $c_1$",0,60,1,10],["c2","추종자 한계비용 $c_2$",0,60,1,10]] },
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
    params:[["alpha","최대 지불의사 $\\alpha$",50,200,1,100],["beta","자기효과 $\\beta$",.5,3,.1,1],["gamma","교차효과 $\\gamma$",0,2.9,.05,.6],["c","한계비용 $c$",0,60,1,10]] },
  { id:"entry", fn:"entry", name:"진입", title:"자유진입과 시장구조",
    theory:`<p>$n$개 대칭 기업의 쿠르노 균형:</p>
      $$q(n)=\\frac{a-c}{b(n+1)},\\quad P(n)=\\frac{a+nc}{n+1},\\quad \\pi(n)=\\frac{1}{b}\\left(\\frac{a-c}{n+1}\\right)^2$$
      <p>진입비용 $e$일 때 자유진입 균형 $n^e$는</p>
      $$\\pi(n^e)\\ge e\\quad\\text{이고}\\quad \\pi(n^e+1)<e$$
      <p>사회후생은 소비자잉여 + 이윤 − 진입비용이다.</p>
      $$W(n)=\\frac{b\\,Q^2}{2}+n\\bigl[\\pi(n)-e\\bigr],\\qquad Q=n\\,q(n)$$`,
    params:[...COMMON,["c","한계비용 $c$",0,60,1,10],["e","진입비용 $e$",1,400,1,40],["nmax","그래프 범위 $n$",5,40,1,15]] },
  { id:"conduct", fn:"conduct", name:"시장지배력", title:"행태 모수 λ와 러너지수",
    theory:`<p>행태 모수 $\\lambda$를 둔 한계수입과 균형 조건:</p>
      $$MR(\\lambda)=P+\\lambda\\,P'(Q)\\,Q,\\qquad P+\\lambda P'(Q)\\,Q=c$$
      <p>$\\lambda=0$ 완전경쟁, $\\lambda=1/n$ 대칭 $n$기업 쿠르노, $\\lambda=1$ 독점.</p>
      <p>러너지수는 수요의 가격탄력성 $\\eta=-\\dfrac{\\partial Q}{\\partial P}\\dfrac{P}{Q}$로</p>
      $$L=\\frac{P-c}{P}=\\frac{\\lambda}{\\eta}$$`,
    params:[...COMMON,["c","한계비용 $c$",0,60,1,20],["lam","행태 모수 $\\lambda$",0,1,.01,.5]] },
  { id:"compare", fn:"compare", name:"모형 비교", title:"네 가지 모형 비교",
    theory:`<p>동질재·대칭 비용에서 시장 산출량:</p>
      $$Q^{PC}=\\frac{a-c}{b}>Q^{S}=\\frac{3(a-c)}{4b}>Q^{C}=\\frac{2(a-c)}{3b}>Q^{M}=\\frac{a-c}{2b}$$
      <p>가격은 반대 순서이고, 사회후생 $W=\\dfrac{bQ^2}{2}+(P-c)Q$는 산출량과 같은 방향으로 움직인다.</p>`,
    params:[...COMMON,["c","한계비용 $c$",0,60,1,10]] },
];

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
  const re = new RegExp(`^def ${m.fn}\\(`, "m");
  const i = src.search(re);
  let j = src.slice(i + 1).search(/^(def |# -{5,})/m);
  $("code").textContent = src.slice(i, j < 0 ? undefined : i + 1 + j).trim();
  run();
}

async function run() {
  document.body.classList.add("busy");
  py.globals.set("_args", py.toPy(vals));
  const out = JSON.parse(await py.runPythonAsync(`import models\nmodels.${cur.fn}(**_args)`));
  $("plot").src = "data:image/png;base64," + out.img;
  $("note").textContent = out.note;
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
