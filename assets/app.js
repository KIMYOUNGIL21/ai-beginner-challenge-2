const lessons = [
  { track: "guide", id: "welcome", day: "안내", title: "처음 오신 분께", file: "00_환영합니다.md" },
  { track: "guide", id: "day0", day: "준비", title: "설치부터 첫 폴더까지", file: "Day00_시작전준비.md" },
  { track: "guide", id: "terms", day: "준비", title: "왕초보 용어사전", file: "Day00_왕초보용어사전.md" },
  { track: "guide", id: "rules", day: "공통", title: "매일 인증하는 방법", file: "00_오픈카톡_인증규칙.md" },
  { track: "guide", id: "day1", day: "1일", title: "콘텐츠 스튜디오 2종", file: "Day01_Artifact진단기_실행서.md" },
  { track: "guide", id: "day2", day: "2일", title: "LIFE BRAND 운영본부", file: "Day02_Projects_실행서_v2.md" },
  { track: "guide", id: "day3", day: "3일", title: "브랜드 론칭 디자인", file: "Day03_Design_실행서_v2.md" },
  { track: "guide", id: "day4", day: "4일", title: "가족 여행 브리핑북", file: "Day04_Cowork_실행서_v2.md" },
  { track: "guide", id: "day5", day: "5일", title: "오늘의 작전실", file: "Day05_Code_실행서_v2.md" },
  { track: "guide", id: "day6", day: "6일", title: "20~23초 숏츠 주문서", file: "Day06_Skills_Connectors_실행서_v2.md" },
  { track: "guide", id: "day7", day: "7일", title: "20~23초 AI 쇼츠", file: "Day07_AI쇼츠.md" },
  { track: "guide", id: "references", day: "참고", title: "공식 레퍼런스", file: "01_레퍼런스_목록.md" },
  { track: "home", id: "h0", day: "안내", title: "둘째 날 과제란?", file: "home-intro.md" },
  { track: "home", id: "h1", day: "1일", title: "우리 집 식단표", file: "home-day1.md" },
  { track: "home", id: "h2", day: "2일", title: "우리 집 비서 방", file: "home-day2.md" },
  { track: "home", id: "h3", day: "3일", title: "초대 카드 · 주간 계획표", file: "home-day3.md" },
  { track: "home", id: "h4", day: "4일", title: "이번 주 할 일 한눈에", file: "home-day4.md" },
  { track: "home", id: "h5", day: "5일", title: "집안일 체크판", file: "home-day5.md" },
  { track: "5min", id: "m0", day: "안내", title: "폰으로 5분이란?", file: "5min-intro.md" },
  { track: "5min", id: "m1", day: "1일", title: "폰에서도 화면이 됩니다", file: "5min-day1.md" },
  { track: "5min", id: "m2", day: "2일", title: "프로젝트 기억 확인", file: "5min-day2.md" },
  { track: "5min", id: "m3", day: "3일", title: "내 색 3개 · 제목 놀이", file: "5min-day3.md" },
  { track: "5min", id: "m4", day: "4일", title: "냉장고 브리핑", file: "5min-day4.md" },
  { track: "5min", id: "m5", day: "5일", title: "물 마시기 카운터", file: "5min-day5.md" },
  { track: "5min", id: "m6", day: "6일", title: "내 말투 규칙 5줄", file: "5min-day6.md" },
  { track: "5min", id: "m7", day: "7일", title: "다음 쇼츠 대본", file: "5min-day7.md" }
];

const nav = document.querySelector("#lessonNav");
const content = document.querySelector("#content");
const loading = document.querySelector("#loading");
const pager = document.querySelector("#pager");
const sidebar = document.querySelector("#sidebar");
const overlay = document.querySelector("#overlay");

function readCompleted() {
  try {
    const saved = JSON.parse(localStorage.getItem("challenge-completed") || "[]");
    return new Set(Array.isArray(saved) ? saved : []);
  } catch {
    return new Set();
  }
}

const completed = readCompleted();

function renderNav(activeId) {
  const activeTrack = (lessons.find(l => l.id === activeId) || lessons[0]).track;
  document.querySelectorAll(".tab").forEach(tab => {
    const on = tab.dataset.track === activeTrack;
    tab.classList.toggle("active", on);
    tab.setAttribute("aria-selected", String(on));
  });
  nav.innerHTML = lessons.filter(l => l.track === activeTrack).map(lesson => `
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

// CommonMark는 닫는 ** 뒤에 한글 조사가 바로 붙으면 강조로 해석하지
// 않을 수 있다. 코드 블록은 그대로 두고, 본문에서만 강조 표시를 HTML로 바꾼다.
function normalizeKoreanStrong(markdown) {
  let inFence = false;
  return markdown.split("\n").map(line => {
    if (/^\s*```/.test(line)) {
      inFence = !inFence;
      return line;
    }
    if (inFence) return line;
    return line.replace(/(^|[\s([{|>:\-–—])\*\*([^*\n]+)\*\*(?=[가-힣])/g, "$1<strong>$2</strong>");
  }).join("\n");
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
      ? value => window.marked.parse(normalizeKoreanStrong(value), { gfm: true, breaks: false })
      : window.markdownFallback;
    if (!parser) throw new Error("교재 변환기를 불러오지 못했습니다.");
    content.innerHTML = parser(markdown);
    enhanceArticle();
    document.title = `${lesson.title} | AI 왕초보 챌린지 3기`;
    const trackLessons = lessons.filter(l => l.track === lesson.track);
    const trackIndex = trackLessons.findIndex(l => l.id === lesson.id);
    document.querySelector("#prevButton").disabled = trackIndex === 0;
    document.querySelector("#nextButton").disabled = trackIndex === trackLessons.length - 1;
    document.querySelector("#prevButton").onclick = () => location.hash = trackLessons[trackIndex - 1]?.id;
    document.querySelector("#nextButton").onclick = () => location.hash = trackLessons[trackIndex + 1]?.id;
    const hero = document.querySelector(".hero-block");
    if (lesson.track === "5min") {
      hero.querySelector(".hero-eyebrow").textContent = "그밤PD · 5-MIN PLAY";
      hero.querySelector(".hero-title").textContent = "이불 속에서 5분, 폰으로 노는 시간";
    } else if (lesson.track === "home") {
      hero.querySelector(".hero-eyebrow").textContent = "그밤PD · DAY 2 OF 2";
      hero.querySelector(".hero-title").textContent = "배운 걸 오늘 내 것으로";
    } else {
      hero.querySelector(".hero-eyebrow").textContent = "그밤PD · 14 DAYS JOURNEY";
      hero.querySelector(".hero-title").textContent = "하루 한 걸음, 나도 만드는 사람";
    }
    const completeButton = document.querySelector("#completeButton");
    completeButton.textContent = completed.has(lesson.id) ? "✓ 확인 완료" : "✓ 여기까지 봤어요";
    completeButton.setAttribute("aria-pressed", String(completed.has(lesson.id)));
    completeButton.onclick = () => {
      completed.add(lesson.id);
      try {
        localStorage.setItem("challenge-completed", JSON.stringify([...completed]));
      } catch {
        // 저장을 막은 브라우저에서도 현재 화면의 진도 표시는 유지한다.
      }
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
