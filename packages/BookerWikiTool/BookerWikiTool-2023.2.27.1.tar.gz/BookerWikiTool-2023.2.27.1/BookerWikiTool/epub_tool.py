from io import BytesIO
import zipfile
from os import path
from imgyaso import pngquant_bts
import sys
from EpubCrawler.util import is_pic, safe_mkdir, safe_rmdir
import subprocess as subp
from pyquery import PyQuery as pq
import re

def convert_to_epub(fname):
    nfname = re.sub(r'\.\w+$', '', fname) + '.epub'
    print(f'{fname} => {nfname}')
    subp.Popen(f'ebook-convert "{fname}" "{nfname}"', 
        shell=True, stdin=subp.PIPE, stdout=subp.PIPE).communicate()
    if not path.exists(nfname):
        raise FileNotFoundError(f'{nfname} not found')
    return nfname

def comp_epub(args):
    fname = args.file
    if fname.endswith('.mobi') or \
        fname.endswith('.azw3'):
            fname = convert_to_epub(fname)
    elif not fname.endswith('.epub'):
        print('请提供EPUB')
        return
        
    bio = BytesIO(open(fname, 'rb').read())
    zip = zipfile.ZipFile(bio, 'r', zipfile.ZIP_DEFLATED)
    new_bio = BytesIO()
    new_zip = zipfile.ZipFile(new_bio, 'w', zipfile.ZIP_DEFLATED)
    
    for n in zip.namelist():
        print(n)
        data = zip.read(n)
        if is_pic(n):
            data = pngquant_bts(data)
        new_zip.writestr(n, data)
        
    zip.close()
    new_zip.close()
    open(fname, 'wb').write(new_bio.getvalue())
    print('done...')
        
        
def get_opf_flist(cont_opf):
    cont_opf = re.sub(r'<\?xml[^>]*\?>', '', cont_opf)
    cont_opf = re.sub(r'xmlns=".+?"', '', cont_opf)
    rt = pq(cont_opf)
    el_refs = rt('itemref')
    ids = [
        el_refs.eq(i).attr('idref') 
        for i in range(len(el_refs))
    ]
    el_its = rt('item')
    id_map = {
        pq(el).attr('id'):
        pq(el).attr('href')
        for el in el_its
    }
    return [
        id_map[id]
        for id in ids
        if id in id_map
    ]

def get_toc_lv(el_nav):
    cnt = 0
    while el_nav and el_nav.is_('nav'):
        cnt += 1
        el_nav = el_nav.parent()
    return cnt

def get_ncx_toc(toc_ncx, rgx="", hlv=0):
    toc_ncx = re.sub(r'<\?xml[^>]*\?>', '', toc_ncx)
    toc_ncx = re.sub(r'(?<=<)ncx:', '', toc_ncx)
    toc_ncx = re.sub(r'(?<=</)ncx:', '', toc_ncx)
    toc_ncx = re.sub(r'xmlns=".+?"', '', toc_ncx)
    toc_ncx = re.sub(r'<(/?)navLabel', r'<\1label', toc_ncx)
    toc_ncx = re.sub(r'<(/?)navPoint', r'<\1nav', toc_ncx)
    toc_ncx = re.sub(r'<(/?)navmap', r'<\1map', toc_ncx)
    rt = pq(toc_ncx)
    el_nps = rt('nav')
    toc = []
    for i in range(len(el_nps)):
        el = el_nps.eq(i)
        title = el.children('label>text').text()
        src = el.children('content').attr('src')
        toc.append({
            'idx': i,
            'title': title.strip(),
            'src': src,
            'level': get_toc_lv(el),
        })
    if rgx:
        toc = [
            ch for ch in toc 
            if re.search(rgx, ch['title'])
        ]
    if hlv:
        toc = [
            ch for ch in toc 
            if ch['level'] <= hlv
        ]
    return toc

def get_epub_toc(args):
    fname = args.fname
    if not fname.endswith('.epub'):
        print('请提供 EPUB 文件')
        return
        
    bio = BytesIO(open(fname, 'rb').read())
    zip = zipfile.ZipFile(bio, 'r', zipfile.ZIP_DEFLATED)
    _, ncx_fname, _ = get_toc_and_content_path(zip)
    if ncx_fname is None:
        print('未找到目录文件 toc.ncx')
        return
    toc_ncx = zip.read(ncx_fname).decode('utf8')
    toc = get_ncx_toc(toc_ncx, args.regex, args.hlevel)
    for i, ch in enumerate(toc):
        pref = '>' * (ch["level"] - 1)
        if pref: pref += ' '
        print(f'{pref}{i}-{ch["idx"]}：{ch["src"]}\n{pref}{ch["title"]}')

def get_html_body(html):
    html = re.sub(r'<\?xml[^>]*\?>', '', html)
    rt = pq(html)
    return rt('body').html() if rt('body') else html

def get_toc_and_content_path(zip):
    book_dirs = ['', 'OEBPS', 'EPUB']
    ncx_path = None
    book_dir = None
    for d in book_dirs:
        test = path.join(d, 'toc.ncx').replace('\\', '/')
        if test not in zip.namelist():
            continue
        book_dir = d
        ncx_path = test
        break;
    if ncx_path is None: return (None, None, None)
    opf_fnames = ['content.opf', 'book.opf']
    opf_path = None
    for f in opf_fnames:
        test = path.join(book_dir, f).replace('\\', '/')
        if  test not in  zip.namelist():
            continue
        opf_path = test
    if opf_path is None: return (None, None, None)
    return (book_dir, ncx_path, opf_path)
            

def exp_epub_chs(args):
    fname = args.fname
    rgx = args.regex
    hlv = args.hlevel
    st = int(args.start)
    if st == -1: st = 0
    ed = int(args.end)
    if ed == -1: ed = 2 ** 32
    dir = args.dir
    
    if not fname.endswith('.epub'):
        print('请提供 EPUB 文件')
        return

    # 获取目录和文件列表
    bio = BytesIO(open(fname, 'rb').read())
    zip = zipfile.ZipFile(bio, 'r', zipfile.ZIP_DEFLATED)
    book_dir, ncx_fname, opf_fname = get_toc_and_content_path(zip)
    if book_dir is None:
        print('未找到目录文件 toc.ncx')
        return
    toc_ncx = zip.read(ncx_fname).decode('utf8')
    cont_opf = zip.read(opf_fname).decode('utf8')
    toc = get_ncx_toc(toc_ncx, rgx, hlv)
    flist = get_opf_flist(cont_opf)
    toc_flist = {
        re.sub(r'#.+$|\?.+$', '', ch['src']) 
        for ch in toc
    }
    # 按照目录合并文件
    chs = []
    for f in flist:
        cont = zip.read(
            path.join(book_dir, f).replace('\\', '/')
        ).decode('utf8')
        cont = get_html_body(cont)
        if f in toc_flist:
            chs.append([cont])
        else:
            if chs: chs[-1].append(cont)
    chs = chs[st:ed+1]
    chs = ['\n'.join(ch) for ch in chs]
    chs = [
        f'<html><head></head><body>{ch}</body></html>' 
        for ch in chs
    ]
    l = len(str(len(chs)))
    for i, ch in enumerate(chs):
        fname = path.join(dir, str(i).zfill(l) + '.html')
        open(fname, 'w', encoding='utf8').write(ch)