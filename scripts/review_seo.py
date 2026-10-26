"""Page metadata from a reviewed content map. No GBP or search account writes."""
import json
import re
from html import escape


def apply_seo(text, rel, root, business):
    pages=json.loads((root/'content/seo.json').read_text())['pages']
    route='/' if rel=='index.html' else '/'+rel.removesuffix('index.html')
    if route not in pages: return text
    p=pages[route]; base=business['siteUrl'].rstrip('/')
    canonical=base+p.get('canonical',route)
    text=re.sub(r'<title>.*?</title>','<title>'+escape(p['title'])+'</title>',text,flags=re.S)
    text=re.sub(r'<meta\b(?=[^>]*(?:name=[\'\"]description[\'\"]|property=[\'\"]og:[^\'\"]+[\'\"]|name=[\'\"]twitter:[^\'\"]+[\'\"]))[^>]*>','',text,flags=re.I)
    text=re.sub(r'<link\b(?=[^>]*rel=[\'\"]canonical[\'\"])[^>]*>','',text,flags=re.I)
    text=re.sub(r'<script\b[^>]*type=[\'\"]application/ld\+json[\'\"][^>]*>.*?</script>','',text,flags=re.S)
    head='<meta name="description" content="'+escape(p['description'],quote=True)+'"><link rel="canonical" href="'+canonical+'">'
    meta={'og:type':'website','og:locale':'ko_KR','og:site_name':'Mashcore','og:title':p['title'],'og:description':p['description'],'og:url':canonical,'og:image':base+'/assets/media/mashcore-og.png','og:image:width':'1200','og:image:height':'630','og:image:alt':'Mashcore — 전략·브랜드·디지털 설계'}
    head+=''.join('<meta property="'+k+'" content="'+escape(v,quote=True)+'">' for k,v in meta.items())
    head+='<meta name="twitter:card" content="summary_large_image">'
    webpage={'@context':'https://schema.org','@type':'WebPage','@id':canonical+'#page','name':p['title'],'description':p['description'],'url':canonical,'inLanguage':'ko','publisher':{'@id':base+'/#organization'}}
    schemas=[webpage]
    if route in ('/','/about/'):
        schemas.append({'@context':'https://schema.org','@type':'Organization','@id':base+'/#organization','name':business['companyName'],'url':base+'/','email':business['email'],'description':'사업의 방향, 브랜드의 말, 홈페이지와 상담의 흐름을 설계합니다.','address':{'@type':'PostalAddress','streetAddress':business['address'],'addressCountry':'KR'}})
    head+=''.join('<script type="application/ld+json">'+json.dumps(s,ensure_ascii=False).replace('<','\\u003c')+'</script>' for s in schemas)
    return text.replace('</head>',head+'</head>',1)
