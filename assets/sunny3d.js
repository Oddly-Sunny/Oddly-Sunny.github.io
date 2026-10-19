/* Sunny in 3D: the felt cloud rebuilt as an 8-lobe pillow with shell-rendered fur (Three.js, vendored).
   Mounts into any [data-sunny3d] element that already holds the flat .sn-mascot as a fallback;
   the canvas fades in only once WebGL is running. Fur sways a little and lags when Sunny turns;
   Sunny looks toward the mouse. Rendering pauses off screen and in hidden tabs. */
import * as THREE from './vendor/three.module.min.js';

const SHELLS = matchMedia('(pointer: coarse)').matches ? 30 : 48;
const FUR = 0.12;             // fur length, in units of the pillow radius
const EYES = [[-0.25, -0.07], [0.25, -0.07]];
const CHEEKS = [[-0.42, -0.25], [0.42, -0.25]];

// pillow outline: 8 rounded lobes, pinched valleys (measured from the photo: lobes at 22.5deg + k*45deg, valley depth ~15%)
const lobe = (t) => Math.pow(Math.abs(Math.cos(4 * (t - Math.PI / 8))), 0.9);
const radius = (t) => 0.87 + 0.13 * lobe(t);

function pillow() {
  const g = new THREE.SphereGeometry(1, 160, 112);
  const p = g.attributes.position, v = new THREE.Vector3();
  for (let i = 0; i < p.count; i++) {
    v.fromBufferAttribute(p, i);
    const t = Math.atan2(v.y, v.x), ring = Math.hypot(v.x, v.y);
    const r = radius(t);
    // puffy front, flatter back, soft creases running in from each valley
    const crease = 1 - 0.05 * (1 - lobe(t)) * ring;
    const depth = (v.z > 0 ? 0.5 : 0.36) * crease;
    p.setXYZ(i, v.x * r, v.y * r, v.z * depth);
  }
  g.computeVertexNormals();
  return g;
}

const vert = /* glsl */`
  uniform float uShells, uLen, uTime;
  uniform vec2 uLag;
  out vec3 vRest; out vec3 vN; out float vH; out vec3 vWorldN;
  void main() {
    float h = float(gl_InstanceID) / uShells;
    vec3 n = normalize(normal);
    // fur is combed outward from the centre of the face, like the felt in the photo
    vec3 comb = normalize(vec3(position.xy + 1e-4, 0.0));
    comb = normalize(comb - n * dot(comb, n));
    float len = uLen * (0.75 + 0.25 * smoothstep(0.2, 0.9, length(position.xy)));
    vec3 p = position + n * len * h + comb * len * 0.55 * h * h;
    // a little sway, and lag when the body turns
    float s = h * h;
    p.x += (sin(uTime * 1.3 + position.y * 4.0 + position.z * 2.0) * 0.010 - uLag.x * 0.06) * s;
    p.y += (cos(uTime * 1.1 + position.x * 3.5) * 0.008 - uLag.y * 0.06 - 0.012) * s;
    vRest = position; vH = h;
    vN = normalize(normalMatrix * n);
    gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0);
  }`;

const frag = /* glsl */`
  precision highp float;
  uniform float uDensity;
  uniform vec2 uEyes[2]; uniform vec2 uCheeks[2];
  in vec3 vRest; in vec3 vN; in float vH;
  out vec4 outColor;
  float hash(vec3 p) { p = fract(p * 0.3183099 + 0.1); p *= 17.0; return fract(p.x * p.y * p.z * (p.x + p.y + p.z)); }
  void main() {
    float h = vH;
    // strands sit on a grid across the face (the pillow is mostly flat), offset away from the origin to avoid seams
    vec2 q = vRest.xy * uDensity + vec2(311.7, 173.3);
    vec3 c = vec3(floor(q), vRest.z > 0.0 ? 1.0 : 2.0);
    vec2 f = fract(q) - 0.5;
    float rnd = hash(c + 0.37), rnd2 = hash(c * 1.31 + 17.3);
    float len = mix(0.45, 1.0, rnd);
    bool front = vRest.z > 0.0;
    // keep the eyes clear of fur
    if (front && h > 0.0) {
      for (int i = 0; i < 2; i++) if (length((vRest.xy - uEyes[i]) * vec2(1.0, 0.92)) < 0.1) discard;
    }
    if (h > 0.0) {
      if (h > len) discard;
      float w = 0.7 * (1.0 - 0.85 * h / len);
      if (length(f + (rnd2 - 0.5) * 0.3 + vec2(sin(h * 6.0 + rnd * 6.28), cos(h * 5.0 + rnd2 * 6.28)) * 0.12 * h) > w) discard;
    }
    vec3 root = vec3(0.72, 0.60, 0.46), mid = vec3(0.89, 0.81, 0.70), tip = vec3(0.99, 0.95, 0.88);
    vec3 col = mix(root, mix(mid, tip, smoothstep(0.35, 1.0, h)), smoothstep(0.0, 0.35, h));
    col *= mix(0.93, 1.05, rnd2);
    // soft valleys between the lobes
    float a = atan(vRest.y, vRest.x);
    float valley = 1.0 - pow(abs(cos(4.0 * (a - 0.3927))), 0.9);
    col *= 1.0 - 0.09 * valley * smoothstep(0.25, 0.85, length(vRest.xy)) * (1.0 - h * 0.5);
    // blush
    if (front) for (int i = 0; i < 2; i++) {
      float d = length((vRest.xy - uCheeks[i]) * vec2(1.0, 1.7));
      col = mix(col, vec3(0.93, 0.62, 0.58), 0.45 * smoothstep(0.17, 0.0, d));
    }
    vec3 L = normalize(vec3(-0.35, 0.65, 0.85));
    float dif = 0.8 + 0.3 * max(dot(vN, L), 0.0);
    float rim = pow(1.0 - max(vN.z, 0.0), 2.0) * 0.18;
    float ao = mix(0.78, 1.0, h);
    outColor = vec4(col * dif * ao + rim * tip * h, 1.0);
  }`;

