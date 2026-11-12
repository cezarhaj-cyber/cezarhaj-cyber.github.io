# -*- coding: utf-8 -*-
"""Builds index.html (bilingual EN/RO) from cv_data.py."""
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cv_data import *  # noqa: E402,F403

esc = html.escape


def bi(ro, en, tag="span", cls="", raw=False):
    f = (lambda s: s) if raw else esc
    c = f' {cls}' if cls else ""
    return (f'<{tag} class="l-en{c}" lang="en">{f(en)}</{tag}>'
            f'<{tag} class="l-ro{c}" lang="ro">{f(ro)}</{tag}>')


def link(url, text=None):
    t = esc(text or url.replace("https://", "").replace("http://", "").rstrip("/"))
    return f'<a href="{esc(url)}" target="_blank" rel="noopener">{t}</a>'


def h2(ro, en, id_):
    return f'<h2 id="{id_}">{bi(ro, en)}</h2>'


def tags(g_ro, g_en):
    def chips(s):
        return "".join(f'<li>{esc(t.strip())}</li>' for t in s.split(","))
    return (f'<ul class="tags l-en" lang="en">{chips(g_en)}</ul>'
            f'<ul class="tags l-ro" lang="ro">{chips(g_ro)}</ul>')


def experience():
    out, last_year = [], None
    for e in sorted(EXPERIENCE, key=lambda e: e["start"], reverse=True):
        d_ro, d_en = e["dates"]
        current = "Prezent" in d_ro
        o_ro, o_en = e["org"]
        org = bi(o_ro, o_en)
        if e["url"]:
            from urllib.parse import urlparse
            org += f' · {link(e["url"], urlparse(e["url"]).netloc.replace("www.", ""))}'
        outputs = ""
        if e["out"]:
            items = "".join(f"<li>{o}</li>" for o in e["out"])
            outputs = (f'<div class="outputs"><span class="lbl">{bi("Rezultate-cheie", "Key outputs")}</span>'
                       f'<ul>{items}</ul></div>')
        badge = f'<span class="badge">{bi("în curs", "current")}</span>' if current else ""
        out.append(f'''
<article class="job{' is-current' if current else ''}">
  <div class="when">{bi(d_ro, d_en)}{badge}</div>
  <div class="what">
    <h3>{bi(*e["title"])}</h3>
    <p class="org">{org}</p>
    {bi(*e["desc"], tag="p", cls="desc")}
    {outputs}
    {tags(*e["tags"])}
  </div>
</article>''')
    return "\n".join(out)


def education():
    rows = []
    for d, t_ro, t_en, x_ro, x_en, o_ro, o_en, l_ro, l_en in EDUCATION:
        lvl = f' · {bi(l_ro, l_en)}' if l_en else ""
        rows.append(f'''
<article class="job">
  <div class="when">{esc(d)}</div>
  <div class="what">
    <h3>{bi(t_ro, t_en)}</h3>
    <p class="org">{bi(o_ro, o_en)}{lvl}</p>
    {bi(x_ro, x_en, tag="p", cls="desc")}
  </div>
</article>''')
    rows.append(f'<p class="certs"><strong>{bi("Alte certificări", "Other certifications")}:</strong> {bi(*CERTS)}</p>')
    return "\n".join(rows)


def roles():
    items = "".join(f'<li><span class="yr">{bi(r, e)}</span><span>{bi(t_ro, t_en)}</span></li>'
                    for r, e, t_ro, t_en in ROLES)
    return f'<ul class="roles">{items}</ul>'


def skills():
    head = ("<tr><th></th>"
            + "".join(f"<th>{bi(r, e)}</th>" for r, e in [("Ascultare", "Listening"), ("Citire", "Reading"),
                                                          ("Interacțiune", "Interaction"), ("Discurs", "Production"),
                                                          ("Scriere", "Writing")])
            + "</tr>")
    body = "".join(f"<tr><th>{bi(r, e)}</th>" + "".join(f"<td>{lv}</td>" for lv in levels) + "</tr>"
                   for r, e, levels in LANGS)
    langs = f'''
<div class="langs">
  <p><strong>{bi("Limba maternă", "Mother tongue")}:</strong> {bi("română", "Romanian")}</p>
  <div class="tablewrap"><table><thead>{head}</thead><tbody>{body}</tbody></table></div>
  <p class="note">{bi("Autoevaluare conform Cadrului european comun de referință pentru limbi (CECRL).", "Self-assessment on the Common European Framework of Reference for Languages (CEFR).")}</p>
</div>'''
    blocks = "".join(f'<div class="skill"><h3>{bi(r, e)}</h3>{bi(x_ro, x_en, tag="p")}</div>'
                     for r, e, x_ro, x_en in SKILLS)
    return langs + f'<div class="skills">{blocks}</div>'


