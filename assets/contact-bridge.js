// Optional, local-only handoff from the two fixed home-page choices.
// No free text, storage, network request, submission, or mail action.
const concernText=Object.freeze({
 discovery:'고객에게 잘 발견되지 않아요.',
 expression:'사진과 설명이 충분히 전달되지 않아요.',
 connection:'문의나 예약으로 잘 이어지지 않아요.',
 operations:'반복 업무와 운영 방식이 고민이에요.'
});
const scopeText=Object.freeze({
 channels:'검색·지도·채널부터 함께 살펴보고 싶습니다.',
 content:'사진·콘텐츠·브랜드 표현부터 함께 살펴보고 싶습니다.',
 website:'홈페이지·문의·예약 경로부터 함께 살펴보고 싶습니다.',
 workflow:'운영·AI 활용·업무 구조부터 함께 살펴보고 싶습니다.'
});

function readContext(fragment){
 if(typeof fragment!=='string'||fragment.length>120||!fragment.startsWith('#inquiry?'))return null;
 const params=new URLSearchParams(fragment.slice(9));
 const entries=[...params.entries()];
 if(entries.length!==2||params.getAll('concern').length!==1||params.getAll('scope').length!==1)return null;
 const concern=params.get('concern'),scope=params.get('scope');
 if(!Object.hasOwn(concernText,concern)||!Object.hasOwn(scopeText,scope))return null;
 return {concern,scope};
}

const context=readContext(window.location.hash);
const form=document.querySelector('[data-inquiry-form]');
if(context&&form){
 const situation=form.querySelector('textarea[name="situation"]');
 const scope=form.querySelector('textarea[name="scope"]');
 const note=form.querySelector('[data-inquiry-context-note]');
 if(situation&&scope){
  let applied=false;
  for(const [field,value] of [[situation,concernText[context.concern]],[scope,scopeText[context.scope]]]){
   // Preserve restored form values and any typing that happened before startup.
   if(field.value.trim())continue;
   field.value=value;
   field.dispatchEvent(new Event('input',{bubbles:true}));
   applied=true;
  }
  if(note&&applied)note.hidden=false;
  // The enums have served their purpose. Keep a useful plain page anchor.
  window.history.replaceState(window.history.state,'',window.location.pathname+window.location.search+'#inquiry');
  form.scrollIntoView({block:'start',behavior:'instant'});
 }
}
