import { createServer } from 'node:http';
import { createReadStream, statSync, existsSync } from 'node:fs';
import { resolve, extname, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
const root = resolve(process.env.R35_ROOT || fileURLToPath(new URL('../../', import.meta.url)));
const types = { '.html':'text/html; charset=utf-8', '.css':'text/css; charset=utf-8', '.js':'text/javascript; charset=utf-8', '.woff2':'font/woff2', '.webp':'image/webp', '.png':'image/png', '.jpg':'image/jpeg', '.mp4':'video/mp4', '.txt':'text/plain; charset=utf-8', '.xml':'application/xml' };
const server = createServer((req,res) => {
  try {
    let path = decodeURIComponent(new URL(req.url,'http://localhost').pathname);
    if (path.startsWith('/sense-r35/') && existsSync(resolve(root,'experiments/sense-r35'))) path = '/experiments/sense-r35/' + path.slice('/sense-r35/'.length);
    if (path.split('/').some(part => part.startsWith('.'))) { res.writeHead(403); return res.end(); }
    let file = resolve(root, '.' + path);
    if (file !== root && !file.startsWith(root + sep)) { res.writeHead(403); return res.end(); }
    if (statSync(file).isDirectory()) file = resolve(file,'index.html');
    const size = statSync(file).size;
    const headers = { 'Content-Type':types[extname(file)] || 'application/octet-stream', 'Cache-Control':'no-store', 'Accept-Ranges':'bytes' };
    const range = req.headers.range?.match(/^bytes=(\d+)-(\d*)$/);
    if (range) {
      const start = Number(range[1]), end = Math.min(range[2] ? Number(range[2]) : size - 1, size - 1);
      if (start >= size || start > end) { res.writeHead(416, {'Content-Range':`bytes */${size}`}); return res.end(); }
      res.writeHead(206, {...headers,'Content-Length':end-start+1,'Content-Range':`bytes ${start}-${end}/${size}`});
      if(req.method === 'HEAD')return res.end();
      createReadStream(file,{start,end}).pipe(res);
    } else {
      res.writeHead(200,{...headers,'Content-Length':size});
      if(req.method === 'HEAD')return res.end();
      createReadStream(file).pipe(res);
    }
  } catch { res.writeHead(404); res.end('Not found'); }
});
const port=Number(process.env.PORT || 8350);
server.listen(port,'127.0.0.1',() => console.log(`Local preview: http://127.0.0.1:${port}/`));
