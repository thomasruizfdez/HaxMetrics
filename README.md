# HaxMetrics

HaxMetrics es una herramienta para analizar replays de Haxball en formato .hbr2 y extraer métricas útiles para el análisis de partidos.

## Formato de archivo .hbr2

El formato de archivo .hbr2 es el formato utilizado por Haxball para almacenar las replays de los partidos. A continuación se detalla la estructura de estos archivos:

### Estructura Básica

1. **Encabezado**:

   - Identificador: `'HBR2'` (4 bytes) - Magic bytes que identifican el tipo de archivo
   - Versión: `uint32` (4 bytes) - Actualmente la versión es 3

2. **Datos Comprimidos**:
   - El resto del archivo está comprimido utilizando zlib
   - Método de descompresión en Python:
   ```python
   decompressed_data = zlib.decompress(compressed_data, wbits=-15)
   ```

Estructura de Datos Descomprimidos

Basado en el análisis realizado, los datos descomprimidos tienen la siguiente estructura:

    Cabecera de la Sala (primeros bytes):
        Estado (2 bytes): Valor 0x0000 para salas estándar, 0x0003 para salas con información adicional
        Nombre de la Sala:
            Longitud del nombre (1 byte): Indica la cantidad de bytes que ocupa el nombre
            Nombre (N bytes): El nombre de la sala como texto, donde N es la longitud especificada

    Configuración de la Sala:
        Estado de Equipos (1 byte): Indica si los equipos están bloqueados
        Límite de Goles (4 bytes): Número máximo de goles para finalizar el partido
        Límite de Tiempo (4 bytes): Tiempo máximo de juego en segundos
        Campo Desconocido (4 bytes): Función no identificada

    Información del Stadium (Mapa):
        Tipo de Stadium (1 byte): Si es 0xFF, indica que es un stadium personalizado
        Para stadiums personalizados:
            Longitud del nombre del stadium (1 byte)
            Nombre del stadium (N bytes)
        Campo de Configuración (4 bytes): Generalmente con valor 1, propósito exacto desconocido
        Datos del Stadium: Coordenadas, dimensiones y propiedades del mapa (formato en análisis)