function mount(el) {
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
    if (!renderer.capabilities.isWebGL2) throw new Error('webgl2');
  } catch (e) { return; }
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const canvas = renderer.domElement;
  canvas.className = 'sunny3d-canvas';
  canvas.setAttribute('aria-hidden', 'true');
  el.appendChild(canvas);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(26, 1, 0.1, 20);
  camera.position.set(0, 0, 5.4);

  const rig = new THREE.Group(); scene.add(rig);
  const geo = pillow();
  const uniforms = {
    uShells: { value: SHELLS }, uLen: { value: FUR }, uTime: { value: 0 }, uLag: { value: new THREE.Vector2() },
    uDensity: { value: 150 },
    uEyes: { value: EYES.map(([x, y]) => new THREE.Vector2(x, y)) },
    uCheeks: { value: CHEEKS.map(([x, y]) => new THREE.Vector2(x, y)) },
  };
  const furMat = new THREE.ShaderMaterial({ vertexShader: vert, fragmentShader: frag, uniforms, glslVersion: THREE.GLSL3 });
  const fur = new THREE.InstancedMesh(geo, furMat, SHELLS + 1);
  const id = new THREE.Matrix4();
  for (let i = 0; i <= SHELLS; i++) fur.setMatrixAt(i, id);
  fur.frustumCulled = false;
  rig.add(fur);

  // eyes: glossy dark ellipsoids with a catchlight, set into the face
  scene.add(new THREE.AmbientLight(0xffffff, 0.6));
  const key = new THREE.DirectionalLight(0xffffff, 2.2); key.position.set(-2, 3, 5); scene.add(key);
  const eyeMat = new THREE.MeshStandardMaterial({ color: 0x140b08, roughness: 0.18, metalness: 0.0 });
  const glint = new THREE.MeshBasicMaterial({ color: 0xffffff });
  const ray = new THREE.Raycaster(), body = new THREE.Mesh(geo);
  body.updateMatrixWorld();
  const eyes = EYES.map(([x, y]) => {
    ray.set(new THREE.Vector3(x, y, 2), new THREE.Vector3(0, 0, -1));
    const hit = ray.intersectObject(body)[0];
    const z = hit ? hit.point.z : 0.45;
    const g = new THREE.Group(); g.position.set(x, y, z + 0.015);
    const ball = new THREE.Mesh(new THREE.SphereGeometry(0.105, 40, 28), eyeMat);
    ball.scale.set(0.95, 1.08, 0.55);
    const shine = new THREE.Mesh(new THREE.SphereGeometry(0.03, 16, 12), glint);
    shine.position.set(-0.035, 0.045, 0.055);
    g.add(ball, shine); rig.add(g);
    return g;
  });

  function resize() {
    const w = el.clientWidth, h = el.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h; camera.updateProjectionMatrix();
  }
  resize();
  new ResizeObserver(resize).observe(el);

  // look toward the mouse (desktop pointer only); idle drift otherwise
  let tx = 0, ty = 0, rx = 0, ry = 0, last = { x: 0, y: 0 }, mouse = false;
  addEventListener('pointermove', (e) => {
    if (e.pointerType && e.pointerType !== 'mouse') return;
    const r = el.getBoundingClientRect();
    const dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2);
    const d = Math.hypot(dx, dy) || 1, k = Math.min(1, d / 500);
    tx = dx / d * k; ty = dy / d * k; mouse = true;
  }, { passive: true });
  document.documentElement.addEventListener('mouseleave', () => { mouse = false; });

  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let visible = true, raf = 0, t0 = performance.now(), blinkAt = 2.5;
  function frame(now) {
    raf = 0;
    const t = (now - t0) / 1000;
    const gx = mouse ? tx : Math.sin(t * 0.45) * 0.35, gy = mouse ? ty : Math.sin(t * 0.31) * 0.2;
    rx += (gx - rx) * 0.07; ry += (gy - ry) * 0.07;
    rig.rotation.y = rx * 0.42; rig.rotation.x = ry * 0.3;
    rig.position.y = Math.sin(t * 0.9) * 0.035;
    uniforms.uLag.value.set((rx - last.x) * 25, (ry - last.y) * 25);
    last.x = rx; last.y = ry;
    uniforms.uTime.value = t;
    eyes.forEach((g) => { g.children[0].position.set(rx * 0.02, -ry * 0.015, 0); });
    // blink every few seconds
    const b = t - blinkAt, s = b > 0 && b < 0.16 ? 0.12 + Math.abs(b - 0.08) / 0.08 * 0.88 : 1;
    if (b > 0.16) blinkAt = t + 3 + Math.random() * 3;
    eyes.forEach((g) => { g.scale.y = s; });
    renderer.render(scene, camera);
    if (!still && visible && !document.hidden) raf = requestAnimationFrame(frame);
  }
  const go = () => { if (!raf) raf = requestAnimationFrame(frame); };
  new IntersectionObserver((es) => { visible = es[0].isIntersecting; if (visible) go(); }, { threshold: 0 }).observe(el);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) go(); });
  renderer.render(scene, camera);
  el.classList.add('is-3d');
  go();
}

document.querySelectorAll('[data-sunny3d]').forEach(mount);
