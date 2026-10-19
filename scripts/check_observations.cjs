/* Verify the new visitor tasks using the real HTML and event handlers. Not a layout engine. */
const {parseHTML}=require('linkedom');
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const checks=[];
for(const route of ['index.html','mobile/index.html']){
  const source=fs.readFileSync(path.join(root,route),'utf8');
  const {document,Event}=parseHTML(source);
  const win={matchMedia:()=>({matches:false,addEventListener(){}}),addEventListener(){},innerHeight:844,scrollY:0};
  const context={document,window:win,requestAnimationFrame:()=>1,navigator:{},console};
  const run=name=>vm.runInNewContext(fs.readFileSync(path.join(root,'assets/js',name),'utf8'),context);
  const click=el=>el.dispatchEvent(new Event('click',{bubbles:true,cancelable:true}));
  const key=(el,value)=>{const event=new Event('keydown',{bubbles:true,cancelable:true});event.key=value;el.dispatchEvent(event)};
  const panels=Array.from(document.querySelectorAll('[data-layout-study]'));
  // The same questions and approved business identity remain available without JS.
  assert.equal(panels.length,3);
  assert.ok(panels.every(panel=>!panel.hidden));
  assert.ok(document.querySelector('[data-observation-tabs]').hidden);
  assert.ok(Array.from(document.querySelectorAll('[data-layout-controls]')).every(x=>x.hidden));
  assert.equal(document.querySelector('[data-business-info] dd').textContent,'247-02-04104');
  assert.equal(document.querySelector('[data-business-info]').hidden,false);
  assert.ok(document.querySelectorAll('details summary').length>=2);
  checks.push(route+': no-JS reading, native disclosure markup, business number visible');

  run('site-config.js');run('site.js');run('observations.js');
  const tabs=Array.from(document.querySelectorAll('[data-observation-tabs] [role="tab"]'));
  assert.equal(tabs.length,3);
  assert.equal(panels.filter(panel=>!panel.hidden).length,1);
  assert.equal(document.querySelector('[data-observation-tabs]').hidden,false);
  const questionTexts=new Set();
  for(let i=0;i<tabs.length;i++){
    click(tabs[i]);
    const panel=panels[i],surface=panel.querySelector('[data-layout-surface]');
    assert.equal(panel.hidden,false);
    assert.equal(panels.filter(x=>!x.hidden).length,1);
    assert.equal(tabs.filter(x=>x.getAttribute('aria-selected')==='true').length,1);
    questionTexts.add(panel.querySelector('h3').textContent);
    const originalNodes=Array.from(surface.children);
    const originalOrder=originalNodes.map(node=>node.dataset.layoutBlock).join(',');
    const originalContent=originalNodes.map(node=>node.textContent).sort();
    const disclosure=surface.querySelector('details');
    if(disclosure)disclosure.setAttribute('open','');
    click(panel.querySelector('[data-layout-choice="b"]'));
    assert.equal(surface.dataset.layout,'b');
    assert.notEqual(Array.from(surface.children).map(node=>node.dataset.layoutBlock).join(','),originalOrder);
    assert.deepEqual(Array.from(surface.children).map(node=>node.textContent).sort(),originalContent);
    assert.ok(originalNodes.every(node=>node.parentNode===surface));
    if(disclosure)assert.ok(disclosure.hasAttribute('open'));
    assert.match(panel.querySelector('[data-layout-status]').textContent,/배치 B/);
    assert.equal(panel.querySelectorAll('[data-layout-choice][aria-pressed="true"]').length,1);
    if(panel.dataset.layoutStudy==='hand')assert.equal(surface.lastElementChild.dataset.layoutBlock,'action');
    if(panel.dataset.layoutStudy==='reading')assert.equal(surface.querySelector('[data-layout-block="price"]').nextElementSibling.dataset.layoutBlock,'included');
    if(panel.dataset.layoutStudy==='decision')assert.equal(surface.querySelector('[data-layout-block="conditions"]').nextElementSibling.dataset.layoutBlock,'action');
    click(panel.querySelector('[data-layout-choice="a"]'));
    assert.equal(Array.from(surface.children).map(node=>node.dataset.layoutBlock).join(','),originalOrder);
  }
  assert.equal(questionTexts.size,3);
  key(tabs[2],'Home');assert.equal(tabs[0].getAttribute('aria-selected'),'true');
  key(tabs[0],'ArrowRight');assert.equal(tabs[1].getAttribute('aria-selected'),'true');
  key(tabs[1],'End');assert.equal(tabs[2].getAttribute('aria-selected'),'true');
  assert.equal(document.querySelectorAll('[data-chapter]').length,4);
  assert.ok(document.querySelector('a[href="/work/weplace/"]'));
  assert.ok(document.querySelector('a[href="/research/chore-to-play/"]'));
  assert.equal(document.querySelector('[data-business-info]').children.length,1);
  checks.push(route+': three distinct questions, keyboard selection, reversible A/B order, unchanged content and disclosure state, portfolio/research paths');
}
const home=fs.readFileSync(path.join(root,'index.html'),'utf8');
const expectedMobile=home.replace('class="landing-page"','class="landing-page mobile-edition"').replace('<title>Mashcore —','<title>Mashcore 모바일 —');
assert.equal(fs.readFileSync(path.join(root,'mobile/index.html'),'utf8'),expectedMobile);
checks.push('Desktop and explicit mobile content synchronized exactly');
console.log(JSON.stringify({status:'passed',environment:'Node DOM simulation; browser layout and physical device checks not performed',checks},null,2));
