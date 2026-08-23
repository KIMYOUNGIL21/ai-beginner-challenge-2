/* CDN이 막혀도 교재의 글·표·이미지·다운로드 링크를 읽을 수 있게 하는 경량 Markdown 변환기 */
(function () {
  const escapeHtml = value => String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");

  const safeUrl = value => /^(?:javascript|vbscript|data):/i.test(value.trim()) ? "#" : value;

  const inline = value => escapeHtml(value)
    .replace(/!\[([^\]]*)\]\(([^\s)]+)(?:\s+&quot;[^&]*&quot;)?\)/g,
      (_, alt, url) => `<img src="${safeUrl(url)}" alt="${alt}" loading="lazy">`)
    .replace(/\[([^\]]+)\]\(([^\s)]+)(?:\s+&quot;[^&]*&quot;)?\)/g,
      (_, label, url) => `<a href="${safeUrl(url)}">${label}</a>`)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>");

  const splitTableRow = line => {
    const trimmed = line.trim().replace(/^\|/, "").replace(/\|$/, "");
    return trimmed.split("|").map(cell => cell.trim());
  };

  const isTableDivider = line => {
    const cells = splitTableRow(line);
    return cells.length > 1 && cells.every(cell => /^:?-{3,}:?$/.test(cell));
  };

  const listItem = value => {
    const task = value.match(/^\[([ xX])\]\s+(.+)$/);
    if (!task) return `<li>${inline(value)}</li>`;
    const checked = task[1].toLowerCase() === "x" ? " checked" : "";
    return `<li class="task-item"><input type="checkbox" disabled${checked}> ${inline(task[2])}</li>`;
  };

  window.markdownFallback = function (markdown) {
    const lines = String(markdown).replace(/\r/g, "").split("\n");
    const output = [];
    let paragraph = [];
    let list = null;
    let quote = [];
    let code = null;

    const flushParagraph = () => {
      if (paragraph.length) output.push(`<p>${inline(paragraph.join(" "))}</p>`);
      paragraph = [];
    };
    const flushList = () => {
      if (list) output.push(`<${list.type}>${list.items.map(listItem).join("")}</${list.type}>`);
      list = null;
    };
    const flushQuote = () => {
      if (quote.length) output.push(`<blockquote><p>${inline(quote.join(" "))}</p></blockquote>`);
      quote = [];
    };
    const flushAll = () => { flushParagraph(); flushList(); flushQuote(); };

    for (let index = 0; index < lines.length; index += 1) {
      const line = lines[index];
      if (code !== null) {
        if (/^```/.test(line)) {
          output.push(`<pre><code>${escapeHtml(code.replace(/\n$/, ""))}</code></pre>`);
          code = null;
        } else code += `${line}\n`;
        continue;
      }
      if (/^```/.test(line)) { flushAll(); code = ""; continue; }
      if (!line.trim()) { flushAll(); continue; }

      if (line.includes("|") && isTableDivider(lines[index + 1] || "")) {
        flushAll();
        const headings = splitTableRow(line);
        const alignments = splitTableRow(lines[index + 1]).map(cell => {
          if (cell.startsWith(":") && cell.endsWith(":")) return "center";
          if (cell.endsWith(":")) return "right";
          return "left";
        });
        const rows = [];
        index += 2;
        while (index < lines.length && lines[index].trim() && lines[index].includes("|")) {
          rows.push(splitTableRow(lines[index]));
          index += 1;
        }
        index -= 1;
        const head = headings.map((cell, i) => `<th style="text-align:${alignments[i] || "left"}">${inline(cell)}</th>`).join("");
        const body = rows.map(row => `<tr>${headings.map((_, i) => `<td style="text-align:${alignments[i] || "left"}">${inline(row[i] || "")}</td>`).join("")}</tr>`).join("");
        output.push(`<table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`);
        continue;
      }

      const heading = line.match(/^(#{1,6})\s+(.+)$/);
      if (heading) {
        flushAll();
        const level = heading[1].length;
        output.push(`<h${level}>${inline(heading[2])}</h${level}>`);
        continue;
      }
      if (/^\s*(?:-{3,}|\*{3,}|_{3,})\s*$/.test(line)) { flushAll(); output.push("<hr>"); continue; }

      const item = line.match(/^\s*(?:([-+*])|(\d+)\.)\s+(.+)$/);
      if (item) {
        flushParagraph(); flushQuote();
        const type = item[2] ? "ol" : "ul";
        if (list && list.type !== type) flushList();
        if (!list) list = { type, items: [] };
        list.items.push(item[3]);
        continue;
      }
      const quoted = line.match(/^>\s?(.*)$/);
      if (quoted) { flushParagraph(); flushList(); quote.push(quoted[1]); continue; }
      flushList(); flushQuote(); paragraph.push(line.trim());
    }
    if (code !== null) output.push(`<pre><code>${escapeHtml(code)}</code></pre>`);
    flushAll();
    return output.join("\n");
  };
})();
