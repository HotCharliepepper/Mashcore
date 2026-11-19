/* Adapted from the supplied WHY Resonance proof. The existing gold SVG remains
   the only signature; this bounded 2D layer is decorative and has no input UI. */
const TAU = Math.PI * 2;
const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
const rectData = ({ x, y, width, height }) => ({ x, y, width, height });
const seedRandom = (seed) => () => {
  let n = seed += 0x6D2B79F5;
  n = Math.imul(n ^ n >>> 15, n | 1);
  n ^= n + Math.imul(n ^ n >>> 7, n | 61);
  return ((n ^ n >>> 14) >>> 0) / 4294967296;
};

export function mountWhyResonance({ container, anchor, mode = 'subtle', questionMarks = true, exclusions = [], bpm = 71.4 } = {}) {
  const rhythmBpm = [71.4,80,84,88].includes(Number(bpm)) ? Number(bpm) : 71.4;
  const beatMs = 60000 / rhythmBpm;
  // Keep the reviewed four-beat travel independent of the quieter layer count.
  // 84 * .85 = 71.4 BPM: each journey now takes exactly 1 / .85 as long.
  const waveLifeMs = beatMs * 4;
  let setting = mode === 'dimensional' ? 'dimensional' : 'subtle';
  let showQuestions = !!questionMarks, manuallyPaused = false, externallyReduced = false, alive = true;
  let unavailable = !container?.getBoundingClientRect || !anchor?.getBoundingClientRect ? 'missing-anchor' : '';
  const doc = container?.ownerDocument || globalThis.document;
  const win = doc?.defaultView;
  const canvas = doc?.createElement('canvas');
  let ctx = null;
  try { ctx = canvas?.getContext('2d', { alpha: true }); } catch { /* Static SVG remains. */ }
  if (!ctx || !win) unavailable ||= 'canvas-unavailable';
  if (unavailable) return {
    setMode(value) { setting = value === 'dimensional' ? 'dimensional' : 'subtle'; },
    setQuestions(value) { showQuestions = !!value; },
    setPaused(value) { manuallyPaused = !!value; },
    setReduced(value) { externallyReduced = !!value; },
    getState() { return { ready: false, available: false, failure: unavailable, reason: unavailable, mode: setting, questions: showQuestions, paused: manuallyPaused, externalReduced: externallyReduced, destroyed: !alive, raf: 0, frameCount: 0 }; },
    destroy() { alive = false; canvas?.remove(); }
  };

  const media = (query) => win.matchMedia?.(query) || { matches: false };
  const reduced = media('(prefers-reduced-motion: reduce)');
  const coarse = media('(pointer: coarse)');
  const previousAttribute = container.getAttribute('data-why-resonance');
  const previousPosition = container.style.position;
  const positioned = win.getComputedStyle(container).position === 'static';
  if (positioned) container.style.position = 'relative';
  container.setAttribute('data-why-resonance', 'mounted');
  canvas.className = 'mashcore-why-resonance';
  canvas.setAttribute('aria-hidden', 'true');
  canvas.setAttribute('role', 'presentation');
  container.prepend(canvas);

  let width = 0, height = 0, left = 0, top = 0, dpr = 1, cx = 0, cy = 0;
  let minRadius = 28, maxRadius = 130, ellipseRatio = .46, surroundY = 0, mobile = false, visible = false;
  let raf = 0, lastTick = 0, lastDrawElapsed = -Infinity, elapsed = 0, scrollTimer = 0;
  let frameCount = 0, geometryCount = 0, lastDrawMs = 0, totalDrawMs = 0, maxDrawMs = 0;
  let anchorRect = null, hostRect = null, protectedEllipse = null, masks = [], marks = [];
  let ringCache = null, shadeCache = null, maskCache = null, renderedQuestions = 0;
  let serif = 'serif', sans = 'sans-serif';
  let resizeObserver = null, intersectionObserver = null;
  const cleanups = [];
  const listen = (node, event, fn, options) => { node.addEventListener(event, fn, options); cleanups.push(() => node.removeEventListener(event, fn, options)); };
  const listenMedia = (query, fn) => {
    if (query.addEventListener) listen(query, 'change', fn);
    else if (query.addListener) { query.addListener(fn); cleanups.push(() => query.removeListener(fn)); }
  };
  const isReduced = () => reduced.matches || externallyReduced;
  const pausedReasons = () => [!visible && 'offscreen', doc.hidden && 'hidden', reduced.matches && 'reduced-motion', externallyReduced && 'site-reduced-motion', manuallyPaused && 'manual', !alive && 'destroyed'].filter(Boolean);
  const canRun = () => alive && width > 0 && height > 0 && pausedReasons().length === 0;
  const waveCount = () => mobile || isReduced() ? 2 : 3;
  const questionLimit = () => mobile ? (setting === 'subtle' ? 5 : 8) : (setting === 'subtle' ? 10 : 16);
  const intersects = (a, b) => a.x < b.x + b.width && a.x + a.width > b.x && a.y < b.y + b.height && a.y + a.height > b.y;
  const layer = (w, h) => {
    const node = doc.createElement('canvas'); node.width = Math.ceil(w * dpr); node.height = Math.ceil(h * dpr);
    const context = node.getContext('2d', { alpha: true });
    context?.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { node, context, width: w, height: h };
  };
  function makeCaches() {
    const radius = maxRadius, pad = 20, w = radius * 2 + pad * 2, h = radius * ellipseRatio * 2 + pad * 2;
    ringCache = layer(w, h);
    const c = ringCache.context;
    if (c) {
      const ring = (offsetY, start = 0, end = TAU) => {
        c.beginPath();
        const steps = Math.ceil((end - start) * 24);
        for (let i = 0; i <= steps; i++) {
          const a = start + (end - start) * i / steps;
          const r = radius * (1 + .008 * Math.sin(a * 3 + .8) + .005 * Math.sin(a * 5));
          const x = w / 2 + Math.cos(a) * r, y = h / 2 + Math.sin(a) * r * ellipseRatio + offsetY;
          if (i) c.lineTo(x, y); else c.moveTo(x, y);
        }
      };
      ring(2.2); c.strokeStyle = 'rgba(27,57,44,.15)'; c.lineWidth = 5;
      c.shadowColor = 'rgba(15,40,29,.24)'; c.shadowBlur = 8 * dpr; c.shadowOffsetY = 2 * dpr; c.stroke();
      c.shadowBlur = 0; c.shadowOffsetY = 0;
      ring(-1.2, Math.PI * 1.08, Math.PI * 1.95); c.strokeStyle = 'rgba(137,169,148,.28)'; c.lineWidth = 1.25; c.stroke();
      ring(1.5, Math.PI * .04, Math.PI * .93); c.strokeStyle = 'rgba(29,59,45,.19)'; c.lineWidth = 1.05; c.stroke();
    }
    shadeCache = layer(width, height);
    const shade = shadeCache.context;
    if (shade) {
      const gradient = shade.createRadialGradient(cx, surroundY, 0, cx, surroundY, maxRadius * .98);
      gradient.addColorStop(0, 'rgba(30,62,46,0)');
      gradient.addColorStop(.13, 'rgba(30,62,46,.016)');
      gradient.addColorStop(.32, 'rgba(30,62,46,.055)');
      gradient.addColorStop(.62, 'rgba(54,82,61,.032)');
      gradient.addColorStop(1, 'rgba(54,82,61,0)');
      shade.save(); shade.translate(cx, surroundY); shade.scale(1, ellipseRatio); shade.translate(-cx, -surroundY);
      shade.fillStyle = gradient; shade.fillRect(0, 0, width, height / ellipseRatio); shade.restore();
    }
    // Fade before the protected copy, so the wave never meets a hard text box.
    // This alpha mask is cached on geometry changes; no per-frame blur is used.
    maskCache = layer(width, height);
    const maskContext = maskCache.context, feather = mobile ? 10 : 14;
    if (maskContext) for (const mask of masks) {
      const { x, y, width: w, height: h } = mask;
      if (x + w + feather < 0 || y + h + feather < 0 || x - feather > width || y - feather > height) continue;
      maskContext.fillStyle = '#000'; maskContext.fillRect(x, y, w, h);
      const band = (x1, y1, x2, y2, bx, by, bw, bh) => {
        const gradient = maskContext.createLinearGradient(x1, y1, x2, y2);
        gradient.addColorStop(0, 'rgba(0,0,0,1)');
        gradient.addColorStop(.25, 'rgba(0,0,0,.84)');
        gradient.addColorStop(.75, 'rgba(0,0,0,.16)');
        gradient.addColorStop(1, 'rgba(0,0,0,0)');
        maskContext.fillStyle = gradient; maskContext.fillRect(bx, by, bw, bh);
      };
      band(x, y, x, y - feather, x, y - feather, w, feather);
      band(x, y + h, x, y + h + feather, x, y + h, w, feather);
      band(x, y, x - feather, y, x - feather, y, feather, h);
      band(x + w, y, x + w + feather, y, x + w, y, feather, h);
      for (const [px, py, dx, dy] of [[x, y, -1, -1], [x + w, y, 1, -1], [x, y + h, -1, 1], [x + w, y + h, 1, 1]]) {
        const gradient = maskContext.createRadialGradient(px, py, 0, px, py, feather);
        gradient.addColorStop(0, 'rgba(0,0,0,1)');
        gradient.addColorStop(.25, 'rgba(0,0,0,.84)');
        gradient.addColorStop(.75, 'rgba(0,0,0,.16)');
        gradient.addColorStop(1, 'rgba(0,0,0,0)');
        maskContext.fillStyle = gradient;
        maskContext.fillRect(px + (dx < 0 ? -feather : 0), py + (dy < 0 ? -feather : 0), feather, feather);
      }
    }
  }
  function makeMarks() {
    marks = [];
    const random = seedRandom(940311), target = questionLimit();
    for (let attempts = 0; marks.length < target && attempts < 240; attempts++) {
      const x = cx + (random() * 2 - 1) * maxRadius * 1.05;
      const y = surroundY + (random() * 2 - 1) * maxRadius * ellipseRatio;
      const size = (mobile ? 10.5 : 12) + random() * (mobile ? 4.5 : 8);
      const box = { x: x - size * .6 - 3, y: y - size * .65 - 3, width: size * 1.2 + 6, height: size * 1.3 + 6 };
      const distance = ((x - cx) / maxRadius) ** 2 + ((y - surroundY) / (maxRadius * ellipseRatio)) ** 2;
      if (distance < .12 || distance > 1.04 || box.x < 8 || box.y < 8 || box.x + box.width > width - 8 || box.y + box.height > height - 8) continue;
      if (masks.some(mask => intersects(box, mask)) || marks.some(mark => Math.hypot(x - mark.x, y - mark.y) < (mobile ? 25 : 33))) continue;
      marks.push({ x, y, size, opacity: .065 + random() * .07, phase: random() * TAU, rotation: (random() - .5) * .36, serif: random() > .25 });
    }
  }
  function geometry() {
    if (!alive) return;
    const host = container.getBoundingClientRect(), glyph = anchor.getBoundingClientRect();
    const brand = container.querySelector(':scope > .final-brand')?.getBoundingClientRect();
    hostRect = rectData(host); anchorRect = rectData(glyph); geometryCount++;
    mobile = win.innerWidth <= 650 || coarse.matches;
    dpr = Math.min(win.devicePixelRatio || 1, mobile ? 1.5 : 2);
    width = Math.max(1, Math.min(1440, container.clientWidth || host.width));
    height = Math.max(1, Math.min(620, container.clientHeight || host.height));
    const glyphX = glyph.left - host.left + glyph.width / 2, glyphY = glyph.top - host.top + glyph.height / 2;
    left = clamp(glyphX - width / 2, 0, Math.max(0, host.width - width));
    top = clamp(glyphY - height / 2, 0, Math.max(0, host.height - height));
    cx = glyphX - left; cy = glyphY - top;
    ellipseRatio = mobile ? .46 : clamp(240 / width, .26, .38);
    maxRadius = Math.max(24, Math.min((brand?.width || width * .86) * .57 + 16, cx - 12, width - cx - 12, (height / 2 - 12) / ellipseRatio));
    // The wave starts at the real gold y, then opens around the existing mark.
    // Both centers and the entire ellipse remain inside this same bounded canvas.
    const brandY = brand ? brand.top - host.top - top + brand.height / 2 : cy;
    surroundY = clamp(brandY, maxRadius * ellipseRatio + 12, height - maxRadius * ellipseRatio - 12);
    minRadius = Math.min(maxRadius * .46, Math.max(mobile ? 28 : 34, glyph.height * 1.12));
    protectedEllipse = { x: cx, y: cy, rx: glyph.width / 2 + 7, ry: glyph.height / 2 + 7 };
    masks = exclusions.filter(node => node?.getBoundingClientRect).map(node => {
      const box = node.getBoundingClientRect();
      return { x: box.left - host.left - left - 8, y: box.top - host.top - top - 7, width: box.width + 16, height: box.height + 14 };
    });
    canvas.width = Math.round(width * dpr); canvas.height = Math.round(height * dpr);
    Object.assign(canvas.style, { width: `${width}px`, height: `${height}px`, left: `${left}px`, top: `${top}px` });
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const style = win.getComputedStyle(container);
    serif = style.getPropertyValue('--font-editorial').trim() || style.getPropertyValue('--font-serif').trim() || 'serif';
    sans = style.getPropertyValue('--font-sans').trim() || 'sans-serif';
    visible = host.left + left < win.innerWidth && host.left + left + width > 0 && host.top + top < win.innerHeight && host.top + top + height > 0;
    makeCaches(); makeMarks(); draw(); sync();
  }
  function draw() {
    if (!alive || !width || !height) return;
    const start = win.performance.now(), t = elapsed / 1000, strength = setting === 'subtle' ? .7 : 1.12;
    ctx.clearRect(0, 0, width, height);
    ctx.save();
    ctx.beginPath(); ctx.rect(0, 0, width, height);
    ctx.ellipse(cx, cy, protectedEllipse.rx, protectedEllipse.ry, 0, 0, TAU, true);
    ctx.clip('evenodd');
    if (shadeCache?.context) { ctx.globalAlpha = strength * (isReduced() ? .65 : 1); ctx.drawImage(shadeCache.node, 0, 0, width, height); }
    if (ringCache?.context) for (let i = 0; i < waveCount(); i++) {
      const phase = isReduced() ? .48 + i * .36 : (elapsed / waveLifeMs + i / waveCount()) % 1;
      const radius = minRadius + (maxRadius - minRadius) * phase;
      const fade = Math.min(1, phase / .12) * (1 - phase) ** .85;
      const scale = radius / maxRadius;
      const w = ringCache.width * scale, h = ringCache.height * scale;
      const waveY = cy + (surroundY - cy) * phase ** .65;
      ctx.globalAlpha = fade * strength * (isReduced() ? .52 : 1);
      ctx.drawImage(ringCache.node, cx - w / 2, waveY - h / 2, w, h);
    }
    renderedQuestions = 0;
    if (showQuestions) {
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = 'rgb(37,69,53)';
      for (const mark of marks) {
        if (isReduced() && renderedQuestions >= (mobile ? 2 : 3)) break;
        ctx.save();
        ctx.globalAlpha = mark.opacity * strength * (isReduced() ? .6 : .86 + .14 * Math.sin(t * .42 + mark.phase));
        ctx.translate(mark.x, mark.y); ctx.rotate(mark.rotation);
        ctx.font = `${mark.serif ? 'italic ' : ''}${mark.size}px ${mark.serif ? serif : sans}`;
        ctx.fillText('?', 0, 0); ctx.restore(); renderedQuestions++;
      }
    }
    ctx.restore();
    if (maskCache?.context) {
      ctx.save(); ctx.globalCompositeOperation = 'destination-out';
      ctx.drawImage(maskCache.node, 0, 0, width, height); ctx.restore();
    }
    // Exclusions protect complete copy/CTA rectangles, not only their text ink.
    for (const mask of masks) ctx.clearRect(mask.x, mask.y, mask.width, mask.height);
    lastDrawMs = win.performance.now() - start; maxDrawMs = Math.max(maxDrawMs, lastDrawMs); totalDrawMs += lastDrawMs; frameCount++;
  }
  function stop() { if (raf) win.cancelAnimationFrame(raf); raf = 0; lastTick = 0; }
  function tick(now) {
    raf = 0;
    if (!canRun()) { lastTick = 0; return; }
    if (lastTick) elapsed += Math.max(0, now - lastTick);
    lastTick = now;
    if (elapsed - lastDrawElapsed >= 1000 / (mobile ? 24 : 30)) { draw(); lastDrawElapsed = elapsed; }
    raf = win.requestAnimationFrame(tick);
  }
  function sync() {
    if (!canRun()) stop();
    else if (!raf) { lastTick = 0; raf = win.requestAnimationFrame(tick); }
  }
  function visibilityCheck() {
    scrollTimer = 0;
    if (!alive) return;
    const box = canvas.getBoundingClientRect();
    visible = box.bottom > 0 && box.top < win.innerHeight && box.right > 0 && box.left < win.innerWidth;
    sync();
  }
  listen(doc, 'visibilitychange', sync);
  listen(win, 'resize', geometry, { passive: true });
  listenMedia(reduced, () => { stop(); draw(); sync(); });
  listenMedia(coarse, geometry);
  if (win.ResizeObserver) {
    resizeObserver = new win.ResizeObserver(geometry);
    resizeObserver.observe(container); resizeObserver.observe(anchor);
    exclusions.forEach(node => { if (node?.nodeType === 1) resizeObserver.observe(node); });
  }
  if (win.IntersectionObserver) {
    intersectionObserver = new win.IntersectionObserver(entries => { visible = entries.some(entry => entry.isIntersecting); sync(); }, { threshold: 0 });
    intersectionObserver.observe(canvas);
  } else listen(win, 'scroll', () => { if (!scrollTimer) scrollTimer = win.setTimeout(visibilityCheck, 60); }, { passive: true });
  geometry();
  doc.fonts?.ready?.then(() => { if (alive) geometry(); });

  return {
    setMode(value) {
      const next = value === 'dimensional' ? 'dimensional' : 'subtle';
      if (!alive || setting === next) return;
      setting = next; makeMarks(); draw();
    },
    setQuestions(value) {
      const next = !!value;
      if (!alive || showQuestions === next) return;
      showQuestions = next; draw();
    },
    setPaused(value) {
      const next = !!value;
      if (!alive || manuallyPaused === next) return;
      manuallyPaused = next; sync(); draw();
    },
    setReduced(value) {
      const next = !!value;
      // Hero refreshes its ARIA state during rendering, even if it is unchanged.
      // Repeated policy input must not restart time or render an offscreen layer.
      if (!alive || externallyReduced === next) return;
      externallyReduced = next; stop(); draw(); sync();
    },
    getState() {
      return {
        ready: alive, available: true, failure: null, destroyed: !alive, mode: setting, questions: showQuestions, paused: manuallyPaused,
        reducedMotion: isReduced(), nativeReducedMotion: reduced.matches, externalReduced: externallyReduced, visible, hidden: doc.hidden, pausedReasons: pausedReasons(), raf,
        bpm: rhythmBpm, baselineBpm: 84, speedRatio: rhythmBpm / 84, beatMs, waveLifeMs, beatIndex: Math.floor(elapsed / beatMs), elapsedMs: elapsed, frameCount, geometryCount, targetFps: mobile ? 24 : 30, mobile, dpr,
        canvas: { left, top, width, height, pixelWidth: canvas.width, pixelHeight: canvas.height },
        anchor: anchorRect ? { ...anchorRect } : null, container: hostRect ? { ...hostRect } : null,
        center: { x: cx, y: cy, containerX: cx + left, containerY: cy + top },
        protectedCenter: protectedEllipse ? { ...protectedEllipse } : null,
        exclusions: masks.map(mask => ({ ...mask })), minRadius, maxRadius, ellipseRatio, surroundCenter: { x: cx, y: surroundY }, waves: waveCount(),
        questionLimit: questionLimit(), questionsPlaced: marks.length, questionsDrawn: renderedQuestions,
        lastDrawMs, averageDrawMs: frameCount ? totalDrawMs / frameCount : 0, maxDrawMs,
        hoverPauses: false, pointerListeners: 0, geometryReadsPerFrame: 0
      };
    },
    destroy() {
      if (!alive) return;
      alive = false; stop(); if (scrollTimer) win.clearTimeout(scrollTimer);
      resizeObserver?.disconnect(); intersectionObserver?.disconnect(); cleanups.forEach(cleanup => cleanup()); canvas.remove();
      if (previousAttribute === null) container.removeAttribute('data-why-resonance'); else container.setAttribute('data-why-resonance', previousAttribute);
      if (positioned && container.style.position === 'relative') container.style.position = previousPosition;
      ringCache = null; shadeCache = null; maskCache = null;
    }
  };
}