def pubs(items):
    lis = []
    for cit, urls in items:
        links = " ".join(link(u, "link ↗") for u in urls)
        lis.append(f"<li>{cit} {links}</li>")
    return "<ol class=\"pubs\">" + "".join(lis) + "</ol>"


STATS = [
    ("15+", "ani de experiență în politici publice", "years in public policy"),
    ("50,000+", "cetățeni formați în competențe digitale", "citizens trained in digital skills"),
    ("47", "sisteme de învățământ superior monitorizate (SEÎS)", "higher education systems monitored (EHEA)"),
    ("310", "citări · indice h 12 (Google Scholar, iun. 2026)", "citations · h-index 12 (Google Scholar, Jun 2026)"),
]


def stats():
    return '<ul class="stats">' + "".join(
        f'<li><strong>{esc(n)}</strong>{bi(r, e)}</li>' for n, r, e in STATS) + "</ul>"


def areas():
    items = "".join(
        f'<li class="area{" lead-area" if i == 0 else ""}"><span class="num">{i + 1:02d}</span>'
        f'<h3>{bi(t_ro, t_en)}</h3>{bi(x_ro, x_en, tag="p")}</li>'
        for i, (t_ro, t_en, x_ro, x_en) in enumerate(AREAS))
    return f'<ol class="areas">{items}</ol>'


NAV = [("profile", "Profil", "Profile"), ("expertise", "Expertiză", "Expertise"), ("experience", "Experiență", "Experience"),
       ("education", "Educație", "Education"), ("roles", "Roluri internaționale", "International roles"),
       ("skills", "Competențe", "Skills"), ("publications", "Publicații", "Publications")]

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
           "%3Crect width='64' height='64' rx='14' fill='%231f3a5f'/%3E%3Ctext x='32' y='42' font-family='Georgia,serif' "
           "font-size='28' fill='%23fff' text-anchor='middle'%3ECH%3C/text%3E%3C/svg%3E")

