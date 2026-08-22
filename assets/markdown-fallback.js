/* CDN이 막혔을 때도 기본 교재를 읽을 수 있게 하는 최소 Markdown 변환기 */
(function () {
  const escapeHtml = value => value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");

  const inline = value => escapeHtml(value)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2">$1</a>')
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>");

  window.markdownFallback = function (markdown) {
    const lines = markdown.replace(/\r/g, "").split("\n");
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
      if (list) output.push(`<${list.type}>${list.items.map(item => `<li>${inline(item)}</li>`).join("")}</${list.type}>`);
      list = null;
    };
    const flushQuote = () => {
      if (quote.length) output.push(`<blockquote><p>${inline(quote.join(" "))}</p></blockquote>`);
      quote = [];
    };
    const flushAll = () => { flushParagraph(); flushList(); flushQuote(); };

    for (const line of lines) {
      if (code !== null) {
        if (/^```/.test(line)) {
          output.push(`<pre><code>${escapeHtml(code.replace(/\n$/, ""))}</code></pre>`);
          code = null;
        } else code += `${line}\n`;
        continue;
      }
      if (/^```/.test(line)) { flushAll(); code = ""; continue; }
      if (!line.trim()) { flushAll(); continue; }
      const heading = line.match(/^(#{1,3})\s+(.+)$/);
      if (heading) { flushAll(); output.push(`<h${heading[1].length}>${inline(heading[2])}</h${heading[1].length}>`); continue; }
      if (/^---+$/.test(line.trim())) { flushAll(); output.push("<hr>"); continue; }
      const item = line.match(/^\s*(?:([-*])|(\d+)\.)\s+(.+)$/);
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
