// Optional local-only context. No text, storage, request, submission or mail action.
const intentText=Object.freeze({
 brand:['브랜드의 첫 문장과 표현을 함께 정리하고 싶습니다.','핵심 메시지와 브랜드 표현 기준부터 함께 살펴보고 싶습니다.'],
 website:['홈페이지에서 서비스를 이해하고 문의하는 흐름을 함께 살펴보고 싶습니다.','정보 구조와 화면 설계부터 살펴보고 싶습니다. 홈페이지·코드 구현 범위는 함께 확인하겠습니다.'],
 workflow:['운영의 목적과 판단 기준, 사람과 AI가 함께 검토할 흐름을 정리하고 싶습니다.','핵심 질문, 판단 기준과 검토 흐름부터 함께 정리하고 싶습니다.'],
 unsure:['어디부터 시작할지 함께 살펴보고, 먼저 확인할 질문을 정리하고 싶습니다.','핵심 관찰, 우선 과제와 다음 확인 방법부터 함께 살펴보고 싶습니다.']
});
// Preserve already shared links from the previous two-choice version.
const concernText=Object.freeze({
 discovery:'고객에게 잘 발견되지 않아요.',expression:'사진과 설명이 충분히 전달되지 않아요.',connection:'문의나 예약으로 잘 이어지지 않아요.',operations:'반복 업무와 운영 방식이 고민이에요.'
});
const scopeText=Object.freeze({
 channels:'검색·지도·채널부터 함께 살펴보고 싶습니다.',content:'사진·콘텐츠·브랜드 표현부터 함께 살펴보고 싶습니다.',website:'홈페이지·문의·예약 경로부터 함께 살펴보고 싶습니다.',workflow:'운영·AI 활용·업무 구조부터 함께 살펴보고 싶습니다.'
});

export function readContext(fragment){
 if(typeof fragment!=='string'||fragment.length>120||!fragment.startsWith('#inquiry?'))return null;
 const params=new URLSearchParams(fragment.slice(9)),entries=[...params.entries()];
 if(entries.length===1&&params.getAll('intent').length===1){
  const intent=params.get('intent');
  return Object.hasOwn(intentText,intent)?{intent,situation:intentText[intent][0],scope:intentText[intent][1]}:null;
 }
 if(entries.length!==2||params.getAll('concern').length!==1||params.getAll('scope').length!==1)return null;
 const concern=params.get('concern'),scope=params.get('scope');
 return Object.hasOwn(concernText,concern)&&Object.hasOwn(scopeText,scope)?{concern,situation:concernText[concern],scope:scopeText[scope]}:null;
}

const context=readContext(window.location.hash);
const form=document.querySelector('[data-inquiry-form]');
if(context&&form){
 const situation=form.querySelector('textarea[name="situation"]');
 const scope=form.querySelector('textarea[name="scope"]');
 const note=form.querySelector('[data-inquiry-context-note]');
 if(situation&&scope){
  let applied=false;
  for(const [field,value] of [[situation,context.situation],[scope,context.scope]]){
   // Keep Back/Forward-restored values and typing that precedes module startup.
   if(field.value.trim())continue;
   field.value=value;
   field.dispatchEvent(new Event('input',{bubbles:true}));
   applied=true;
  }
  if(note&&applied)note.hidden=false;
  window.history.replaceState(window.history.state,'',window.location.pathname+window.location.search+'#inquiry');
  form.scrollIntoView({block:'start',behavior:'instant'});
 }
}
