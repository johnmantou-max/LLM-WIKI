#!/usr/bin/env python3
"""Render approved user-sourced Markdown into GitHub Pages-compatible static HTML.
Uses only Python stdlib. Source facts cannot be invented during rendering.
"""
from pathlib import Path
from datetime import date
from html import escape
import json, re, hashlib, math
from urllib.parse import quote
ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = [
 ('BTC 與區塊鏈基礎','BTC / BLOCKCHAIN','₿','工作量證明、區塊、交易、UTXO'),
 ('技術分析','TECHNICAL ANALYSIS','⌁','K 線、EMA、MACD、RSI'),
 ('價格行為與 SMC','PRICE ACTION / SMC','◇','OB、FVG、流動性與市場結構'),
 ('永續合約與槓桿','PERPETUAL FUTURES','⇄','永續合約、槓桿、保證金、資金費率'),
 ('總體經濟','MACRO ECONOMICS','◎','Fed、CPI、美債殖利率、DXY'),
 ('交易心理與風險管理','RISK / MINDSET','◈','停損、倉位管理、交易心理'),
]
CATS = [x[0] for x in CATEGORIES]
SITE_CSS = r'''
:root{color-scheme:dark;--bg:#080e1b;--panel:#111b2b;--panel2:#172338;--line:#27374c;--txt:#e9f1fe;--muted:#8a9db7;--accent:#65e5c5;--amber:#f4bd74}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 85% -5%,#14424b80,transparent 37%),var(--bg);color:var(--txt);font:15px/1.65 'Microsoft JhengHei','Noto Sans TC',ui-sans-serif,system-ui,sans-serif;min-height:100vh}a{color:inherit;text-decoration:none}button,input{font:inherit}a:focus-visible,button:focus-visible,input:focus-visible{outline:2px solid var(--accent);outline-offset:3px}.layout{display:grid;grid-template-columns:255px minmax(0,1fr);min-height:100vh}.sidebar{border-right:1px solid var(--line);padding:30px 20px;position:sticky;top:0;height:100vh;background:#0d1625e8;display:flex;flex-direction:column}.brand{display:flex;align-items:center;gap:12px;font-weight:850;font-size:19px;letter-spacing:-.5px;margin-bottom:38px}.coin{height:40px;width:40px;border-radius:12px;background:#285e58;color:#b8ffee;display:grid;place-items:center;font-size:28px;box-shadow:0 5px 22px #5cf2be18}.tag{font-size:10px;font-weight:850;color:#72f0cd;letter-spacing:2px;display:block;margin:0 0 14px}.nav a{display:flex;align-items:center;gap:12px;padding:12px 15px;margin:4px 0;color:#9eb0c9;border-radius:10px;font-size:14px}.nav a:hover,.nav a.current{background:#1c3544;color:#b9ffdf}.nav a span{font-size:17px;color:#77bbaa}.side-bottom{margin-top:auto;border-top:1px solid var(--line);padding-top:16px;font-size:12px;color:var(--muted)}.side-bottom b{color:var(--amber)}main{min-width:0;padding:44px max(32px,calc((100vw - 1240px)/2));max-width:1500px}.hero{padding:65px 0 37px;max-width:910px}.eyebrow{text-transform:uppercase;font-size:12px;letter-spacing:2.5px;color:var(--accent);font-weight:850}.hero h1{font-size:clamp(36px,5vw,73px);line-height:1.11;letter-spacing:-2.5px;margin:19px 0}.hero h1 em{font-style:normal;color:var(--accent)}.lead{font-size:17px;color:#abbcd1;line-height:1.85;max-width:720px}.actions{display:flex;gap:12px;flex-wrap:wrap;margin:27px 0}.btn{display:inline-flex;justify-content:center;align-items:center;gap:8px;border:1px solid #3d5766;background:#1b2c42;border-radius:10px;padding:11px 18px;font-weight:750;font-size:14px;color:#ddf8f6;cursor:pointer}.btn.primary{background:#77ebc8;color:#07382f;border-color:#77ebc8}.btn:hover{filter:brightness(1.12)}.label{font-size:12px;color:var(--muted);letter-spacing:1.8px;text-transform:uppercase;font-weight:800;margin:28px 0 16px}.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:13px;max-width:870px}.metric,.card,.pane{background:linear-gradient(150deg,#152136,#111a2a);border:1px solid var(--line);border-radius:15px}.metric{padding:21px 23px}.metric strong{display:block;font-size:31px;line-height:1.3}.metric small{display:block;color:var(--muted);font-size:12px;margin-top:4px}.section-head{display:flex;align-items:end;justify-content:space-between;gap:15px;margin-top:48px}.section-head h2{font-size:26px;margin:0}.section-head span{color:var(--muted);font-size:13px}.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:15px;margin:20px 0 34px}.card{padding:21px;min-height:180px;position:relative;transition:.2s}.card:hover{border-color:#57c7b5;transform:translateY(-3px)}.card-icon{color:var(--accent);font-size:27px;font-weight:850}.card h3{margin:10px 0 6px;font-size:17px}.card p{font-size:13px;color:var(--muted);line-height:1.7;margin:0}.card .count{position:absolute;right:18px;top:20px;font-size:12px;color:#89a7ba}.status{border:1px solid #675538;background:#3a30221c;color:#f3d9a5;border-radius:12px;padding:15px 18px;margin:25px 0;font-size:14px}.status.ok{border-color:#2d6f5b;background:#143e321c;color:#b9f1dd}.status b{display:block;margin-bottom:3px}.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:17px 0}.step{border-left:3px solid #52bdab;padding:4px 0 6px 17px}.step h3{font-size:15px;margin:0}.step p{font-size:13px;color:var(--muted);margin:5px 0}.page-title{font-size:clamp(28px,4vw,46px);letter-spacing:-1px;margin:20px 0 5px}.sub{color:var(--muted);max-width:850px}.toolbar{display:flex;gap:10px;flex-wrap:wrap;margin:24px 0}.search{width:min(100%,380px);padding:12px 15px;border:1px solid var(--line);background:var(--panel);border-radius:10px;color:#fff}.filter{border:1px solid var(--line);background:#172437;color:#b9c9da;padding:8px 12px;border-radius:50px;cursor:pointer;font-size:12px}.filter.active{background:#1d5149;color:#9df3d9;border-color:#4ea793}.article-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:13px}.article-row{padding:20px;border:1px solid var(--line);background:var(--panel);border-radius:13px}.article-row h3{margin:5px 0 7px;font-size:18px}.article-row .desc{font-size:13px;color:var(--muted);margin:0}.article-row .meta{color:var(--accent);font-weight:700;font-size:11px}.article-row .link{display:inline-block;color:#9feee0;font-size:13px;margin-top:12px}.article{border:1px solid var(--line);background:#101a2b;border-radius:16px;padding:27px 34px;margin:26px 0;max-width:940px}.article h2{font-size:26px;letter-spacing:-.5px}.article h3{font-size:19px;margin:26px 0 5px;color:#cbf7eb}.article p,.article li{color:#c9d6e7}.article blockquote{border-left:3px solid var(--accent);padding:2px 15px;background:#19283a;margin-left:0;color:#dbeee9}.article code{background:#1b2b3e;border-radius:4px;padding:1px 5px}.citation{color:#7fe3cf;font-weight:700;font-size:12px;border-bottom:1px dashed #5aaea4}.sources{border-top:1px solid var(--line);margin-top:22px;padding-top:16px;color:var(--muted);font-size:12px}.source-item{font-size:13px;padding:10px 0;border-bottom:1px solid var(--line)}.source-item a{color:var(--accent);word-break:break-word}.workflow{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:25px 0}.node{border:1px solid #345368;border-radius:13px;padding:19px;background:#142239;min-height:148px}.node b{font-size:13px;color:var(--accent);letter-spacing:1px}.node h3{margin:7px 0;font-size:18px}.node p{color:var(--muted);font-size:13px;margin:0}.diagram{background:#111c2d;border:1px solid var(--line);border-radius:18px;overflow:hidden;padding:8px;margin-top:26px}.diagram svg{width:100%;height:auto;display:block}.diagram .hub{fill:#205448;stroke:#71dabb;stroke-width:2}.diagram .leaf{fill:#14253b;stroke:#406078;stroke-width:2;cursor:pointer}.diagram .edge{stroke:#3d6871;stroke-width:2}.diagram text{fill:#e9faff;font-family:inherit;font-weight:700;pointer-events:none}.diagram a:hover .leaf{fill:#27565a}.footer{border-top:1px solid var(--line);margin-top:55px;padding:20px 0;color:#7185a1;font-size:12px}.hidden{display:none!important}@media(max-width:1080px){.cards{grid-template-columns:repeat(2,1fr)}.workflow{grid-template-columns:repeat(2,1fr)}main{padding:32px}.sidebar{width:210px}.layout{grid-template-columns:210px 1fr}}@media(max-width:720px){.layout{display:block}.sidebar{position:relative;height:auto;width:auto;padding:16px 18px;border-right:0;border-bottom:1px solid var(--line)}.brand{margin:0 0 12px}.nav{display:flex;overflow-x:auto;gap:2px}.nav a{padding:7px 10px;white-space:nowrap}.side-bottom{display:none}main{padding:20px 18px}.hero{padding:32px 0 19px}.hero h1{letter-spacing:-1px}.metrics,.cards,.article-list,.workflow,.steps{grid-template-columns:1fr}.article{padding:17px}.section-head{display:block}.section-head span{display:block;margin-top:5px}}'''
SITE_JS = r'''
(function(){const input=document.querySelector('#search');const buttons=[...document.querySelectorAll('.filter')];const rows=[...document.querySelectorAll('.article-row')];let cat='all';const run=()=>{let query=(input?.value||'').toLowerCase();let n=0;rows.forEach(el=>{let yes=(cat==='all'||el.dataset.category===cat)&&el.textContent.toLowerCase().includes(query);el.classList.toggle('hidden',!yes);if(yes)n++});const empty=document.querySelector('#filter-empty');if(empty)empty.classList.toggle('hidden',n>0||rows.length===0)};input?.addEventListener('input',run);buttons.forEach(b=>b.addEventListener('click',()=>{cat=b.dataset.filter;buttons.forEach(x=>x.classList.toggle('active',x===b));run()}));if(input){let wanted=new URLSearchParams(location.search).get('category');if(wanted){let b=buttons.find(x=>x.dataset.filter===wanted);b?.click()}}})();'''
SLIDE_CSS=r'''
*{box-sizing:border-box}html,body{margin:0;height:100%;background:#070e1c;color:#eef8ff;font-family:'Microsoft JhengHei','Noto Sans TC',system-ui,sans-serif}body{overflow:hidden}.deck{min-height:100vh;display:grid;place-items:center;padding:20px 20px 90px}.slide{display:none;position:relative;width:min(1180px,100%);aspect-ratio:16/9;max-height:calc(100vh - 125px);border-radius:16px;border:1px solid #385569;background:radial-gradient(circle at 85% 10%,#21565390,transparent 37%),linear-gradient(145deg,#14253b,#0c1628);padding:3.5% 5%;overflow:auto;flex-direction:column;justify-content:space-between;box-shadow:0 15px 80px #0008}.slide.active{display:flex}.slide .head,.slide .foot{display:flex;justify-content:space-between;align-items:center;gap:14px;color:#93abc2;font-size:clamp(10px,1.15vw,14px)}.slide .head b{color:#7cf0cb;letter-spacing:2px}.slide .foot{font-size:clamp(8px,1vw,12px)}.slide .content{margin:auto 0;max-width:94%}.slide .eyebrow{font-size:clamp(10px,1.1vw,15px);color:#84f7ce;letter-spacing:2px;font-weight:850}.slide h1{font-size:clamp(26px,4.6vw,65px);line-height:1.2;margin:15px 0 10px;letter-spacing:-1px}.slide .summary{font-size:clamp(14px,1.6vw,22px);line-height:1.7;color:#b6d5e3}.slide .bullets{font-size:clamp(13px,1.6vw,20px);line-height:1.5;color:#d4e8ee;padding-left:1.3em;max-width:940px}.slide .bullets li{margin:9px 0}.slide .foot a{color:#74e8c3;margin-left:5px;text-decoration:underline}.slide .evidence{font-size:clamp(12px,1.45vw,19px);color:#9cb5cb;margin-top:24px}.slide .ref{color:#91efce}.decknav{position:fixed;bottom:16px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:13px;border:1px solid #3e5d72;background:#14253cec;padding:9px 14px;border-radius:45px;z-index:10}.decknav button{border:1px solid #46697e;background:#213b4c;color:white;font:inherit;border-radius:40px;width:36px;height:36px;cursor:pointer}.decknav a{color:#8bf5d1;text-decoration:none;font-size:13px}.decknav .pagecount{white-space:nowrap;font-size:12px;color:#b8ccdc;min-width:60px;text-align:center}.unfinished{color:#ffd79f}.progress{position:fixed;bottom:0;left:0;height:3px;background:#79f0c9;transition:width .2s}@media(max-width:680px){.deck{padding:10px 8px 86px}.slide{aspect-ratio:4/5;max-height:calc(100vh - 110px);padding:7%}.slide h1{font-size:clamp(24px,7vw,40px)}.slide .summary{font-size:clamp(15px,3.5vw,20px)}.slide .bullets{font-size:clamp(13px,1.6vw,20px);line-height:1.5;color:#d4e8ee;padding-left:1.3em;max-width:940px}.slide .bullets li{margin:9px 0}.slide .foot a{color:#74e8c3;margin-left:5px;text-decoration:underline}.slide .evidence{font-size:13px}.slide .head,.slide .foot{font-size:10px}}@media print{body{overflow:visible;background:white}.deck{display:block;padding:0}.slide,.slide.active{display:flex!important;width:100%;height:100vh;max-height:none;page-break-after:always;border-radius:0;box-shadow:none;-webkit-print-color-adjust:exact;print-color-adjust:exact}.decknav,.progress{display:none}}'''

