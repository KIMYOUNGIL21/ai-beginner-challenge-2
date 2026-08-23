const lessons = [
  { id: "welcome", day: "안내", title: "처음 오신 분께", file: "00_환영합니다.md" },
  { id: "day0", day: "준비", title: "설치부터 첫 폴더까지", file: "Day00_시작전준비.md" },
  { id: "terms", day: "준비", title: "왕초보 용어사전", file: "Day00_왕초보용어사전.md" },
  { id: "rules", day: "공통", title: "매일 인증하는 방법", file: "00_오픈카톡_인증규칙.md" },
  { id: "day1", day: "1일", title: "프롬프트 제조기", file: "Day01_Artifact진단기_실행서.md" },
  { id: "day2", day: "2일", title: "내 콘텐츠 작업방", file: "Day02_Projects_실행서_v2.md" },
  { id: "day3", day: "3일", title: "인스타 카드뉴스", file: "Day03_Design_실행서_v2.md" },
  { id: "day4", day: "4일", title: "Cowork 안내문", file: "Day04_Cowork_실행서_v2.md" },
  { id: "day5", day: "5일", title: "Code 웹 도구", file: "Day05_Code_실행서_v2.md" },
  { id: "day6", day: "6일", title: "스킬 + 커넥터", file: "Day06_Skills_Connectors_실행서_v2.md" },
  { id: "day7", day: "7일", title: "내 첫 AI 쇼츠", file: "Day07_AI쇼츠.md" },
  { id: "references", day: "참고", title: "공식 레퍼런스", file: "01_레퍼런스_목록.md" }
];

const nav = document.querySelector("#lessonNav");
const content = document.querySelector("#content");
const loading = document.querySelector("#loading");
const pager = document.querySelector("#pager");
const sidebar = document.querySelector("#sidebar");
const overlay = document.querySelector("#overlay");
const completed = new Set(JSON.parse(localStorage.getItem("challenge-completed") || "[]"));

function renderNav(activeId) {
  nav.innerHTML = lessons.map(lesson => `
    <a class="nav-link ${lesson.id === activeId ? "active" : ""}" href="#${lesson.id}" ${lesson.id === activeId ? 'aria-current="page"' : ""}>
      <span class="nav-day">${lesson.day}</span>
      <span>${lesson.title}</span>
      <span class="nav-check">${completed.has(lesson.id) ? "✓" : ""}</span>
    </a>`).join("");
}

function enhanceArticle() {
  content.querySelectorAll("table").forEach(table => {
    const wrap = document.createElement("div");
    wrap.className = "table-wrap";
    table.parentNode.insertBefore(wrap, table);
    wrap.appendChild(table);
  });
  content.querySelectorAll("pre").forEach(pre => {
    const button = document.createElement("button");
    button.className = "copy-button";
    button.type = "button";
    button.setAttribute("aria-label", "명령어 복사");
    button.textContent = "복사";
    button.addEventListener("click", async () => {
      const value = pre.querySelector("code")?.innerText || pre.innerText;
      try {
        await navigator.clipboard.writeText(value);
        showToast("복사했습니다");
      } catch {
        showToast("복사하지 못했습니다. 글자를 직접 선택해 주세요.");
      }
    });
    pre.appendChild(button);
  });
  content.querySelectorAll("a").forEach(link => {
    if (link.hostname && link.hostname !== location.hostname) {
      link.target = "_blank";
      link.rel = "noopener noreferrer";
    }
  });
}

async function loadLesson() {
  const id = location.hash.replace("#", "") || "welcome";
  const index = Math.max(0, lessons.findIndex(item => item.id === id));
  const lesson = lessons[index];
  renderNav(lesson.id);
  loading.hidden = false;
  content.hidden = true;
  pager.hidden = true;
  try {
    const response = await fetch(encodeURI(lesson.file));
    if (!response.ok) throw new Error("교재 파일을 찾을 수 없습니다.");
    const markdown = await response.text();
    const parser = window.marked?.parse
      ? value => window.marked.parse(value, { gfm: true, breaks: false })
      : window.markdownFallback;
    if (!parser) throw new Error("교재 변환기를 불러오지 못했습니다.");
    content.innerHTML = parser(markdown);
    enhanceArticle();
    document.title = `${lesson.title} | AI 왕초보 챌린지 2기`;
    document.querySelector("#prevButton").disabled = index === 0;
    document.querySelector("#nextButton").disabled = index === lessons.length - 1;
    document.querySelector("#prevButton").onclick = () => location.hash = lessons[index - 1]?.id;
    document.querySelector("#nextButton").onclick = () => location.hash = lessons[index + 1]?.id;
    const completeButton = document.querySelector("#completeButton");
    completeButton.textContent = completed.has(lesson.id) ? "✓ 확인 완료" : "✓ 여기까지 봤어요";
    completeButton.setAttribute("aria-pressed", String(completed.has(lesson.id)));
    completeButton.onclick = () => {
      completed.add(lesson.id);
      localStorage.setItem("challenge-completed", JSON.stringify([...completed]));
      renderNav(lesson.id);
      completeButton.textContent = "✓ 확인 완료";
      completeButton.setAttribute("aria-pressed", "true");
      showToast("진도를 저장했습니다");
    };
    loading.hidden = true;
    content.hidden = false;
    pager.hidden = false;
    window.scrollTo(0, 0);
    closeMenu();
  } catch (error) {
    loading.textContent = `교재를 열지 못했습니다: ${error.message}`;
    loading.setAttribute("role", "alert");
  }
}

function showToast(message) {
  const toast = document.querySelector("#toast");
  toast.textContent = message;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 1400);
}

function closeMenu() {
  sidebar.classList.remove("open");
  overlay.classList.remove("open");
  document.querySelector("#menuButton").setAttribute("aria-expanded", "false");
}

document.querySelector("#menuButton").addEventListener("click", () => {
  sidebar.classList.toggle("open");
  overlay.classList.toggle("open");
  document.querySelector("#menuButton").setAttribute("aria-expanded", String(sidebar.classList.contains("open")));
});
overlay.addEventListener("click", closeMenu);
document.addEventListener("keydown", event => {
  if (event.key === "Escape") closeMenu();
});
window.addEventListener("hashchange", loadLesson);
loadLesson();
