/* Runtime state tests in a minimal DOM/event harness. Not a rendered browser test.
   Run from the repository: node scripts/check_review_interactions.cjs
   Uses generated dist runtime scripts; the generated DOM is checked by check_public.py.
   MASHCORE_TEST_ROOT may select a different generated-output directory. */
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.resolve(process.env.MASHCORE_TEST_ROOT || path.resolve(__dirname, '..', 'dist'));
const checks = [];
const tick = () => new Promise(resolve => setImmediate(resolve));
class Element {
  constructor(id = '') {
    this.id = id; this.attrs = {}; this.dataset = {}; this.children = [];
    this.listeners = {}; this.queries = {}; this.textContent = ''; this.hidden = false;
    this.value = ''; this.style = {}; this.focused = false;
    const classes = new Set();
    this.classList = { add: key => classes.add(key), remove: key => classes.delete(key), contains: key => classes.has(key), toggle: (key, force) => { const on = force ?? !classes.has(key); if (on) classes.add(key); else classes.delete(key); return on; } };
  }
  setAttribute(k, v) { this.attrs[k] = String(v); }
  getAttribute(k) { return this.attrs[k] ?? null; }
  removeAttribute(k) { delete this.attrs[k]; }
  hasAttribute(k) { return k in this.attrs; }
  querySelectorAll(k) { return this.queries[k] || []; }
  querySelector(k) { return this.querySelectorAll(k)[0] || null; }
  append(...nodes) { for (const node of nodes) { if (node.parentNode) node.parentNode.children = node.parentNode.children.filter(x => x !== node); this.children.push(node); node.parentNode = this; } }
  addEventListener(k, fn) { (this.listeners[k] ||= []).push(fn); }
  fire(type, details = {}) { const event = { target: this, type, prevented: false, preventDefault() { this.prevented = true; }, ...details }; for (const fn of this.listeners[type] || []) fn(event); return event; }
  focus() { this.focused = true; }
  select() { this.selected = true; }
  closest() { return null; }
}
function environment() {
  const document = new Element(); document.documentElement = new Element(); document.body = new Element();
  const ids = {}; document.getElementById = id => ids[id] || null; document.createElement = () => new Element();
  const window = { matchMedia: () => ({ matches: false, addEventListener() {} }), addEventListener() {}, innerHeight: 800, scrollY: 0, isSecureContext: true, MASHCORE_BUSINESS: { email: 'weplacehyun@naver.com', registrationNumber: '247-02-04104' } };
  const clipboard = [];
  const navigator = { clipboard: { writeText: async text => { clipboard.push(text); } } };
  const context = { document, window, navigator, requestAnimationFrame: () => 1, console };
  const run = file => vm.runInNewContext(fs.readFileSync(path.join(root, 'assets/js', file), 'utf8'), context, { filename: file });
  return { document, ids, window, navigator, clipboard, run };
}
function inquiry() {
  const env = environment();
  for (const id of ['question', 'question-count', 'question-error', 'copy-status', 'email-question', 'copy-question', 'select-question']) env.ids[id] = new Element(id);
  env.ids.question.setAttribute('maxlength', '1000');
  env.run('site.js'); return env;
}
function observations(malformed = false) {
  const env = environment(), lab = new Element(), tabs = new Element(); tabs.hidden = true;
  env.document.queries['[data-observation-lab]'] = [lab];
  lab.queries['[data-observation-tabs]'] = [tabs];
  const keys = { hand: ['action', 'intro', 'context'], reading: ['intro', 'price', 'context', 'included'], decision: ['intro', 'action', 'conditions'] };
  const panels = [], choices = [], fallbacks = [];
  for (const [name, blocks] of Object.entries(keys)) {
    const panel = new Element('study-' + name), surface = new Element(), controls = new Element(), status = new Element();
    panel.dataset.layoutStudy = name; controls.hidden = true;
    panel.queries['[data-layout-surface]'] = [surface]; panel.queries['[data-layout-controls]'] = [controls]; panel.queries['[data-layout-status]'] = [status];
    for (const key of blocks) { const el = new Element(); el.dataset.layoutBlock = key; el.textContent = name + ':' + key; el.open = true; surface.append(el); }
    if (malformed && name === 'hand') surface.children.pop();
    controls.queries['[data-layout-choice]'] = ['a', 'b'].map(layout => { const el = new Element(); el.dataset.layoutChoice = layout; return el; });
    const choice = new Element('tab-' + name); choice.setAttribute('aria-controls', panel.id); choice.setAttribute('aria-selected', 'false'); choice.setAttribute('role', 'tab');
    choices.push(choice); panels.push(panel); fallbacks.push(new Element());
  }
  tabs.queries['button[aria-controls]'] = choices; lab.queries['[data-layout-study]'] = panels; lab.queries['[data-layout-fallback]'] = fallbacks;
  return { ...env, lab, tabs, choices, panels, fallbacks };
}
async function main() {
  const e = inquiry(), q = e.ids.question, mail = e.ids['email-question'], copy = e.ids['copy-question'], status = e.ids['copy-status'];
  assert.equal(q.hasAttribute('maxlength'), false);
  assert.equal(new URL(mail.href).pathname, 'weplacehyun@naver.com');
  assert.equal(new URL(mail.href).searchParams.get('subject'), '[Mashcore] 함께할 일 문의');
  assert.equal(new URL(mail.href).searchParams.has('body'), false);
  copy.fire('click'); assert.match(status.textContent, /복사할 내용을 먼저/); assert.equal(e.clipboard.length, 0);
  checks.push('Empty inquiry: recipient and subject only; empty copy gives guidance without success');
  q.value = '  한글 줄바꿈\n& # % 👋  '; q.fire('input');
  assert.equal(new URL(mail.href).searchParams.get('body'), q.value);
  assert.match(e.ids['question-count'].textContent, new RegExp('^' + Array.from(q.value).length));
  const mailEvent = mail.fire('click'); assert.equal(mailEvent.prevented, false); assert.match(status.textContent, /직접 보내주세요/);
  copy.fire('click'); await tick(); assert.equal(e.clipboard.at(-1), q.value); assert.match(status.textContent, /아직 전송되지 않았습니다/);
  checks.push('Exact unicode, whitespace, newline, ampersand, hash and percent survive URI and clipboard');
  q.value = '😀'.repeat(1000); q.fire('input'); assert.equal(q.getAttribute('aria-invalid'), 'false'); assert.equal(mail.getAttribute('aria-disabled'), 'false');
  q.value += '한'; q.fire('input'); const longValue = q.value;
  assert.equal(q.getAttribute('aria-invalid'), 'true'); assert.equal(mail.getAttribute('aria-disabled'), 'true');
  const attempts = e.clipboard.length; copy.fire('click'); assert.equal(e.clipboard.length, attempts); assert.equal(mail.fire('click').prevented, true); assert.equal(q.value, longValue); assert.match(e.ids['question-error'].textContent, /입력란에 남아/);
  e.ids['select-question'].fire('click'); assert.equal(q.selected, true); assert.equal(q.value, longValue);
  checks.push('1000 code points accepted; 1001 blocks scripted actions, retains original and manual selection');
  q.value = 'ㅎ'; q.fire('compositionstart'); q.fire('input'); assert.equal(q.value, 'ㅎ'); assert.equal(mail.fire('click').prevented, true);
  q.value = '한글'; q.fire('compositionend'); assert.equal(q.value, '한글'); assert.equal(mail.fire('click').prevented, false);
  checks.push('Korean composition is never rewritten; actions wait until composition ends');
  e.navigator.clipboard.writeText = async () => { throw new Error('denied'); }; copy.fire('click'); await tick();
  assert.match(status.textContent, /자동 복사가 되지 않았습니다/); assert.doesNotMatch(status.textContent, /^질문을 복사했습니다/); assert.equal(q.selected, true);
  e.window.isSecureContext = false; copy.fire('click'); assert.match(status.textContent, /직접 복사/);
  checks.push('Rejected or unavailable clipboard never shows success; selection and manual guidance remain');
  const nav = environment(), menu = new Element('main-nav'), trigger = new Element(), link = new Element();
  nav.ids['main-nav'] = menu; nav.document.queries['.menu-btn'] = [trigger]; menu.queries.a = [link]; nav.run('site.js');
  trigger.fire('click'); assert.equal(trigger.getAttribute('aria-expanded'), 'true'); nav.document.fire('keydown', { key: 'Escape' }); assert.equal(trigger.getAttribute('aria-expanded'), 'false'); assert.equal(trigger.focused, true);
  trigger.focused = false; trigger.fire('click'); link.fire('click'); assert.equal(trigger.getAttribute('aria-expanded'), 'false'); assert.equal(trigger.focused, true);
  checks.push('Menu Escape and link close return focus to the menu trigger');
  const biz = environment(), existing = new Element(), first = new Element(), empty = new Element(); existing.append(first); biz.document.queries['[data-business-info]'] = [existing, empty]; biz.run('site.js'); assert.equal(existing.children[0], first); assert.equal(existing.children.length, 1); assert.equal(empty.children.length, 2); assert.equal(empty.children[1].children[1].children[0].getAttribute('href'), 'mailto:weplacehyun@naver.com');
  checks.push('Pre-rendered business footer survives runtime; only empty fallback is filled');
  const obs = observations(); obs.run('observations.js'); assert.equal(obs.tabs.hidden, false); assert.equal(obs.panels.filter(p => !p.hidden).length, 1); assert.ok(obs.fallbacks.every(f => f.hidden));
  for (let i = 0; i < obs.panels.length; i++) {
    const panel = obs.panels[i], surface = panel.querySelector('[data-layout-surface]'), controls = panel.querySelector('[data-layout-controls]'), original = [...surface.children];
    obs.choices[i].fire('click'); assert.equal(panel.hidden, false); assert.equal(obs.choices[i].getAttribute('aria-pressed'), 'true');
    controls.querySelectorAll('[data-layout-choice]')[1].fire('click'); assert.equal(surface.dataset.layout, 'b'); assert.notDeepEqual(surface.children, original); assert.ok(original.every(node => surface.children.includes(node) && node.open));
    controls.querySelectorAll('[data-layout-choice]')[0].fire('click'); assert.deepEqual(surface.children, original);
  }
  obs.choices[2].fire('keydown', { key: 'Home' }); assert.equal(obs.choices[0].getAttribute('aria-pressed'), 'true'); obs.choices[0].fire('keydown', { key: 'ArrowRight' }); assert.equal(obs.choices[1].getAttribute('aria-pressed'), 'true'); assert.equal(obs.choices[1].focused, true);
  checks.push('Three perspectives and reversible A/B use the same nodes and disclosure state; keyboard and pressed state work');
  const bad = observations(true); bad.run('observations.js'); assert.equal(bad.tabs.hidden, true); assert.ok(bad.panels.every(p => !p.hidden)); assert.ok(bad.fallbacks.every(f => !f.hidden));
  checks.push('Incomplete A/B initialization keeps static content and comparison alternatives visible');
  console.log(JSON.stringify({ status: 'passed', testedRoot: root, environment: 'Node VM with minimal DOM/event harness using generated dist scripts; no browser layout, device, mail app or SMTP execution', checks }, null, 2));
}
main().catch(error => { console.error(error); process.exitCode = 1; });