def load_json(p,default):
    try: return json.loads(p.read_text(encoding='utf-8'))
    except (FileNotFoundError,ValueError):return default

def parse_frontmatter(raw):
    m=re.match(r'^---\s*\n(.*?)\n---\s*\n',raw,re.S)
    front={}
    if m:
        for line in m.group(1).splitlines():
            if ':' in line:
                k,v=line.split(':',1);front[k.strip()]=v.strip().strip('"\'')
    return front,raw[m.end():] if m else raw

CITE=re.compile(r'\[@(SRC-[A-F0-9]{10}):p(\d+):L(\d+)-L(\d+)\]')

def render_inline(t,refs):
    # escape HTML first, transform only safe fixed patterns
    t=escape(t)
    t=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',t)
    t=re.sub(r'`([^`]+)`',r'<code>\1</code>',t)
    def repl(m):
        sid,p,a,b=m.groups();refs.add(sid)
        return f'<a class="citation" href="data/extracted/{sid}.md" target="_blank" title="來源 {sid} 第 {p} 頁 L{a}–L{b}">[{sid} p{p}:L{a}–L{b}]</a>'
    t=CITE.sub(repl,t)
    # markdown local links, protect external safe protocol only
    t=re.sub(r'\[([^\[\]]+)\]\(([^\s\)]+)\)',lambda m: f'<a href="{escape(m.group(2),quote=True)}">{m.group(1)}</a>' if not re.match(r'(?i)javascript:',m.group(2)) else m.group(1),t)
    return t

