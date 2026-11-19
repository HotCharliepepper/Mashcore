// Project names and roles remain the readable fallback. Keep the logo's space
// when its optional image is unavailable; do not invent a replacement mark.
for (const image of document.querySelectorAll('#field-projects .field-project-logo img')) {
  const frame = image.closest('.field-project-logo');
  const failed = () => { frame.style.visibility = 'hidden'; };
  const loaded = () => { frame.style.removeProperty('visibility'); };
  image.addEventListener('error', failed);
  image.addEventListener('load', loaded);
  if (image.complete && !image.naturalWidth) failed();
}