constructor() {
this.jc = - 1;
this.T = this.ic = null;
this.Gd = 2; // Kick timeout
this.gd = 0; // Kick rate limit
this.me = 1; // Kick rate limit burst
this.kb = this.Ga = 3; // Score limit, Time limit
this.Ac = !1; // Teams are locked
this.M = null; // Game
this.K = []; // Players
this.lc = ''; // Room name
this.T = q.Vh() [0]; // Stadium
this.mb = [ null, new wa, new wa ]; // Team colors
this.mb[1].hb.push(u.ia.S); // Red team color
this.mb[2].hb.push(u.Da


ga(a) {
a.Eb(this.lc); // Room name
a.m(this.Ac ? 1 : 0); // Teams locked
a.R(this.kb); // Score limit
a.R(this.Ga); // Time limit
a.oj(this.me); // Kick rate limit burst
a.m(this.gd); // Kick rate limit
a.m(this.Gd); // Kick timeout
this.T.ga(a); // Stadium
a.m(null != this.M ? 1 : 0); // Game active
null != this.M && this.M.ga(a); // Game state
a.m(this.K.length); // Player count
for (let b = 0; b < this.K.length; ) this.K[b++].wa(a); // Players
this.mb[1].ga(a); // Red team colors
this.mb[2].ga(a); // Blue team colors
}

ma(a) {
this.lc = a.Ab(); // Room name
this.Ac = 0 != a.F(); // Teams locked
this.kb = a.N(); // Score limit
this.Ga = a.N(); // Time limit
this.me = a.Di(); // Kick rate limit burst
this.gd = a.F(); // Kick rate limit
this.Gd = a.F(); // Kick timeout
this.T = q.ma(a); // Stadium

// Game state
var b = 0 != a.F();
this.M = null;
b && (this.M = new Y, this.M.ma(a, this));

// Players
let c = a.F();
for (var d = this.K; d.length > c; ) d.pop();
for (d = 0; d < c; ) {
let e = new ya;
e.xa(a, b ? this.M.va.H : null);
this.K[d++] = e;
}

// Team colors
this.mb[1].ma(a);
this.mb[2].ma(a);
}

constructor() {
this.L = []; // Vertices
this.X = []; // Segments
this.sa = []; // Planes
this.vc = []; // Goals
this.H = []; // Discs
this.qb = []; // Joints
this.Md = []; // Red spawn points
this.vd = []; // Blue spawn points
this.Kd = new cc; // Player physics
this.Nh = 255; // BG color
this.Ue = this.mf = 0; // View width properties
this.$f = !0; // Can be stored
this.Df = !1; // Full reset after goal
}

// Dimensiones y propiedades del campo
this.D = ''; // Nombre del estadio
this.ud = 0; // Tipo de fondo (0=ninguno, 1=grass, 2=hockey)
this.be = 0; // Ancho del campo
this.ae = 0; // Alto del campo
this.bd = 0; // Radio del kick-off
this.Gc = 0; // Radio de las esquinas
this.Te = 0; // Línea de gol (sólo hockey)
this.td = 0; // Color de fondo
this.bc = 0; // Ancho máximo
this.sc = 0; // Alto máximo
this.mc = 0; // Distancia de spawn

ga(a) {
a.m(this.Nh); // BG color
if (!this.cf()) { // Si no es un estadio predeterminado
a.Eb(this.D); // Nombre
a.R(this.ud); // Tipo de fondo
a.u(this.be); // Ancho
a.u(this.ae); // Alto
a.u(this.bd); // Radio kick-off
a.u(this.Gc); // Radio esquinas
a.u(this.Te); // Línea de gol
a.R(this.td); // Color de fondo
a.u(this.bc); // Ancho máximo
a.u(this.sc); // Alto máximo
a.u(this.mc); // Distancia de spawn
this.Kd.ga(a); // Physics del jugador
a.Xb(this.mf); // Max view width
a.m(this.Ue); // Camera follow
a.m(this.$f ? 1 : 0); // Can be stored
a.m(this.Df ? 1 : 0); // Full reset after goal

    // Vertices
    a.m(this.L.length);
    for (var b = 0; b < this.L.length; ) {
      var c = b++; let e = this.L[c];
      e.Dd = c; e.ga(a);
    }

    // Segments
    a.m(this.X.length);
    b = 0;
    for (c = this.X; b < c.length; ) c[b++].ga(a);

    // Planes
    a.m(this.sa.length);
    b = 0;
    for (c = this.sa; b < c.length; ) c[b++].ga(a);

    // Goals
    a.m(this.vc.length);
    b = 0;
    for (c = this.vc; b < c.length; ) c[b++].ga(a);

    // Discs
    a.m(this.H.length);
    b = 0;
    for (c = this.H; b < c.length; ) c[b++].ga(a);

    // Joints
    a.m(this.qb.length);
    b = 0;
    for (c = this.qb; b < c.length; ) c[b++].ga(a);

    // Spawn points
    a.m(this.Md.length);
    b = 0;
    for (c = this.Md; b < c.length; ) {
      d = c[b]; ++b;
      a.u(d.x); a.u(d.y);
    }

    a.m(this.vd.length);
    b = 0;
    for (c = this.vd; b < c.length; ) {
      d = c[b]; ++b;
      a.u(d.x); a.u(d.y);
    }

}
}

ws(a) {
this.D = a.Ab(); // Nombre
this.ud = a.N(); // Tipo de fondo
this.be = a.w(); // Ancho
this.ae = a.w(); // Alto
this.bd = a.w(); // Radio kick-off
this.Gc = a.w(); // Radio esquinas
this.Te = a.w(); // Línea de gol
this.td = a.N(); // Color de fondo
this.bc = a.w(); // Ancho máximo
this.sc = a.w(); // Alto máximo
this.mc = a.w(); // Distancia de spawn
this.Kd.ma(a); // Physics del jugador
this.mf = a.Sb(); // Max view width
this.Ue = a.F(); // Camera follow
this.$f = 0 != a.F(); // Can be stored
this.Df = 0 != a.F(); // Full reset after goal

// Vertices
this.L = [];
for (var c = a.F(), d = 0; d < c; ) {
var e = new G;
e.ma(a);
e.Dd = d++;
this.L.push(e);
}

// Segments
this.X = [];
c = a.F();
for (d = 0; d < c; ) {
++d;
e = new I;
e.ma(a, this.L);
this.X.push(e);
}

// Planes
this.sa = [];
c = a.F();
for (d = 0; d < c; ) {
++d;
e = new R;
e.ma(a);
this.sa.push(e);
}

// Goals
this.vc = [];
c = a.F();
for (d = 0; d < c; ) {
++d;
e = new Kb;
e.ma(a);
this.vc.push(e);
}

// Discs
this.H = [];
c = a.F();
for (d = 0; d < c; ) {
++d;
e = new Aa;
e.ma(a);
this.H.push(e);
}

// Joints
this.qb = [];
c = a.F();
for (d = 0; d < c; ) {
++d;
e = new ob;
e.ma(a);
this.qb.push(e);
}

// Spawn points
this.Md = b(); // Lee los puntos de spawn rojos
this.vd = b(); // Lee los puntos de spawn azules
}

class G {
constructor() {
this.Dd = 0; // Índice
this.B = 32; // Collision mask
this.i = 63; // Collision groups
this.o = 1; // Bounce coefficient
this.a = new P(0, 0); // Posición
}
}

class I {
constructor() {
this.Sg = this.Tg = this.ya = null;
this.tk = 0;
this.ea = this.$ = this.fe = null;
this.Hc = 0;
this.o = 1;
this.i = 63;
this.B = 32;
this.vb = 1 / 0;
this.bb = !0;
this.S = 0;
}
}

class R {
constructor() {
this.B = 32;
this.i = 63;
this.o = 1;
this.Va = 0;
this.ya = new P(0, 0); // Normal
}
}

class Kb {
constructor() {
this.Ae = u.Oa; // Equipo
this.ea = new P(0, 0); // Punto final
this.$ = new P(0, 0); // Punto inicial
}
}

class Aa {
constructor() {
this.i = this.B = 63;
this.S = 16777215; // Color
this.Ea = 0.99; // Damping
this.ca = 1; // Inverse mass
this.o = 0.5; // Bounce coefficient
this.V = 10; // Radio
this.ra = new P(0, 0); // Gravedad
this.G = new P(0, 0); // Velocidad
this.a = new P(0, 0); // Posición
}
}

class ob {
constructor() {
this.S = 0; // Color
this.ye = 1 / 0; // Fuerza
this.Ib = this.fc = 100; // Longitud
this.ge = this.he = 0; // Discos conectados
}
}

class cc {
constructor() {
this.ff = 0; // Kickback
this.V = 15; // Radio
this.B = 0; // Collision mask
this.ra = new P(0, 0); // Gravedad
this.ca = this.o = 0.5; // Masa y rebote
this.Ea = 0.96; // Damping
this.Qe = 0.1; // Aceleración
this.gf = 0.07; // Kick acceleration
this.hf = 0.96; // Kick damping
this.ef = 5; // Kick strength
}
}

ss() {
// Verificar si el estadio puede ser almacenado
if (!this.$f) throw v.C(0);

let a = {}; // Objeto JSON resultante

// Guardar vértices
let c = [];
for (let d = 0; d < this.L.length; ) {
let f = this.L[d];
++d;
f.Dd = b++;
c.push(q.Es(f));
}

// Guardar segmentos
let b = [];
for (let e = 0; e < this.X.length; ) {
b.push(q.Pr(this.X[e++], d));
}

// Guardar planos
d = [];
for (let f = 0; f < this.sa.length; ) {
d.push(q.Pq(this.sa[f++]));
}

// Guardar porterías
e = [];
for (let g = 0; g < this.vc.length; ) {
e.push(q.pp(this.vc[g++]));
}

// Guardar física del jugador
f = q.Sq(this.Kd);

// Guardar discos
g = [];
for (let h = 0; h < this.H.length; ) {
g.push(q.So(this.H[h++], h));
}

// Guardar uniones
h = [];
for (let k = 0; k < this.qb.length; ) {
h.push(q.Hp(this.qb[k++]));
}

// Guardar puntos de spawn
k = [];
for (let l = 0; l < this.Md.length; ) {
let r = this.Md[l];
++l;
k.push([r.x, r.y]);
}

l = [];
for (let n = 0; n < this.vd.length; ) {
let t = this.vd[n];
++n;
l.push([t.x, t.y]);
}

// Estructura principal del JSON
c = {
name: this.D,
width: this.bc,
height: this.sc,
bg: a,
vertexes: c,
segments: b,
planes: d,
goals: e,
discs: g,
playerPhysics: f,
ballPhysics: 'disc0'
};

// Propiedades opcionales
q.pa(c, 'maxViewWidth', this.mf, 0);
q.pa(c, 'cameraFollow', 1 == this.Ue ? 'player' : '', '');
q.pa(c, 'spawnDistance', this.mc, 200);
0 != h.length && (c.joints = h);
0 != k.length && (c.redSpawnPoints = k);
0 != l.length && (c.blueSpawnPoints = l);
q.pa(c, 'kickOffReset', this.Df ? 'full' : 'partial', 'partial');

// Propiedades del fondo
switch (this.ud) {
case 1:
b = 'grass';
break;
case 2:
b = 'hockey';
break;
default:
b = 'none'
}
q.pa(a, 'type', b, 'none');
q.pa(a, 'width', this.be, 0);
q.pa(a, 'height', this.ae, 0);
q.pa(a, 'kickOffRadius', this.bd, 0);
q.pa(a, 'cornerRadius', this.Gc, 0);
q.Eg(a, this.td, 7441498);
q.pa(a, 'goalLine', this.Te, 0);

return c;
}