def markdown_to_html(src):
    lines=src.splitlines();buf=[];refs=set();in_list=False;in_code=False
    def close_list():
        nonlocal in_list
        if in_list:buf.append('</ul>');in_list=False
    for ln in lines:
        if ln.strip().startswith('```'):
            close_list();buf.append('</pre>' if in_code else '<pre>');in_code=not in_code;continue
        if in_code:buf.append(escape(ln));continue
        if not ln.strip():close_list();continue
        head=re.match(r'^(#{1,4})\s+(.*)',ln)
        if head:
            close_list();n=len(head.group(1));buf.append(f'<h{n+1}>{render_inline(head.group(2),refs)}</h{n+1}>');continue
        if ln.startswith('> '):close_list();buf.append('<blockquote>'+render_inline(ln[2:],refs)+'</blockquote>');continue
        if re.match(r'^\s*[-*]\s+',ln):
            if not in_list:buf.append('<ul>');in_list=True
            buf.append('<li>'+render_inline(re.sub(r'^\s*[-*]\s+','',ln),refs)+'</li>');continue
        close_list();buf.append('<p>'+render_inline(ln.strip(),refs)+'</p>')
    close_list()
    return '\n'.join(buf),refs

def site_shell(name,body,status):
    nav=[('index.html','⌂','首頁'),('wiki.html','▤','知識庫'),('graph.html','◎','知識關聯圖'),('deck.html','▣','HTML 簡報'),('workflow.html','⇄','Graph / Loop')]
    sidebar=''.join(f'<a href="{href}" class="{"current" if name==href else ""}"><span>{ic}</span>{label}</a>' for href,ic,label in nav)
    return f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BTC Trading Wiki｜{escape(name.split('.')[0])}</title><meta name="description" content="可追溯來源的個人 BTC 交易知識庫"><link rel="stylesheet" href="assets/site.css"></head><body><div class="layout"><aside class="sidebar"><a href="index.html" class="brand"><span class="coin">₿</span><span>BTC <span style="color:#80ecd0">ATLAS</span><small style="display:block;font-size:11px;color:#829ab7;font-weight:500">PERSONAL LLM WIKI</small></span></a><span class="tag">NAVIGATION</span><nav class="nav">{sidebar}</nav><div class="side-bottom">PROJECT v1.0<br><b>{escape(status)}</b><br>手動匯入 · 精確引用 · Graph + Loop</div></aside><main>{body}<footer class="footer">BTC Trading Wiki · Source-first learning · 不提供即時交易訊號或投資建議</footer></main></div><script src="assets/site.js"></script></body></html>'''

def safe_slug(p):return re.sub(r'[^a-zA-Z0-9_-]','-',p.stem)

def main():
    idx=load_json(ROOT/'data/source_index.json',{'sources':[],'errors':[]})
    sources=idx.get('sources',[]);source_map={s['id']:s for s in sources}
    entries=[]
    for p in sorted((ROOT/'wiki'/'pages').glob('*.md')):
        fm,content=parse_frontmatter(p.read_text(encoding='utf-8'))
        if fm.get('status','draft').lower() not in {'draft','approved'}:continue
        body,refs=markdown_to_html(content)
        if not refs:continue  # unreferenced article never published
        entries.append({'slug':safe_slug(p),'title':fm.get('title',p.stem),'category':fm.get('category','未分類'), 'summary':fm.get('summary',''), 'tags':fm.get('tags',''),'status':fm.get('status','draft').lower(),'body':body,'refs':sorted(refs),'raw':content})
    count=len(sources);pages=sum(e['status']=='approved' for e in entries);drafts=sum(e['status']=='draft' for e in entries);ready=(count>=5 and pages>=6 and set(CATS).issubset({x['category'] for x in entries if x['status']=='approved'}))
    preview_mode = not ready and count>=5 and len(entries)>0
    phase=('正式發布｜已由使用者確認' if ready else (f'已整理 {count} 篇來源摘要、{len(entries)} 篇學習筆記｜尚待確認' if preview_mode else '待完成｜等待來源與審查'))
    cat_cards=''.join(f'''<a class="card" href="wiki.html?category={quote(c)}"><span class="card-icon">{icon}</span><span class="count">{sum(e['category']==c for e in entries):02d} ARTICLES</span><h3>{escape(c)}</h3><p>{escape(desc)}</p></a>''' for c,en,icon,desc in CATEGORIES)
    home=f'''<section class="hero"><span class="eyebrow">A source-grounded personal knowledge system</span><h1>讀懂 BTC。<br><em>建立自己的交易知識地圖。</em></h1><p class="lead">從技術分析、價格行為、永續合約到總體經濟，用可追溯的資料整理觀念。Karpathy LLM Wiki 思路：原始資料唯讀、Wiki 持續維護、每次更新都有紀錄。</p><div class="actions"><a href="wiki.html" class="btn primary">探索知識庫　→</a><a href="graph.html" class="btn">查看關聯圖</a><a href="workflow.html" class="btn">了解工作流程</a></div></section><section class="metrics"><div class="metric"><strong>{count:02d}</strong><small>實際匯入來源（目標 ≥5）</small></div><div class="metric"><strong>{len(entries):02d}</strong><small>Wiki 正式文章（已核准 {pages}）</small></div><div class="metric"><strong>{len({e["category"] for e in entries}):02d}</strong><small>已涵蓋的知識領域</small></div></section><div class="status {'ok' if ready else ''}"><b>{escape(phase)}</b>{'已由使用者確認發布；來源引文可透過原文連結自行追溯。' if ready else ('已批次匯入來源摘要並完成六大領域的學習筆記；內容仍待逐項人工核對，尚非正式審查通過的知識庫。' if preview_mode else '請提供資料並建立 Wiki。')}</div><div class="section-head"><h2>六大學習領域</h2><span>按領域進入 Wiki</span></div><div class="cards">{cat_cards}</div><div class="section-head"><h2>知識如何生成？</h2><span>不是一次 Prompt，而是可驗證的工作流程</span></div><div class="steps"><div class="step"><h3>01 / 手動批次匯入</h3><p>只讀 raw/ 中使用者提供的文件，保留 SHA-256、頁碼與行號。</p></div><div class="step"><h3>02 / 建立與審查 Wiki</h3><p>AI 根據證據編寫、逐條引用、保留矛盾，人工通過後才公開。</p></div><div class="step"><h3>03 / 生成成果</h3><p>輸出 Wiki、關聯圖與 HTML 簡報；Graph 控流程、Loop 修錯。</p></div></div>'''
    (ROOT/'index.html').write_text(site_shell('index.html',home,phase),encoding='utf-8')
    # wiki
    filters=''.join(f'<button class="filter" data-filter="{escape(c,quote=True)}">{escape(c)}</button>' for c in CATS)
    rows=''.join(f'<article class="article-row" data-category="{escape(e["category"],quote=True)}"><div class="meta">{escape(e["category"])} · {len(e["refs"])} 個來源 ID · {('未核准' if e['status']=='draft' else '正式文章')}</div><h3>{escape(e["title"])}</h3><p class="desc">{escape(e["summary"])}</p><a class="link" href="#article-{e["slug"]}">閱讀文章　↗</a></article>' for e in entries)
    detail=''.join(f'''<section class="article" id="article-{e['slug']}"><span class="eyebrow">{escape(e['category'])} / {escape(e['status'].upper())}</span>{e['body']}<div class="sources"><b>來源文件（筆記定位＋原始網站）</b>{''.join(f'<div class="source-item">{sid} · {escape(source_map.get(sid,{}).get("title","未註冊來源"))} · <a href="data/extracted/{sid}.md" target="_blank">查看摘記</a> · <a href="{escape(source_map.get(sid,{}).get("url","#"),quote=True)}" target="_blank" rel="noopener">核對原文</a></div>' for sid in e['refs'])}</div></section>''' for e in entries)
    empty='''<div class="status"><b>目前沒有可預覽的 Wiki 文章</b>請先完成批次匯入與撰寫。</div>''' if not entries else ''
    wiki=f'''<span class="eyebrow">PERSONAL KNOWLEDGE BASE</span><h1 class="page-title">BTC 交易知識庫</h1><p class="sub">目前整理 {len(entries)} 篇來源導向的學習筆記，已涵蓋六大領域。引用 p1:Lx 是本站摘要行號；請透過原始網頁核對對應章節。</p><div class="toolbar"><input id="search" class="search" type="search" placeholder="搜尋文章、名詞、分類…" aria-label="搜尋 Wiki"><button data-filter="all" class="filter active">全部</button>{filters}</div><div class="article-list">{rows}</div><p class="hidden" id="filter-empty">沒有符合條件的文章。</p>{empty}{detail}<div class="section-head"><h2>已匯入來源登錄</h2></div>{''.join(f'<div class="source-item">{s["id"]} · {escape(s["title"])} · {escape(s["file"])} · <a href="{escape(s["extracted_file"],quote=True)}">查看位置化文字</a></div>' for s in sources) if sources else '<p class="sub">尚無任何來源。</p>'}'''
    (ROOT/'wiki.html').write_text(site_shell('wiki.html',wiki,phase),encoding='utf-8')
    # graph: hub + six categories navigable. The hub lines are navigation only, not unproved causal claims.
    pos=[(170,140),(490,85),(810,140),(170,420),(490,480),(810,420)]
    lines=''.join(f'<line class="edge" x1="490" y1="280" x2="{x}" y2="{y}"/>' for x,y in pos)
    svgleaves=''.join(f'<a href="wiki.html?category={quote(cat)}" aria-label="前往 {escape(cat)}"><rect class="leaf" x="{x-135}" y="{y-39}" width="270" height="78" rx="14"/><text x="{x}" y="{y-5}" font-size="16" text-anchor="middle">{escape(cat)}</text><text x="{x}" y="{y+20}" font-size="11" text-anchor="middle" fill="#9cb5d0">{sum(e["category"]==cat for e in entries)} 篇文章</text></a>' for (x,y),(cat,*_) in zip(pos,CATEGORIES))
    rel=load_json(ROOT/'wiki'/'relations.json',{'relations':[]})
    if not rel.get('relations'):
        rel=load_json(ROOT/'wiki'/'relations.json',{'relations':[]})
    lookup={e['slug']:e for e in entries}
    graph=f'''<span class="eyebrow">KNOWLEDGE RELATIONSHIPS</span><h1 class="page-title">知識關聯圖</h1><p class="sub">先呈現六大分類導航，線條代表「屬於同一 Wiki」而非價格因果或交易模型。下方連結依來源整理，供對照學習；線條不代表價格因果。</p><div class="diagram"><svg viewBox="0 0 980 560" role="img" aria-label="BTC Wiki 六大分類導覽圖">{lines}<circle class="hub" cx="490" cy="280" r="89"/><text x="490" y="267" text-anchor="middle" font-size="30">BTC WIKI</text><text x="490" y="294" text-anchor="middle" font-size="12">可追溯知識</text>{svgleaves}</svg></div><div class="section-head"><h2>知識關聯與延伸閱讀</h2><span>{len(rel.get('relations',[]))} 條</span></div>{''.join(f'<div class="source-item"><a href="wiki.html#article-{escape(str(r.get("from","")),quote=True)}">{escape(lookup[r["from"]]["title"] if r.get("from") in lookup else str(r.get("from","")))}</a> → <a href="wiki.html#article-{escape(str(r.get("to","")),quote=True)}">{escape(lookup[r["to"]]["title"] if r.get("to") in lookup else str(r.get("to","")))}</a><div>{escape(str(r.get("relation","")))}</div><small>證據：{", ".join(escape(source_map[sid]["title"]) for sid in r.get("source_ids",[]) if sid in source_map)}</small></div>' for r in rel.get('relations',[])) or '<p class="sub">暫無已登錄的知識關聯。</p>'}'''
    # Optional second graph: approved article-to-article relationships, not guessed categories.
    linked=[]
    lookup={e['slug']:e for e in entries}
    for r in rel.get('relations',[]):
        if r.get('from') in lookup and r.get('to') in lookup and r.get('from')!=r.get('to'):
            linked.append(r)
    if linked:
        involved=sorted(set([r['from'] for r in linked]+[r['to'] for r in linked]))
        locations={slug:(490+340*math.cos(2*math.pi*i/len(involved)),290+200*math.sin(2*math.pi*i/len(involved))) for i,slug in enumerate(involved)}
        edge_svg=''.join(f'<line class="edge" x1="{locations[r["from"]][0]:.1f}" y1="{locations[r["from"]][1]:.1f}" x2="{locations[r["to"]][0]:.1f}" y2="{locations[r["to"]][1]:.1f}"/>' for r in linked)
        node_svg=''.join(f'<a href="wiki.html#article-{escape(slug,quote=True)}"><rect class="leaf" x="{xy[0]-104:.1f}" y="{xy[1]-26:.1f}" width="208" height="52" rx="12"/><text x="{xy[0]:.1f}" y="{xy[1]+5:.1f}" text-anchor="middle" font-size="13">{escape(lookup[slug]["title"][:15])}</text></a>' for slug,xy in locations.items())
        graph+=f'''<h2 class="page-title">知識關聯圖</h2><p class="sub">依來源整理的學習關聯；線條不表示價格上的因果關係。</p><div class="diagram"><svg viewBox="0 0 980 570" role="img" aria-label="已審查文章關聯圖">{edge_svg}{node_svg}</svg></div>'''
    (ROOT/'graph.html').write_text(site_shell('graph.html',graph,phase),encoding='utf-8')
    nodes=[('INTAKE','來源受理','首批五篇由使用者指定，新增來源由使用者授權補充'),('EXTRACT','解析與定位','保留 SHA-256、PDF 頁碼、每頁行號'),('EVIDENCE','來源證據卡','整理直接證據、矛盾、適用條件'),('SYNTHESIZE','撰寫知識','依六領域整合成 Markdown Wiki'),('LINT','品質檢查','檢查引用、結構、缺漏和連結'),('HUMAN','人工確認','檢查語義忠實度，核准文章與大綱'),('RENDER','產生網頁','正式發布使用已核准文章，保留引用與核准紀錄'),('VERIFY','渲染驗收','瀏覽器檢查溢出與連結'),('DELIVER','交件與反思','附過程、限制、檢查報告及網站網址')]
    wf=''.join(f'<div class="node"><b>{i+1:02d} / {tag}</b><h3>{label}</h3><p>{description}</p></div>' for i,(tag,label,description) in enumerate(nodes))
    workflow=f'''<span class="eyebrow">GRAPH CONTROLS THE FLOW · LOOP FIXES THE NODE</span><h1 class="page-title">可執行的工作流程</h1><p class="sub">流程不是一句「幫我檢查」。每一個節點都有輸入、輸出、可驗證的條件，以及失敗時的退回路線。</p><div class="workflow">{wf}</div><div class="status"><b>Loop 剎車條件</b>每個節點最多修正 3 輪；全部通過就停止。缺來源、來源不支援結論、資料矛盾未釐清或達到上限時停止並記錄，不得編造答案。</div><div class="section-head"><h2>失敗時退回哪裡？</h2></div><div class="steps"><div class="step"><h3>引文位置錯誤 → EVIDENCE / EXTRACT</h3><p>核對原始文字、修正位置，不必重建全部頁面。</p></div><div class="step"><h3>教學內容不符來源 → SYNTHESIZE</h3><p>只修改錯誤 Wiki 文章，再重新產生對應頁。</p></div><div class="step"><h3>文字溢出 → RENDER</h3><p>只修 CSS 與排版，不在排版時變更原始論點。</p></div></div><a class="btn" href="wiki.html">查看 Wiki　→</a>'''
    (ROOT/'workflow.html').write_text(site_shell('workflow.html',workflow,phase),encoding='utf-8')
    # The published deck reflects the approval state of the Markdown articles.
    def slide_bullets(entry, limit=4):
        result=[]
        for ln in entry['raw'].splitlines():
            if ln.startswith('- '):
                clean=CITE.sub('',ln[2:]).strip()
                if clean and not clean.startswith(('如需核對','本文是教學')):
                    result.append(clean)
            if len(result)>=limit:break
        return result
    if entries and count>=5:
        slide_data=[('BTC 交易知識地圖','根據已匯入來源整理的 BTC 學習導覽',[],['正式發布：本站內容已由使用者確認。','本次資料涵蓋 BTC 基礎、技術分析、SMC、合約、宏觀與風險管理。'])]
        for e in entries[:11]:
            slide_data.append((e['title'],e['summary'],e['refs'],slide_bullets(e)))

    else:
        slide_data=[('BTC Trading Wiki','教學簡報尚未生成：仍缺可讀的指定來源',[],[])]
    slides=[]
    for i,(title,summary,refids,bullets) in enumerate(slide_data):
        reftext=' · '.join(escape(source_map[x].get('title',x)) for x in refids if x in source_map) if refids else '流程與來源聲明'
        links=' '.join(f'<a href="{escape(source_map[x].get("url","#"),quote=True)}" target="_blank" rel="noopener">原文 {j+1}</a>' for j,x in enumerate(refids) if x in source_map)
        points=''.join('<li>'+escape(x)+'</li>' for x in bullets)
        slides.append(f'''<section class="slide {'active' if i==0 else ''}" data-slide="{i+1}"><div class="head"><b>BTC TRADING WIKI · 正式版</b><span>{i+1:02d} / {len(slide_data):02d}</span></div><div class="content"><div class="eyebrow">SOURCE-GROUNDED BTC LEARNING</div><h1>{escape(title)}</h1><p class="summary">{escape(summary)}</p><ul class="bullets">{points}</ul></div><div class="foot"><span>來源：{reftext} {links}</span><span>{date.today().isoformat()}</span></div></section>''')
    deckjs='''(()=>{const slides=[...document.querySelectorAll('.slide')];let i=0;const count=slides.length;const label=document.getElementById('counter');const bar=document.getElementById('bar');function go(n){slides[i].classList.remove('active');i=Math.max(0,Math.min(count-1,n));slides[i].classList.add('active');label.textContent=`${i+1} / ${count}`;bar.style.width=((i+1)/count*100)+'%';history.replaceState(null,'',`#s${i+1}`)}document.getElementById('prev').onclick=()=>go(i-1);document.getElementById('next').onclick=()=>go(i+1);document.addEventListener('keydown',e=>{if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();go(i+1)}if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();go(i-1)}});document.getElementById('fs').onclick=()=>{if(document.fullscreenElement)document.exitFullscreen();else document.documentElement.requestFullscreen?.()};const hash=location.hash.match(/^#s(\\d+)$/);go(hash?+hash[1]-1:0)})();'''
    deck=f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BTC Trading Wiki｜HTML 簡報</title><link rel="stylesheet" href="assets/deck.css"></head><body><main class="deck">{''.join(slides)}</main><nav class="decknav"><button id="prev" aria-label="上一張">←</button><span class="pagecount" id="counter">1 / {len(slides)}</span><button id="next" aria-label="下一張">→</button><button id="fs" aria-label="全螢幕">⛶</button><a href="wiki.html">Wiki</a><a href="index.html">首頁</a></nav><div id="bar" class="progress"></div><script>{deckjs}</script></body></html>'''
    (ROOT/'deck.html').write_text(deck,encoding='utf-8')
    (ROOT/'assets'/'site.css').write_text(SITE_CSS,encoding='utf-8')
    (ROOT/'assets'/'site.js').write_text(SITE_JS,encoding='utf-8')
    (ROOT/'assets'/'deck.css').write_text(SLIDE_CSS,encoding='utf-8')
    (ROOT/'data'/'site.json').write_text(json.dumps({'source_count':count,'approved_count':pages,'preview_article_count':len(entries),'preview_mode':not ready,'six_categories_ready':ready,'slide_count':len(slides),'articles':[{k:x[k] for k in ['slug','title','category','summary','refs','status']} for x in entries]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('render: sources=',count,' approved=',pages,' drafts=',drafts,' deck=',len(slides),' ready=',ready)

if __name__=='__main__':main()
