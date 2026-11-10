const MODELS = [
  { id:"cournot", fn:"cournot", name:"쿠르노", title:"쿠르노 모형: 수량 경쟁과 담합의 붕괴",
    theory:`<p>역수요 <code>P = a − b(q₁+q₂)</code>, 한계비용 <code>c₁, c₂</code>.</p>
      <p>반응함수 <code>q₁ = (a−c₁)/2b − q₂/2</code> — 상대 수량이 늘면 내 수량은 줄어요(전략적 대체재).</p>
      <p>대칭 균형 <code>q* = (a−c)/3b</code>, <code>P* = (a+2c)/3</code>.</p>
      <p>회색 선은 두 기업이 번갈아 최적 반응을 하며 균형에 수렴하는 경로예요.</p>`,
    params:[["a","수요 절편 a",50,200,1,100],["b","수요 기울기 b",.5,3,.1,1],["c1","기업 1 한계비용 c₁",0,60,1,10],["c2","기업 2 한계비용 c₂",0,60,1,10],["start1","시작점 q₁",0,100,1,5],["start2","시작점 q₂",0,100,1,60],["rounds","조정 횟수",1,20,1,8]] },
  { id:"bertrand", fn:"bertrand", name:"베르트랑", title:"베르트랑 모형: 가격 경쟁과 역설",
    theory:`<p>동질재, 가격을 동시에 선택. 더 싼 기업이 시장 전체를 가져가요.</p>
      <p><code>p₁ = p₂ − ε</code> 로 서로 낮추다 보면 <code>p* = c</code>, 이윤 0 — 베르트랑 역설.</p>
      <p>비용이 다르면 저비용 기업이 상대 비용 바로 밑 가격으로 시장을 차지해요.</p>`,
    params:[["a","수요 절편 a",50,200,1,100],["b","수요 기울기 b",.5,3,.1,1],["c1","기업 1 한계비용 c₁",0,60,1,10],["c2","기업 2 한계비용 c₂",0,60,1,10],["p1_0","시작 가격 p₁",0,150,1,80],["p2_0","시작 가격 p₂",0,150,1,75],["eps","인하 폭 ε",.5,10,.5,2],["rounds","라운드 수",2,150,2,80]] },
  { id:"stackelberg", fn:"stackelberg", name:"스타켈베르크", title:"스타켈베르크 모형: 선도자 이점",
    theory:`<p>기업 1이 먼저 수량을 정하고, 기업 2가 관찰한 뒤 정해요. 역진귀납법으로 풀어요.</p>
      <p>추종자 <code>q₂ = (a−c)/2b − q₁/2</code>, 선도자 <code>q₁ˢ = (a−c)/2b</code>.</p>
      <p>파란 등이윤곡선이 추종자 반응함수와 접하는 점이 균형이에요.</p>`,
    params:[["a","수요 절편 a",50,200,1,100],["b","수요 기울기 b",.5,3,.1,1],["c1","선도자 한계비용 c₁",0,60,1,10],["c2","추종자 한계비용 c₂",0,60,1,10]] },
  { id:"differentiated", fn:"differentiated", name:"제품 차별화", title:"제품 차별화: 가격 경쟁 vs 수량 경쟁",
    theory:`<p>한계효용 <code>α − βqᵢ − γqⱼ</code>. γ가 클수록 두 재화가 가까운 대체재(γ→β면 동질재).</p>
      <p>같은 수요에서 베르트랑 가격은 쿠르노보다 낮아요. 가격은 전략적 보완재라 반응함수가 우상향이에요.</p>
      <p>별 표시는 기업 1이 먼저 가격을 정하는 순차 경쟁의 결과(후발자 이점).</p>`,
    params:[["alpha","최대 지불의사 α",50,200,1,100],["beta","자기효과 β",.5,3,.1,1],["gamma","교차효과 γ",0,2.9,.05,.6],["c","한계비용 c",0,60,1,10]] },
  { id:"entry", fn:"entry", name:"진입", title:"자유진입과 시장구조",
    theory:`<p>n기업 쿠르노: <code>q(n) = (a−c)/b(n+1)</code>, <code>π(n) = (a−c)²/b(n+1)²</code>.</p>
      <p>자유진입 균형: <code>π(nᵉ) ≥ e</code> 이고 <code>π(nᵉ+1) &lt; e</code>.</p>
      <p>사회후생(소비자잉여+이윤−진입비용)을 극대화하는 기업 수와 비교해 보세요.</p>`,
    params:[["a","수요 절편 a",50,200,1,100],["b","수요 기울기 b",.5,3,.1,1],["c","한계비용 c",0,60,1,10],["e","진입비용 e",1,400,1,40],["nmax","그래프 범위 n",5,40,1,15]] },
  { id:"conduct", fn:"conduct", name:"시장지배력", title:"행태 모수 λ와 러너지수",
    theory:`<p>균형 조건 <code>P + λP′(Q)Q = c</code>.</p>
      <p>λ=0 완전경쟁, λ=1 독점, λ=1/n 대칭 n기업 쿠르노.</p>
      <p>러너지수 <code>L = (P−c)/P = λ/η</code> (η: 수요의 가격탄력성).</p>`,
    params:[["a","수요 절편 a",50,200,1,100],["b","수요 기울기 b",.5,3,.1,1],["c","한계비용 c",0,60,1,20],["lam","행태 모수 λ",0,1,.01,.5]] },
  { id:"compare", fn:"compare", name:"모형 비교", title:"네 가지 모형 비교",
    theory:`<p>동질재·대칭 비용에서 시장 산출량 순서:</p><p><code>완전경쟁 &gt; 스타켈베르크 &gt; 쿠르노 &gt; 독점</code></p>
      <p>가격과 이윤은 대체로 반대 방향, 사회후생은 산출량과 같은 방향이에요.</p>`,
    params:[["a","수요 절편 a",50,200,1,100],["b","수요 기울기 b",.5,3,.1,1],["c","한계비용 c",0,60,1,10]] },
];

const $ = id => document.getElementById(id);
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
    d.innerHTML = `<label for="p_${k}">${label}<output id="o_${k}">${def}</output></label>
      <input id="p_${k}" type="range" min="${min}" max="${max}" step="${step}" value="${def}">`;
    d.querySelector("input").addEventListener("input", e => {
      vals[k] = parseFloat(e.target.value); $("o_" + k).textContent = vals[k];
      clearTimeout(timer); timer = setTimeout(run, 120);
    });
    f.appendChild(d);
  });
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
