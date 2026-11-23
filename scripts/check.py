#!/usr/bin/env python3
"""Deterministic checks. Missing user-supplied sources => honestly report incomplete (exit 1)."""
from pathlib import Path
from datetime import datetime
from html.parser import HTMLParser
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
CATS=['BTC 與區塊鏈基礎','技術分析','價格行為與 SMC','永續合約與槓桿','總體經濟','交易心理與風險管理']
CITE=re.compile(r'\[@(SRC-[A-F0-9]{10}):p(\d+):L(\d+)-L(\d+)\]')
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.slide_count=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'href' in d:self.links.append(d['href'])
        if tag=='section' and 'slide' in d.get('class','').split(): self.slide_count+=1

def read_json(p,default):
    try:return json.loads(p.read_text(encoding='utf-8'))
    except Exception:return default

def frontmatter(t):
    m=re.match(r'^---\s*\n(.*?)\n---\s*\n',t,re.S)
    out={}
    if m:
        for line in m.group(1).splitlines():
            if ':' in line:
                k,v=line.split(':',1);out[k.strip()]=v.strip().strip('"\'')
    return out

def run():
    checks=[]
    def ck(name,ok,detail='',category='STRUCTURE'):
        checks.append((category,name,bool(ok),str(detail)))
    data=read_json(ROOT/'data'/'source_index.json',{})
    sources=data.get('sources',[]);src={s['id']:s for s in sources if 'id' in s}
    ck('使用者指定／授權來源摘要 ingest ≥5 份',len(sources)>=5, f'目前 {len(sources)} 份；非原文全文','SOURCE')
    ck('來源 ID 唯一',len(src)==len(sources))
    ck('無解析失敗',not data.get('errors',[]), ', '.join(data.get('errors',[])))
    for s in sources:
        p=ROOT/'raw'/s['file']
        ck(f'{s["id"]} 原始檔存在',p.is_file(),s['file'])
        if p.is_file():
            sha=hashlib.sha256(p.read_bytes()).hexdigest()
            ck(f'{s["id"]} SHA-256 未被修改',sha==s['sha256'])
        ck(f'{s["id"]} 定位文字存在',(ROOT/s['extracted_file']).is_file())
        ck(f'{s["id"]} 含文字位置',bool(s.get('pages')) and any(bool(p.get('lines')) for p in s['pages']))
    approved=[];drafts=[];total_cites=0
    for p in sorted((ROOT/'wiki/pages').glob('*.md')):
        text=p.read_text(encoding='utf-8');meta=frontmatter(text)
        if meta.get('status') not in ('approved','draft'):continue
        if meta.get('status')=='draft': drafts.append((p,meta,text))
        else: approved.append((p,meta,text))
        ck(f'{p.name} 分類有效',meta.get('category') in CATS,meta.get('category',''))
        ck(f'{p.name} 有摘要',bool(meta.get('summary')))
        cites=list(CITE.finditer(text));total_cites+=len(cites)
        ck(f'{p.name} 有精確引用',bool(cites),'未發現 [@SRC-id:pN:Lx-Ly]')
        for match in cites:
            sid,pno,lo,hi=match.groups();num,lo,hi=int(pno),int(lo),int(hi)
            s=src.get(sid)
            valid=bool(s and 1<=num<=len(s['pages']) and 1<=lo<=hi<=len(s['pages'][num-1]['lines']))
            ck(f'{p.name} 引用位置 {sid} p{num} L{lo}–L{hi}',valid,'只驗證位置存在，不代表語義支持')
    draftrefs=0
    for p,meta,text in drafts:
        ck(f'{p.name} 草稿分類有效', meta.get('category') in CATS, meta.get('category',''), 'DRAFT')
        matches=list(CITE.finditer(text));draftrefs+=len(matches)
        ck(f'{p.name} 草稿有引用',bool(matches),'來源註記為原創摘記的定位，不是原網頁全文行號','DRAFT')
        for match in matches:
            sid, pno, lo, hi=match.groups(); num,lo,hi=int(pno),int(lo),int(hi)
            srcitem=src.get(sid)
            valid=bool(srcitem and 1<=num<=len(srcitem['pages']) and 1<=lo<=hi<=len(srcitem['pages'][num-1]['lines']))
            ck(f'{p.name} 草稿引用 {sid} p{num} L{lo}–L{hi}', valid, '摘記位置存在，不等於原文逐字核對','DRAFT')
    ck('未核准草稿狀態一致',len(drafts)==0 or draftrefs>0, f'未核准文章 {len(drafts)} 篇','STRUCTURE')
    # Knowledge link validation is structural, not semantic approval.
    relation_doc=read_json(ROOT/'wiki'/'relations.json',{'relations':[]})
    slugs={p.stem for p,_,_ in approved+drafts}
    ck('六大領域已有可查詢 Wiki 文章',set(CATS).issubset({m.get('category') for _,m,_ in approved+drafts}),'涵蓋六大領域','STRUCTURE')
    for j,rel in enumerate(relation_doc.get('relations',[]),1):
        ck(f'關聯 {j} 兩端文章存在',rel.get('from') in slugs and rel.get('to') in slugs and rel.get('from')!=rel.get('to'),'不可引用不存在的文章')
        ck(f'關聯 {j} 至少一個來源 ID 且都已登錄',bool(rel.get('source_ids')) and all(x in src for x in rel.get('source_ids',[])),'不代表連結語義獲得核准')
    ck('六大領域皆有 approved 文章',set(CATS).issubset({m.get('category') for _,m,_ in approved}),f'目前涵蓋 {len({m.get("category") for _,m,_ in approved})} 類','BLOCKER')
    ck('approved 文章 ≥6 篇',len(approved)>=6, f'{len(approved)} 篇','BLOCKER')
    ck('經核准文章總引文 >0',total_cites>0,f'{total_cites} 處','BLOCKER')
    for f in ['AGENTS.md','wiki/index.md','wiki/log.md','docs/requirements-v1.0.md','.agents/workflows/ingest.md','.agents/workflows/topic-slides.md','.agents/workflows/lint.md','index.html','wiki.html','graph.html','deck.html','workflow.html','assets/site.css','assets/site.js','assets/deck.css']:
        ck(f'{f} 存在',(ROOT/f).is_file())
    for html in ['index.html','wiki.html','graph.html','deck.html','workflow.html']:
        path=ROOT/html
        if not path.exists():continue
        h=Links();h.feed(path.read_text(encoding='utf-8'))
        for link in h.links:
            if link.startswith(('https://','http://','#','mailto:')):continue
            if not link or link.startswith(('javascript:','data:')):
                ck(f'{html} 安全連結',False,link);continue
            loc=link.split('#',1)[0].split('?',1)[0]
            if not loc:continue
            target=(ROOT/loc).resolve()
            ck(f'{html} 連結：{loc}',target.is_relative_to(ROOT.resolve()) and target.is_file())
    site=read_json(ROOT/'data/site.json',{})
    count=int(site.get('slide_count',0))
    ck('HTML 簡報 8–15 頁',8<=count<=15,f'{count} 頁','STRUCTURE')
    ck('正式簡報已核准',8<=count<=15 and not site.get('preview_mode',True) and bool(site.get('six_categories_ready')), '需人工核准 + 六領域完整','BLOCKER')
    ck('實際已核准文章計數正確',site.get('approved_count',-1)==len(approved))
    ck('文章預覽計數與來源一致',site.get('preview_article_count',-1)==len(approved)+len(drafts))
    ck('Wiki 的來源數據與 ingest 一致',site.get('source_count',-1)==len(sources))
    ck('簡報內容由六領域資料支撐',bool(site.get('six_categories_ready')),'需通過六類核准及 5 篇來源','BLOCKER')
    review=ROOT/'docs/manual-review.md'
    rv=review.read_text(encoding='utf-8') if review.is_file() else ''
    ck('使用者人工核准紀錄已登錄','審查結論：已通過' in rv and '審查結論：**未審查' not in rv,'使用者確認後登錄；不代表獨立 AI 原文逐句審查','BLOCKER')
    passed=sum(1 for _,_,ok,_ in checks if ok);total=len(checks);success=passed==total
    report=['# BTC Trading Wiki | 靜態品質檢查', '',f'- 執行日期：{datetime.now().isoformat(timespec="seconds")}',f'- 整體狀態：**{"PASS / 靜態關卡通過" if success else "INCOMPLETE / 尚未全部通過"}**',f'- 總計：**{passed}/{total}** 項通過。','', '| 類型 | 驗證項目 | 結果 | 補充 |','|---|---|---|---|']
    for cat,name,ok,detail in checks:
        report.append(f'| {cat} | {name.replace("|","/")} | {"PASS" if ok else "FAIL"} | {detail.replace("|","/")} |')
    report+=['','> 本腳本只驗證**自撰來源筆記的檔案、行號、SHA-256 與結構**，並非網頁原文全文的位置校驗。即使 PASS 仍需由獨立 AI / 人工檢查原文是否真的支持論點，以及真實瀏覽器版面。','', '## 未完成項目', '']
    failed=[(cat,name) for cat,name,ok,_ in checks if not ok]
    report+=['- '+cat+'：'+name for cat,name in failed] if failed else ['- 無靜態驗證失敗；請確認人工及瀏覽器檢查紀錄。']
    (ROOT/'reports').mkdir(exist_ok=True)
    (ROOT/'reports/latest.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    for cat,name in failed: print('FAIL',cat, name)
    print('CHECK',passed,'/',total, 'PASS' if success else 'INCOMPLETE')
    return 0 if success else 1

if __name__=='__main__':sys.exit(run())