CSS = r"""
:root{--ink:#1c2430;--muted:#5b6575;--line:#e3e6eb;--bg:#fbfaf7;--card:#fff;--accent:#1f3a5f;--accent2:#b5651d;--chip:#eef2f7}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 "Source Sans 3",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;-webkit-font-smoothing:antialiased}
html[data-lang="en"] .l-ro, html[data-lang="ro"] .l-en{display:none!important}
a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:2px}
a:hover{color:var(--accent2)}
.wrap{max-width:900px;margin:0 auto;padding:0 24px}
header.top{background:var(--accent);color:#fff;padding:56px 0 40px}
header.top a{color:#fff}
.bar{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap}
h1{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:clamp(2rem,5vw,2.9rem);line-height:1.1;margin:0 0 8px;letter-spacing:-.01em}
.headline{font-size:1.15rem;opacity:.92;margin:0 0 18px;max-width:640px}
.contact{display:flex;flex-wrap:wrap;gap:6px 22px;margin:0;padding:0;list-style:none;font-size:.95rem;opacity:.95}
.tools{display:flex;gap:8px;align-items:center;margin-bottom:12px}
.switch{display:inline-flex;border:1px solid rgba(255,255,255,.5);border-radius:999px;overflow:hidden}
.switch button,.print{font:inherit;font-size:.85rem;font-weight:600;letter-spacing:.04em;background:transparent;color:#fff;border:0;padding:6px 14px;cursor:pointer}
.switch button[aria-pressed="true"]{background:#fff;color:var(--accent)}
.print{border:1px solid rgba(255,255,255,.5);border-radius:999px}
.print:hover,.switch button:hover{background:rgba(255,255,255,.15)}
.switch button[aria-pressed="true"]:hover{background:#fff}
nav.toc{position:sticky;top:0;z-index:5;background:rgba(251,250,247,.94);backdrop-filter:blur(6px);border-bottom:1px solid var(--line)}
nav.toc ul{display:flex;gap:4px 20px;flex-wrap:wrap;list-style:none;margin:0;padding:12px 0}
nav.toc a{color:var(--muted);text-decoration:none;font-size:.9rem;font-weight:600}
nav.toc a:hover{color:var(--accent)}
main{padding:12px 0 64px}
section{padding-top:28px}
h2{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.55rem;color:var(--accent);margin:24px 0 16px;padding-bottom:8px;border-bottom:2px solid var(--line);scroll-margin-top:60px}
h3{font-size:1.02rem;line-height:1.4;margin:0 0 4px}
.lead{font-size:1.06rem}
.stats{list-style:none;padding:0;margin:24px 0 8px;display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.stats li{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;font-size:.85rem;color:var(--muted);line-height:1.35}
.stats strong{display:block;font-family:"Source Serif 4",Georgia,serif;font-size:1.6rem;color:var(--accent);line-height:1.2;margin-bottom:2px}
.callout{background:var(--card);border-left:3px solid var(--accent2);padding:12px 16px;border-radius:0 8px 8px 0;margin:16px 0}
.callout p{margin:4px 0}
.areas{list-style:none;padding:0;margin:16px 0 0;display:grid;grid-template-columns:1fr 1fr;gap:12px}
.area{position:relative;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 18px 14px 52px}
.area .num{position:absolute;left:16px;top:14px;font-family:"Source Serif 4",Georgia,serif;font-weight:600;color:var(--accent2);font-size:1.05rem}
.area p{margin:0;font-size:.92rem;color:#333c49}
.area.lead-area{grid-column:1/-1;border-left:4px solid var(--accent2);background:#fffaf4}
.job{display:grid;grid-template-columns:170px 1fr;gap:20px;padding:18px 0;border-top:1px solid var(--line)}
.job:first-of-type{border-top:0}
.when{font-size:.88rem;color:var(--muted);font-weight:600;line-height:1.4}
.badge{display:inline-block;margin-top:6px;font-size:.7rem;text-transform:uppercase;letter-spacing:.06em;background:var(--accent2);color:#fff;border-radius:4px;padding:1px 7px}
.is-current .when{color:var(--accent)}
.org{margin:0 0 6px;color:var(--muted);font-size:.92rem}
.desc{margin:0 0 8px}
.outputs{font-size:.92rem;margin:6px 0 8px}
.outputs .lbl{font-weight:700;font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;color:var(--accent2)}
.outputs ul{margin:4px 0 0;padding-left:18px}
.tags{list-style:none;padding:0;margin:8px 0 0;display:flex;flex-wrap:wrap;gap:6px}
.tags li{background:var(--chip);color:#36506f;font-size:.75rem;padding:2px 9px;border-radius:999px}
.certs{margin-top:14px;font-size:.95rem}
.roles{list-style:none;padding:0;margin:0}
.roles li{display:grid;grid-template-columns:170px 1fr;gap:20px;padding:9px 0;border-top:1px solid var(--line)}
.roles li:first-child{border-top:0}
.roles .yr{color:var(--muted);font-weight:600;font-size:.88rem}
.tablewrap{overflow-x:auto}
table{border-collapse:collapse;margin:8px 0;font-size:.92rem;background:var(--card)}
th,td{border:1px solid var(--line);padding:6px 12px;text-align:center}
thead th{background:var(--chip);font-weight:600;font-size:.82rem}
tbody th{text-align:left}
.note{font-size:.82rem;color:var(--muted);margin:0}
.skills{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px}
.skill{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 18px}
.skill p{margin:0;font-size:.93rem}
.pubs{padding-left:22px;font-size:.93rem}
.pubs li{margin:0 0 10px;padding-left:4px}
.pubs a{font-size:.82rem;white-space:nowrap}
h3.sub{font-size:1.05rem;margin:24px 0 8px;color:var(--ink)}
footer{border-top:1px solid var(--line);padding:24px 0 40px;color:var(--muted);font-size:.85rem}
@media (max-width:720px){
  .areas{grid-template-columns:1fr}
  h2{scroll-margin-top:96px}
  .stats{grid-template-columns:1fr 1fr}
  .job,.roles li{grid-template-columns:1fr;gap:4px}
  .skills{grid-template-columns:1fr}
  header.top{padding:36px 0 28px}
}
@media print{
  @page{margin:16mm 14mm}
  body{background:#fff;font-size:10.5pt}
  header.top{background:#fff;color:var(--ink);padding:0 0 10px;border-bottom:2px solid var(--accent)}
  header.top a{color:var(--ink)}
  h1{color:var(--accent)}
  .tools,nav.toc,footer .src{display:none}
  .stats li,.skill,.area{border-color:#ccc}
  .area{break-inside:avoid}
  .job,.roles li,.skill,.pubs li{break-inside:avoid}
  h2{break-after:avoid}
  a{color:var(--ink);text-decoration:none}
  .pubs a{display:none}
}
"""

