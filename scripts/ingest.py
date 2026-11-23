#!/usr/bin/env python3
"""Read ONLY user-staged raw documents; preserve filename, SHA-256, PDF pages and text line positions.
This step makes source text available to a coding agent. It does NOT fabricate a wiki article.
"""
from pathlib import Path
from datetime import date
import hashlib, json, re, sys
ROOT = Path(__file__).resolve().parents[1]
RAW, OUT = ROOT/'raw', ROOT/'data'/'extracted'
ALLOWED = {'.md', '.txt', '.pdf'}

def pages_from_file(path):
    if path.suffix.lower() == '.pdf':
        try:
            from pypdf import PdfReader
        except ImportError:
            raise RuntimeError('PDF needs pypdf: pip install -r requirements.txt')
        reader = PdfReader(str(path))
        return [p.extract_text(extraction_mode='layout') or '' for p in reader.pages]
    txt = path.read_text(encoding='utf-8-sig')
    return [txt]

def import_all():
    OUT.mkdir(parents=True, exist_ok=True)
    rawfiles = sorted(p for p in RAW.rglob('*') if p.is_file() and p.suffix.lower() in ALLOWED and p.name.lower() != 'readme.md')
    entries, errors, duplicates, seen = [], [], [], {}
    manifest = ROOT/'sources'/'manifest.json'
    meta = {}
    if manifest.exists():
        try:
            data = json.loads(manifest.read_text(encoding='utf-8'))
            meta = {e['file']: e for e in data.get('sources', []) if 'file' in e}
        except (ValueError, OSError) as e:
            errors.append('manifest 格式錯誤: '+str(e))
    for path in rawfiles:
        relative = path.relative_to(RAW).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        sid = 'SRC-'+digest[:10].upper()
        if digest in seen:
            duplicates.append(f'{relative} = {seen[digest]}（完全相同，已去重）')
            continue
        seen[digest] = relative
        try:
            page_texts = pages_from_file(path)
            if not any(t.strip() for t in page_texts):
                raise RuntimeError('沒有可讀取文字；掃描 PDF 請先由使用者提供可搜尋文字版本')
            outlines, pages = [f'# {sid} 來源文字（抽取版）', f'- Raw: raw/{relative}', f'- SHA-256: {digest}', ''], []
            for i, text in enumerate(page_texts, 1):
                lines = [line.strip() for line in text.replace('\r', '').split('\n') if line.strip()]
                pages.append({'page':i, 'lines': lines})
                outlines.append(f'## p{i}'+('（PDF 原始頁碼順序）' if path.suffix.lower()=='.pdf' else '（文字文件）'))
                outlines.extend(f'[L{j}] {line}' for j,line in enumerate(lines,1))
                outlines.append('')
            (OUT/f'{sid}.md').write_text('\n'.join(outlines)+'\n',encoding='utf-8')
            info = meta.get(relative, {})
            entries.append({'id':sid,'file':relative,'title':info.get('title') or path.stem,
                'url':info.get('url',''),'published_at':info.get('published_at',''),
                'public_ok':info.get('public_ok',False), 'sha256':digest,
                'pages': pages,'extracted_file':f'data/extracted/{sid}.md'})
        except Exception as e:
            errors.append(f'{relative}: {e}')
    idx={'generated_at':date.today().isoformat(),'source_count':len(entries),'sources':entries,'errors':errors,'duplicates':duplicates}
    (ROOT/'data'/'source_index.json').write_text(json.dumps(idx,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report=['# 批次匯入紀錄','',f'- 日期：{date.today().isoformat()}',f'- 實際可讀文件：**{len(entries)}**',f'- 最低 5 篇門檻：**{"已達" if len(entries)>=5 else "未達"}**','', '| ID | 原始檔 | 頁數 | SHA-256 前12碼 |','|---|---|---:|---|']
    report += [f'| {e["id"]} | `{e["file"]}` | {len(e["pages"])} | `{e["sha256"][:12]}` |' for e in entries]
    if errors: report += ['', '## 無法匯入',''] + ['- '+err for err in errors]
    if duplicates: report += ['', '## 偵測到完全重複的文件（不計入篇數）',''] + ['- '+d for d in duplicates]
    report+=['','> 這只代表原始資料成功解析。Wiki 寫作、逐條引文核對、AI 獨立審查與人工核准**尚未自動完成**。']
    (ROOT/'docs'/'import-report.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    log = ROOT/'wiki'/'log.md'
    if log.is_file():
        with log.open('a',encoding='utf-8') as fp:
            status = '達標' if len(entries)>=5 else '未達標'
            fp.write(f'\n## [{date.today().isoformat()}] ingest | batch scan\n- 來源：{len(entries)} 篇；解析錯誤：{len(errors)}；完全重複：{len(duplicates)}；5 篇門檻：{status}。\n- 詳情：docs/import-report.md、data/source_index.json；此處不代表 AI 語義審查已執行。\n')
    print(f'匯入 {len(entries)} 篇；錯誤 {len(errors)}；{ "達" if len(entries)>=5 else "未達"} 5 篇門檻')
    for err in errors: print('ERROR',err, file=sys.stderr)
    return 1 if errors else 0

if __name__=='__main__':sys.exit(import_all())