JS = r"""
(function(){
  var root=document.documentElement, KEY='cv-lang';
  function set(l, save){
    root.setAttribute('data-lang', l); root.lang = l;
    document.title = l==='ro' ? 'Mihai Cezar Hâj — CV' : 'Mihai Cezar Hâj — CV';
    var bs=document.querySelectorAll('.switch button');
    for(var i=0;i<bs.length;i++) bs[i].setAttribute('aria-pressed', bs[i].getAttribute('data-l')===l ? 'true':'false');
    if(save){ try{ localStorage.setItem(KEY,l); }catch(e){} }
  }
  var q=(location.search.match(/[?&]lang=(en|ro)/)||[])[1] || (location.hash==='#ro'?'ro':location.hash==='#en'?'en':null);
  var s=null; try{ s=localStorage.getItem(KEY); }catch(e){}
  var nav=(navigator.language||'').toLowerCase().indexOf('ro')===0?'ro':null;
  set(q||s||nav||'en', false);
  document.addEventListener('click',function(ev){
    var b=ev.target.closest('.switch button'); if(b){ set(b.getAttribute('data-l'), true); }
    if(ev.target.closest('.print')) window.print();
  });
})();
"""


def page():
    nav = "".join(f'<li><a href="#{i}">{bi(r, e)}</a></li>' for i, r, e in NAV)
    return f'''<!DOCTYPE html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mihai Cezar Hâj — CV</title>
<meta name="description" content="Curriculum vitae of Mihai Cezar Hâj, PhD — public-sector and education-policy expert (higher education, Bologna Process, digital skills, AI in education). Bucharest, Romania.">
<meta name="author" content="Mihai Cezar Hâj">
<meta property="og:type" content="profile">
<meta property="og:title" content="Mihai Cezar Hâj — CV">
<meta property="og:description" content="Public-sector and education-policy expert: higher education, Bologna Process, digital skills, AI in education.">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&family=Source+Serif+4:opsz,wght@8..60,600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<header class="top">
  <div class="wrap">
    <div class="bar">
      <div>
        <h1>Mihai Cezar Hâj</h1>
        {bi("Expert în politici publice și educaționale · Doctor în Științe Politice", "Public-sector and education-policy expert · PhD in Political Science", tag="p", cls="headline")}
      </div>
      <div class="tools">
        <div class="switch" role="group" aria-label="Language / Limba"><button type="button" data-l="en" aria-pressed="true">EN</button><button type="button" data-l="ro" aria-pressed="false">RO</button></div>
        <button type="button" class="print">{bi("Tipărește / PDF", "Print / PDF")}</button>
      </div>
    </div>
    <ul class="contact">
      <li>✉ <a href="mailto:cezarhaj@gmail.com">cezarhaj@gmail.com</a></li>
      <li>{bi("București, România", "Bucharest, Romania")}</li>
      <li>{link(SCHOLAR_URL, "Google Scholar")}</li>
    </ul>
  </div>
</header>
<nav class="toc"><div class="wrap"><ul>{nav}</ul></div></nav>
<main class="wrap">
  <section>
    {h2("Profil", "Profile", "profile")}
    {bi(*PROFILE, tag="p", cls="lead")}
    {stats()}
  </section>
  <section>
    {h2("Domenii de expertiză", "Areas of expertise", "expertise")}
    {bi(*EXPERTISE_INTRO, tag="p")}
    {areas()}
  </section>
  <section>
    {h2("Experiență profesională", "Professional experience", "experience")}
    {experience()}
  </section>
  <section>
    {h2("Educație și formare", "Education and training", "education")}
    {education()}
  </section>
  <section>
    {h2("Grupuri de lucru internaționale și alte roluri", "International working groups and other roles", "roles")}
    {roles()}
  </section>
  <section>
    {h2("Competențe", "Skills", "skills")}
    {skills()}
  </section>
  <section>
    {h2("Publicații", "Publications", "publications")}
    <p>{bi("Indicatori de citare (Google Scholar, iunie 2026): 310 citări · indice h 12 · indice i10 14. Lista completă și actualizată: ", "Citation metrics (Google Scholar, June 2026): 310 citations · h-index 12 · i10-index 14. Full, up-to-date list: ")}{link(SCHOLAR_URL, "Google Scholar")}.</p>
    <h3 class="sub">{bi("Cărți, capitole și articole", "Books, chapters and articles")}</h3>
    {pubs(BOOKS)}
    <h3 class="sub">{bi("Studii, rapoarte și note de politici", "Studies, reports and policy briefs")}</h3>
    {pubs(REPORTS)}
  </section>
</main>
<footer>
  <div class="wrap">{bi("Actualizat: noiembrie 2026", "Last updated: November 2026")} · Mihai Cezar Hâj</div>
</footer>
<script>{JS}</script>
</body>
</html>
'''


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
    out.write_text(page(), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size // 1024} KB, {len(EXPERIENCE)} positions)")
