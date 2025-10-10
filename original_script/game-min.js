/*
 HaxBall © Mario Carbajal - All rights reserved.
 8be54ed5
*/
'use strict';
(
  function (pa) {
    function ka() {
      return w.Pe(this, '')
    }
    function M(a, b) {
      if (null == b) return null;
      null == b.wh &&
      (b.wh = pa.Jj++);
      var c;
      null == a.wj ? a.wj = {}
       : c = a.wj[b.wh];
      null == c &&
      (c = b.bind(a), a.wj[b.wh] = c);
      return c
    }
    function gc(a) {
      return 66 > a ? 66 : 400 < a ? 400 : a
    }
    class Nb {
      static Kr(a, b) {
        Nb.vm(new Blob([a], {
          type: 'octet/stream'
        }), b)
      }
      static Lr(a, b) {
        Nb.vm(new Blob([a], {
          type: 'text/plain'
        }), b)
      }
      static vm(a, b) {
        let c = window.document.createElement('a');
        c.style.display = 'display: none';
        window.document.body.appendChild(c);
        a = URL.createObjectURL(a);
        c.href = a;
        c.download = b;
        c.click();
        URL.revokeObjectURL(a);
        c.remove()
      }
    }
    class hc {
      static h(a, b, c, d) {
        null != a &&
        a(b, c, d)
      }
    }
    class gb {
      constructor() {
        this.lb = null;
        this.f = x.Ia(gb.O);
        let a = x.Ba(this.f),
        b = this;
        a.get('cancel').onclick = function () {
          H.h(b.ti)
        };
        this.xi = a.get('pick');
        this.xk = a.get('delete');
        this.Lk = a.get('export');
        let c = a.get('list'),
        d = a.get('file');
        this.Xg();
        this.xi.onclick = function () {
          null != b.lb &&
          b.lb.Xd().then(function (e) {
            D.h(b.Cg, e)
          })
        };
        this.xk.onclick = function () {
          if (null != b.lb) {
            var e = b.lb.ln;
            null != e &&
            (b.lb.La.remove(), b.lb = null, e(), b.Xg())
          }
        };
        this.Lk.onclick = function () {
          null != b.lb &&
          b.lb.Xd().then(function (e) {
            Nb.Lr(e.Ce(), e.D + '.hbs')
          })
        };
        this.Ai(c);
        this.am = hb.ni(c);
        window.setTimeout(function () {
          b.am.update()
        }, 0);
        d.onchange = function () {
          var e = d.files;
          if (!(1 > e.length)) {
            e = e.item(0);
            var f = new FileReader;
            f.onload = function () {
              try {
                var g = f.result;
                let h = new q;
                h.el(g);
                D.h(b.Cg, h)
              } catch (h) {
                g = v.Mb(h).Fb(),
                g instanceof SyntaxError ? D.h(b.vi, 'SyntaxError in line: ' + Q.Je(g.lineNumber)) : g instanceof Sa ?
                D.h(b.vi, g.eq) : D.h(b.vi, 'Error loading stadium file.')
              }
            };
            f.readAsText(e)
          }
        }
      }
      Xg() {
        this.xi.disabled = null == this.lb;
        this.xk.disabled = null == this.lb ||
        null == this.lb.ln;
        this.Lk.disabled = null == this.lb
      }
      ll(a, b, c) {
        let d = window.document.createElement('div');
        d.textContent = a;
        d.className = 'elem';
        null != c &&
        d.classList.add('custom');
        let e = {
          La: d,
          Xd: b,
          ln: c
        },
        f = this;
        d.onclick = function () {
          null != f.lb &&
          f.lb.La.classList.remove('selected');
          f.lb = e;
          d.classList.add('selected');
          f.Xg()
        };
        d.ondblclick = function () {
          f.lb = e;
          f.Xg();
          return f.xi.onclick()
        };
        return d
      }
      Ai(a) {
        let b = q.Vh(),
        c = 0;
        for (; c < b.length; ) {
          let e = b[c];
          ++c;
          a.appendChild(this.ll(e.D, function () {
            return Promise.resolve(e)
          }, null))
        }
        let d = this;
        ib.getAll().then(
          function (e) {
            let f = 0;
            for (; f < e.length; ) {
              let g = e[f];
              ++f;
              let h = g.id;
              a.appendChild(
                d.ll(
                  g.name,
                  function () {
                    return ib.get(h)
                  },
                  function () {
                    return ib.delete(h)
                  }
                )
              )
            }
            d.am.update()
          }
        )
      }
    }
    class qa {
    }
    class jb {
      constructor() {
        this.Rb = - 1;
        this.gb = new T(m.j.li.v());
        this.Wc = new ic;
        this.f = x.Ia(jb.O);
        let a = x.Ba(this.f);
        this.Tb = new Ob(a.get('red-score'), 0);
        this.Ob = new Ob(a.get('blue-score'), 0);
        x.replaceWith(a.get('timer'), this.Wc.f);
        x.replaceWith(a.get('canvas'), this.gb.na)
      }
      A(a) {
        var b = m.j.li.v();
        if (this.gb.Fp != b) {
          let c = this.gb.na;
          this.gb = new T(b);
          x.replaceWith(c, this.gb.na)
        }
        b = a.M;
        null == b ? this.f.hidden = !0 : (
          this.f.hidden = !1,
          this.Wc.es(60 * a.Ga),
          this.Wc.ds(b.Nc | 0),
          this.Ob.set(b.Ob),
          this.Tb.set(b.Tb),
          this.gb.Rc(a, this.Rb)
        )
      }
    }
    class Y {
      constructor() {
        this.jc = - 1;
        this.ic = null;
        this.Tb = this.Ob = this.Nc = this.Ta = 0;
        this.ke = u.ia;
        this.yc = this.Cb = 0;
        this.va = new Ta;
        this.Ga = 0;
        this.kb = 5;
        this.T = null
      }
      Cp(a) {
        this.Ra = a;
        this.kb = a.kb;
        this.Ga = a.Ga;
        this.T = a.T;
        this.va.L = this.T.L;
        this.va.sa = this.T.sa;
        this.va.X = this.T.X;
        this.va.qb = this.T.qb;
        a = 0;
        let b = this.T.H;
        for (; a < b.length; ) this.va.H.push(b[a++].Zp());
        this.$k()
      }
      Wk(a) {
        if (a.fa == u.Oa) a.I = null;
         else {
          a.W = 0;
          var b = a.I;
          null == b &&
          (b = new ra, a.I = b, this.va.H.push(b));
          var c = this.T.Kd;
          b.S = 0;
          b.V = c.V;
          b.ca = c.ca;
          b.Ea = c.Ea;
          b.o = c.o;
          b.i = 39;
          b.B = a.fa.B | c.B;
          var d = a.fa == u.ia ? this.T.Md : this.T.vd;
          0 == d.length ? (b.a.x = a.fa.Oh * this.T.bc, b.a.y = 0) : (a = b.a, d = d[d.length - 1], a.x = d.x, a.y = d.y);
          d = b.G;
          d.x = 0;
          d.y = 0;
          b = b.ra;
          c = c.ra;
          b.x = c.x;
          b.y = c.y
        }
      }
      A(a) {
        if (0 < this.Ta) 120 > this.Ta &&
        this.Ta--;
         else {
          var b = this.Ra.zt;
          null != b &&
          b();
          b = this.Ra.K;
          for (var c = 0; c < b.length; ) {
            var d = b[c];
            ++c;
            if (null != d.I) {
              0 == (d.W & 16) &&
              (d.Yb = !1);
              var e = this.T.Kd;
              0 < d.Zc &&
              d.Zc--;
              d.Bc < this.Ra.me &&
              d.Bc++;
              if (d.Yb && 0 >= d.Zc && 0 <= d.Bc) {
                for (var f = !1, g = 0, h = this.va.H; g < h.length; ) {
                  var k = h[g];
                  ++g;
                  if (0 != (k.B & 64) && k != d.I) {
                    var l = k.a,
                    n = d.I.a,
                    r = l.x - n.x;
                    l = l.y - n.y;
                    n = Math.sqrt(r * r + l * l);
                    if (4 > n - k.V - d.I.V) {
                      f = r / n;
                      r = l / n;
                      l = e.ef;
                      var t = n = k.G;
                      k = k.ca;
                      n.x = t.x + f * l * k;
                      n.y = t.y + r * l * k;
                      t = d.I;
                      k = - e.ff;
                      n = l = t.G;
                      t = t.ca;
                      l.x = n.x + f * k * t;
                      l.y = n.y + r * k * t;
                      f = !0
                    }
                  }
                }
                f &&
                (
                  null != this.Ra.zi &&
                  this.Ra.zi(d),
                  d.Yb = !1,
                  d.Zc = this.Ra.Gd,
                  d.Bc -= this.Ra.gd
                )
              }
              f = d.W;
              h = g = 0;
              0 != (f & 1) &&
              --h;
              0 != (f & 2) &&
              ++h;
              0 != (f & 4) &&
              --g;
              0 != (f & 8) &&
              ++g;
              0 != g &&
              0 != h &&
              (f = Math.sqrt(g * g + h * h), g /= f, h /= f);
              f = d.I.G;
              k = d.Yb ? e.gf : e.Qe;
              f.x += g * k;
              f.y += h * k;
              d.I.Ea = d.Yb ? e.hf : e.Ea
            }
          }
          c = 0;
          d = this.va.H;
          e = 0;
          for (g = d.length; e < g; ) f = e++,
          h = d[f],
          0 != (h.B & 128) &&
          (Y.yk[c] = f, f = Y.ul[c], h = h.a, f.x = h.x, f.y = h.y, ++c);
          this.va.A(a);
          if (0 == this.Cb) {
            for (a = 0; a < b.length; ) c = b[a],
            ++a,
            null != c.I &&
            (c.I.i = 39 | this.ke.Jp);
            b = this.va.H[0].G;
            0 < b.x * b.x + b.y * b.y &&
            (this.Cb = 1)
          } else if (1 == this.Cb) {
            this.Nc += 0.016666666666666666;
            for (a = 0; a < b.length; ) d = b[a],
            ++a,
            null != d.I &&
            (d.I.i = 39);
            d = u.Oa;
            b = this.va.H;
            for (a = 0; a < c && (d = a++, d = this.T.ro(b[Y.yk[d]].a, Y.ul[d]), d == u.Oa); );
            d != u.Oa ? (
              this.Cb = 2,
              this.yc = 150,
              this.ke = d,
              d == u.ia ? this.Ob++ : this.Tb++,
              null != this.Ra.dj &&
              this.Ra.dj(d.Dg),
              null != this.Ra.nm &&
              this.Ra.nm(d.ba)
            ) : 0 < this.Ga &&
            this.Nc >= 60 * this.Ga &&
            this.Tb != this.Ob &&
            (null != this.Ra.fj && this.Ra.fj(), this.Sm())
          } else if (2 == this.Cb) this.yc--,
          0 >= this.yc &&
          (
            0 < this.kb &&
            (this.Tb >= this.kb || this.Ob >= this.kb) ||
            0 < this.Ga &&
            this.Nc >= 60 * this.Ga &&
            this.Tb != this.Ob ? this.Sm() : (this.$k(), null != this.Ra.Uq && this.Ra.Uq())
          );
           else if (3 == this.Cb && (this.yc--, 0 >= this.yc && (b = this.Ra, null != b.M))) {
            b.M = null;
            a = 0;
            for (c = b.K; a < c.length; ) d = c[a],
            ++a,
            d.I = null,
            d.Nb = 0;
            null != b.Kf &&
            b.Kf(null)
          }
        }
      }
      Sm() {
        this.yc = 300;
        this.Cb = 3;
        null != this.Ra.ej &&
        this.Ra.ej(this.Tb > this.Ob ? u.ia : u.Da)
      }
      $k() {
        let a = this.Ra.K;
        this.Cb = 0;
        for (var b = this.T.H, c = this.va.H, d = 0, e = this.T.Df ? b.length : 1; d < e; ) {
          var f = d++;
          b[f].Vk(c[f])
        }
        b = [
          0,
          0,
          0
        ];
        for (c = 0; c < a.length; ) if (d = a[c], ++c, this.Wk(d), e = d.fa, e != u.Oa) {
          f = d.I.a;
          var g = this.T,
          h = b[e.ba],
          k = e == u.ia ? g.Md : g.vd;
          0 == k.length ? (k = h + 1 >> 1, 0 == (h & 1) && (k = - k), g = g.mc * e.Oh, h = 55 * k) : (h >= k.length && (h = k.length - 1), h = k[h], g = h.x, h = h.y);
          f.x = g;
          f.y = h;
          b[e.ba]++;
          d.Nb = b[e.ba]
        }
      }
      ga(a) {
        this.va.ga(a);
        a.R(this.yc);
        a.R(this.Cb);
        a.R(this.Tb);
        a.R(this.Ob);
        a.u(this.Nc);
        a.R(this.Ta);
        a.m(this.ke.ba)
      }
      ma(a, b) {
        this.va.ma(a);
        this.yc = a.N();
        this.Cb = a.N();
        this.Tb = a.N();
        this.Ob = a.N();
        this.Nc = a.w();
        this.Ta = a.N();
        a = a.zf();
        this.ke = 1 == a ? u.ia : 2 == a ? u.Da : u.Oa;
        this.Ra = b;
        this.kb = b.kb;
        this.Ga = b.Ga;
        this.T = b.T;
        this.va.L = this.T.L;
        this.va.X = this.T.X;
        this.va.sa = this.T.sa;
        this.va.qb = this.T.qb
      }
      uc() {
        let a = qa.Cc,
        b = this.ic;
        this.jc != a &&
        (null == b && (this.ic = b = new Y), this.jc = a, Y.zd(b, this));
        return b
      }
      static zd(a, b) {
        a.Ra = b.Ra.uc();
        a.kb = b.kb;
        a.Ga = b.Ga;
        a.va = b.va.uc();
        a.yc = b.yc;
        a.Cb = b.Cb;
        a.Tb = b.Tb;
        a.Ob = b.Ob;
        a.Nc = b.Nc;
        a.Ta = b.Ta;
        a.T = b.T;
        a.ke = b.ke
      }
    }
    class sa {
      constructor() {
        this.fd = new Map
      }
      Pa(a, b) {
        this.fd.set(a, b)
      }
      v(a) {
        return this.fd.get(a)
      }
      sr(a) {
        this.fd.delete(a)
      }
      kp(a) {
        let b = [],
        c = this.fd.keys(),
        d = c.next();
        for (; !d.done; ) {
          let e = d.value;
          d = c.next();
          this.fd.get(e) == a &&
          b.push(e)
        }
        return b
      }
      Ce() {
        let a = {},
        b = this.fd.keys(),
        c = b.next();
        for (; !c.done; ) {
          let d = c.value;
          c = b.next();
          a[d] = this.fd.get(d)
        }
        return JSON.stringify(a)
      }
      static gg(a) {
        let b = new sa,
        c = Ac.mn(a),
        d = 0;
        for (; d < c.length; ) {
          let e = c[d];
          ++d;
          b.fd.set(e, a[e])
        }
        return b
      }
      static Th(a) {
        return sa.gg(JSON.parse(a))
      }
      static vk() {
        let a = new sa;
        a.Pa('ArrowUp', 'Up');
        a.Pa('KeyW', 'Up');
        a.Pa('ArrowDown', 'Down');
        a.Pa('KeyS', 'Down');
        a.Pa('ArrowLeft', 'Left');
        a.Pa('KeyA', 'Left');
        a.Pa('ArrowRight', 'Right');
        a.Pa('KeyD', 'Right');
        a.Pa('KeyX', 'Kick');
        a.Pa('Space', 'Kick');
        a.Pa('ControlLeft', 'Kick');
        a.Pa('ControlRight', 'Kick');
        a.Pa('ShiftLeft', 'Kick');
        a.Pa('ShiftRight', 'Kick');
        a.Pa('Numpad0', 'Kick');
        return a
      }
    }
    class Q {
      static Je(a) {
        return w.Pe(a, '')
      }
      static parseInt(a) {
        a = parseInt(a);
        return isNaN(a) ? null : a
      }
    }
    class J {
      constructor(a, b) {
        null == b &&
        (b = !1);
        this.s = a;
        this.Ua = b;
        this.a = 0
      }
      sb(a) {
        null ==
        a &&
        (a = this.s.byteLength - this.a);
        if (this.a + a > this.s.byteLength) throw v.C('Read too much');
        let b = new Uint8Array(this.s.buffer, this.s.byteOffset + this.a, a);
        this.a += a;
        return b
      }
      bm(a) {
        let b = this.sb(a);
        a = new ArrayBuffer(a);
        (new Uint8Array(a)).set(b);
        return a
      }
      zf() {
        return this.s.getInt8(this.a++)
      }
      F() {
        return this.s.getUint8(this.a++)
      }
      Di() {
        let a = this.s.getInt16(this.a, this.Ua);
        this.a += 2;
        return a
      }
      Sb() {
        let a = this.s.getUint16(this.a, this.Ua);
        this.a += 2;
        return a
      }
      N() {
        let a = this.s.getInt32(this.a, this.Ua);
        this.a += 4;
        return a
      }
      jb() {
        let a = this.s.getUint32(this.a, this.Ua);
        this.a += 4;
        return a
      }
      Ci() {
        let a = this.s.getFloat32(this.a, this.Ua);
        this.a += 4;
        return a
      }
      w() {
        let a = this.s.getFloat64(this.a, this.Ua);
        this.a += 8;
        return a
      }
      Bb() {
        let a = this.a,
        b = 0,
        c,
        d = 0;
        do c = this.s.getUint8(a + b),
        5 > b &&
        (d |= (c & 127) << 7 * b >>> 0),
        ++b;
        while (0 != (c & 128));
        this.a += b;
        return d | 0
      }
      re(a) {
        let b = this.a,
        c,
        d = '';
        for (a = b + a; b < a; ) c = J.Po(this.s, b),
        b += c.length,
        d += String.fromCodePoint(c.char);
        if (b != a) throw v.C(
          'Actual string length differs from the specified: ' + (b - a) +
          ' bytes'
        );
        this.a = b;
        return d
      }
      Ab() {
        let a = this.Bb();
        return 0 >= a ? null : this.re(a - 1)
      }
      kc() {
        return this.re(this.Bb())
      }
      dm() {
        return this.re(this.F())
      }
      Jg() {
        let a = this.kc();
        return JSON.parse(a)
      }
      static Po(a, b) {
        var c = a.getUint8(b);
        let d,
        e,
        f,
        g,
        h = b;
        if (0 == (c & 128)) ++b;
         else if (192 == (c & 224)) d = a.getUint8(b + 1),
        c = (c & 31) << 6 | d & 63,
        b += 2;
         else if (224 == (c & 240)) d = a.getUint8(b + 1),
        e = a.getUint8(b + 2),
        c = (c & 15) << 12 | (d & 63) << 6 | e & 63,
        b += 3;
         else if (240 == (c & 248)) d = a.getUint8(b + 1),
        e = a.getUint8(b + 2),
        f = a.getUint8(b + 3),
        c = (c & 7) << 18 | (d & 63) << 12 | (e & 63) << 6 | f & 63,
        b += 4;
         else if (248 == (c & 252)) d = a.getUint8(b + 1),
        e = a.getUint8(b + 2),
        f = a.getUint8(b + 3),
        g = a.getUint8(b + 4),
        c = (c & 3) << 24 | (d & 63) << 18 | (e & 63) << 12 | (f & 63) << 6 | g & 63,
        b += 5;
         else if (252 == (c & 254)) d = a.getUint8(b + 1),
        e = a.getUint8(b + 2),
        f = a.getUint8(b + 3),
        g = a.getUint8(b + 4),
        a = a.getUint8(b + 5),
        c = (c & 1) << 30 | (d & 63) << 24 | (e & 63) << 18 | (f & 63) << 12 | (g & 63) << 6 | a & 63,
        b += 6;
         else throw v.C(
          'Cannot decode UTF8 character at offset ' + b + ': charCode (' + c + ') is invalid'
        );
        return {
          char: c,
          length: b - h
        }
      }
    }
    class Bc {
      constructor(a, b) {
        this.x = a;
        this.y = b
      }
    }
    class C {
      static Ys() {
        try {
          return window.self != window.top
        } catch (a) {
          return !0
        }
      }
      static ih(a) {
        return new Promise(
          function (b, c) {
            let d = window.document.createElement('img');
            d.onload = function () {
              URL.revokeObjectURL(d.src);
              d.onload = null;
              b(d)
            };
            d.onerror = function () {
              URL.revokeObjectURL(d.src);
              c(null)
            };
            d.src = URL.createObjectURL(new Blob([a], {
              type: 'image/png'
            }))
          }
        )
      }
      static xj(a) {
        C.Ys() &&
        C.Ss(
          function () {
            Jc.xj();
            let b = null == m.j.$e.v() ? la.lp().then(function (d) {
              m.j.$e.ha(d)
            }, function () {
            }) : Promise.resolve(null),
            c = Z.v('res.dat', 'arraybuffer').then(
              function (d) {
                d = new JSZip(d);
                m.Qa = new jc(d);
                return Promise.all(
                  [m.Qa.Xo,
                  C.ih(d.file('images/grass.png').asArrayBuffer()).then(function (e) {
                    return m.qp = e
                  }),
                  C.ih(d.file('images/concrete.png').asArrayBuffer()).then(function (e) {
                    return m.Co = e
                  }),
                  C.ih(d.file('images/concrete2.png').asArrayBuffer()).then(function (e) {
                    return m.Ao = e
                  }),
                  C.ih(d.file('images/typing.png').asArrayBuffer()).then(function (e) {
                    return m.cn = e
                  })]
                )
              }
            );
            Promise.all([c,
            b]).then(function () {
              C.gt(a)
            })
          }
        )
      }
      static Ss(a) {
        let b = Modernizr,
        c = 'canvas datachannel dataview es6collections peerconnection promises websockets'.split(' '),
        d = [],
        e = 0;
        for (; e < c.length; ) {
          let f = c[e];
          ++e;
          b[f] ||
          d.push(f)
        }
        0 != d.length ? (
          window.document.body.innerHTML = '',
          C.$g = window.document.createElement('div'),
          window.document.body.appendChild(C.$g),
          a = new kb(d),
          C.Na(a.f)
        ) : a()
      }
      static gt(a) {
        window.document.body.innerHTML = '';
        C.$g = window.document.createElement('div');
        window.document.body.appendChild(C.$g);
        let b = null;
        b = function () {
          m.Qa.rm();
          window.document.removeEventListener('click', b, !0)
        };
        window.document.addEventListener('click', b, !0);
        a()
      }
      static Na(a) {
        null != C.wn &&
        C.wn.remove();
        null != a &&
        (C.$g.appendChild(a), C.wn = a)
      }
    }
    class Ua {
      constructor(a) {
        function b(g, h) {
          function k() {
            l.className = n.Le ? 'icon-ok' : 'icon-cancel'
          }
          g = c.get(g);
          let l = g.querySelector('i'),
          n = {
            Le: h
          };
          k();
          g.onclick = function () {
            n.Le = !n.Le;
            k();
            e.Dn(e.vj)
          };
          return n
        }
        this.vj = [];
        this.Vs = a;
        this.La = x.Ia(Ua.Ij);
        let c = x.Ba(this.La),
        d = new lb(c);
        this.Ej = c.get('refresh');
        this.tn = c.get('join');
        a = c.get('create');
        this.Qs = c.get('count');
        let e = this;
        a.onclick = function () {
          H.h(e.it)
        };
        c.get('changenick').onclick = function () {
          H.h(e.ht)
        };
        c.get('settings').onclick = function () {
          H.h(e.kt)
        };
        let f = c.get('replayfile');
        f.onchange = function () {
          var g = f.files;
          if (!(1 > g.length)) {
            g = g.item(0);
            var h = new FileReader;
            h.onload = function () {
              D.h(e.jt, h.result)
            };
            h.readAsArrayBuffer(g)
          }
        };
        this.Us = b('fil-full', !0);
        this.lt = b('fil-pass', !0);
        this.Ts = b('fil-empty', !0);
        this.at = c.get('listscroll');
        this.nt = hb.ni(this.at);
        this.yj = c.get('list');
        this.Ej.onclick = function () {
          d.hm();
          e.on()
        };
        this.tn.onclick = function () {
          null != e.Wd &&
          D.h(e.zn, e.Wd.rt)
        };
        this.on()
      }
      on() {
        function a() {
          d.Ej.disabled = !1;
          d.Dn(b);
          return null
        }
        this.In(null);
        this.Ej.disabled = !0;
        x.Qf(this.yj);
        let b = [];
        this.vj = [];
        let c = Pb.get().then(function (e) {
          return b = e
        }, function () {
          return null
        }),
        d = this;
        Ua.mt(c).then(a, a)
      }
      Dn(a) {
        this.vj = a;
        Pb.tt(this.Vs, a);
        a.sort(function (k, l) {
          return k.Ze - l.Ze
        });
        x.Qf(this.yj);
        let b = 0,
        c = 0,
        d = !this.Us.Le,
        e = !this.lt.Le,
        f = !this.Ts.Le,
        g = this,
        h = 0;
        for (; h < a.length; ) {
          let k = a[h];
          ++h;
          let l = k.je;
          if (d && l.K >= l.lf) continue;
          if (e && l.Jb) continue;
          if (f && 0 == l.K) continue;
          let n = new mb(k);
          n.La.ondblclick = function () {
            D.h(g.zn, k)
          };
          n.La.onclick = function () {
            g.In(n)
          };
          this.yj.appendChild(n.La);
          b += l.K;
          ++c
        }
        this.Qs.textContent = '' + b + ' players in ' + c + ' rooms';
        this.nt.update()
      }
      In(a) {
        null != this.Wd &&
        this.Wd.La.classList.remove('selected');
        this.Wd = a;
        null != this.Wd &&
        this.Wd.La.classList.add('selected');
        this.tn.disabled = null == this.Wd
      }
      static mt(a) {
        let b = new Promise(function (c, d) {
          window.setTimeout(function () {
            d(null)
          }, 5000)
        });
        return Promise.race([b,
        a])
      }
    }
    class nb {
      constructor() {
        this.f = x.Ia(nb.O);
        let a = x.Ba(this.f),
        b = this;
        a.get('cancel').onclick = function () {
          D.h(b.rb, !1)
        };
        a.get('leave').onclick = function () {
          D.h(b.rb, !0)
        }
      }
    }
    class kc {
      constructor(a) {
        let b = [],
        c = 0;
        for (; c < a; ) ++c,
        b.push(0);
        this.Og = b;
        this.Mf = this.qf = 0
      }
      Pa(a) {
        this.Mf -= this.Og[this.qf];
        this.Og[this.qf] = a;
        this.Mf += a;
        this.qf++;
        this.qf >= this.Og.length &&
        (this.qf = 0)
      }
      ao() {
        return this.Mf / this.Og.length
      }
    }
    class Qb {
      constructor(a) {
        this.et = a;
        this.cb = []
      }
      add(a) {
        var b = this.cb.length;
        let c = 0,
        d = this.Yd = 0;
        for (; d <
        b; ) {
          let e = d++,
          f = this.cb[e];
          f.index++;
          f.weight *= 0.97;
          this.cb[c].index < f.index &&
          (c = e);
          this.Yd += f.weight
        }
        b >= this.et ? (b = this.cb[c], this.Yd -= b.weight, this.cb.splice(c, 1)) : b = new lc;
        b.value = a;
        b.weight = 1;
        b.index = 0;
        this.Yd += b.weight;
        for (a = 0; a < this.cb.length && this.cb[a].value <= b.value; ) ++a;
        this.cb.splice(a, 0, b)
      }
      mh() {
        if (0 == this.cb.length) return 0;
        if (1 == this.cb.length) return this.cb[0].value;
        var a = 0.5 * this.Yd;
        let b = this.cb[0].weight,
        c = 0;
        for (; c < this.cb.length - 1 && !(b >= a); ) ++c,
        b += this.cb[c].weight;
        return this.cb[c].value
      }
      max() {
        return 0 ==
        this.cb.length ? 0 : this.cb[this.cb.length - 1].value
      }
    }
    class Cc {
      static pn() {
        try {
          let a = window.localStorage;
          a.getItem('');
          if (0 == a.length) {
            let b = '_hx_' + Math.random();
            a.setItem(b, b);
            a.removeItem(b)
          }
          return a
        } catch (a) {
          return null
        }
      }
    }
    class ic {
      constructor() {
        this.Ga = 0;
        this.Ck = this.Dk = !1;
        this.Ye = 0;
        this.f = window.document.createElement('div');
        this.f.className = 'game-timer-view';
        this.f.appendChild(this.Lq = this.ee('OVERTIME!', 'overtime'));
        this.f.appendChild(this.gq = this.ee('0', 'digit'));
        this.f.appendChild(this.fq = this.ee('0', 'digit'));
        this.f.appendChild(this.ee(':', null));
        this.f.appendChild(this.Nr = this.ee('0', 'digit'));
        this.f.appendChild(this.Mr = this.ee('0', 'digit'))
      }
      ee(a, b) {
        let c = window.document.createElement('span');
        c.textContent = a;
        c.className = b;
        return c
      }
      ds(a) {
        if (a != this.Ye) {
          let b = a % 60,
          c = a / 60 | 0;
          this.Mr.textContent = '' + b % 10;
          this.Nr.textContent = '' + (b / 10 | 0) % 10;
          this.fq.textContent = '' + c % 10;
          this.gq.textContent = '' + (c / 10 | 0) % 10;
          this.Ye = a
        }
        this.im();
        this.jm()
      }
      es(a) {
        this.Ga = a;
        this.im();
        this.jm()
      }
      im() {
        this.Zr(0 != this.Ga && this.Ye >
        this.Ga)
      }
      jm() {
        this.fs(this.Ye < this.Ga && this.Ye > this.Ga - 30)
      }
      Zr(a) {
        a != this.Ck &&
        (this.Lq.className = a ? 'overtime on' : 'overtime', this.Ck = a)
      }
      fs(a) {
        a != this.Dk &&
        (
          this.f.className = a ? 'game-timer-view time-warn' : 'game-timer-view',
          this.Dk = a
        )
      }
    }
    class ob {
      constructor() {
        this.S = 0;
        this.ye = 1 / 0;
        this.Ib = this.fc = 100;
        this.ge = this.he = 0
      }
      ga(a) {
        a.m(this.ge);
        a.m(this.he);
        a.u(this.Ib);
        a.u(this.fc);
        a.u(this.ye);
        a.R(this.S)
      }
      ma(a) {
        this.ge = a.F();
        this.he = a.F();
        this.Ib = a.w();
        this.fc = a.w();
        this.ye = a.w();
        this.S = a.N()
      }
      A(a) {
        var b = a[this.ge];
        a = a[this.he];
        if (null != b && null != a) {
          var c = b.a,
          d = a.a,
          e = c.x - d.x;
          c = c.y - d.y;
          var f = Math.sqrt(e * e + c * c);
          if (!(0 >= f)) {
            e /= f;
            c /= f;
            d = b.ca / (b.ca + a.ca);
            d != d &&
            (d = 0.5);
            if (this.Ib >= this.fc) {
              var g = this.Ib;
              var h = 0
            } else if (f <= this.Ib) g = this.Ib,
            h = 1;
             else if (f >= this.fc) g = this.fc,
            h = - 1;
             else return;
            f = g - f;
            if (0 == 0 * this.ye) d = this.ye * f * 0.5,
            e *= d,
            c *= d,
            h = d = b.G,
            b = b.ca,
            d.x = h.x + e * b,
            d.y = h.y + c * b,
            d = b = a.G,
            a = a.ca,
            b.x = d.x + - e * a,
            b.y = d.y + - c * a;
             else {
              g = f * d;
              var k = b.a,
              l = b.a;
              k.x = l.x + e * g * 0.5;
              k.y = l.y + c * g * 0.5;
              l = k = a.a;
              f -= g;
              k.x = l.x - e * f * 0.5;
              k.y = l.y - c * f * 0.5;
              f = b.G;
              g = a.G;
              f = e * (f.x - g.x) + c * (f.y - g.y);
              0 >= f * h &&
              (
                d *= f,
                b = h = b.G,
                h.x = b.x - e * d,
                h.y = b.y - c * d,
                a = b = a.G,
                d = f - d,
                b.x = a.x + e * d,
                b.y = a.y + c * d
              )
            }
          }
        }
      }
    }
    class Dc {
      static xf(a) {
        let b = new mc('([^&=]+)=?([^&]*)', 'g');
        a = a.substring(1);
        var c = 0;
        let d = new Map;
        for (; b.bt(a, c); ) {
          c = b.xn(1);
          c = decodeURIComponent(c.split('+').join(' '));
          let e = b.xn(2);
          d.set(c, decodeURIComponent(e.split('+').join(' ')));
          c = b.ct();
          c = c.Dj + c.$s
        }
        return d
      }
      static v() {
        return Dc.xf(window.top.location.search)
      }
    }
    class hb {
      static ni(a) {
        return new PerfectScrollbar(a, {
          handlers: hb.Ap
        })
      }
    }
    class Kc {
      static xf(a) {
        a = a.split(' ');
        let b = a[4];
        if ('typ' != a[6]) throw v.C(null);
        return {
          vs: a[7],
          Dp: b
        }
      }
    }
    class Rb {
      static rh(a) {
        return new Promise(
          function (b, c) {
            a.onsuccess = function () {
              b(a.result)
            };
            a.onerror = c
          }
        )
      }
    }
    class Ba {
      constructor(a) {
        function b() {
          let t = g[f];
          a.Ol = e ? t : 0;
          c.get('spd').textContent = t + 'x'
        }
        this.lg = !1;
        this.f = x.Ia(Ba.O);
        let c = x.Ba(this.f);
        this.Ji = a;
        let d = this;
        c.get('reset').onclick = function () {
          a.Ki();
          d.Dl()
        };
        let e = !0,
        f = 2,
        g = [
          0.5,
          0.75,
          1,
          2,
          3
        ];
        b();
        let h = c.get('playicon');
        h.classList.add('icon-pause');
        c.get('play').onclick = function () {
          e = !e;
          let t = h.classList;
          t.toggle('icon-play', !e);
          t.toggle('icon-pause', e);
          b()
        };
        c.get('spdup').onclick = function () {
          f += 1;
          let t = g.length - 1;
          f > t &&
          (f = t);
          b()
        };
        c.get('spddn').onclick = function () {
          --f;
          0 > f &&
          (f = 0);
          b()
        };
        this.ps = c.get('time');
        let k = c.get('timebar');
        this.ir = c.get('progbar');
        let l = c.get('timetooltip'),
        n = 0,
        r = a.ol;
        for (; n < r.length; ) {
          let t = r[n];
          ++n;
          let z = window.document.createElement('div');
          z.className = 'marker';
          z.classList.add('k' + t.kind);
          z.style.left = 100 * t.Dj + '%';
          k.appendChild(z)
        }
        k.onclick = function (t) {
          a.Or((t.pageX - k.offsetLeft) / k.clientWidth * a.vh * a.Bf);
          d.lg ||
          (d.lg = !0, d.Eq(), d.Dl())
        };
        k.onmousemove = function (t) {
          t = (t.pageX - k.offsetLeft) / k.clientWidth;
          l.textContent = Ba.pl(a.Bf * a.vh * t);
          return l.style.left = 'calc(' + 100 * t + '% - 30px)'
        };
        this.Np = c.get('leave');
        this.Np.onclick = function () {
          H.h(d.ne)
        }
      }
      A() {
        this.ps.textContent = Ba.pl(this.Ji.Ub);
        this.ir.style.width = 100 * this.Ji.mp() + '%';
        !this.lg ||
        0 < this.Ji.Pd ||
        (this.lg = !1, this.Dq())
      }
      static pl(a) {
        a = a / 1000 | 0;
        return (a / 60 | 0) + ':' + aa.Of(Q.Je(a % 60))
      }
    }
    class ta {
      constructor(a, b, c, d) {
        this.D = a;
        this.Gs = d;
        this.mi = b;
        d = null;
        null != b &&
        (d = b.getItem(a));
        this.hn = c(d)
      }
      v() {
        return this.hn
      }
      ha(a) {
        this.hn = a;
        if (null != this.mi) try {
          let b = this.Gs(a);
          null == b ? this.mi.removeItem(this.D) : this.mi.setItem(this.D, b)
        } catch (b) {
        }
      }
    }
    class Pb {
      static parse(a) {
        a.F();
        let b = [];
        for (; 0 != a.s.byteLength - a.a; ) {
          let c = a.re(a.Sb()),
          d = a.bm(a.Sb());
          try {
            let e = new Sb;
            e.ma(new J(new DataView(d), !1));
            let f = new nc;
            f.je = e;
            f.ba = c;
            b.push(f)
          } catch (e) {
          }
        }
        return b
      }
      static Xs(a, b, c, d) {
        return Math.acos(
          Math.sin(a) * Math.sin(c) + Math.cos(a) * Math.cos(c) * Math.cos(b - d)
        )
      }
      static tt(a, b) {
        let c = a.Jc;
        a = a.Mc;
        let d = 0;
        for (; d < b.length; ) {
          let e = b[d];
          ++d;
          let f = e.je;
          e.Ze = 6378 * Pb.Xs(
            0.017453292519943295 * f.Jc,
            0.017453292519943295 * f.Mc,
            0.017453292519943295 * c,
            0.017453292519943295 * a
          );
          isFinite(e.Ze) ||
          (e.Ze = 22000)
        }
      }
      static get() {
        return Z.v(m.Se + 'api/list', 'arraybuffer').then(function (a) {
          return Pb.parse(new J(new DataView(a), !1))
        })
      }
    }
    class oc {
    }
    class Tb {
      constructor(a) {
        this.$b = a.slice()
      }
      eval(a) {
        var b = this.$b.length - 1;
        if (a <= this.$b[0]) return this.$b[1];
        if (a >= this.$b[b]) return this.$b[b -
        2];
        var c = 0;
        b = b / 5 | 0;
        do {
          var d = b + c >>> 1;
          a > this.$b[5 * d] ? c = d + 1 : b = d - 1
        } while (c <= b);
        c = 5 * b;
        b = this.$b[c];
        a = (a - b) / (this.$b[c + 5] - b);
        b = a * a;
        d = b * a;
        return (2 * d - 3 * b + 1) * this.$b[c + 1] + (d - 2 * b + a) * this.$b[c + 2] + ( - 2 * d + 3 * b) * this.$b[c + 3] + (d - b) * this.$b[c + 4]
      }
    }
    class p {
      constructor() {
        p.yb ||
        this.Za()
      }
      Za() {
        this.Fn = this.Gn = this.Dc = 0
      }
      Bn() {
        return !0
      }
      apply() {
        throw v.C('missing implementation');
      }
      xa() {
        throw v.C('missing implementation');
      }
      wa() {
        throw v.C('missing implementation');
      }
      static Ha(a) {
        null == a.delay &&
        (a.delay = !0);
        null == a.Ca &&
        (a.Ca = !0);
        return a
      }
      static Ja(a) {
        a.Qn = p.Nf;
        if (null == a.Aa) throw v.C('Class doesn\'t have a config');
        a.prototype.Ge = a.Aa;
        p.qn.set(p.Nf, a);
        p.Nf++
      }
      static Cj(a, b) {
        let c = w.nn(a).Qn;
        if (null == c) throw v.C('Tried to pack unregistered action');
        b.m(c);
        a.wa(b)
      }
      static th(a) {
        var b = a.F();
        b = Object.create(p.qn.get(b).prototype);
        b.Dc = 0;
        b.ob = 0;
        b.xa(a);
        return b
      }
    }
    class Ca {
      constructor(a) {
        this.cg = null;
        this.bl = this.Lh = !1;
        this.hd = window.performance.now();
        this.Nd = null;
        this.Re = 0;
        this.qo = new pb(3, 1000);
        this.W = new Ub;
        this.Ng = 'Waiting for link';
        this.Ni = this.zm = !1;
        this.Bd = 0;
        let b = this;
        this.dg = new Vb(a, function (d) {
          b.l.Ka.Hb(d)
        });
        this.za = a;
        a.U.Qo = function (d) {
          b.zm != d &&
          (b.zm = d, a.ta(Da.qa(d)))
        };
        this.l = new ua(a.xc);
        window.top.document.body.classList.add('hb-playing');
        this.Uh = new Wb(this.l, a.U.oa(a.xc).D);
        this.Uh.Hi(a.U);
        this.l.Ka.El = M(this, this.oq);
        this.l.Ka.wg = M(this, this.nq);
        window.document.addEventListener('keydown', M(this, this.Fa));
        window.document.addEventListener('keyup', M(this, this.ld));
        window.onbeforeunload = function () {
          return 'Are you sure you want to leave the room?'
        };
        this.W.Bg = function (d) {
          a.A();
          a.ta(d)
        };
        this.W.xl = function (d) {
          'ToggleChat' == d &&
          b.l.Ka.$m()
        };
        this.l.Xa.Kq = function (d) {
          a.ta(va.qa(1, d))
        };
        this.l.Xa.Cq = function (d) {
          a.ta(va.qa(0, d))
        };
        this.l.Cg = function (d) {
          a.ta(Ea.qa(d))
        };
        this.l.Xa.Hq = function () {
          a.ta(new Va)
        };
        this.l.Xa.Iq = function () {
          a.ta(new Wa)
        };
        this.l.Xa.vq = function () {
          b.an()
        };
        this.l.Xa.Ag = function (d, e) {
          a.ta(fa.qa(d, e))
        };
        this.l.Xa.oe = M(this, this.Fr);
        this.l.Xa.lq = function () {
          a.ta(new Xa)
        };
        this.l.Xa.yq = function () {
          Ca.jr(a)
        };
        this.l.Xa.Jq = function (d) {
          a.ta(Fa.qa(d))
        };
        this.l.Xa.wf = function (d) {
          let e = a.U.oa(d);
          if (null != e) {
            let f = new qb(e, b.Ni);
            f.rb = function () {
              b.l.ab(null)
            };
            f.kq = function (g, h) {
              a.ta(Ga.qa(g, h))
            };
            f.ui = function () {
              b.gs(e)
            };
            b.l.ab(f.f, function () {
              f.A(a.U, b.Ni)
            })
          }
        };
        this.l.Xa.Fq = function () {
          let d = new rb;
          d.rb = function () {
            b.l.ab(null)
          };
          b.l.ab(d.f, function () {
            d.Yr(b.Ng)
          })
        };
        this.l.Xa.zq = function () {
          if (null == b.Nd) b.ls();
           else {
            let d = b.Nd.stop();
            b.Nd = null;
            Ca.wm(d)
          }
          b.l.Xa.bs(null != b.Nd)
        };
        window.requestAnimationFrame(M(this, this.sf));
        this.Sh = window.setInterval(function () {
          b.l.Jf.Gm(b.Bd);
          b.Bd = 0
        }, 1000);
        this.lj = window.setInterval(function () {
          a.A()
        }, 50);
        var c = m.j.Ad.v();
        c = - 200 > c ? - 200 : 1000 < c ? 1000 : c;
        0 != c &&
        (
          a.Fm(m.j.Ad.v()),
          this.l.Ka.Hb('Extrapolation set to ' + c + ' msec')
        )
      }
      ls() {
        this.Nd = new pc(this.za, 3)
      }
      gs(a) {
        a = new sb(a);
        let b = this;
        a.rb = function () {
          b.l.ab(null)
        };
        a.ui = function (c, d, e) {
          b.za.ta(ma.qa(c, d, e));
          b.l.ab(null)
        };
        this.l.ab(a.f)
      }
      la() {
        window.document.removeEventListener('keydown', M(this, this.Fa));
        window.document.removeEventListener('keyup', M(this, this.ld));
        window.onbeforeunload = null;
        window.cancelAnimationFrame(this.Re);
        window.top.document.body.classList.remove('hb-playing');
        this.W.la();
        window.clearInterval(this.Sh);
        window.clearInterval(this.lj);
        window.clearTimeout(this.cg)
      }
      Fr(a) {
        let b = [],
        c = 0,
        d = this.za.U.K;
        for (; c < d.length; ) {
          let e = d[c];
          ++c;
          e.fa == a &&
          b.push(fa.qa(e.Z, u.Oa))
        }
        for (a = 0; a < b.length; ) this.za.ta(b[a++])
      }
      sf() {
        this.Re = window.requestAnimationFrame(M(this, this.sf));
        this.W.A();
        this.za.A();
        this.Rc()
      }
      Rc() {
        var a = window.performance.now();
        1 == m.j.Rh.v() &&
        28.333333333333336 > a - this.hd ||
        (
          this.hd = a,
          this.Bd++,
          a = this.za.U.oa(this.za.xc),
          null != a &&
          (this.Ni = a.fb),
          this.l.A(this.za)
        )
      }
      oq(a) {
        let b = this;
        this.dg.xf(a) ||
        this.qo.Go(function () {
          let c = new Ya;
          c.$c = a;
          b.za.ta(c)
        })
      }
      nq(a) {
        this.Lh = a;
        let b = this;
        null == this.cg &&
        (
          this.cg = window.setTimeout(function () {
            b.cg = null;
            b.Am(b.Lh)
          }, 1000),
          this.Am(this.Lh)
        )
      }
      Am(a) {
        a != this.bl &&
        (this.za.ta(Ha.qa(a ? 0 : 1)), this.bl = a)
      }
      an() {
        if (null != this.za.U.M) {
          let a = new Za;
          a.Pf = 120 != this.za.U.M.Ta;
          this.za.ta(a)
        }
      }
      Fa(a) {
        var b = m.j.Rd;
        let c = null != m.j.Jd.v().v(a.code);
        switch (a.keyCode) {
          case 9:
          case 13:
            this.l.Ka.$a.focus({
              preventScroll: !0
            });
            a.preventDefault();
            break;
          case 27:
            this.l.Zk() ? this.l.ab(null) : (b = this.l, b.we(!b.od));
            a.preventDefault();
            break;
          case 48:
            c ? this.W.Fa(a) : b.ha(0);
            break;
          case 49:
            c ? this.W.Fa(a) : b.ha(1);
            break;
          case 50:
            c ? this.W.Fa(a) : b.ha(2);
            break;
          case 51:
            c ? this.W.Fa(a) : b.ha(3);
            break;
          case 52:
            c ? this.W.Fa(a) : b.ha(4);
            break;
          case 53:
            c ? this.W.Fa(a) : b.ha(5);
            break;
          case 54:
            c ? this.W.Fa(a) : b.ha(6);
            break;
          case 55:
            c ? this.W.Fa(a) : b.ha(7);
            break;
          case 80:
            this.an();
            break;
          default:
            this.W.Fa(a)
        }
      }
      ld(a) {
        this.W.ld(a)
      }
      static wm(a) {
        let b = new Date;
        Nb.Kr(
          a,
          'HBReplay-' + b.getFullYear() + '-' + aa.Of('' + (b.getMonth() + 1)) + '-' + aa.Of('' + b.getDate()) + '-' + aa.Of('' + b.getHours()) + 'h' + aa.Of('' + b.getMinutes()) + 'm.hbr2'
        )
      }
      static jr(a) {
        var b = a.U.K;
        let c = [];
        var d = 0;
        let e = 0;
        for (var f = 0; f < b.length; ) {
          let g = b[f];
          ++f;
          g.fa == u.Oa &&
          c.push(g.Z);
          g.fa == u.ia ? ++d : g.fa == u.Da &&
          ++e
        }
        f = c.length;
        0 != f &&
        (
          b = function () {
            return c.splice(Math.random() * c.length | 0, 1) [0]
          },
          e == d ? 2 > f ||
          (a.ta(fa.qa(b(), u.ia)), a.ta(fa.qa(b(), u.Da))) : (d = e > d ? u.ia : u.Da, a.ta(fa.qa(b(), d)))
        )
      }
    }
    class qc {
      constructor(a) {
        this.hd = window.performance.now();
        this.W = new Ub;
        this.Bd = this.Re = 0;
        this.za = a;
        this.l = new ua(a.xc);
        let b = new Wb(this.l);
        b.Hi(a.U);
        window.document.addEventListener('keydown', M(this, this.Fa));
        window.document.addEventListener('keyup', M(this, this.ld));
        let c = this;
        this.W.xl = function (d) {
          'ToggleChat' == d &&
          c.l.Ka.$m()
        };
        window.requestAnimationFrame(M(this, this.sf));
        this.Sh = window.setInterval(function () {
          c.l.Jf.Gm(c.Bd);
          c.Bd = 0
        }, 1000);
        this.Jm(m.j.Rd.v());
        this.l.f.classList.add('replayer');
        this.se = new Ba(a);
        this.se.Eq = function () {
          b.xs(a.U)
        };
        this.se.Dq = function () {
          c.l.we(null == a.U.M);
          b.Hi(a.U)
        };
        this.se.Dl = function () {
          c.l.ib.gb.Gr()
        };
        this.l.f.appendChild(this.se.f);
        this.lj = window.setInterval(function () {
          a.A()
        }, 50)
      }
      la() {
        window.document.removeEventListener('keydown', M(this, this.Fa));
        window.document.removeEventListener('keyup', M(this, this.ld));
        window.onbeforeunload = null;
        window.cancelAnimationFrame(this.Re);
        window.clearInterval(this.Sh);
        window.clearInterval(this.lj);
        this.W.la()
      }
      sf() {
        this.Re = window.requestAnimationFrame(M(this, this.sf));
        this.za.A();
        this.Rc()
      }
      Rc() {
        this.se.A();
        let a = window.performance.now();
        1 == m.j.Rh.v() &&
        28.333333333333336 > a - this.hd ||
        (
          this.hd = a,
          this.Bd++,
          this.Jm(m.j.Rd.v()),
          0 < this.za.Pd ||
          this.l.A(this.za)
        )
      }
      Fa(a) {
        var b = m.j.Rd;
        let c = null != m.j.Jd.v().v(a.code);
        switch (a.keyCode) {
          case 27:
            this.l.Zk() ? this.l.ab(null) : (b = this.l, b.we(!b.od));
            a.preventDefault();
            break;
          case 48:
            c ? this.W.Fa(a) : b.ha(0);
            break;
          case 49:
            c ? this.W.Fa(a) : b.ha(1);
            break;
          case 50:
            c ? this.W.Fa(a) : b.ha(2);
            break;
          case 51:
            c ? this.W.Fa(a) : b.ha(3);
            break;
          case 52:
            c ? this.W.Fa(a) :
            b.ha(4);
            break;
          case 53:
            c ? this.W.Fa(a) : b.ha(5);
            break;
          case 54:
            c ? this.W.Fa(a) : b.ha(6);
            break;
          case 55:
            c ? this.W.Fa(a) : b.ha(7);
            break;
          default:
            this.W.Fa(a)
        }
      }
      ld(a) {
        this.W.ld(a)
      }
      Jm() {
        let a = m.j.Rd.v(),
        b = this.l.ib.gb;
        b.te = m.j.Mi.v();
        b.Wg = 35;
        0 >= a ? b.Ld = 610 : (b.Ld = 0, b.Ig = 1 + 0.25 * (a - 1))
      }
    }
    class Lc {
      static description(a) {
        switch (a) {
          case 4001:
            return 'The room was closed.';
          case 4100:
            return 'The room is full.';
          case 4101:
            return 'Wrong password.';
          case 4102:
            return 'You are banned from this room.';
          case 4103:
            return 'Incompatible game version.';
          default:
            return 'Connection closed (' + a + ')'
        }
      }
    }
    class tb {
      constructor() {
        this.mg = !1;
        this.D = '';
        this.Ch = 0;
        this.Zf = '';
        this.mb = new wa;
        let a = window.document.createElement('canvas');
        a.width = 64;
        a.height = 64;
        this.Kb = a.getContext('2d', null);
        this.$j = null;
        this.Mo()
      }
      Mo() {
        let a = window.document.createElement('canvas');
        a.width = 160;
        a.height = 34;
        this.Ul = a.getContext('2d', null)
      }
      As() {
        let a = this.Ul;
        a.resetTransform();
        a.clearRect(0, 0, 160, 34);
        a.font = '26px sans-serif';
        a.fillStyle = 'white';
        160 < a.measureText(this.D).width ? (a.textAlign = 'left', a.translate(2, 29)) : (a.textAlign = 'center', a.translate(80, 29));
        a.fillText(this.D, 0, 0)
      }
      Yo(a, b, c) {
        a.drawImage(this.Ul.canvas, 0, 0, 160, 34, b - 40, c - 34, 80, 17)
      }
      A(a, b) {
        if (null != a.I) {
          let c = m.j.Vm.v() ? b.mb[a.fa.ba] : a.fa.Um,
          d = null != a.Sd ? a.Sd : a.Zb,
          e = m.j.Km.v() &&
          null != d;
          if (!tb.so(this.mb, c) || !e && a.Nb != this.Ch || e && this.Zf != d) tb.Io(this.mb, c),
          e ? (this.Zf = d, this.Ch = - 1) : (this.Zf = '' + a.Nb, this.Ch = a.Nb),
          this.qr(this.Zf)
        }
        this.Ro = 0 < b.M.Ta ||
        !a.Yb ? 'black' : a.Yb &&
        0 >= a.Zc &&
        0 <= a.Bc ? 'white' : 'black';
        a.D != this.D &&
        (this.D = a.D, this.As())
      }
      qr(a) {
        let b = this.mb.hb;
        if (!(1 > b.length)) {
          this.Kb.save();
          this.Kb.translate(32, 32);
          this.Kb.rotate(3.141592653589793 * this.mb.sd / 128);
          for (var c = - 32, d = 64 / b.length, e = 0; e < b.length; ) this.Kb.fillStyle = T.nc(b[e++]),
          this.Kb.fillRect(c, - 32, d + 4, 64),
          c += d;
          this.Kb.restore();
          this.Kb.fillStyle = T.nc(this.mb.pd);
          this.Kb.textAlign = 'center';
          this.Kb.textBaseline = 'alphabetic';
          this.Kb.font = '900 34px \'Arial Black\',\'Arial Bold\',Gadget,sans-serif';
          this.Kb.fillText(a, 32, 44);
          this.$j = this.Kb.createPattern(this.Kb.canvas, 'no-repeat')
        }
      }
      static so(a, b) {
        if (a.sd != b.sd || a.pd != b.pd) return !1;
        a = a.hb;
        b = b.hb;
        if (a.length != b.length) return !1;
        let c = 0,
        d = a.length;
        for (; c < d; ) {
          let e = c++;
          if (a[e] != b[e]) return !1
        }
        return !0
      }
      static Io(a, b) {
        a.sd = b.sd;
        a.pd = b.pd;
        a.hb = b.hb.slice(0)
      }
    }
    class ub {
      constructor() {
        this.f = x.Ia(ub.O);
        let a = x.Ba(this.f);
        this.Lc = a.get('log');
        this.Fh = a.get('cancel')
      }
      da(a) {
        let b = window.document.createElement('p');
        b.textContent = a;
        this.Lc.appendChild(b)
      }
    }
    class Ia {
    }
    class x {
      static Ba(a) {
        let b = new Map,
        c = 0;
        for (a = a.querySelectorAll('[data-hook]'); c <
        a.length; ) {
          let d = a[c++];
          b.set(d.getAttribute('data-hook'), d)
        }
        return b
      }
      static Ia(a, b) {
        null == b &&
        (b = 'div');
        b = window.document.createElement(b);
        b.innerHTML = a;
        return b.firstElementChild
      }
      static replaceWith(a, b) {
        a.parentElement.replaceChild(b, a)
      }
      static Qf(a) {
        let b = a.firstChild;
        for (; null != b; ) a.removeChild(b),
        b = a.firstChild
      }
    }
    class Sa {
      constructor(a) {
        this.eq = a
      }
    }
    class xa {
      constructor() {
        this.jc = - 1;
        this.T = this.ic = null;
        this.Gd = 2;
        this.gd = 0;
        this.me = 1;
        this.kb = this.Ga = 3;
        this.Ac = !1;
        this.M = null;
        this.K = [];
        this.lc = '';
        this.T = q.Vh() [0];
        this.mb = [
          null,
          new wa,
          new wa
        ];
        this.mb[1].hb.push(u.ia.S);
        this.mb[2].hb.push(u.Da.S)
      }
      ks(a) {
        if (null == this.M) {
          this.M = new Y;
          for (var b = 0, c = this.K; b < c.length; ) {
            let d = c[b];
            ++b;
            d.I = null;
            d.Nb = 0
          }
          this.M.Cp(this);
          null != this.aj &&
          this.aj(a)
        }
      }
      ag(a, b, c) {
        if (b.fa != c) {
          b.fa = c;
          O.remove(this.K, b);
          this.K.push(b);
          if (null != this.M) {
            null != b.I &&
            (O.remove(this.M.va.H, b.I), b.I = null);
            this.M.Wk(b);
            let d = 0,
            e = !1;
            for (; !e; ) {
              ++d;
              e = !0;
              let f = 0,
              g = this.K;
              for (; f < g.length; ) {
                let h = g[f];
                ++f;
                if (h != b && h.fa == b.fa && h.Nb == d) {
                  e = !1;
                  break
                }
              }
            }
            b.Nb = d
          }
          hc.h(this.Wl, a, b, c)
        }
      }
      oa(a) {
        let b = 0,
        c = this.K;
        for (; b < c.length; ) {
          let d = c[b];
          ++b;
          if (d.Z == a) return d
        }
        return null
      }
      A(a) {
        null != this.M &&
        this.M.A(a)
      }
      ga(a) {
        a.Eb(this.lc);
        a.m(this.Ac ? 1 : 0);
        a.R(this.kb);
        a.R(this.Ga);
        a.oj(this.me);
        a.m(this.gd);
        a.m(this.Gd);
        this.T.ga(a);
        a.m(null != this.M ? 1 : 0);
        null != this.M &&
        this.M.ga(a);
        a.m(this.K.length);
        let b = 0,
        c = this.K;
        for (; b < c.length; ) c[b++].wa(a);
        this.mb[1].ga(a);
        this.mb[2].ga(a)
      }
      ma(a) {
        this.lc = a.Ab();
        this.Ac = 0 != a.F();
        this.kb = a.N();
        this.Ga = a.N();
        this.me = a.Di();
        this.gd = a.F();
        this.Gd = a.F();
        this.T = q.ma(a);
        var b = 0 != a.F();
        this.M = null;
        b &&
        (this.M = new Y, this.M.ma(a, this));
        b = null == this.M ? null : this.M.va.H;
        let c = a.F();
        for (var d = this.K; d.length > c; ) d.pop();
        for (d = 0; d < c; ) {
          let e = new ya;
          e.xa(a, b);
          this.K[d++] = e
        }
        this.mb[1].ma(a);
        this.mb[2].ma(a)
      }
      Ok() {
        let a = 0;
        var b = A.ka();
        this.ga(b);
        for (b = b.rs(); 4 <= b.s.byteLength - b.a; ) a ^= b.N();
        return a
      }
      gp() {
        let a = A.ka(4);
        a.R(this.Ok());
        return a.Vg()
      }
      zo(a) {
        a = (new J(new DataView(a))).N();
        D.h(this.Qo, this.Ok() != a)
      }
      Im(a) {
        this.nm = a
      }
      Pb(a) {
        if (0 == a) return !0;
        a = this.oa(a);
        return null != a &&
        a.fb ? !0 : !1
      }
      Xr(a, b, c, d) {
        this.Gd = 0 > b ? 0 : 255 < b ? 255 : b;
        this.gd = 0 > c ? 0 : 255 < c ? 255 : c;
        0 > d ? d = 0 : 100 < d &&
        (d = 100);
        this.me = this.gd * d;
        Xb.h(this.al, a, this.Gd, this.gd, d)
      }
      uc() {
        let a = qa.Cc,
        b = this.ic;
        this.jc != a &&
        (null == b && (this.ic = b = new xa), this.jc = a, xa.zd(b, this));
        return b
      }
      static zd(a, b) {
        a.lc = b.lc;
        if (null == b.K) a.K = null;
         else {
          null == a.K &&
          (a.K = []);
          let d = a.K,
          e = b.K;
          for (var c = e.length; d.length > c; ) d.pop();
          c = 0;
          let f = e.length;
          for (; c < f; ) {
            let g = c++;
            d[g] = e[g].Ws()
          }
        }
        a.M = null == b.M ? null : b.M.uc();
        a.Ac = b.Ac;
        a.kb = b.kb;
        a.Ga = b.Ga;
        a.me = b.me;
        a.gd = b.gd;
        a.Gd = b.Gd;
        a.T = b.T;
        a.mb = b.mb
      }
    }
    class Ob {
      constructor(a, b) {
        this.La = a;
        this.value = b;
        a.textContent = '' + b
      }
      set(a) {
        this.value != a &&
        (this.value = a, this.La.textContent = '' + this.value)
      }
    }
    class lc {
      constructor() {
      }
    }
    class sb {
      constructor(a) {
        this.f = x.Ia(sb.O);
        let b = x.Ba(this.f);
        this.nf = b.get('title');
        this.Ei = b.get('reason');
        this.bo = b.get('ban-btn');
        this.eo = b.get('ban-text');
        this.df = b.get('kick');
        this.wd = b.get('close');
        let c = this;
        this.bo.onclick = function () {
          c.Sj(!c.ak)
        };
        this.wd.onclick = function () {
          H.h(c.rb)
        };
        this.df.onclick = function () {
          hc.h(c.ui, c.Rb, c.Ei.value, c.ak)
        };
        this.Ei.onkeydown = function (d) {
          return d.stopPropagation()
        };
        this.Ei.maxLength = 100;
        this.Rb = a.Z;
        this.nf.textContent = 'Kick ' + a.D;
        this.Sj(!1)
      }
      Sj(a) {
        this.ak = a;
        this.eo.textContent = a ? 'Yes' : 'No'
      }
    }
    class rc {
      constructor() {
        this.Mh = 0;
        this.cq = 400;
        this.Sk = 64;
        this.mj = 32;
        this.na = window.document.createElement('canvas');
        this.fg = window.document.createElement('canvas');
        this.f = window.document.createElement('div');
        this.fg.width = this.na.width = this.mj;
        this.fg.height = this.na.height = this.Sk;
        this.Qh = this.fg.getContext('2d', null);
        this.c = this.na.getContext('2d', null);
        this.c.fillStyle = 'green';
        let a = [],
        b = 0,
        c = this.mj;
        for (; b < c; ) ++b,
        a.push(0);
        this.Oq = a;
        this.f.appendChild(this.fg);
        this.f.className = 'graph';
        this.f.hidden = !0
      }
      Wn(a) {
        this.f.hidden = !1;
        0 > a ? (a = 150, this.c.fillStyle = '#c13535') : this.c.fillStyle = '#32FF32';
        let b = this.mj,
        c = this.Sk,
        d = this.Mh++;
        this.Mh >= b &&
        (this.Mh = 0);
        this.Oq[d] = a;
        this.c.clearRect(d, 0, 1, c);
        a = a * c / this.cq;
        this.c.fillRect(d, c - a, 1, a);
        this.Qh.clearRect(0, 0, b, c);
        this.Qh.drawImage(this.na, b - d - 1, 0);
        this.Qh.drawImage(this.na, - d - 1, 0)
      }
    }
    class vb {
      static Op() {
        if (null != vb.Bi) return vb.Bi;
        vb.Bi = new Promise(
          function (a, b) {
            var c = window.grecaptcha;
            null != c ? a(c) : (
              c = window.document.createElement('script'),
              c.src = 'https://www.google.com/recaptcha/api.js?onload=___recaptchaload&render=explicit',
              window.document.head.appendChild(c),
              window.___recaptchaload = function () {
                a(window.grecaptcha)
              },
              c.onerror = function () {
                b(null)
              }
            )
          }
        );
        return vb.Bi
      }
    }
    class wb {
      constructor() {
        this.Ml = new rc;
        this.f = x.Ia(wb.O);
        let a = x.Ba(this.f);
        this.Fg = a.get('ping');
        this.bp = a.get('fps');
        x.replaceWith(a.get('graph'), this.Ml.f)
      }
      $r(a, b) {
        this.Fg.textContent = 'Ping: ' + a + ' - ' + b
      }
      Gm(a) {
        this.bp.textContent = 'Fps: ' + a
      }
    }
    class sc {
      constructor(a) {
        this.f = a;
        let b = x.Ba(a);
        this.ho = b.get('sound-bar');
        this.Bp = b.get('sound-icon');
        this.fo = b.get('sound-bar-bg');
        let c = this;
        b.get('sound-btn').onclick = function () {
          m.j.xe.ha(!m.j.xe.v());
          c.A()
        };
        b.get('sound-slider').onmousedown = function (d) {
          function e(g) {
            g.preventDefault();
            {
              let h = c.fo.getBoundingClientRect();
              g = (g.clientY - h.top) / h.height
            }
            g = 1 - g;
            m.j.Yi.ha(1 < g ? 1 : 0 > g ? 0 : g);
            m.j.xe.ha(!0);
            c.A()
          }
          e(d);
          let f = null;
          f = function (g) {
            e(g);
            a.classList.toggle('dragging', !1);
            window.document.removeEventListener('mousemove', e, !1);
            window.document.removeEventListener('mouseup', f, !1)
          };
          a.classList.toggle('dragging', !0);
          window.document.addEventListener('mousemove', e, !1);
          window.document.addEventListener('mouseup', f, !1)
        };
        this.A()
      }
      A() {
        let a = m.j.Yi.v(),
        b = !m.j.xe.v();
        if (this.Lp != a || this.Kp != b) this.Lp = a,
        (this.Kp = b) &&
        (a = 0),
        this.Bp.className = 'icon-' + (0 >= a ? 'volume-off' : 0.5 >= a ? 'volume-down' : 'volume-up'),
        this.ho.style.top = 100 * (1 - a) + '%',
        m.Qa.Gi()
      }
    }
    class ua {
      constructor(a) {
        this.tl = this.sl = this.vl = null;
        this.ib = new jb;
        this.od = !1;
        this.Jf = new wb;
        this.Ka = new $a;
        this.Xa = new xb(a);
        this.ib.Rb = a;
        this.f = x.Ia(ua.O);
        a = x.Ba(this.f);
        this.us = a.get('top-section');
        this.yf = a.get('popups');
        this.yf.style.display = 'none';
        a.get('gameplay').appendChild(this.ib.f);
        x.replaceWith(a.get('chatbox'), this.Ka.f);
        x.replaceWith(a.get('stats'), this.Jf.f);
        this.si = a.get('menu');
        let b = this;
        this.si.onclick = function () {
          b.we(!b.od);
          b.si.blur()
        };
        new sc(a.get('sound'));
        a.get('settings').onclick = function () {
          let c = new na;
          c.rb = function () {
            b.ab(null)
          };
          b.ab(c.f)
        };
        this.Xa.ne = function () {
          let c = new nb;
          c.rb = function (d) {
            b.ab(null);
            d &&
            H.h(b.ne)
          };
          b.ab(c.f)
        };
        this.Xa.Gq = function () {
          let c = new gb;
          c.ti = function () {
            b.ab(null)
          };
          c.Cg = function (d) {
            D.h(b.Cg, d);
            b.ab(null)
          };
          c.vi = function (d) {
            d = new ba('Error loading stadium', d, [
              'Ok'
            ]);
            d.Wa = function () {
              b.ab(null)
            };
            b.ab(d.f)
          };
          b.ab(c.f)
        }
      }
      Ur(a) {
        this.tl !=
        a &&
        (this.tl = a, this.f.style.setProperty('--chat-opacity', '' + a))
      }
      Tr(a) {
        this.sl != a &&
        (this.sl = a, this.f.classList.toggle('chat-bg-full', a))
      }
      cs(a) {
        this.vl != a &&
        (this.vl = a, this.ib.f.classList.toggle('restricted', a))
      }
      A(a) {
        null == a.U.M &&
        this.we(!0);
        this.od &&
        this.Xa.A(a.U, a.U.oa(a.xc));
        H.h(this.Xl);
        this.si.disabled = null == a.U.M;
        let b = m.j.Rd.v(),
        c = this.ib.gb;
        c.te = m.j.Mi.v();
        this.Ur(m.j.Ih.v());
        this.Tr('full' == m.j.jk.v());
        this.cs(0 == b);
        let d = this.Ka.f.getBoundingClientRect().height;
        0 == b ? (
          c.Ig = 1,
          c.Ld = 0,
          c.Wg = 0,
          this.ib.gb.Dh = 0,
          this.ib.f.style.paddingBottom = d + 'px'
        ) : (
          c.Wg = 35,
          0 >= b ? c.Ld = 610 : (c.Ld = 0, c.Ig = 1 + 0.25 * (b - 1)),
          this.ib.gb.Dh = d * window.devicePixelRatio,
          this.ib.f.style.paddingBottom = '0'
        );
        a = a.hg();
        this.ib.A(a);
        m.Qa.sk.wt(a)
      }
      we(a) {
        this.od != a &&
        (
          this.od = a,
          this.f.classList.toggle('showing-room-view', this.od),
          this.od ? this.us.appendChild(this.Xa.f) : this.Xa.f.remove()
        )
      }
      Zk() {
        return null != ua.Tq
      }
      ab(a, b) {
        x.Qf(this.yf);
        ua.Tq = a;
        null != a ? (
          this.yf.style.display = 'flex',
          this.yf.appendChild(a),
          this.Xl = b
        ) : (this.yf.style.display = 'none', this.Xl = null)
      }
    }
    class R {
      constructor() {
        this.B = 32;
        this.i = 63;
        this.o = 1;
        this.Va = 0;
        this.ya = new P(0, 0)
      }
      ga(a) {
        let b = this.ya;
        a.u(b.x);
        a.u(b.y);
        a.u(this.Va);
        a.u(this.o);
        a.R(this.i);
        a.R(this.B)
      }
      ma(a) {
        let b = this.ya;
        b.x = a.w();
        b.y = a.w();
        this.Va = a.w();
        this.o = a.w();
        this.i = a.N();
        this.B = a.N()
      }
    }
    class Yb {
      constructor(a) {
        this.rd = null;
        this.mr = 10000;
        this.Ed = !0;
        a.mk();
        this.Sa = a.Sa;
        this.cd = a.cd;
        this.ze = a.ze;
        this.rd = a.rd;
        this.Wm = window.performance.now();
        let b = null,
        c = this;
        b = function () {
          var e = c.mr - c.ns();
          0 >= e ? c.la() : (
            window.clearTimeout(c.Zm),
            e = window.setTimeout(b, e + 1000),
            c.Zm = e
          )
        };
        b();
        this.Sa.oniceconnectionstatechange = function () {
          let e = c.Sa.iceConnectionState;
          'closed' != e &&
          'failed' != e ||
          c.la()
        };
        a = 0;
        let d = this.cd;
        for (; a < d.length; ) {
          let e = d[a];
          ++a;
          e.onmessage = function (f) {
            c.Ed &&
            (c.Wm = window.performance.now(), null != c.zg && c.zg(f.data))
          };
          e.onclose = function () {
            c.la()
          }
        }
      }
      ns() {
        return window.performance.now() - this.Wm
      }
      Vb(a, b) {
        if (this.Ed && (a = this.cd[a], 'open' == a.readyState)) {
          b = b.Vg();
          try {
            a.send(b)
          } catch (c) {
            b = v.Mb(c).Fb(),
            pa.console.log(b)
          }
        }
      }
      la() {
        window.clearTimeout(this.Zm);
        this.Ed &&
        (this.Ed = !1, this.Sa.close(), null != this.tf && this.tf())
      }
    }
    class Ja {
      constructor(a, b, c) {
        this.rd = this.Be = null;
        this.ze = [];
        this.wk = 0;
        this.Gl = !1;
        this.ig = [];
        this.cd = [];
        this.Sa = new RTCPeerConnection({
          iceServers: b
        }, Ja.Fo);
        let d;
        this.jg = new Promise(function (f) {
          d = f
        });
        let e = this;
        this.Sa.onicecandidate = function (f) {
          null == f.candidate ? d(e.ig) : (
            f = f.candidate,
            null != f.candidate &&
            '' != f.candidate &&
            (null != e.xg && e.xg(f), e.ig.push(f))
          )
        };
        for (b = 0; b < c.length; ) this.Ko(c[b++]);
        this.ba = a
      }
      cj(a) {
        null == a &&
        (a = 10000);
        window.clearTimeout(this.Be);
        this.Be = window.setTimeout(M(this, this.zp), a)
      }
      async Jo(a, b) {
        await this.Sa.setRemoteDescription(a);
        a = await this.Sa.createAnswer();
        await this.Sa.setLocalDescription(a);
        let c = 0;
        for (; c < b.length; ) this.Qj(b[c++]);
        try {
          await Ec.Ym(this.jg, 500)
        } catch (d) {
        }
        return a
      }
      async Lo() {
        let a = await this.Sa.createOffer();
        await this.Sa.setLocalDescription(a);
        try {
          await Ec.Ym(this.jg, 1000)
        } catch (b) {
        }
        return a
      }
      Ko(a) {
        let b = {
          id: this.cd.length,
          negotiated: !0,
          ordered: a.ordered
        };
        a.reliable ||
        (b.maxRetransmits = 0);
        a = this.Sa.createDataChannel(a.name, b);
        a.binaryType = 'arraybuffer';
        let c = this;
        a.onopen = function () {
          let d = 0,
          e = c.cd;
          for (; d < e.length; ) if ('open' != e[d++].readyState) return;
          null != c.Hd &&
          c.Hd()
        };
        a.onclose = function () {
          c.Yh()
        };
        a.onmessage = function () {
          c.Yh()
        };
        this.cd.push(a)
      }
      Qj(a) {
        let b = this;
        window.setTimeout(function () {
          b.Sa.addIceCandidate(a)
        }, this.wk)
      }
      zp() {
        this.Yh()
      }
      Yh() {
        null != this.kd &&
        this.kd();
        this.la()
      }
      la() {
        this.mk();
        this.Sa.close()
      }
      mk() {
        window.clearTimeout(this.Be);
        this.Hd = this.xg = this.kd = null;
        this.Sa.onicecandidate = null;
        this.Sa.ondatachannel = null;
        this.Sa.onsignalingstatechange = null;
        this.Sa.oniceconnectionstatechange = null;
        let a = 0,
        b = this.cd;
        for (; a < b.length; ) {
          let c = b[a];
          ++a;
          c.onopen = null;
          c.onclose = null;
          c.onmessage = null
        }
      }
    }
    class Ac {
      static mn(a) {
        let b = [];
        if (null != a) {
          let d = Object.prototype.hasOwnProperty;
          for (var c in a) '__id__' != c &&
          'hx__closures__' != c &&
          d.call(a, c) &&
          b.push(c)
        }
        return b
      }
    }
    class Ka {
      constructor(a) {
        this.Fd = new Map;
        this.f = x.Ia(Ka.O);
        this.f.className += ' ' + a.Oo;
        let b = x.Ba(this.f);
        this.eb = b.get('list');
        this.hi = b.get('join-btn');
        this.Li = b.get('reset-btn');
        a == u.Oa &&
        this.Li.remove();
        this.hi.textContent = '' + a.D;
        this.f.ondragover = this.f.Ct = function (d) {
          - 1 != d.dataTransfer.types.indexOf('player') &&
          d.preventDefault()
        };
        let c = this;
        this.f.ondrop = function (d) {
          d.preventDefault();
          d = d.dataTransfer.getData('player');
          null != d &&
          (d = Q.parseInt(d), null != d && za.h(c.Ag, d, a))
        };
        this.hi.onclick = function () {
          D.h(c.sq, a)
        };
        this.Li.onclick = function () {
          D.h(c.oe, a)
        }
      }
      A(a, b, c, d) {
        this.hi.disabled = b ||
        c;
        this.Li.disabled = c;
        b = new Set;
        c = this.Fd.keys();
        for (var e = c.next(); !e.done; ) {
          var f = e.value;
          e = c.next();
          b.add(f)
        }
        let g = this;
        for (c = 0; c < a.length; ) e = a[c],
        ++c,
        f = this.Fd.get(e.Z),
        null == f &&
        (
          f = new yb(e),
          f.wf = function (h) {
            D.h(g.wf, h)
          },
          this.Fd.set(e.Z, f),
          this.eb.appendChild(f.f)
        ),
        f.A(e, d),
        b.delete(e.Z);
        d = b.values();
        for (b = d.next(); !b.done; ) c = b.value,
        b = d.next(),
        this.Fd.get(c).f.remove(),
        this.Fd.delete(c);
        d = 0;
        for (b = a.length - 1; d < b; ) e = d++,
        c = this.Fd.get(a[e].Z).f,
        e = this.Fd.get(a[e + 1].Z).f,
        c.nextSibling != e &&
        this.eb.insertBefore(c, e)
      }
    }
    class da {
      constructor(a, b) {
        let c = [],
        d = 0;
        for (; d < a.length; ) c.push(this.$p(a[d++], b));
        this.kf = c
      }
      fp() {
        return 2.31 + 0.1155 * (this.kf.length - 1)
      }
      Rc(a, b) {
        b /= 2.31;
        let c = 0;
        a.imageSmoothingEnabled = !0;
        let d = 0,
        e = this.kf;
        for (; d < e.length; ) {
          let g = e[d];
          ++d;
          var f = b - 0.05 * c;
          let h = da.Ln.eval(f),
          k = 35 * - (this.kf.length - 1) + 70 * c;
          f = 180 * da.Mn.eval(f);
          a.globalAlpha = h;
          a.drawImage(g, f * (0 != (c & 1) ? - 1 : 1) - 0.5 * g.width, k - 0.5 * g.height);
          a.globalAlpha = 1;
          ++c
        }
        a.imageSmoothingEnabled = !1
      }
      Cr(a) {
        let b = 0;
        a.imageSmoothingEnabled = !0;
        let c = 0,
        d = this.kf;
        for (; c < d.length; ) {
          let e = d[c];
          ++c;
          a.drawImage(e, 0.5 * - e.width, 35 * - (this.kf.length -
          1) + 70 * b - 0.5 * e.height);
          ++b
        }
        a.imageSmoothingEnabled = !1
      }
      nc(a) {
        return 'rgba(' + [(a & 16711680) >>> 16,
        (a & 65280) >>> 8,
        a & 255].join() + ',255)'
      }
      $p(a, b) {
        let c = window.document.createElement('canvas'),
        d = c.getContext('2d', null);
        d.font = '900 70px \'Arial Black\',\'Arial Bold\',Gadget,sans-serif';
        c.width = Math.ceil(d.measureText(a).width) + 7;
        c.height = 90;
        d.font = '900 70px \'Arial Black\',\'Arial Bold\',Gadget,sans-serif';
        d.textAlign = 'left';
        d.textBaseline = 'middle';
        d.fillStyle = 'black';
        d.fillText(a, 7, 52);
        d.fillStyle = this.nc(b);
        d.fillText(a, 0, 45);
        return c
      }
    }
    class pc {
      constructor(a, b) {
        this.yn = 0;
        this.version = 1;
        this.oh = 0;
        this.Vd = A.ka(1000);
        this.Rf = A.ka(16384);
        this.version = b;
        let c = this.oh = a.Y;
        this.zj = a;
        a.U.ga(this.Rf);
        let d = this;
        a.hc = function (f) {
          let g = a.Y;
          d.Rf.nb(g - c);
          c = g;
          d.Rf.Xb(f.P);
          p.Cj(f, d.Rf)
        };
        this.Vd.Xb(0);
        let e = this.oh;
        a.U.Im(function (f) {
          let g = a.Y;
          d.Vd.nb(g - e);
          d.Vd.m(f);
          d.yn++;
          e = g
        })
      }
      stop() {
        this.zj.hc = null;
        this.zj.U.Im(null);
        this.Vd.s.setUint16(0, this.yn, this.Vd.Ua);
        this.Vd.Lb(this.Rf.Wb());
        let a = pako.deflateRaw(this.Vd.Wb()),
        b = A.ka(a.byteLength +
        32);
        b.pj('HBR2');
        b.tb(this.version);
        b.tb(this.zj.Y - this.oh);
        b.Lb(a);
        return b.Wb()
      }
    }
    class Ec {
      static Ym(a, b) {
        return new Promise(
          function (c, d) {
            let e = window.setTimeout(function () {
              d('Timed out')
            }, b);
            a.then(
              function (f) {
                window.clearTimeout(e);
                c(f)
              },
              function (f) {
                window.clearTimeout(e);
                d(f)
              }
            )
          }
        )
      }
    }
    class mb {
      constructor(a) {
        this.La = x.Ia(mb.Ij, 'tbody');
        var b = x.Ba(this.La);
        let c = b.get('name'),
        d = b.get('players'),
        e = b.get('distance'),
        f = b.get('pass');
        b = b.get('flag');
        this.rt = a;
        let g = a.je;
        c.textContent = g.D;
        d.textContent = '' + g.K + '/' + g.lf;
        f.textContent = g.Jb ? 'Yes' : 'No';
        e.textContent = '' + (a.Ze | 0) + 'km';
        try {
          b.classList.add('f-' + g.ub.toLowerCase())
        } catch (h) {
        }
        9 > a.je.Ee &&
        this.La.classList.add('old')
      }
    }
    class Ub {
      constructor() {
        this.Qc = new Set;
        this.ng = 0;
        window.document.addEventListener('focusout', M(this, this.zl))
      }
      la() {
        window.document.removeEventListener('focusout', M(this, this.zl))
      }
      A() {
        let a = 0;
        this.Qc.has('Up') &&
        (a = 1);
        this.Qc.has('Down') &&
        (a |= 2);
        this.Qc.has('Left') &&
        (a |= 4);
        this.Qc.has('Right') &&
        (a |= 8);
        this.Qc.has('Kick') &&
        (a |= 16);
        if (null != this.Bg && a != this.ng) {
          this.ng = a;
          let b = new La;
          b.input = a;
          this.Bg(b)
        }
      }
      Fa(a) {
        var b = a.code;
        b = m.j.Jd.v().v(b);
        null != b &&
        (a.preventDefault(), this.tq(b))
      }
      ld(a) {
        a = m.j.Jd.v().v(a.code);
        null != a &&
        this.jq(a)
      }
      tq(a) {
        this.Qc.has(a) ||
        (this.Qc.add(a), this.A(), D.h(this.xl, a))
      }
      jq(a) {
        this.Qc.delete(a) &&
        this.A()
      }
      zl() {
        if (null != this.Bg && 0 != this.ng) {
          this.Qc.clear();
          this.ng = 0;
          let a = new La;
          a.input = 0;
          this.Bg(a)
        }
      }
    }
    class wa {
      constructor() {
        this.pd = 16777215;
        this.hb = []
      }
      ga(a) {
        a.m(this.sd);
        a.R(this.pd);
        a.m(this.hb.length);
        let b = 0,
        c = this.hb;
        for (; b < c.length; ) a.R(c[b++])
      }
      ma(a) {
        this.sd = a.F();
        this.pd = a.N();
        let b = a.F();
        if (3 < b) throw v.C('too many');
        this.hb = [];
        let c = 0;
        for (; c < b; ) ++c,
        this.hb.push(a.N())
      }
    }
    class B {
      static Yp() {
        C.xj(function () {
          B.Ek(B.fr)
        });
        B.Pp()
      }
      static Pp() {
        let a = m.j.Yj.v();
        null == a ? U.ep().then(function (b) {
          B.Xe = b;
          m.j.Yj.ha(b.ts())
        }).catch(function () {
        }) : U.cp(a).then(function (b) {
          return B.Xe = b
        }).catch(function () {
        })
      }
      static hp() {
        let a = Cc.pn();
        return null != a ? null != a.getItem('crappy_router') : !1
      }
      static Ek(a) {
        let b = new zb(m.j.pe.v());
        b.Bl = function (c) {
          m.j.pe.ha(c);
          m.Qa.rm();
          a()
        };
        C.Na(b.f);
        b.Db.focus()
      }
      static Fk(a, b) {
        a = new ca(a);
        a.Wa = b;
        C.Na(a.f)
      }
      static To(a, b) {
        function c() {
          let f = new ab('Failed', null);
          f.Wa = function () {
            B.xb()
          };
          C.Na(f.f)
        }
        function d(f) {
          f = f.sitekey;
          if (null == f) throw v.C(null);
          B.Fk(f, function (g) {
            e(a, g)
          })
        }
        C.Na((new ba('Connecting', 'Connecting...', [])).f);
        let e = null;
        e = function (f, g) {
          Z.Yl(m.Se + 'api/client', 'room=' + f + '&rcr=' + g, Z.Lj).then(
            function (h) {
              switch (h.action) {
                case 'connect':
                  h = h.token;
                  if (null == h) throw v.C(null);
                  b(h);
                  break;
                case 'recaptcha':
                  d(h);
                  break;
                default:
                  throw v.C(null);
              }
            }
          ).catch(function () {
            c()
          })
        };
        e(a, '')
      }
      static fr() {
        let a = Dc.v(),
        b = a.get('c'),
        c = a.get('p');
        a.get('v');
        null != b ? null != c ? B.Ph(b) : B.eg(b) : B.xb()
      }
      static xb() {
        let a = new Ua(m.j.Wh());
        C.Na(a.La);
        a.zn = function (b) {
          if (9 != b.je.Ee) {
            let c = new ba(
              'Incompatible version',
              'The room is running a different version.',
              [
                'Ok'
              ]
            );
            C.Na(c.f);
            c.Wa = function () {
              C.Na(a.La);
              c.Wa = null
            }
          } else b.je.Jb ? B.Ph(b.ba) : B.eg(b.ba)
        };
        a.it = function () {
          B.Uo()
        };
        a.ht = function () {
          B.Ek(B.xb)
        };
        a.kt = function () {
          B.Hk()
        };
        a.jt = function (b) {
          B.Vo(b)
        }
      }
      static Hk() {
        let a = new na(!0),
        b = window.document.createElement('div');
        b.className = 'view-wrapper';
        b.appendChild(a.f);
        C.Na(b);
        a.rb = function () {
          B.xb()
        };
        a.mq = function () {
          let c = new Ab,
          d = window.document.createElement('div');
          d.className = 'view-wrapper';
          d.appendChild(c.f);
          C.Na(d);
          c.rb = function () {
            B.Hk()
          }
        }
      }
      static pi(a, b) {
        return '' + pa.location.origin + '/play?c=' + a + (b ? '&p=1' : '')
      }
      static Uo() {
        let a = m.j.pe.v(),
        b = new Bb('' + a + '\'s room');
        C.Na(b.f);
        b.ti = function () {
          B.xb()
        };
        b.rq = function (c) {
          function d() {
            if (!c.vt) {
              var t = new Sb;
              t.Ee = 9;
              t.D = g.lc;
              t.K = g.K.length;
              t.lf = k.tg + 1;
              t.ub = f.ub;
              t.Jb = null != k.Jb;
              t.Jc = f.Jc;
              t.Mc = f.Mc;
              var z = A.ka(16);
              t.ga(z);
              k.Vi(z.Vg())
            }
          }
          C.Na((new ba('Creating room', 'Connecting...', [])).f);
          let e = null,
          f = m.j.Wh(),
          g = new xa;
          g.lc = c.name;
          let h = new ya;
          h.D = a;
          h.fb = !0;
          h.country = f.ub;
          h.Zb = m.j.Ah.v();
          g.K.push(h);
          let k = new Zb({
            iceServers: m.kg,
            Aj: m.Se + 'api/host',
            state: g,
            version: 9
          });
          k.tg = c.dt - 1;
          k.Jb = c.password;
          d();
          let l = new Ca(k),
          n = !1;
          k.vf = function (t, z) {
            B.Fk(t, function (K) {
              z(K);
              C.Na(l.l.f);
              n = !0
            })
          };
          let r = window.setInterval(function () {
            k.ta(Ma.qa(k))
          }, 3000);
          k.yl = function (t) {
            null != g.oa(t) &&
            k.ta(ma.qa(t, 'Bad actor', !1))
          };
          k.pq = function (t, z) {
            let K = z.kc();
            if (25 < K.length) throw v.C('name too long');
            let N = z.kc();
            if (3 < N.length) throw v.C('country too long');
            z = z.Ab();
            if (null != z && 2 < z.length) throw v.C('avatar too long');
            k.ta(Na.qa(t, K, N, z));
            d()
          };
          k.qq = function (t) {
            null != g.oa(t) &&
            k.ta(ma.qa(t, null, !1))
          };
          k.yg = function (t) {
            e = t;
            l.Ng = B.pi(t, null != k.Jb);
            n ||
            (n = !0, C.Na(l.l.f))
          };
          l.Uh.wq = function (t, z, K, N) {
            k.Zo(t, z, K, N)
          };
          l.Uh.xq = function () {
            d()
          };
          l.l.ne = function () {
            k.la();
            l.la();
            B.xb();
            window.clearInterval(r)
          };
          l.dg.Rg = function (t) {
            k.Jb = t;
            d();
            null != e &&
            (l.Ng = B.pi(e, null != k.Jb))
          };
          l.dg.Hm = function (t) {
            k.Ui(t)
          };
          l.dg.ce = M(k, k.ce)
        }
      }
      static Ph(a) {
        let b = new Cb;
        C.Na(b.f);
        b.Wa = function (c) {
          null == c ? B.xb() : B.eg(a, c)
        }
      }
      static Vo(a) {
        try {
          let b = new qc(new $b(new Uint8Array(a), new xa, 3));
          b.se.ne = function () {
            b.la();
            B.xb()
          };
          C.Na(b.l.f)
        } catch (b) {
          let c = v.Mb(b).Fb();
          if (c instanceof ac) a = new ba(
            'Incompatible replay version',
            'The replay file is of a different version',
            [
              'Open player',
              'Cancel'
            ]
          ),
          C.Na(a.f),
          a.Wa = function (d) {
            0 == d ? (
              d = window.top.location,
              window.top.open(
                d.protocol + '//' + d.hostname + (null != d.port ? ':' + d.port : '') + '/replay?v=' + c.Ee,
                '_self'
              )
            ) : B.xb()
          };
           else {
            let d = new ba('Replay error', 'Couldn\'t load the file.', [
              'Ok'
            ]);
            C.Na(d.f);
            d.Wa = function () {
              d.Wa = null;
              B.xb()
            }
          }
        }
      }
      static eg(a, b, c) {
        try {
          let d = B.hp(),
          e = new xa,
          f = A.ka();
          f.oc(m.j.pe.v());
          f.oc(m.j.Wh().ub);
          f.Eb(m.j.Ah.v());
          let g = new Oa(
            a,
            {
              iceServers: m.kg,
              Aj: m.Hs,
              state: e,
              version: 9,
              xt: f.Vg(),
              password: b,
              En: d,
              Kn: c,
              Rs: B.Xe
            }
          ),
          h = new ub;
          h.da('Connecting to master...');
          h.Fh.onclick = function () {
            g.Id = null;
            g.uf = null;
            g.la();
            B.xb()
          };
          C.Na(h.f);
          let k = function (r, t) {
            r = new ab(r, t);
            r.Wa = function () {
              B.xb()
            };
            C.Na(r.f)
          },
          l = function () {
            let r = new ba('Connection Failed', '', [
              'Ok'
            ]);
            r.de.innerHTML = '<p>Failed to connect to room host.</p><p>If this problem persists please see the <a href=\'https://github.com/haxball/haxball-issues/wiki/Connection-Issues\' target=\'_blank\'>troubleshooting guide</a>.</p>';
            r.Wa = function () {
              B.xb()
            };
            C.Na(r.f)
          },
          n = function () {
            let r = new Ca(g);
            g.Cl = function (t) {
              r.l.Jf.$r(g.Gg.mh() | 0, g.Gg.max() | 0);
              r.l.Jf.Ml.Wn(t)
            };
            r.Ng = B.pi(a, !1);
            C.Na(r.l.f);
            r.l.ne = function () {
              g.Id = null;
              g.la();
              r.la();
              B.xb()
            };
            g.Id = function () {
              g.Id = null;
              r.la();
              let t = null == r.Nd ? null : r.Nd.stop();
              k(g.zk, t)
            }
          };
          g.uf = function (r) {
            g.uf = null;
            g.Id = null;
            switch (r.pb) {
              case 1:
                l();
                break;
              case 2:
                switch (r.reason) {
                  case 4004:
                    B.To(a, function (t) {
                      B.eg(a, b, t)
                    });
                    break;
                  case 4101:
                    null == b ? B.Ph(a) : k(Oa.Jh(r), null);
                    break;
                  default:
                    k(Oa.Jh(r), null)
                }
                break;
              default:
                k(Oa.Jh(r), null)
            }
          };
          g.Id = function (r) {
            switch (r) {
              case 1:
                h.da('Connecting to peer...');
                break;
              case 2:
                h.da('Awaiting state...');
                break;
              case 3:
                n()
            }
          };
          g.Bq = function () {
            h.da('Trying reverse connection...')
          }
        } catch (d) {
          c = v.Mb(d).Fb(),
          pa.console.log(c),
          c = new ba('Unexpected Error', '', []),
          c.de.innerHTML = 'An error ocurred while attempting to join the room.<br><br>This might be caused by a browser extension, try disabling all extensions and refreshing the site.<br><br>The error has been printed to the inspector console.',
          C.Na(c.f)
        }
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
        this.S = 0
      }
      ga(a) {
        let b = 0,
        c = a.a;
        a.m(0);
        a.m(this.$.Dd);
        a.m(this.ea.Dd);
        0 != this.Hc &&
        (b = 1, a.u(this.Hc));
        this.vb != 1 / 0 &&
        (b |= 2, a.u(this.vb));
        0 != this.S &&
        (b |= 4, a.R(this.S));
        this.bb &&
        (b |= 8);
        a.s.setUint8(c, b);
        a.u(this.o);
        a.R(this.i);
        a.R(this.B)
      }
      ma(a, b) {
        let c = a.F();
        this.$ = b[a.F()];
        this.ea = b[a.F()];
        this.Hc = 0 != (c & 1) ? a.w() : 0;
        this.vb = 0 != (c & 2) ? a.w() : 1 / 0;
        this.S = 0 != (c & 4) ? a.N() : 0;
        this.bb = 0 != (c & 8);
        this.o = a.w();
        this.i = a.N();
        this.B = a.N()
      }
      Vc(a) {
        a *=
        0.017453292519943295;
        if (0 > a) {
          a = - a;
          let b = this.$;
          this.$ = this.ea;
          this.ea = b;
          this.Hc = - this.Hc
        }
        a > I.On &&
        a < I.Nn &&
        (this.vb = 1 / Math.tan(a / 2))
      }
      ip() {
        return 0 != 0 * this.vb ? 0 : 114.59155902616465 * Math.atan(1 / this.vb)
      }
      qe() {
        if (0 == 0 * this.vb) {
          var a = this.ea.a,
          b = this.$.a,
          c = 0.5 * (a.x - b.x);
          a = 0.5 * (a.y - b.y);
          b = this.$.a;
          let d = this.vb;
          this.fe = new P(b.x + c + - a * d, b.y + a + c * d);
          a = this.$.a;
          b = this.fe;
          c = a.x - b.x;
          a = a.y - b.y;
          this.tk = Math.sqrt(c * c + a * a);
          c = this.$.a;
          a = this.fe;
          this.Sg = new P( - (c.y - a.y), c.x - a.x);
          c = this.fe;
          a = this.ea.a;
          this.Tg = new P( - (c.y -
          a.y), c.x - a.x);
          0 >= this.vb &&
          (a = c = this.Sg, c.x = - a.x, c.y = - a.y, a = c = this.Tg, c.x = - a.x, c.y = - a.y)
        } else a = this.$.a,
        b = this.ea.a,
        c = a.x - b.x,
        a = - (a.y - b.y),
        b = Math.sqrt(a * a + c * c),
        this.ya = new P(a / b, c / b)
      }
    }
    class ab {
      constructor(a, b) {
        this.f = x.Ia(ab.O);
        let c = x.Ba(this.f);
        this.iq = c.get('ok');
        let d = this;
        this.iq.onclick = function () {
          H.h(d.Wa)
        };
        this.mm = c.get('replay');
        let e = null != b;
        this.mm.hidden = !e;
        e &&
        (this.mm.onclick = function () {
          Ca.wm(b)
        });
        c.get('reason').textContent = a
      }
    }
    class tc {
      constructor(a) {
        this.rl = new kc(15);
        this.ci = 0;
        this.Pj = new Map;
        this.np = new pb(100, 16);
        this.Lg = !1;
        this.zb = 0;
        this.ua = a;
        a = A.ka(8);
        a.u(Math.random());
        this.Ve = a.Wb()
      }
      Vb(a, b) {
        null == b &&
        (b = 0);
        this.ua.Vb(b, a)
      }
    }
    class Vb {
      constructor(a, b) {
        this.za = a;
        this.da = b
      }
      xf(a) {
        if ('/' != a.charAt(0)) return !1;
        if (1 == a.length) return !0;
        a = aa.st(O.substr(a, 1, null)).split(' ');
        let b = a[0],
        c = this;
        switch (b) {
          case 'avatar':
            2 == a.length &&
            (this.Em(a[1]), this.da('Avatar set'));
            break;
          case 'checksum':
            var d = this.za.U.T;
            a = d.D;
            d.cf() ? this.da('Current stadium is original: "' + a + '"') : (
              d = aa.hh(d.lk(), 8),
              this.da('Stadium: "' + a + '" (checksum: ' + d + ')')
            );
            break;
          case 'clear_avatar':
            this.Em(null);
            this.da('Avatar cleared');
            break;
          case 'clear_bans':
            null == this.ce ? this.da('Only the host can clear bans') : (this.ce(), this.da('All bans have been cleared'));
            break;
          case 'clear_password':
            null == this.Rg ? this.da('Only the host can change the password') : (this.Rg(null), this.da('Password cleared'));
            break;
          case 'colors':
            try {
              d = Vb.Mq(a),
              this.za.ta(d)
            } catch (g) {
              a = v.Mb(g).Fb(),
              'string' == typeof a &&
              this.da(a)
            }
            break;
          case 'extrapolation':
            2 ==
            a.length ? (
              a = Q.parseInt(a[1]),
              null != a &&
              - 200 <= a &&
              1000 >= a ? (
                m.j.Ad.ha(a),
                this.za.Fm(a),
                this.da('Extrapolation set to ' + a + ' msec')
              ) : this.da(
                'Extrapolation must be a value between -200 and 1000 milliseconds'
              )
            ) : this.da('Extrapolation requires a value in milliseconds.');
            break;
          case 'handicap':
            2 == a.length ? (
              a = Q.parseInt(a[1]),
              null != a &&
              0 <= a &&
              300 >= a ? (this.za.Vr(a), this.da('Ping handicap set to ' + a + ' msec')) : this.da(
                'Ping handicap must be a value between 0 and 300 milliseconds'
              )
            ) : this.da('Ping handicap requires a value in milliseconds.');
            break;
          case 'kick_ratelimit':
            if (4 > a.length) this.da('Usage: /kick_ratelimit <min> <rate> <burst>');
             else {
              d = Q.parseInt(a[1]);
              var e = Q.parseInt(a[2]);
              a = Q.parseInt(a[3]);
              null == d ||
              null == e ||
              null == a ? this.da('Invalid arguments') : this.za.ta(Pa.qa(d, e, a))
            }
            break;
          case 'recaptcha':
            if (null == this.Hm) this.da('Only the host can set recaptcha mode');
             else try {
              if (2 == a.length) {
                switch (a[1]) {
                  case 'off':
                    e = !1;
                    break;
                  case 'on':
                    e = !0;
                    break;
                  default:
                    throw v.C(null);
                }
                this.Hm(e);
                this.da('Room join Recaptcha ' + (e ? 'enabled' : 'disabled'))
              } else throw v.C(null);
            } catch (g) {
              this.da('Usage: /recaptcha <on|off>')
            }
            break;
          case 'set_password':
            2 == a.length &&
            (
              null == this.Rg ? this.da('Only the host can change the password') : (this.Rg(a[1]), this.da('Password set'))
            );
            break;
          case 'store':
            let f = this.za.U.T;
            f.cf() ? this.da('Can\'t store default stadium.') : ib.qt().then(function () {
              return ib.add(f)
            }).then(
              function () {
                c.da('Stadium stored')
              },
              function () {
                c.da('Couldn\'t store stadium')
              }
            );
            break;
          default:
            this.da('Unrecognized command: "' + b + '"')
        }
        return !0
      }
      Em(a) {
        null != a &&
        (a = ha.Xc(a, 2));
        m.j.Ah.ha(a);
        this.za.ta(Qa.qa(a))
      }
      static Mq(a) {
        if (3 > a.length) throw v.C('Not enough arguments');
        if (7 < a.length) throw v.C('Too many arguments');
        let b = new bb,
        c = new wa;
        b.eh = c;
        switch (a[1]) {
          case 'blue':
            c.hb = [
              u.Da.S
            ];
            b.fa = u.Da;
            break;
          case 'red':
            c.hb = [
              u.ia.S
            ];
            b.fa = u.ia;
            break;
          default:
            throw v.C('First argument must be either "red" or "blue"');
        }
        if ('clear' == a[2]) return b;
        c.sd = 256 * Q.parseInt(a[2]) / 360 | 0;
        c.pd = Q.parseInt('0x' + a[3]);
        if (4 < a.length) {
          c.hb = [];
          let d = 4,
          e = a.length;
          for (; d < e; ) c.hb.push(Q.parseInt('0x' + a[d++]))
        }
        return b
      }
    }
    class xb {
      constructor(a) {
        this.Ak = !1;
        this.Om = new Ka(u.Oa);
        this.ck = new Ka(u.Da);
        this.gm = new Ka(u.ia);
        this.f = x.Ia(xb.O);
        let b = x.Ba(this.f);
        this.lc = b.get('room-name');
        this.Rm = b.get('start-btn');
        this.Tm = b.get('stop-btn');
        this.wi = b.get('pause-btn');
        this.$n = b.get('auto-btn');
        this.gl = b.get('lock-btn');
        this.qm = b.get('reset-all-btn');
        this.em = b.get('rec-btn');
        let c = b.get('link-btn'),
        d = b.get('leave-btn'),
        e = b.get('rand-btn');
        this.Lf = b.get('time-limit-sel');
        this.Ef = b.get('score-limit-sel');
        this.Pm = b.get('stadium-name');
        this.Qm = b.get('stadium-pick');
        let f = this;
        this.Qm.onclick = function () {
          H.h(f.Gq)
        };
        this.ei(b.get('red-list'), this.gm, a);
        this.ei(b.get('blue-list'), this.ck, a);
        this.ei(b.get('spec-list'), this.Om, a);
        this.nl(this.Lf, this.ml());
        this.nl(this.Ef, this.ml());
        this.Lf.onchange = function () {
          D.h(f.Kq, f.Lf.selectedIndex)
        };
        this.Ef.onchange = function () {
          D.h(f.Cq, f.Ef.selectedIndex)
        };
        this.Rm.onclick = function () {
          H.h(f.Hq)
        };
        this.Tm.onclick = function () {
          H.h(f.Iq)
        };
        this.wi.onclick = function () {
          H.h(f.vq)
        };
        this.$n.onclick = function () {
          H.h(f.lq)
        };
        this.gl.onclick = function () {
          D.h(f.Jq, !f.ji)
        };
        this.qm.onclick = function () {
          null != f.oe &&
          (f.oe(u.Da), f.oe(u.ia))
        };
        this.em.onclick = function () {
          H.h(f.zq)
        };
        c.onclick = function () {
          H.h(f.Fq)
        };
        d.onclick = function () {
          H.h(f.ne)
        };
        e.onclick = function () {
          H.h(f.yq)
        };
        this.Tj(!1);
        this.Uj(!1)
      }
      ei(a, b, c) {
        x.replaceWith(a, b.f);
        let d = this;
        b.Ag = function (e, f) {
          za.h(d.Ag, e, f)
        };
        b.oe = function (e) {
          D.h(d.oe, e)
        };
        b.sq = function (e) {
          za.h(d.Ag, c, e)
        };
        b.wf = function (e) {
          D.h(d.wf, e)
        }
      }
      ml() {
        let a = [],
        b = 0;
        for (; 15 > b; ) {
          let c = b++;
          a.push(null == c ? 'null' : '' +
          c)
        }
        return a
      }
      nl(a, b) {
        let c = 0;
        for (; c < b.length; ) {
          let d = b[c++],
          e = window.document.createElement('option');
          e.textContent = d;
          a.appendChild(e)
        }
      }
      bs(a) {
        this.em.classList.toggle('active', a)
      }
      A(a, b) {
        this.Dr != a.lc &&
        (this.Dr = a.lc, this.lc.textContent = a.lc);
        b = null == b ? !1 : b.fb;
        this.Ak != b &&
        (this.f.className = 'room-view' + (b ? ' admin' : ''), this.Ak = b);
        var c = !b ||
        null != a.M;
        this.Lf.disabled = c;
        this.Ef.disabled = c;
        this.Qm.disabled = c;
        c = null != a.M;
        this.Rm.hidden = c;
        this.Tm.hidden = !c;
        this.wi.hidden = !c;
        this.Lf.selectedIndex = a.Ga;
        this.Ef.selectedIndex = a.kb;
        this.Pm.textContent = a.T.D;
        this.Pm.classList.toggle('custom', !a.T.cf());
        let d = a.Ac;
        for (var e = this.gm, f = a.K, g = [], h = 0; h < f.length; ) {
          var k = f[h];
          ++h;
          k.fa == u.ia &&
          g.push(k)
        }
        e.A(g, d, c, b);
        e = this.ck;
        f = a.K;
        g = [];
        for (h = 0; h < f.length; ) k = f[h],
        ++h,
        k.fa == u.Da &&
        g.push(k);
        e.A(g, d, c, b);
        e = this.Om;
        f = a.K;
        g = [];
        for (h = 0; h < f.length; ) k = f[h],
        ++h,
        k.fa == u.Oa &&
        g.push(k);
        e.A(g, d, c, b);
        this.qm.disabled = c;
        this.ji != a.Ac &&
        this.Tj(a.Ac);
        c &&
        (a = 120 == a.M.Ta, this.Kl != a && this.Uj(a))
      }
      Tj(a) {
        this.ji = a;
        this.gl.innerHTML = this.ji ? '<i class=\'icon-lock\'></i>Unlock' :
        '<i class=\'icon-lock-open\'></i>Lock'
      }
      Uj(a) {
        this.Kl = a;
        this.wi.innerHTML = '<i class=\'icon-pause\'></i>' + (this.Kl ? 'Resume (P)' : 'Pause (P)')
      }
    }
    class rb {
      constructor() {
        this.Bk = null;
        this.f = x.Ia(rb.O);
        var a = x.Ba(this.f);
        this.og = a.get('link');
        let b = a.get('copy');
        a = a.get('close');
        let c = this;
        this.og.onfocus = function () {
          c.og.select()
        };
        b.onclick = function () {
          c.og.select();
          return window.document.execCommand('Copy')
        };
        a.onclick = function () {
          H.h(c.rb)
        }
      }
      Yr(a) {
        this.Bk != a &&
        (this.Bk = a, this.og.value = a)
      }
    }
    class D {
      static h(a, b) {
        null !=
        a &&
        a(b)
      }
    }
    class zb {
      constructor(a) {
        function b() {
          d.Ic() &&
          null != d.Bl &&
          d.Bl(d.Db.value)
        }
        this.f = x.Ia(zb.O);
        let c = x.Ba(this.f);
        this.Db = c.get('input');
        this.rf = c.get('ok');
        let d = this;
        this.Db.maxLength = 25;
        this.Db.value = a;
        this.Db.oninput = function () {
          d.A()
        };
        this.Db.onkeydown = function (e) {
          13 == e.keyCode &&
          b()
        };
        this.rf.onclick = b;
        this.A()
      }
      Ic() {
        let a = this.Db.value;
        return 25 >= a.length ? 0 < a.length : !1
      }
      A() {
        this.rf.disabled = !this.Ic()
      }
    }
    class uc {
      constructor() {
        function a(g) {
          return new ta(
            g,
            f,
            function (h) {
              if (null == h) return null;
              try {
                return la.Th(h)
              } catch (k) {
                return null
              }
            },
            function (h) {
              if (null == h) return null;
              try {
                return h.Ce()
              } catch (k) {
                return null
              }
            }
          )
        }
        function b(g, h) {
          return new ta(
            g,
            f,
            function (k) {
              return null != k ? '0' != k : h
            },
            function (k) {
              return k ? '1' : '0'
            }
          )
        }
        function c(g, h) {
          return new ta(
            g,
            f,
            function (k) {
              let l = h;
              try {
                null != k &&
                (l = parseFloat(k))
              } catch (n) {
              }
              return l
            },
            function (k) {
              return '' + k
            }
          )
        }
        function d(g, h) {
          return new ta(
            g,
            f,
            function (k) {
              let l = h;
              try {
                null != k &&
                (l = Q.parseInt(k))
              } catch (n) {
              }
              return l
            },
            function (k) {
              return '' + k
            }
          )
        }
        function e(g, h, k) {
          return new ta(
            g,
            f,
            function (l) {
              return null == l ? h : ha.Xc(l, k)
            },
            function (l) {
              return l
            }
          )
        }
        let f = Cc.pn();
        this.pe = e('player_name', '', 25);
        this.Rd = d('view_mode', - 1);
        this.Rh = d('fps_limit', 0);
        this.Ah = e('avatar', null, 2);
        e('rctoken', null, 1024);
        this.Vm = b('team_colors', !0);
        this.Uk = b('show_indicators', !0);
        this.Yi = c('sound_volume', 1);
        this.xe = b('sound_main', !0);
        this.Xi = b('sound_chat', !0);
        this.Nm = b('sound_highlight', !0);
        this.Mm = b('sound_crowd', !0);
        this.Yj = e('player_auth_key', null, 1024);
        this.Ad = d('extrapolation', 0);
        this.Mi = c('resolution_scale', 1);
        this.Km = b('show_avatars', !0);
        this.kk = d('chat_height', 160);
        this.Hh = d('chat_focus_height', 140);
        this.Ih = c('chat_opacity', 0.8);
        this.jk = e('chat_bg_mode', 'compact', 50);
        this.li = b('low_latency_canvas', !0);
        this.$e = a('geo');
        this.af = a('geo_override');
        this.Jd = function () {
          return new ta(
            'player_keys',
            f,
            function (g) {
              if (null == g) return sa.vk();
              try {
                return sa.Th(g)
              } catch (h) {
                return sa.vk()
              }
            },
            function (g) {
              try {
                return g.Ce()
              } catch (h) {
                return null
              }
            }
          )
        }()
      }
      Wh() {
        return null != this.af.v() ? this.af.v() : null != this.$e.v() ? this.$e.v() :
        new la
      }
    }
    class Fc {
      constructor(a) {
        this.current = 0;
        this.Ks = a
      }
      next() {
        return this.Ks[this.current++]
      }
    }
    class P {
      constructor(a, b) {
        this.x = a;
        this.y = b
      }
    }
    class kb {
      constructor(a) {
        this.f = x.Ia(kb.O);
        x.Ba(this.f).get('features').textContent = a.join(', ')
      }
    }
    class vc {
      constructor(a, b) {
        this.uh = null;
        this.ut = 0.025;
        this.He = this.qh = this.Sf = 0;
        this.fh = b.createGain();
        this.fh.gain.value = 0;
        b = b.createBufferSource();
        b.buffer = a;
        b.connect(this.fh);
        b.loop = !0;
        b.start()
      }
      update() {
        var a = window.performance.now();
        let b = a - this.vn;
        this.vn = a;
        this.He += (this.qh - this.He) * this.ut;
        this.Sf -= b;
        0 >= this.Sf &&
        (this.Sf = this.qh = 0);
        0 >= this.qh &&
        0.05 > this.He &&
        (window.clearInterval(this.uh), this.uh = null, this.He = 0);
        a = m.j.Mm.v() ? this.He : 0;
        this.fh.gain.value = a
      }
      Fj(a) {
        this.qh = a;
        this.Sf = 166.66666666666666;
        let b = this;
        null == this.uh &&
        (
          this.uh = window.setInterval(function () {
            b.update()
          }, 17),
          this.vn = window.performance.now()
        )
      }
      connect(a) {
        this.fh.connect(a)
      }
      wt(a) {
        let b = a.M;
        if (null != b) if (2 == b.Cb) 0 >= b.Ta &&
        this.Fj(1);
         else if (1 == b.Cb) {
          let e = b.va.H[0],
          f = null,
          g = null,
          h = null,
          k = 0,
          l = null,
          n = null,
          r = null,
          t = 0,
          z = u.ia.Oh,
          K = 0;
          for (a = a.K; K < a.length; ) {
            let N = a[K];
            ++K;
            if (null == N.I) continue;
            var c = N.I.a;
            let Db = e.a;
            var d = c.x - Db.x;
            c = c.y - Db.y;
            d = d * d + c * c;
            if (N.fa == u.ia) {
              if (null == f || f.a.x * z < N.I.a.x * z) f = N.I;
              if (null == g || g.a.x * z > N.I.a.x * z) g = N.I;
              if (null == h || d < k) h = N.I,
              k = d
            } else if (N.fa == u.Da) {
              if (null == l || l.a.x * z < N.I.a.x * z) l = N.I;
              if (null == n || n.a.x * z > N.I.a.x * z) n = N.I;
              if (null == r || d < t) r = N.I,
              t = d
            }
          }
          null != n &&
          null != g &&
          0 >= b.Ta &&
          (
            h.a.x > n.a.x &&
            e.a.x > n.a.x &&
            20 < e.a.x &&
            this.Fj(0.3),
            r.a.x < g.a.x &&
            e.a.x < g.a.x &&
            - 20 > e.a.x &&
            this.Fj(0.3)
          )
        }
      }
    }
    class ca {
      constructor(a) {
        let b = new ba('Only humans', '', []);
        this.f = b.f;
        b.de.style.minHeight = '78px';
        let c = this;
        vb.Op().then(
          function (d) {
            null == ca.Kg &&
            (
              ca.Kg = window.document.createElement('div'),
              b.de.appendChild(ca.Kg),
              ca.lr = d.render(
                ca.Kg,
                {
                  sitekey: a,
                  callback: function (e) {
                    D.h(ca.fm, e)
                  },
                  theme: 'dark'
                }
              )
            );
            d.reset(ca.lr);
            ca.fm = function (e) {
              window.setTimeout(function () {
                D.h(c.Wa, e)
              }, 1000);
              ca.fm = null
            };
            b.de.appendChild(ca.Kg)
          }
        )
      }
    }
    class Jc {
      static xj() {
        p.Ja(Eb);
        p.Ja(Ha);
        p.Ja(cb);
        p.Ja(La);
        p.Ja(Ya);
        p.Ja(Na);
        p.Ja(ma);
        p.Ja(Va);
        p.Ja(Wa);
        p.Ja(Za);
        p.Ja(va);
        p.Ja(Ea);
        p.Ja(fa);
        p.Ja(Fa);
        p.Ja(Ga);
        p.Ja(Xa);
        p.Ja(Da);
        p.Ja(Ma);
        p.Ja(Qa);
        p.Ja(bb);
        p.Ja(Fb);
        p.Ja(Pa);
        p.Ja(Gb);
        p.Ja(Hb)
      }
    }
    class H {
      static h(a) {
        null != a &&
        a()
      }
    }
    class m {
    }
    class Ra {
    }
    class w {
      static nn(a) {
        if (null == a) return null;
        if (a instanceof Array) return Array;
        {
          let b = a.g;
          if (null != b) return b;
          a = w.Nj(a);
          return null != a ? w.Un(a) : null
        }
      }
      static Pe(a, b) {
        if (null == a) return 'null';
        if (5 <= b.length) return '<...>';
        var c = typeof a;
        'function' == c &&
        (a.b || a.Wf) &&
        (c = 'object');
        switch (c) {
          case 'function':
            return '<function>';
          case 'object':
            if (a.Gb) {
              var d = Ib[a.Gb].$d[a.pb];
              c = d.wc;
              if (d.Oe) {
                b += '\t';
                var e = [],
                f = 0;
                for (d = d.Oe; f < d.length; ) {
                  let g = d[f];
                  f += 1;
                  e.push(w.Pe(a[g], b))
                }
                a = e;
                return c + '(' + a.join(',') + ')'
              }
              return c
            }
            if (a instanceof Array) {
              c = '[';
              b += '\t';
              e = 0;
              for (f = a.length; e < f; ) d = e++,
              c += (0 < d ? ',' : '') + w.Pe(a[d], b);
              return c += ']'
            }
            try {
              e = a.toString
            } catch (g) {
              return '???'
            }
            if (
              null != e &&
              e != Object.toString &&
              'function' == typeof e &&
              (c = a.toString(), '[object Object]' != c)
            ) return c;
            c = '{\n';
            b += '\t';
            e = null != a.hasOwnProperty;
            f = null;
            for (f in a) e &&
            !a.hasOwnProperty(f) ||
            'prototype' == f ||
            '__class__' == f ||
            '__super__' == f ||
            '__interfaces__' == f ||
            '__properties__' == f ||
            (2 != c.length && (c += ', \n'), c += b + f + ' : ' + w.Pe(a[f], b));
            b = b.substring(1);
            return c += '\n' + b + '}';
          case 'string':
            return a;
          default:
            return String(a)
        }
      }
      static Mj(a, b) {
        for (; ; ) {
          if (null == a) return !1;
          if (a == b) return !0;
          let c = a.ad;
          if (null != c && (null == a.ja || a.ja.ad != c)) {
            let d = 0,
            e = c.length;
            for (; d < e; ) {
              let f = c[d++];
              if (f == b || w.Mj(f, b)) return !0
            }
          }
          a = a.ja
        }
      }
      static Sn(a, b) {
        if (null == b) return !1;
        switch (b) {
          case Array:
            return a instanceof Array;
          case Gc:
            return 'boolean' == typeof a;
          case Nc:
            return null != a;
          case E:
            return 'number' == typeof a;
          case bc:
            return 'number' == typeof a ? (a | 0) === a : !1;
          case String:
            return 'string' == typeof a;
          default:
            if (null != a) if ('function' == typeof b) {
              if (w.Rn(a, b)) return !0
            } else {
              if ('object' == typeof b && w.Tn(b) && a instanceof b) return !0
            } else return !1;
            return b == Oc &&
            null != a.b ||
            b == Pc &&
            null != a.Wf ? !0 : null != a.Gb ? Ib[a.Gb] == b : !1
        }
      }
      static Rn(a, b) {
        return a instanceof b ? !0 : b.xh ? w.Mj(w.nn(a), b) : !1
      }
      static J(a, b) {
        if (null == a || w.Sn(a, b)) return a;
        throw v.C('Cannot cast ' +
        Q.Je(a) + ' to ' + Q.Je(b));
      }
      static Nj(a) {
        a = w.Vn.call(a).slice(8, - 1);
        return 'Object' == a ||
        'Function' == a ||
        'Math' == a ||
        'JSON' == a ? null : a
      }
      static Tn(a) {
        return null != w.Nj(a)
      }
      static Un(a) {
        return pa[a]
      }
    }
    class ba {
      constructor(a, b, c) {
        this.f = x.Ia(ba.O);
        var d = x.Ba(this.f);
        d.get('ok');
        d.get('cancel');
        this.de = d.get('content');
        let e = d.get('title');
        d = d.get('buttons');
        let f = 0,
        g = this,
        h = 0;
        for (; h < c.length; ) {
          let k = c[h++],
          l = f++,
          n = window.document.createElement('button');
          n.textContent = k;
          n.onclick = function () {
            D.h(g.Wa, l)
          };
          d.appendChild(n)
        }
        this.de.textContent = b;
        e.textContent = a
      }
    }
    class O {
      static tj(a, b) {
        a = a.charCodeAt(b);
        if (a == a) return a
      }
      static substr(a, b, c) {
        if (null == c) c = a.length;
         else if (0 > c) if (0 == b) c = a.length + c;
         else return '';
        return a.substr(b, c)
      }
      static remove(a, b) {
        b = a.indexOf(b);
        if ( - 1 == b) return !1;
        a.splice(b, 1);
        return !0
      }
      static now() {
        return Date.now()
      }
    }
    class cc {
      constructor() {
        this.ff = 0;
        this.V = 15;
        this.B = 0;
        this.ra = new P(0, 0);
        this.ca = this.o = 0.5;
        this.Ea = 0.96;
        this.Qe = 0.1;
        this.gf = 0.07;
        this.hf = 0.96;
        this.ef = 5
      }
      ga(a) {
        a.u(this.o);
        a.u(this.ca);
        a.u(this.Ea);
        a.u(this.Qe);
        a.u(this.gf);
        a.u(this.hf);
        a.u(this.ef);
        let b = this.ra;
        a.u(b.x);
        a.u(b.y);
        a.R(this.B);
        a.u(this.V);
        a.u(this.ff)
      }
      ma(a) {
        this.o = a.w();
        this.ca = a.w();
        this.Ea = a.w();
        this.Qe = a.w();
        this.gf = a.w();
        this.hf = a.w();
        this.ef = a.w();
        let b = this.ra;
        b.x = a.w();
        b.y = a.w();
        this.B = a.N();
        this.V = a.w();
        this.ff = a.w()
      }
    }
    class Jb {
      constructor(a, b, c, d) {
        this.Bh = new Set;
        this.Yf = new Set;
        this.Mg = this.Cf = this.Cm = !1;
        this.Tc = null;
        this.Ff = this.ba = '';
        this.Jr = 50000;
        this.Ir = 10000;
        this.xd = new Map;
        this.js = a;
        this.kg = b;
        this.po = c;
        this.Ff = d;
        null == this.Ff &&
        (this.Ff = '');
        this.$i()
      }
      la() {
        window.clearTimeout(this.sm);
        window.clearTimeout(this.ue);
        this.ue = null;
        window.clearInterval(this.Nl);
        this.aa.onmessage = null;
        this.aa.onerror = null;
        this.aa.onclose = null;
        this.aa.onopen = null;
        this.aa.close();
        this.aa = null;
        this.Kk()
      }
      Vi(a) {
        if (null != this.Tc || null != a) {
          if (null != this.Tc && null != a && this.Tc.byteLength == a.byteLength) {
            let c = new Uint8Array(this.Tc),
            d = new Uint8Array(a),
            e = !1,
            f = 0,
            g = this.Tc.byteLength;
            for (; f < g; ) {
              let h = f++;
              if (c[h] != d[h]) {
                e = !0;
                break
              }
            }
            if (!e) return
          }
          this.Tc = a.slice(0);
          this.Mg = !0;
          var b = this;
          null != this.aa &&
          1 == this.aa.readyState &&
          null == this.ue &&
          (
            this.Qi(),
            this.ue = window.setTimeout(function () {
              b.ue = null;
              1 == b.aa.readyState &&
              b.Mg &&
              b.Qi()
            }, 10000)
          )
        }
      }
      Ui(a) {
        function b() {
          null != c.aa &&
          1 == c.aa.readyState &&
          c.Cf != c.Cm &&
          c.Bm();
          c.pm = null
        }
        this.Cf = a;
        let c = this;
        null == this.pm &&
        (b(), this.pm = window.setTimeout(b, 1000))
      }
      $i(a) {
        function b(e) {
          e = e.sitekey;
          if (null == e) throw v.C(null);
          null != d.vf &&
          d.vf(e, function (f) {
            d.$i(f)
          })
        }
        function c(e) {
          let f = e.url;
          if (null == f) throw v.C(null);
          e = e.token;
          if (null == e) throw v.C(null);
          d.aa = new WebSocket(f + '?token=' + e);
          d.aa.binaryType = 'arraybuffer';
          d.aa.onopen = function () {
            d.yp()
          };
          d.aa.onclose = function (g) {
            d.Xh(4001 != g.code)
          };
          d.aa.onerror = function () {
            d.Xh(!0)
          };
          d.aa.onmessage = M(d, d.ai)
        }
        null == a &&
        (a = '');
        let d = this;
        Z.Yl(this.js, 'token=' + this.Ff + '&rcr=' + a, Z.Lj).then(
          function (e) {
            switch (e.action) {
              case 'connect':
                c(e);
                break;
              case 'recaptcha':
                b(e)
            }
          }
        ).catch(function () {
          d.Xh(!0)
        })
      }
      yp() {
        null != this.Tc &&
        this.Qi();
        0 != this.Cf &&
        this.Bm();
        let a = this;
        this.Nl = window.setInterval(function () {
          a.Pi()
        }, 40000)
      }
      ai(a) {
        a = new J(new DataView(a.data), !1);
        switch (a.F()) {
          case 1:
            this.$h(a);
            break;
          case 4:
            this.Zh(a);
            break;
          case 5:
            this.tp(a);
            break;
          case 6:
            this.wp(a)
        }
      }
      $h(a) {
        let b = a.jb(),
        c = ha.Ms(a.sb(a.F())),
        d,
        e,
        f;
        try {
          a = new J(new DataView(pako.inflateRaw(a.sb()).buffer), !1);
          d = 0 != a.F();
          e = a.kc();
          let g = a.Jg(),
          h = [],
          k = 0;
          for (; k < g.length; ) h.push(new RTCIceCandidate(g[k++]));
          f = h
        } catch (g) {
          this.Hf(b, 0);
          return
        }
        this.xp(b, c, e, f, a, d)
      }
      xp(a, b, c, d, e, f) {
        if (16 <= this.xd.size) this.Hf(a, 4104);
         else if (this.Bh.has(b)) this.Hf(a, 4102);
         else {
          for (var g = [], h = 0; h < d.length; ) {
            let r = Jb.Pk(d[h++]);
            if (null != r) {
              if (this.Yf.has(r)) {
                this.Hf(a, 4102);
                return
              }
              g.push(r)
            }
          }
          if (null != this.qk && (h = new J(e.s), h.a = e.a, e = this.qk(b, h), 1 == e.pb)) {
            this.Hf(a, e.reason);
            return
          }
          var k = new Ja(a, this.kg, this.po);
          f &&
          (k.wk = 2500);
          k.ze = g;
          k.rd = b;
          this.xd.set(a, k);
          var l = this,
          n = function () {
            l.Uc(0, k, null);
            l.xd.delete(k.ba)
          };
          k.kd = n;
          k.Hd = function () {
            l.xd.delete(k.ba);
            l.Uc(0, k, null);
            null != l.Al &&
            l.Al(new Yb(k))
          };
          k.cj();
          (
            async function () {
              try {
                let r = await k.Jo(new RTCSessionDescription({
                  sdp: c,
                  type: 'offer'
                }), d);
                l.Ri(k, r, k.ig, null);
                k.jg.then(function () {
                  l.Uc(0, k, null)
                });
                k.xg = function (t) {
                  l.Oi(k, t)
                }
              } catch (r) {
                n()
              }
            }
          ) ()
        }
      }
      Zh(a) {
        let b = a.jb(),
        c;
        try {
          a = new J(new DataView(pako.inflateRaw(a.sb()).buffer), !1),
          c = new RTCIceCandidate(a.Jg())
        } catch (d) {
          return
        }
        this.sp(b, c)
      }
      sp(a, b) {
        a = this.xd.get(a);
        if (null != a) {
          let c = Jb.Pk(b);
          if (null != c && (a.ze.push(c), this.Yf.has(c))) return;
          a.Qj(b)
        }
      }
      tp(a) {
        this.ba = a.re(a.F());
        null != this.yg &&
        this.yg(this.ba)
      }
      wp(a) {
        this.Ff = a.re(a.s.byteLength - a.a)
      }
      Uc(a, b, c) {
        if (!b.Gl) {
          0 == a &&
          (b.Gl = !0);
          var d = b.ba;
          b = A.ka(32, !1);
          b.m(a);
          b.tb(d);
          null != c &&
          (a = pako.deflateRaw(c.Wb()), b.Lb(a));
          this.aa.send(b.Qd())
        }
      }
      Hf(a, b) {
        let c = A.ka(16, !1);
        c.m(0);
        c.tb(a);
        c.Xb(b);
        this.aa.send(c.Qd())
      }
      Pi() {
        let a = A.ka(1, !1);
        a.m(8);
        this.aa.send(a.Qd())
      }
      Qi() {
        this.Mg = !1;
        let a = A.ka(256, !1);
        a.m(7);
        null != this.Tc &&
        a.Yg(this.Tc);
        this.aa.send(a.Qd())
      }
      Bm() {
        let a = A.ka(2, !1);
        a.m(9);
        a.m(this.Cf ? 1 : 0);
        this.aa.send(a.Qd());
        this.Cm = this.Cf
      }
      Ri(a, b, c, d) {
        let e = A.ka(32, !1);
        e.oc(b.sdp);
        e.Zg(c);
        null != d &&
        e.Lb(d.Wb());
        this.Uc(1, a, e)
      }
      Oi(a, b) {
        let c = A.ka(32, !1);
        c.Zg(b);
        this.Uc(4, a, c)
      }
      Kk() {
        let a = this.xd.values(),
        b = a.next();
        for (; !b.done; ) {
          let c = b.value;
          b = a.next();
          c.la()
        }
        this.xd.clear()
      }
      Xh(a) {
        this.Kk();
        window.clearTimeout(this.ue);
        this.ue = null;
        this.Mg = !1;
        window.clearInterval(this.Nl);
        window.clearTimeout(this.sm);
        let b = this;
        a &&
        (
          this.sm = window.setTimeout(function () {
            b.$i()
          }, this.Ir + Math.random() * this.Jr | 0)
        )
      }
      co(a) {
        let b = 0,
        c = a.ze;
        for (; b < c.length; ) this.Yf.add(c[b++]);
        null != a.rd &&
        this.Bh.add(a.rd);
        return {
          Dt: a.ze,
          Bt: a.rd
        }
      }
      ce() {
        this.Yf.clear();
        this.Bh.clear()
      }
      static Pk(a) {
        try {
          let b = Kc.xf(a.candidate);
          if ('srflx' == b.vs) return b.Dp
        } catch (b) {
        }
        return null
      }
    }
    class yb {
      constructor(a) {
        this.D = a.D;
        this.zb = a.zb;
        this.ba = a.Z;
        this.f = x.Ia(yb.O);
        let b = x.Ba(this.f);
        this.nf = b.get('name');
        this.Fg = b.get('ping');
        try {
          b.get('flag').classList.add('f-' + a.country)
        } catch (d) {
        }
        this.nf.textContent = this.D;
        this.Fg.textContent = '' + this.zb;
        let c = this;
        this.f.ondragstart = function (d) {
          d.dataTransfer.setData('player', Q.Je(c.ba))
        };
        this.f.oncontextmenu = function (d) {
          d.preventDefault();
          D.h(c.wf, c.ba)
        };
        this.Dm(a.fb)
      }
      A(a, b) {
        this.f.draggable = b;
        this.zb != a.zb &&
        (this.zb = a.zb, this.Fg.textContent = '' + this.zb);
        this.Xn != a.fb &&
        this.Dm(a.fb)
      }
      Dm(a) {
        this.Xn = a;
        this.f.className = 'player-list-item' + (a ? ' admin' : '')
      }
    }
    class u {
      constructor(a, b, c, d, e, f, g, h) {
        this.Dg = null;
        this.ba = a;
        this.S = b;
        this.Oh = c;
        this.Jp = d;
        this.D = e;
        this.Oo = f;
        this.B = h;
        this.Um = new wa;
        this.Um.hb.push(b)
      }
    }
    class db {
      constructor() {
        this.list = []
      }
      rn(a) {
        let b = 0,
        c = a.ob,
        d = a.Dc,
        e = 0,
        f = this.list;
        for (; e < f.length; ) {
          var g = f[e];
          ++e;
          let h = g.ob;
          if (h > c) break;
          if (h == c) {
            g = g.Dc;
            if (g > d) break;
            g ==
            d &&
            ++d
          }
          ++b
        }
        a.Dc = d;
        this.list.splice(b, 0, a)
      }
      ot(a) {
        let b = 0,
        c = 0,
        d = this.list;
        for (; c < d.length && !(d[c++].ob >= a); ) ++b;
        this.list.splice(0, b)
      }
      Os(a, b) {
        let c = this.list;
        for (; 0 < c.length; ) c.pop();
        db.ft(a.list, b.list, this.list)
      }
      pt(a) {
        let b = 0,
        c = this.list,
        d = 0,
        e = c.length;
        for (; d < e; ) {
          let f = c[d++];
          f.Fe != a &&
          (c[b] = f, ++b)
        }
        for (; c.length > b; ) c.pop()
      }
      Ps(a) {
        let b = 0,
        c = 0,
        d = this.list;
        for (; c < d.length && !(d[c++].ob >= a); ) ++b;
        return b
      }
      static ft(a, b, c) {
        if (0 == a.length) for (a = 0; a < b.length; ) c.push(b[a++]);
         else if (0 == b.length) for (b = 0; b < a.length; ) c.push(a[b++]);
         else {
          let d = 0,
          e = a.length,
          f = 0,
          g = b.length;
          for (; ; ) {
            let h = a[d],
            k = b[f];
            if (h.ob <= k.ob) {
              if (c.push(h), ++d, d >= e) {
                for (; f < g; ) c.push(b[f++]);
                break
              }
            } else if (c.push(k), ++f, f >= g) {
              for (; d < e; ) c.push(a[d++]);
              break
            }
          }
        }
      }
    }
    class Kb {
      constructor() {
        this.Ae = u.Oa;
        this.ea = new P(0, 0);
        this.$ = new P(0, 0)
      }
      ga(a) {
        var b = this.$;
        a.u(b.x);
        a.u(b.y);
        b = this.ea;
        a.u(b.x);
        a.u(b.y);
        a.m(this.Ae.ba)
      }
      ma(a) {
        var b = this.$;
        b.x = a.w();
        b.y = a.w();
        b = this.ea;
        b.x = a.w();
        b.y = a.w();
        a = a.zf();
        this.Ae = 1 == a ? u.ia : 2 == a ? u.Da : u.Oa
      }
    }
    class Ta {
      constructor() {
        this.jc = - 1;
        this.ic = null;
        this.H = []
      }
      ga(a) {
        a.m(this.H.length);
        let b = 0,
        c = this.H.length;
        for (; b < c; ) {
          let d = b++,
          e = this.H[d];
          e.Il = d;
          e.ga(a)
        }
      }
      ma(a) {
        this.H = [];
        let b = a.F(),
        c = 0;
        for (; c < b; ) {
          ++c;
          let d = new ra;
          d.ma(a);
          this.H.push(d)
        }
      }
      A(a) {
        for (var b = 0, c = this.H; b < c.length; ) {
          var d = c[b];
          ++b;
          var e = d.a,
          f = d.a,
          g = d.G;
          e.x = f.x + g.x * a;
          e.y = f.y + g.y * a;
          f = e = d.G;
          g = d.ra;
          d = d.Ea;
          e.x = (f.x + g.x) * d;
          e.y = (f.y + g.y) * d
        }
        a = 0;
        for (b = this.H.length; a < b; ) {
          d = a++;
          c = this.H[d];
          d += 1;
          for (e = this.H.length; d < e; ) f = this.H[d++],
          0 != (f.i & c.B) &&
          0 != (f.B & c.i) &&
          c.wo(f);
          if (0 != c.ca) {
            d = 0;
            for (e = this.sa; d < e.length; ) if (f = e[d], ++d, 0 != (f.i & c.B) && 0 != (f.B & c.i)) {
              g = f.ya;
              var h = c.a;
              g = f.Va - (g.x * h.x + g.y * h.y) + c.V;
              if (0 < g) {
                var k = h = c.a,
                l = f.ya;
                h.x = k.x + l.x * g;
                h.y = k.y + l.y * g;
                g = c.G;
                h = f.ya;
                g = g.x * h.x + g.y * h.y;
                0 > g &&
                (g *= c.o * f.o + 1, k = h = c.G, f = f.ya, h.x = k.x - f.x * g, h.y = k.y - f.y * g)
              }
            }
            d = 0;
            for (e = this.X; d < e.length; ) f = e[d],
            ++d,
            0 != (f.i & c.B) &&
            0 != (f.B & c.i) &&
            c.xo(f);
            d = 0;
            for (e = this.L; d < e.length; ) if (
              f = e[d],
              ++d,
              0 != (f.i & c.B) &&
              0 != (f.B & c.i) &&
              (h = c.a, k = f.a, g = h.x - k.x, h = h.y - k.y, k = g * g + h * h, 0 < k && k <= c.V * c.V)
            ) {
              k = Math.sqrt(k);
              g /= k;
              h /= k;
              k = c.V - k;
              let n = l = c.a;
              l.x = n.x + g * k;
              l.y = n.y + h * k;
              k = c.G;
              k = g * k.x + h * k.y;
              0 > k &&
              (k *= c.o * f.o + 1, l = f = c.G, f.x = l.x - g * k, f.y = l.y - h * k)
            }
          }
        }
        for (a = 0; 2 > a; ) for (++a, b = 0, c = this.qb; b < c.length; ) c[b++].A(this.H)
      }
      uc() {
        let a = qa.Cc,
        b = this.ic;
        this.jc != a &&
        (null == b && (this.ic = b = new Ta), this.jc = a, Ta.zd(b, this));
        return b
      }
      static zd(a, b) {
        if (null == b.H) a.H = null;
         else {
          null == a.H &&
          (a.H = []);
          let d = a.H,
          e = b.H;
          for (var c = e.length; d.length > c; ) d.pop();
          c = 0;
          let f = e.length;
          for (; c < f; ) {
            let g = c++;
            d[g] = e[g].uc()
          }
        }
        a.L = b.L;
        a.X = b.X;
        a.sa = b.sa;
        a.qb = b.qb
      }
    }
    class la {
      constructor() {
        this.ub = '';
        this.Jc = this.Mc = 0
      }
      Ce() {
        return JSON.stringify({
          lat: this.Jc,
          lon: this.Mc,
          code: this.ub
        })
      }
      static Th(a) {
        return la.gg(JSON.parse(a))
      }
      static gg(a) {
        let b = new la;
        b.Jc = a.lat;
        b.Mc = a.lon;
        b.ub = a.code.toLowerCase();
        return b
      }
      static lp() {
        return Z.Nk(m.Se + 'api/geo').then(function (a) {
          return la.gg(a)
        })
      }
    }
    class nc {
      constructor() {
      }
    }
    class Sb {
      constructor() {
      }
      gk() {
        this.D = ha.Xc(this.D, 40);
        this.ub = ha.Xc(this.ub, 3)
      }
      ga(a) {
        this.gk();
        a.Ua = !0;
        a.Xb(this.Ee);
        a.jn(this.D);
        a.jn(this.ub);
        a.nj(this.Jc);
        a.nj(this.Mc);
        a.m(this.Jb ? 1 : 0);
        a.m(this.lf);
        a.m(this.K);
        a.Ua = !1
      }
      ma(a) {
        a.Ua = !0;
        this.Ee = a.Sb();
        this.D = a.dm();
        this.ub = a.dm();
        this.Jc = a.Ci();
        this.Mc = a.Ci();
        this.Jb = 0 != a.F();
        this.lf = a.F();
        this.K = a.F();
        a.Ua = !1;
        if (30 < this.K || 30 < this.lf) throw v.C(null);
        this.gk()
      }
    }
    class ha {
      static Xc(a, b) {
        return a.length <= b ? a : O.substr(a, 0, b)
      }
      static Ms(a) {
        let b = '',
        c = 0,
        d = a.byteLength;
        for (; c < d; ) b += aa.hh(a[c++], 2);
        return b
      }
    }
    class jc {
      constructor(a) {
        function b(d) {
          return new Promise(
            function (e) {
              let f = a.file(d).asArrayBuffer();
              c.c.decodeAudioData(f, e, function () {
                e(null)
              })
            }
          )
        }
        this.c = new AudioContext;
        this.qg = this.c.createGain();
        this.Gi();
        this.qg.connect(this.c.destination);
        let c = this;
        this.Xo = Promise.all(
          [b('sounds/chat.wav').then(function (d) {
            return c.ik = d
          }),
          b('sounds/highlight.wav').then(function (d) {
            return c.Tk = d
          }),
          b('sounds/kick.wav').then(function (d) {
            return c.Ip = d
          }),
          b('sounds/goal.wav').then(function (d) {
            return c.op = d
          }),
          b('sounds/join.wav').then(function (d) {
            return c.Gp = d
          }),
          b('sounds/leave.wav').then(function (d) {
            return c.Mp = d
          }),
          b('sounds/crowd.ogg').then(function (d) {
            c.No = d;
            c.sk = new vc(c.No, c.c);
            c.sk.connect(c.qg)
          })]
        )
      }
      rm() {
        this.c.resume()
      }
      md(a) {
        let b = this.c.createBufferSource();
        b.buffer = a;
        b.connect(this.qg);
        b.start()
      }
      Gi() {
        let a = m.j.Yi.v();
        m.j.xe.v() ||
        (a = 0);
        this.qg.gain.value = a
      }
    }
    class lb {
      constructor(a) {
        this.ql = a.get('notice');
        this.Ho = a.get('notice-contents');
        this.wd = a.get('notice-close');
        this.hm()
      }
      hm() {
        let a = this;
        Z.Nk(m.Se + 'api/notice').then(
          function (b) {
            let c = b.content;
            null != c &&
            '' != c &&
            lb.vo != c &&
            (
              a.Ho.innerHTML = c,
              a.ql.hidden = !1,
              a.wd.onclick = function () {
                lb.vo = c;
                return a.ql.hidden = !0
              }
            )
          }
        )
      }
    }
    class $a {
      constructor() {
        this.bf = this.fi = !1;
        this.f = x.Ia($a.O);
        let a = x.Ba(this.f);
        this.Lc = a.get('log');
        this.ki = a.get('log-contents');
        this.$a = a.get('input');
        this.$a.maxLength = 140;
        let b = this;
        a.get('drag').onmousedown = function (c) {
          function d(h) {
            h.preventDefault();
            m.j.kk.ha(gc(gc(e + (f - h.y))));
            b.$a.blur();
            b.bf = !1;
            b.Af()
          }
          b.f.classList.add('dragging');
          let e = b.pk(),
          f = c.y;
          c.preventDefault();
          let g = null;
          g = function (h) {
            b.f.classList.remove('dragging');
            d(h);
            window.document.removeEventListener('mousemove', d, !1);
            window.document.removeEventListener('mouseup', g, !1)
          };
          window.document.addEventListener('mousemove', d, !1);
          window.document.addEventListener('mouseup', g, !1)
        };
        this.Fc = new dc(
          a.get('autocompletebox'),
          function (c, d) {
            b.$a.value = c;
            b.$a.setSelectionRange(d, d)
          }
        );
        this.$a.onkeydown = function (c) {
          switch (c.keyCode) {
            case 9:
              c.preventDefault();
              b.Fc.Qb.hidden ? b.$a.blur() : b.Fc.Wo();
              break;
            case 13:
              null != b.El &&
              '' != b.$a.value &&
              b.El(b.$a.value);
              b.$a.value = '';
              b.$a.blur();
              break;
            case 27:
              b.Fc.Qb.hidden ? (b.$a.value = '', b.$a.blur()) :
              b.Fc.bi();
              break;
            case 38:
              b.Fc.hk( - 1);
              break;
            case 40:
              b.Fc.hk(1)
          }
          c.stopPropagation()
        };
        this.$a.onfocus = function () {
          null != b.wg &&
          b.wg(!0);
          b.fi = !0;
          b.Af()
        };
        this.$a.onblur = function () {
          null != b.wg &&
          b.wg(!1);
          b.fi = !1;
          b.Fc.bi();
          b.Af()
        };
        this.$a.oninput = function () {
          b.Fc.oo(b.$a.value, b.$a.selectionStart)
        };
        this.Af()
      }
      $m() {
        this.bf = !this.bf;
        this.Af();
        if (!this.bf) {
          let a = this.Lc;
          window.setTimeout(function () {
            a.scrollTop = a.scrollHeight
          }, 200)
        }
      }
      Af() {
        let a = '' + this.pk();
        this.f.style.height = a + 'px'
      }
      pk() {
        let a = gc(m.j.kk.v());
        if (this.fi) {
          let b = gc(m.j.Hh.v());
          a <= b &&
          (a = b)
        } else this.bf &&
        (a = 0);
        return a
      }
      Xp(a, b, c) {
        let d = window.document.createElement('p');
        d.className = 'announcement';
        d.textContent = a;
        0 <= b &&
        (d.style.color = T.nc(b));
        switch (c) {
          case 1:
          case 4:
            d.style.fontWeight = 'bold';
            break;
          case 2:
          case 5:
            d.style.fontStyle = 'italic'
        }
        switch (c) {
          case 3:
          case 4:
          case 5:
            d.style.fontSize = '12px'
        }
        this.hl(d)
      }
      hl(a) {
        var b = this.Lc.clientHeight;
        b = this.Lc.scrollTop + b - this.Lc.scrollHeight >= 0.5 * - b ||
        !$a.Ep(this.Lc);
        this.ki.appendChild(a);
        b &&
        (this.Lc.scrollTop = this.Lc.scrollHeight);
        for (a = b ? 50 : 100; this.ki.childElementCount > a; ) this.ki.firstElementChild.remove()
      }
      da(a, b) {
        let c = window.document.createElement('p');
        null != b &&
        (c.className = b);
        c.textContent = a;
        this.hl(c)
      }
      Hb(a) {
        this.da(a, 'notice')
      }
      static Ep(a) {
        return a.parentElement.querySelector(':hover') == a
      }
    }
    class Wb {
      constructor(a, b) {
        this.di = null;
        this.l = a;
        null != b &&
        (this.di = '@' + aa.replace(b, ' ', '_'))
      }
      jj(a) {
        let b = this.l.Ka.Fc,
        c = [],
        d = 0;
        for (a = a.K; d < a.length; ) {
          let e = a[d];
          ++d;
          c.push({
            D: e.D,
            ba: e.Z
          })
        }
        b.Zj = c
      }
      Hi(a) {
        function b(d) {
          return null == d ? '' :
          ' by ' + d.D
        }
        this.jj(a);
        let c = this;
        a.Sl = function (d) {
          c.l.Ka.Hb('' + d.D + ' has joined');
          m.Qa.md(m.Qa.Gp);
          c.jj(a)
        };
        a.Tl = function (d, e, f, g) {
          D.h(c.xq, d.Z);
          null == e ? d = '' + d.D + ' has left' : (
            Xb.h(c.wq, d.Z, e, null != g ? g.D : null, f),
            d = '' + d.D + ' was ' + (f ? 'banned' : 'kicked') + b(g) + ('' != e ? ' (' + e + ')' : '')
          );
          c.l.Ka.Hb(d);
          m.Qa.md(m.Qa.Mp);
          c.jj(a)
        };
        a.Ql = function (d, e) {
          let f = null != c.di &&
          - 1 != e.indexOf(c.di);
          c.l.Ka.da('' + d.D + ': ' + e, f ? 'highlight' : null);
          m.j.Nm.v() &&
          f ? m.Qa.md(m.Qa.Tk) : m.j.Xi.v() &&
          m.Qa.md(m.Qa.ik)
        };
        a.tm = function (d, e, f, g) {
          c.l.Ka.Xp(d, e, f);
          if (m.j.Xi.v()) switch (g) {
            case 1:
              m.Qa.md(m.Qa.ik);
              break;
            case 2:
              m.Qa.md(m.Qa.Tk)
          }
        };
        a.zi = function () {
          m.Qa.md(m.Qa.Ip)
        };
        a.dj = function (d) {
          m.Qa.md(m.Qa.op);
          let e = c.l.ib.gb.Cd;
          e.Pa(d == u.ia ? e.nr : e.io)
        };
        a.ej = function (d) {
          let e = c.l.ib.gb.Cd;
          e.Pa(d == u.ia ? e.pr : e.jo);
          c.l.Ka.Hb('' + d.D + ' team won the match')
        };
        a.Ll = function (d, e, f) {
          e &&
          !f &&
          c.l.Ka.Hb('Game paused' + b(d))
        };
        a.fj = function () {
          let d = c.l.ib.gb.Cd;
          d.Pa(d.ms)
        };
        a.aj = function (d) {
          c.l.we(!1);
          c.l.ib.gb.Cd.uo();
          c.l.Ka.Hb('Game started' + b(d))
        };
        a.Kf = function (d) {
          null !=
          d &&
          c.l.Ka.Hb('Game stopped' + b(d))
        };
        a.Zi = function (d, e) {
          if (!e.cf()) {
            let f = aa.hh(e.lk(), 8);
            c.l.Ka.Hb('Stadium "' + e.D + '" (' + f + ') loaded' + b(d))
          }
        };
        a.Rl = function (d) {
          let e = window.performance.now();
          9000 > e - d.un ||
          (
            d.un = e,
            c.l.Ka.Hb('' + d.D + ' ' + (d.Td ? 'has desynchronized' : 'is back in sync'))
          )
        };
        a.Wl = function (d, e, f) {
          null != a.M &&
          c.l.Ka.Hb('' + e.D + ' was moved to ' + f.D + b(d))
        };
        a.yi = function (d, e) {
          let f = e.D;
          d = (
            e.fb ? '' + f + ' was given admin rights' : '' + f + '\'s admin rights were taken away'
          ) + b(d);
          c.l.Ka.Hb(d)
        };
        a.Vl = function (d, e) {
          c.l.ib.gb.vp(d, e)
        };
        a.al = function (d, e, f, g) {
          c.l.Ka.Hb(
            'Kick Rate Limit set to (min: ' + e + ', rate: ' + f + ', burst: ' + g + ')' + b(d)
          )
        }
      }
      xs(a) {
        a.Sl = null;
        a.Tl = null;
        a.Ql = null;
        a.tm = null;
        a.zi = null;
        a.dj = null;
        a.ej = null;
        a.Ll = null;
        a.fj = null;
        a.aj = null;
        a.Kf = null;
        a.Zi = null;
        a.Rl = null;
        a.Wl = null;
        a.yi = null;
        a.Vl = null;
        a.al = null
      }
    }
    class Hc {
    }
    class W {
      constructor(a) {
        W.yb ||
        this.Za(a)
      }
      Za(a) {
        this.Y = 0;
        this.U = a
      }
    }
    class wc {
      constructor() {
        this.Wc = 0;
        this.eb = [];
        this.ms = new da(['Time is',
        'Up!'], 16777215);
        this.pr = new da(['Red is',
        'Victorious!'], 15035990);
        this.nr = new da(['Red',
        'Scores!'], 15035990);
        this.jo = new da(['Blue is',
        'Victorious!'], 625603);
        this.io = new da(['Blue',
        'Scores!'], 625603);
        this.Nq = new da(['Game',
        'Paused'], 16777215)
      }
      Pa(a) {
        this.eb.push(a)
      }
      uo() {
        this.eb = [];
        this.Wc = 0
      }
      A(a) {
        0 < this.eb.length &&
        (this.Wc += a) > this.eb[0].fp() &&
        (this.Wc = 0, this.eb.shift())
      }
      Rc(a) {
        0 < this.eb.length &&
        this.eb[0].Rc(a, this.Wc)
      }
    }
    class na {
      constructor(a) {
        function b(y) {
          let F = window.document.createElement('div');
          F.className = 'inputrow';
          var L = window.document.createElement('div');
          L.textContent = y;
          F.appendChild(L);
          L = Lb.kp(y);
          let ea = 0;
          for (; ea < L.length; ) {
            let V = L[ea];
            ++ea;
            let xc = window.document.createElement('div');
            var S = V;
            V.startsWith('Key') &&
            (S = O.substr(V, 3, null));
            xc.textContent = S;
            F.appendChild(xc);
            S = window.document.createElement('i');
            S.className = 'icon-cancel';
            S.onclick = function () {
              Lb.sr(V);
              m.j.Jd.ha(Lb);
              xc.remove()
            };
            xc.appendChild(S)
          }
          L = window.document.createElement('i');
          L.className = 'icon-plus';
          F.appendChild(L);
          L.onclick = function () {
            yc.classList.toggle('show', !0);
            yc.focus();
            yc.onkeydown = function (V) {
              yc.classList.toggle('show', !1);
              V.stopPropagation();
              V = V.code;
              null == Lb.v(V) &&
              (Lb.Pa(V, y), m.j.Jd.ha(Lb), Ic())
            }
          };
          return F
        }
        function c(y, F, L) {
          y = l.get(y);
          if (null == L) y.hidden = !0;
           else {
            y.innerHTML = F + ': <div class=\'flagico\'></div> <span></span>';
            F = y.querySelector('.flagico');
            y = y.querySelector('span');
            try {
              F.classList.add('f-' + L.ub)
            } catch (ea) {
            }
            y.textContent = L.ub.toUpperCase()
          }
        }
        function d() {
          let y = m.j.Hh.v();
          K.textContent = '' + y;
          N.value = '' + y
        }
        function e() {
          let y = m.j.Ih.v();
          t.textContent = '' + y;
          z.value = '' + y
        }
        function f(y, F, L, ea) {
          let S = l.get(y);
          y = F.v();
          S.selectedIndex = ea(y);
          S.onchange = function () {
            F.ha(L(S.selectedIndex))
          }
        }
        function g(y, F, L) {
          function ea(V) {
            S.classList.toggle('icon-ok', V);
            S.classList.toggle('icon-cancel', !V)
          }
          y = l.get(y);
          y.classList.add('toggle');
          let S = window.document.createElement('i');
          S.classList.add('icon-ok');
          y.insertBefore(S, y.firstChild);
          y.onclick = function () {
            let V = !F.v();
            F.ha(V);
            ea(V);
            null != L &&
            L(V)
          };
          ea(F.v())
        }
        function h(y) {
          let F = {
            kn: l.get(y + 'btn'),
            ph: l.get(y + 'sec')
          };
          n.push(F);
          F.kn.onclick = function () {
            k(F)
          }
        }
        function k(y) {
          let F = 0,
          L = 0;
          for (; L < n.length; ) {
            let ea = n[L];
            ++L;
            let S = ea == y;
            S &&
            (na.ym = F);
            ea.ph.classList.toggle('selected', S);
            ea.kn.classList.toggle('selected', S);
            ++F
          }
        }
        null == a &&
        (a = !1);
        this.f = x.Ia(na.O);
        let l = x.Ba(this.f);
        this.wd = l.get('close');
        let n = [];
        h('sound');
        h('video');
        h('misc');
        h('input');
        k(n[na.ym]);
        g('tsound-main', m.j.xe, function () {
          m.Qa.Gi()
        });
        g('tsound-chat', m.j.Xi);
        g('tsound-highlight', m.j.Nm);
        g('tsound-crowd', m.j.Mm);
        f(
          'viewmode',
          m.j.Rd,
          function (y) {
            return y - 1
          },
          function (y) {
            return y + 1
          }
        );
        f('fps', m.j.Rh, function (y) {
          return y
        }, function (y) {
          return y
        });
        let r = [
          1,
          0.75,
          0.5,
          0.25
        ];
        f(
          'resscale',
          m.j.Mi,
          function (y) {
            return r[y]
          },
          function (y) {
            let F = 0,
            L = r.length - 1;
            for (; F < L && !(r[F] <= y); ) ++F;
            return F
          }
        );
        g('tvideo-lowlatency', m.j.li);
        g('tvideo-teamcol', m.j.Vm);
        g('tvideo-showindicators', m.j.Uk);
        g('tvideo-showavatars', m.j.Km);
        let t = l.get('chatopacity-value'),
        z = l.get('chatopacity-range');
        e();
        z.oninput = function () {
          m.j.Ih.ha(parseFloat(z.value));
          e()
        };
        let K = l.get('chatfocusheight-value'),
        N = l.get('chatfocusheight-range');
        d();
        N.oninput = function () {
          m.j.Hh.ha(Q.parseInt(N.value));
          d()
        };
        f(
          'chatbgmode',
          m.j.jk,
          function (y) {
            return 0 == y ? 'full' : 'compact'
          },
          function (y) {
            return 'full' == y ? 0 : 1
          }
        );
        let Db = null,
        Mc = this;
        Db = function () {
          let y = m.j.af.v();
          c('loc', 'Detected location', m.j.$e.v());
          c('loc-ovr', 'Location override', y);
          let F = l.get('loc-ovr-btn');
          F.disabled = !a;
          null == y ? (
            F.textContent = 'Override location',
            F.onclick = function () {
              H.h(Mc.mq)
            }
          ) : (
            F.textContent = 'Remove override',
            F.onclick = function () {
              m.j.af.ha(null);
              Db()
            }
          )
        };
        Db();
        let Lb = m.j.Jd.v(),
        yc = l.get('presskey'),
        Ic = null,
        eb = l.get('inputsec');
        Ic = function () {
          x.Qf(eb);
          eb.appendChild(b('Up'));
          eb.appendChild(b('Down'));
          eb.appendChild(b('Left'));
          eb.appendChild(b('Right'));
          eb.appendChild(b('Kick'));
          eb.appendChild(b('ToggleChat'))
        };
        Ic();
        this.wd.onclick = function () {
          H.h(Mc.rb)
        }
      }
    }
    class ac {
      constructor(a) {
        this.Ee = a
      }
    }
    class Aa {
      constructor() {
        this.i = this.B = 63;
        this.S = 16777215;
        this.Ea = 0.99;
        this.ca = 1;
        this.o = 0.5;
        this.V = 10;
        this.ra = new P(0, 0);
        this.G = new P(0, 0);
        this.a = new P(0, 0)
      }
      ga(a) {
        var b = this.a;
        a.u(b.x);
        a.u(b.y);
        b = this.G;
        a.u(b.x);
        a.u(b.y);
        b = this.ra;
        a.u(b.x);
        a.u(b.y);
        a.u(this.V);
        a.u(this.o);
        a.u(this.ca);
        a.u(this.Ea);
        a.tb(this.S);
        a.R(this.i);
        a.R(this.B)
      }
      ma(a) {
        var b = this.a;
        b.x = a.w();
        b.y = a.w();
        b = this.G;
        b.x = a.w();
        b.y = a.w();
        b = this.ra;
        b.x = a.w();
        b.y = a.w();
        this.V = a.w();
        this.o = a.w();
        this.ca = a.w();
        this.Ea = a.w();
        this.S = a.jb();
        this.i = a.N();
        this.B = a.N()
      }
      Zp() {
        let a = new ra;
        this.Vk(a);
        return a
      }
      Vk(a) {
        var b = a.a,
        c = this.a;
        b.x = c.x;
        b.y = c.y;
        b = a.G;
        c = this.G;
        b.x = c.x;
        b.y = c.y;
        b = a.ra;
        c = this.ra;
        b.x = c.x;
        b.y = c.y;
        a.V = this.V;
        a.o = this.o;
        a.ca = this.ca;
        a.Ea = this.Ea;
        a.S = this.S;
        a.i = this.i;
        a.B = this.B
      }
    }
    class Ab {
      constructor() {
        this.Gf = null;
        this.f = x.Ia(Ab.O);
        var a = x.Ba(this.f);
        let b = this;
        a.get('cancel').onclick = function () {
          H.h(b.rb)
        };
        this.Gh = a.get('change');
        this.Gh.disabled = !0;
        this.Gh.onclick = function () {
          null != b.Gf &&
          b.xm(b.Gf.index)
        };
        a = a.get('list');
        this.Ai(a);
        let c = hb.ni(a);
        window.setTimeout(function () {
          c.update()
        }, 0)
      }
      Ai(a) {
        let b = this,
        c = 0,
        d = Ra.eb.length >> 2;
        for (; c < d; ) {
          var e = c++;
          let f = e,
          g = Ra.eb[e << 2];
          e = Ra.eb[(e << 2) + 1].toLowerCase();
          let h = window.document.createElement('div');
          h.className = 'elem';
          h.innerHTML = '<div class="flagico f-' + e + '"></div> ' + g;
          a.appendChild(h);
          h.onclick = function () {
            null != b.Gf &&
            b.Gf.La.classList.remove('selected');
            b.Gh.disabled = !1;
            b.Gf = {
              La: h,
              index: f
            };
            h.classList.add('selected')
          };
          h.ondblclick = function () {
            b.xm(f)
          }
        }
      }
      xm(a) {
        let b = new la;
        b.ub = Ra.eb[(a << 2) + 1].toLowerCase();
        b.Jc = Ra.eb[(a << 2) + 2];
        b.Mc = Ra.eb[(a << 2) + 3];
        m.j.af.ha(b);
        H.h(this.rb)
      }
    }
    class ya {
      constructor() {
        this.Cc = - 1;
        this.Cn = null;
        this.un = - Infinity;
        this.fa = u.Oa;
        this.I = null;
        this.Bc = this.Zc = 0;
        this.Yb = !1;
        this.W = this.Z = 0;
        this.D = 'Player';
        this.gh = this.zb = 0;
        this.country = null;
        this.Td = !1;
        this.Zb = this.Sd = null;
        this.Nb = 0;
        this.fb = !1
      }
      wa(a) {
        a.m(this.fb ? 1 : 0);
        a.R(this.Nb);
        a.Eb(this.Zb);
        a.Eb(this.Sd);
        a.m(this.Td ? 1 : 0);
        a.Eb(this.country);
        a.R(this.gh);
        a.Eb(this.D);
        a.R(this.W);
        a.nb(this.Z);
        a.m(this.Yb ? 1 : 0);
        a.oj(this.Bc);
        a.m(this.Zc);
        a.m(this.fa.ba);
        a.oj(null == this.I ? - 1 : this.I.Il)
      }
      xa(a, b) {
        this.fb = 0 != a.F();
        this.Nb = a.N();
        this.Zb = a.Ab();
        this.Sd = a.Ab();
        this.Td = 0 != a.F();
        this.country = a.Ab();
        this.gh = a.N();
        this.D = a.Ab();
        this.W = a.N();
        this.Z = a.Bb();
        this.Yb = 0 != a.F();
        this.Bc = a.Di();
        this.Zc = a.F();
        let c = a.zf();
        this.fa = 1 == c ? u.ia : 2 == c ? u.Da : u.Oa;
        a = a.Di();
        this.I = 0 > a ? null : b[a]
      }
      Ws() {
        let a = qa.Cc,
        b = this.Cn;
        this.Cc != a &&
        (null == b && (this.Cn = b = new ya), this.Cc = a, ya.Ns(b, this));
        return b
      }
      static Ns(a, b) {
        a.fb = b.fb;
        a.Nb = b.Nb;
        a.Zb = b.Zb;
        a.Sd = b.Sd;
        a.Td = b.Td;
        a.country = b.country;
        a.gh = b.gh;
        a.zb = b.zb;
        a.D = b.D;
        a.W = b.W;
        a.Z = b.Z;
        a.Yb = b.Yb;
        a.Bc = b.Bc;
        a.Zc = b.Zc;
        a.I = null == b.I ? null : b.I.uc();
        a.fa = b.fa
      }
    }
    class Cb {
      constructor() {
        this.f = x.Ia(Cb.O);
        let a = x.Ba(this.f);
        this.Db = a.get('input');
        this.rf = a.get('ok');
        let b = this;
        a.get('cancel').onclick = function () {
          null != b.Wa &&
          b.Wa(null)
        };
        this.Db.maxLength = 30;
        this.Db.oninput = function () {
          b.A()
        };
        this.Db.onkeydown = function (c) {
          13 == c.keyCode &&
          b.Ic() &&
          null != b.Wa &&
          b.Wa(b.Db.value)
        };
        this.rf.onclick = function () {
          b.Ic() &&
          null != b.Wa &&
          b.Wa(b.Db.value)
        };
        this.A()
      }
      Ic() {
        let a = this.Db.value;
        return 30 >= a.length ? 0 < a.length : !1
      }
      A() {
        this.rf.disabled = !this.Ic()
      }
    }
    class q {
      constructor() {
        this.L = [];
        this.X = [];
        this.sa = [];
        this.vc = [];
        this.H = [];
        this.qb = [];
        this.Md = [];
        this.vd = [];
        this.Kd = new cc;
        this.Nh = 255;
        this.Ue = this.mf = 0;
        this.$f = !0;
        this.Df = !1
      }
      rg() {
        let a = new Aa;
        a.S = 16777215;
        a.i = 63;
        a.B = 193;
        a.V = 10;
        a.Ea = 0.99;
        a.ca = 1;
        a.o = 0.5;
        return a
      }
      ga(a) {
        a.m(this.Nh);
        if (!this.cf()) {
          a.Eb(this.D);
          a.R(this.ud);
          a.u(this.be);
          a.u(this.ae);
          a.u(this.bd);
          a.u(this.Gc);
          a.u(this.Te);
          a.R(this.td);
          a.u(this.bc);
          a.u(this.sc);
          a.u(this.mc);
          this.Kd.ga(a);
          a.Xb(this.mf);
          a.m(this.Ue);
          a.m(this.$f ? 1 : 0);
          a.m(this.Df ? 1 : 0);
          a.m(this.L.length);
          for (var b = 0, c = this.L.length; b < c; ) {
            var d = b++;
            let e = this.L[d];
            e.Dd = d;
            e.ga(a)
          }
          a.m(this.X.length);
          b = 0;
          for (c = this.X; b < c.length; ) c[b++].ga(a);
          a.m(this.sa.length);
          b = 0;
          for (c = this.sa; b < c.length; ) c[b++].ga(a);
          a.m(this.vc.length);
          b = 0;
          for (c = this.vc; b < c.length; ) c[b++].ga(a);
          a.m(this.H.length);
          b = 0;
          for (c = this.H; b < c.length; ) c[b++].ga(a);
          a.m(this.qb.length);
          b = 0;
          for (c = this.qb; b < c.length; ) c[b++].ga(a);
          a.m(this.Md.length);
          b = 0;
          for (c = this.Md; b < c.length; ) d = c[b],
          ++b,
          a.u(d.x),
          a.u(d.y);
          a.m(this.vd.length);
          b = 0;
          for (c = this.vd; b < c.length; ) d = c[b],
          ++b,
          a.u(d.x),
          a.u(d.y)
        }
      }
      ws(a) {
        function b() {
          let f = [],
          g = a.F(),
          h = 0;
          for (; h < g; ) {
            ++h;
            let k = new P(0, 0);
            k.x = a.w();
            k.y = a.w();
            f.push(k)
          }
          return f
        }
        this.D = a.Ab();
        this.ud = a.N();
        this.be = a.w();
        this.ae = a.w();
        this.bd = a.w();
        this.Gc = a.w();
        this.Te = a.w();
        this.td = a.N();
        this.bc = a.w();
        this.sc = a.w();
        this.mc = a.w();
        this.Kd.ma(a);
        this.mf = a.Sb();
        this.Ue = a.F();
        this.$f = 0 != a.F();
        this.Df = 0 != a.F();
        this.L = [];
        for (var c = a.F(), d = 0; d < c; ) {
          var e = new G;
          e.ma(a);
          e.Dd = d++;
          this.L.push(e)
        }
        this.X = [];
        c = a.F();
        for (d = 0; d < c; ) ++d,
        e = new I,
        e.ma(a, this.L),
        this.X.push(e);
        this.sa = [];
        c = a.F();
        for (d = 0; d < c; ) ++d,
        e = new R,
        e.ma(a),
        this.sa.push(e);
        this.vc = [];
        c = a.F();
        for (d = 0; d < c; ) ++d,
        e = new Kb,
        e.ma(a),
        this.vc.push(e);
        this.H = [];
        c = a.F();
        for (d = 0; d < c; ) ++d,
        e = new Aa,
        e.ma(a),
        this.H.push(e);
        this.qb = [];
        c = a.F();
        for (d = 0; d < c; ) ++d,
        e = new ob,
        e.ma(a),
        this.qb.push(e);
        this.Md = b();
        this.vd = b();
        this.qe();
        if (!this.gn()) throw v.C(new Sa('Invalid stadium'));
      }
      gn() {
        return 0 >= this.H.length ||
        0 > this.Gc ||
        0 > this.bd ||
        0 > this.Kd.V ? !1 : !0
      }
      qe() {
        let a = 0,
        b = this.X;
        for (; a < b.length; ) b[a++].qe()
      }
      cf() {
        return 255 != this.Nh
      }
      le(a, b) {
        a = a[b];
        return null != a ? w.J(a, E) : 0
      }
      Wp(a) {
        a = a.canBeStored;
        return null !=
        a ? w.J(a, Gc) : !0
      }
      Ce() {
        return JSON.stringify(this.ss())
      }
      ss() {
        if (!this.$f) throw v.C(0);
        let a = {};
        for (var b = 0, c = [], d = 0, e = this.L; d < e.length; ) {
          var f = e[d];
          ++d;
          f.Dd = b++;
          c.push(q.Es(f))
        }
        d = new I;
        b = [];
        e = 0;
        for (f = this.X; e < f.length; ) b.push(q.Pr(f[e++], d));
        d = [];
        e = 0;
        for (f = this.sa; e < f.length; ) d.push(q.Pq(f[e++]));
        e = [];
        f = 0;
        for (var g = this.vc; f < g.length; ) e.push(q.pp(g[f++]));
        f = q.Sq(this.Kd);
        var h = new Aa;
        g = [];
        for (var k = 0, l = this.H; k < l.length; ) g.push(q.So(l[k++], h));
        h = [];
        k = 0;
        for (l = this.qb; k < l.length; ) h.push(q.Hp(l[k++]));
        k = [];
        l = 0;
        for (var n = this.Md; l < n.length; ) {
          var r = n[l];
          ++l;
          k.push([r.x,
          r.y])
        }
        l = [];
        n = 0;
        for (r = this.vd; n < r.length; ) {
          let t = r[n];
          ++n;
          l.push([t.x,
          t.y])
        }
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
        q.pa(c, 'maxViewWidth', this.mf, 0);
        q.pa(c, 'cameraFollow', 1 == this.Ue ? 'player' : '', '');
        q.pa(c, 'spawnDistance', this.mc, 200);
        0 != h.length &&
        (c.joints = h);
        0 != k.length &&
        (c.redSpawnPoints = k);
        0 != l.length &&
        (c.blueSpawnPoints = l);
        q.pa(c, 'kickOffReset', this.Df ? 'full' : 'partial', 'partial');
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
        return c
      }
      el(a) {
        function b(h) {
          let k = w.J(h[0], E);
          h = w.J(h[1], E);
          null == h &&
          (h = 0);
          null == k &&
          (k = 0);
          return new P(k, h)
        }
        function c(h, k, l, n) {
          null == n &&
          (n = !1);
          var r = d[k];
          if (!n || null != r) if (n = w.J(r, Array), null != n) for (r = 0; r < n.length; ) {
            let t = n[r];
            ++r;
            try {
              q.Zn(t, f),
              h.push(l(t))
            } catch (z) {
              throw v.C(new Sa('Error in "' + k + '" index: ' + h.length));
            }
          }
        }
        let d = JSON5.parse(a);
        this.L = [];
        this.X = [];
        this.sa = [];
        this.vc = [];
        this.H = [];
        this.qb = [];
        this.D = w.J(d.name, String);
        this.bc = w.J(d.width, E);
        this.sc = w.J(d.height, E);
        this.mf = this.le(d, 'maxViewWidth') | 0;
        'player' == d.cameraFollow &&
        (this.Ue = 1);
        this.mc = 200;
        a = d.spawnDistance;
        null != a &&
        (this.mc = w.J(a, E));
        a = d.bg;
        let e;
        switch (a.type) {
          case 'grass':
            e = 1;
            break;
          case 'hockey':
            e = 2;
            break;
          default:
            e = 0
        }
        this.ud = e;
        this.be = this.le(a, 'width');
        this.ae = this.le(a, 'height');
        this.bd = this.le(a, 'kickOffRadius');
        this.Gc = this.le(a, 'cornerRadius');
        this.td = 7441498;
        null != a.color &&
        (this.td = q.pg(a.color));
        this.Te = this.le(a, 'goalLine');
        this.$f = this.Wp(d);
        this.Df = 'full' == d.kickOffReset;
        let f = d.traits;
        a = d.ballPhysics;
        'disc0' != a &&
        (
          null != a ? (a = q.fl(a, this.rg()), a.B |= 192, this.H.push(a)) : this.H.push(this.rg())
        );
        c(this.L, 'vertexes', q.Vp);
        let g = this;
        c(this.X, 'segments', function (h) {
          return q.Up(h, g.L)
        });
        c(this.vc, 'goals', q.Qp);
        c(this.H, 'discs', function (h) {
          return q.fl(h, new Aa)
        });
        c(this.sa, 'planes', q.Sp);
        c(this.qb, 'joints', function (h) {
          return q.Rp(h, g.H)
        }, !0);
        c(this.Md, 'redSpawnPoints', b, !0);
        c(this.vd, 'blueSpawnPoints', b, !0);
        a = d.playerPhysics;
        null != a &&
        (this.Kd = q.Tp(a));
        if (
          255 < this.L.length ||
          255 < this.X.length ||
          255 < this.sa.length ||
          255 < this.vc.length ||
          255 < this.H.length
        ) throw v.C('Error');
        this.qe();
        if (!this.gn()) throw v.C(new Sa('Invalid stadium'));
      }
      lk() {
        let a = q.qs;
        a.a = 0;
        this.ga(a);
        let b = new zc;
        b.Ls(a.Wb());
        b.hash = (b.hash += b.hash << 3) ^ b.hash >>> 11;
        b.hash += b.hash << 15;
        return b.hash | 0
      }
      ro(a, b) {
        let c = 0,
        d = this.vc;
        for (; c < d.length; ) {
          let h = d[c];
          ++c;
          var e = h.$,
          f = h.ea,
          g = b.x - a.x;
          let k = b.y - a.y;
          0 < - (e.y - a.y) * g + (e.x - a.x) * k == 0 < - (f.y - a.y) * g + (f.x - a.x) * k ? e = !1 : (
            g = f.x - e.x,
            f = f.y - e.y,
            e = 0 < - (a.y - e.y) * g + (a.x - e.x) * f == 0 < - (b.y - e.y) * g + (b.x - e.x) * f ? !1 : !0
          );
          if (e) return h.Ae
        }
        return u.Oa
      }
      jd(a, b, c, d, e, f, g, h) {
        null == h &&
        (h = 0);
        this.D = a;
        this.H.push(this.rg());
        this.bc = b;
        this.sc = c;
        this.ud = 1;
        this.td = 7441498;
        this.be = d;
        this.ae = e;
        this.bd = g;
        this.Gc = h;
        this.mc = 0.75 * d;
        400 < this.mc &&
        (this.mc = 400);
        a = new R;
        var k = a.ya;
        k.x = 0;
        k.y = 1;
        a.Va = - c;
        a.o = 0;
        this.sa.push(a);
        a = new R;
        k = a.ya;
        k.x = 0;
        k.y = - 1;
        a.Va = - c;
        a.o = 0;
        this.sa.push(a);
        a = new R;
        k = a.ya;
        k.x = 1;
        k.y = 0;
        a.Va = - b;
        a.o = 0;
        this.sa.push(a);
        a = new R;
        k = a.ya;
        k.x = - 1;
        k.y = 0;
        a.Va = - b;
        a.o = 0;
        this.sa.push(a);
        this.sg(d, 1, f, 13421823, u.Da);
        this.sg( - d, - 1, f, 16764108, u.ia);
        this.kl(g, c);
        b = new R;
        c = b.ya;
        c.x = 0;
        c.y = 1;
        b.Va = - e;
        b.i = 1;
        this.sa.push(b);
        b = new R;
        c = b.ya;
        c.x = 0;
        c.y = - 1;
        b.Va = - e;
        b.i = 1;
        this.sa.push(b);
        b = new G;
        c = b.a;
        c.x = - d;
        c.y = - e;
        b.i = 0;
        c = new G;
        g = c.a;
        g.x = d;
        g.y = - e;
        c.i = 0;
        g = new G;
        a = g.a;
        a.x = d;
        a.y = - f;
        g.i = 0;
        a = new G;
        k = a.a;
        k.x = d;
        k.y = f;
        a.i = 0;
        k = new G;
        var l = k.a;
        l.x = d;
        l.y = e;
        k.i = 0;
        l = new G;
        var n = l.a;
        n.x = - d;
        n.y = e;
        l.i = 0;
        n = new G;
        var r = n.a;
        r.x = - d;
        r.y = f;
        n.i = 0;
        r = new G;
        var t = r.a;
        t.x = - d;
        t.y = - f;
        r.i = 0;
        f = new I;
        f.$ = c;
        f.ea = g;
        f.i = 1;
        f.bb = !1;
        t = new I;
        t.$ = a;
        t.ea = k;
        t.i = 1;
        t.bb = !1;
        let z = new I;
        z.$ = l;
        z.ea = n;
        z.i = 1;
        z.bb = !1;
        let K = new I;
        K.$ = r;
        K.ea = b;
        K.i = 1;
        K.bb = !1;
        this.L.push(b);
        this.L.push(c);
        this.L.push(g);
        this.L.push(a);
        this.L.push(k);
        this.L.push(l);
        this.L.push(n);
        this.L.push(r);
        this.X.push(f);
        this.X.push(t);
        this.X.push(z);
        this.X.push(K);
        this.il(d, e, h);
        this.qe()
      }
      jl(a, b, c, d, e, f, g, h) {
        this.D = a;
        this.H.push(this.rg());
        this.bc = b;
        this.sc = c;
        this.ud = 2;
        this.be = d;
        this.ae = e;
        this.bd = 75;
        this.Gc = h;
        this.Te = g;
        this.mc = 0.75 * (d - g);
        400 < this.mc &&
        (this.mc = 400);
        a = new R;
        var k = a.ya;
        k.x = 0;
        k.y = 1;
        a.Va = - c;
        a.o = 0;
        this.sa.push(a);
        a = new R;
        k = a.ya;
        k.x = 0;
        k.y = - 1;
        a.Va = - c;
        a.o = 0;
        this.sa.push(a);
        a = new R;
        k = a.ya;
        k.x = 1;
        k.y = 0;
        a.Va = - b;
        a.o = 0;
        this.sa.push(a);
        a = new R;
        k = a.ya;
        k.x = - 1;
        k.y = 0;
        a.Va = - b;
        a.o = 0;
        this.sa.push(a);
        this.sg(d - g, 1, f, 13421823, u.Da, 63);
        this.sg( - d + g, - 1, f, 16764108, u.ia, 63);
        this.kl(75, c);
        b = new R;
        c = b.ya;
        c.x = 0;
        c.y = 1;
        b.Va = - e;
        b.i = 1;
        this.sa.push(b);
        b = new R;
        c = b.ya;
        c.x = 0;
        c.y = - 1;
        b.Va = - e;
        b.i = 1;
        this.sa.push(b);
        b = new R;
        c = b.ya;
        c.x = 1;
        c.y = 0;
        b.Va = - d;
        b.i = 1;
        this.sa.push(b);
        b = new R;
        c = b.ya;
        c.x = - 1;
        c.y = 0;
        b.Va = - d;
        b.i = 1;
        this.sa.push(b);
        this.il(d, e, h);
        this.qe()
      }
      sg(a, b, c, d, e, f) {
        var g;
        null == g &&
        (g = 32);
        null == f &&
        (f = 1);
        var h = new G,
        k = h.a;
        k.x = a + 8 * b;
        k.y = - c;
        k = new G;
        var l = k.a;
        l.x = a + 8 * b;
        l.y = c;
        let n = new G;
        l = n.a;
        l.x = h.a.x + 22 * b;
        l.y = h.a.y + 22;
        let r = new G;
        l = r.a;
        l.x = k.a.x + 22 * b;
        l.y = k.a.y - 22;
        l = new I;
        l.$ = h;
        l.ea = n;
        l.Vc(90 * b);
        let t = new I;
        t.$ = r;
        t.ea = n;
        let z = new I;
        z.$ = r;
        z.ea = k;
        z.Vc(90 * b);
        b = this.L.length;
        this.L.push(h);
        this.L.push(k);
        this.L.push(n);
        this.L.push(r);
        h = b;
        for (b = this.L.length; h < b; ) k = h++,
        this.L[k].i = f,
        this.L[k].B = g,
        this.L[k].o = 0.1;
        b = this.X.length;
        this.X.push(l);
        this.X.push(t);
        this.X.push(z);
        h = b;
        for (b = this.X.length; h < b; ) k = h++,
        this.X[k].i = f,
        this.X[k].B = g,
        this.X[k].o = 0.1;
        f = new Aa;
        g = f.a;
        g.x = a;
        g.y = - c;
        f.ca = 0;
        f.V = 8;
        f.S = d;
        this.H.push(f);
        f = new Aa;
        g = f.a;
        g.x = a;
        g.y = c;
        f.ca = 0;
        f.V = 8;
        f.S = d;
        this.H.push(f);
        d = new Kb;
        f = d.$;
        f.x = a;
        f.y = - c;
        f = d.ea;
        f.x = a;
        f.y = c;
        d.Ae = e;
        this.vc.push(d)
      }
      kl(a, b) {
        let c = new G;
        var d = c.a;
        d.x = 0;
        d.y = - b;
        c.o = 0.1;
        c.B = 24;
        c.i = 6;
        d = new G;
        var e = d.a;
        e.x = 0;
        e.y = - a;
        d.o = 0.1;
        d.B = 24;
        d.i = 6;
        e = new G;
        var f = e.a;
        f.x = 0;
        f.y = a;
        e.o = 0.1;
        e.B = 24;
        e.i = 6;
        a = new G;
        f = a.a;
        f.x = 0;
        f.y = b;
        a.o = 0.1;
        a.B = 24;
        a.i = 6;
        b = new I;
        b.$ = c;
        b.ea = d;
        b.B = 24;
        b.i = 6;
        b.bb = !1;
        b.o = 0.1;
        f = new I;
        f.$ = e;
        f.ea = a;
        f.B = 24;
        f.i = 6;
        f.bb = !1;
        f.o = 0.1;
        let g = new I;
        g.$ = d;
        g.ea = e;
        g.B = 8;
        g.i = 6;
        g.bb = !1;
        g.Vc(180);
        g.o = 0.1;
        let h = new I;
        h.$ = e;
        h.ea = d;
        h.B = 16;
        h.i = 6;
        h.bb = !1;
        h.Vc(180);
        h.o = 0.1;
        this.L.push(c);
        this.L.push(d);
        this.L.push(e);
        this.L.push(a);
        this.X.push(b);
        this.X.push(f);
        this.X.push(g);
        this.X.push(h)
      }
      il(a, b, c) {
        if (!(0 >= c)) {
          var d = new G,
          e = d.a;
          e.x = - a + c;
          e.y = - b;
          d.i = 0;
          e = new G;
          var f = e.a;
          f.x = - a;
          f.y = - b + c;
          e.i = 0;
          f = new G;
          var g = f.a;
          g.x = - a + c;
          g.y = b;
          f.i = 0;
          g = new G;
          var h = g.a;
          h.x = - a;
          h.y = b - c;
          g.i = 0;
          h = new G;
          var k = h.a;
          k.x = a - c;
          k.y = b;
          h.i = 0;
          k = new G;
          var l = k.a;
          l.x = a;
          l.y = b - c;
          k.i = 0;
          l = new G;
          var n = l.a;
          n.x = a - c;
          n.y = - b;
          l.i = 0;
          n = new G;
          var r = n.a;
          r.x = a;
          r.y = - b + c;
          n.i = 0;
          a = new I;
          a.$ = d;
          a.ea = e;
          a.i = 1;
          a.bb = !1;
          a.o = 1;
          a.Vc( - 90);
          b = new I;
          b.$ = f;
          b.ea = g;
          b.i = 1;
          b.bb = !1;
          b.o = 1;
          b.Vc(90);
          c = new I;
          c.$ = h;
          c.ea = k;
          c.i = 1;
          c.bb = !1;
          c.o = 1;
          c.Vc( - 90);
          r = new I;
          r.$ = l;
          r.ea = n;
          r.i = 1;
          r.bb = !1;
          r.o = 1;
          r.Vc(90);
          this.L.push(d);
          this.L.push(e);
          this.L.push(f);
          this.L.push(g);
          this.L.push(h);
          this.L.push(k);
          this.L.push(l);
          this.L.push(n);
          this.X.push(a);
          this.X.push(b);
          this.X.push(c);
          this.X.push(r)
        }
      }
      static ma(a) {
        var b = a.F();
        return 255 == b ? (b = new q, b.ws(a), b) : q.Vh() [b]
      }
      static Vh() {
        if (null == q.wb) {
          q.wb = [];
          var a = new q;
          a.jd('Classic', 420, 200, 370, 170, 64, 75);
          q.wb.push(a);
          a = new q;
          a.jd('Easy', 420, 200, 370, 170, 90, 75);
          q.wb.push(a);
          a = new q;
          a.jd('Small', 420, 200, 320, 130, 55, 70);
          q.wb.push(a);
          a = new q;
          a.jd('Big', 600, 270, 550, 240, 80, 80);
          q.wb.push(a);
          a = new q;
          a.jd('Rounded', 420, 200, 370, 170, 64, 75, 75);
          q.wb.push(a);
          a = new q;
          a.jl('Hockey', 420, 204, 398, 182, 68, 120, 100);
          q.wb.push(a);
          a = new q;
          a.jl('Big Hockey', 600, 270, 550, 240, 90, 160, 150);
          q.wb.push(a);
          a = new q;
          a.jd('Big Easy', 600, 270, 550, 240, 95, 80);
          q.wb.push(a);
          a = new q;
          a.jd('Big Rounded', 600, 270, 550, 240, 80, 75, 100);
          q.wb.push(a);
          a = new q;
          a.jd('Huge', 750, 350, 700, 320, 100, 80);
          q.wb.push(a);
          a = 0;
          let b = q.wb.length;
          for (; a < b; ) {
            let c = a++;
            q.wb[c].Nh = c
          }
        }
        return q.wb
      }
      static Zn(a, b) {
        if (null != a.trait && (b = b[w.J(a.trait, String)], null != b)) {
          let c = 0,
          d = Ac.mn(b);
          for (; c < d.length; ) {
            let e = d[c];
            ++c;
            null == a[e] &&
            (a[e] = b[e])
          }
        }
      }
      static ko(a) {
        if (63 == a) return ['all'];
        let b = [];
        0 != (a & 2) &&
        b.push('red');
        0 != (a & 4) &&
        b.push('blue');
        0 != (a & 1) &&
        b.push('ball');
        0 != (a & 8) &&
        b.push('redKO');
        0 != (a & 16) &&
        b.push('blueKO');
        0 != (a & 32) &&
        b.push('wall');
        0 != (a & 64) &&
        b.push('kick');
        0 != (a & 128) &&
        b.push('score');
        0 != (a & 268435456) &&
        b.push('c0');
        0 != (a & 536870912) &&
        b.push('c1');
        0 != (a & 1073741824) &&
        b.push('c2');
        0 != (a & - 2147483648) &&
        b.push('c3');
        return b
      }
      static Kc(a) {
        a = w.J(a, Array);
        let b = 0,
        c = 0;
        for (; c < a.length; ) switch (a[c++]) {
          case 'all':
            b |= 63;
            break;
          case 'ball':
            b |= 1;
            break;
          case 'blue':
            b |= 4;
            break;
          case 'blueKO':
            b |= 16;
            break;
          case 'c0':
            b |= 268435456;
            break;
          case 'c1':
            b |= 536870912;
            break;
          case 'c2':
            b |= 1073741824;
            break;
          case 'c3':
            b |= - 2147483648;
            break;
          case 'kick':
            b |= 64;
            break;
          case 'red':
            b |= 2;
            break;
          case 'redKO':
            b |=
            8;
            break;
          case 'score':
            b |= 128;
            break;
          case 'wall':
            b |= 32
        }
        return b
      }
      static Pc(a, b, c, d) {
        c != d &&
        (a[b] = q.ko(c))
      }
      static Eg(a, b, c) {
        b != c &&
        (a.color = q.yo(b))
      }
      static yo(a) {
        a |= 0;
        return 0 > a ? 'transparent' : aa.hh(a)
      }
      static pg(a) {
        if ('transparent' == a) return - 1;
        if ('string' == typeof a) return Q.parseInt('0x' + Q.Je(a));
        if (a instanceof Array) return ((a[0] | 0) << 16) + ((a[1] | 0) << 8) + (a[2] | 0);
        throw v.C('Bad color');
      }
      static Es(a) {
        let b = {
          x: a.a.x,
          y: a.a.y
        };
        q.pa(b, 'bCoef', a.o, 1);
        q.Pc(b, 'cMask', a.i, 63);
        q.Pc(b, 'cGroup', a.B, 32);
        return b
      }
      static Vp(a) {
        let b = new G;
        b.a.x = w.J(a.x, E);
        b.a.y = w.J(a.y, E);
        var c = a.bCoef;
        null != c &&
        (b.o = w.J(c, E));
        c = a.cMask;
        null != c &&
        (b.i = q.Kc(c));
        a = a.cGroup;
        null != a &&
        (b.B = q.Kc(a));
        return b
      }
      static Pr(a, b) {
        let c = {
          v0: a.$.Dd,
          v1: a.ea.Dd
        };
        q.pa(c, 'bias', a.Hc, b.Hc);
        q.pa(c, 'bCoef', a.o, b.o);
        let d = a.ip();
        q.pa(c, 'curve', d, 0);
        0 != d &&
        (c.curveF = a.vb);
        q.pa(c, 'vis', a.bb, b.bb);
        q.Pc(c, 'cMask', a.i, b.i);
        q.Pc(c, 'cGroup', a.B, b.B);
        q.Eg(c, a.S, b.S);
        return c
      }
      static Up(a, b) {
        let c = new I;
        var d = w.J(a.v1, bc);
        c.$ = b[w.J(a.v0, bc)];
        c.ea = b[d];
        b = a.bias;
        d = a.bCoef;
        let e = a.curve,
        f = a.curveF,
        g = a.vis,
        h = a.cMask,
        k = a.cGroup;
        a = a.color;
        null != b &&
        (c.Hc = w.J(b, E));
        null != d &&
        (c.o = w.J(d, E));
        null != f ? c.vb = w.J(f, E) : null != e &&
        c.Vc(w.J(e, E));
        null != g &&
        (c.bb = w.J(g, Gc));
        null != h &&
        (c.i = q.Kc(h));
        null != k &&
        (c.B = q.Kc(k));
        null != a &&
        (c.S = q.pg(a));
        return c
      }
      static Hp(a) {
        let b = {
          d0: a.ge,
          d1: a.he,
          length: a.Ib >= a.fc ? a.Ib : [
            a.Ib,
            a.fc
          ]
        };
        q.Eg(b, a.S, 0);
        q.pa(b, 'strength', a.ye, 1 / 0);
        return b
      }
      static Rp(a, b) {
        let c = new ob;
        var d = w.J(a.d0, bc),
        e = w.J(a.d1, bc);
        let f = a.color,
        g = a.strength;
        a = a.length;
        if (d >= b.length || 0 > d) throw v.C(null);
        if (e >= b.length || 0 > e) throw v.C(null);
        c.ge = d;
        c.he = e;
        null == a ? (
          d = b[d],
          e = b[e],
          null == d ||
          null == e ? c.fc = c.Ib = 100 : (b = d.a, d = e.a, e = b.x - d.x, b = b.y - d.y, c.fc = c.Ib = Math.sqrt(e * e + b * b))
        ) : a instanceof Array ? (c.Ib = w.J(a[0], E), c.fc = w.J(a[1], E)) : c.fc = c.Ib = w.J(a, E);
        c.ye = null == g ||
        'rigid' == g ? 1 / 0 : w.J(g, E);
        null != f &&
        (c.S = q.pg(f));
        return c
      }
      static Pq(a) {
        let b = {
          normal: [
            a.ya.x,
            a.ya.y
          ],
          dist: a.Va
        };
        q.pa(b, 'bCoef', a.o, 1);
        q.Pc(b, 'cMask', a.i, 63);
        q.Pc(b, 'cGroup', a.B, 32);
        return b
      }
      static Sp(a) {
        let b = new R;
        var c = w.J(a.normal, Array),
        d = w.J(c[0], E),
        e = w.J(c[1], E);
        c = b.ya;
        let f = d;
        var g = e;
        null == e &&
        (g = 0);
        null == d &&
        (f = 0);
        d = f;
        e = Math.sqrt(d * d + g * g);
        c.x = d / e;
        c.y = g / e;
        b.Va = w.J(a.dist, E);
        c = a.bCoef;
        d = a.cMask;
        a = a.cGroup;
        null != c &&
        (b.o = w.J(c, E));
        null != d &&
        (b.i = q.Kc(d));
        null != a &&
        (b.B = q.Kc(a));
        return b
      }
      static pp(a) {
        return {
          p0: [
            a.$.x,
            a.$.y
          ],
          p1: [
            a.ea.x,
            a.ea.y
          ],
          team: a.Ae == u.ia ? 'red' : 'blue'
        }
      }
      static Qp(a) {
        let b = new Kb;
        var c = w.J(a.p0, Array);
        let d = w.J(a.p1, Array),
        e = b.$;
        e.x = c[0];
        e.y = c[1];
        c = b.ea;
        c.x = d[0];
        c.y = d[1];
        switch (a.team) {
          case 'blue':
            a = u.Da;
            break;
          case 'red':
            a = u.ia;
            break;
          default:
            throw v.C('Bad team value');
        }
        b.Ae = a;
        return b
      }
      static Sq(a) {
        let b = {};
        q.pa(b, 'bCoef', a.o, 0.5);
        q.pa(b, 'invMass', a.ca, 0.5);
        q.pa(b, 'damping', a.Ea, 0.96);
        q.pa(b, 'acceleration', a.Qe, 0.1);
        q.pa(b, 'kickingAcceleration', a.gf, 0.07);
        q.pa(b, 'kickingDamping', a.hf, 0.96);
        q.pa(b, 'kickStrength', a.ef, 5);
        q.Pc(b, 'cGroup', a.B, 0);
        if (0 != a.ra.x || 0 != a.ra.y) b.gravity = [
          a.ra.x,
          a.ra.y
        ];
        q.pa(b, 'radius', a.V, 15);
        q.pa(b, 'kickback', a.ff, 0);
        return b
      }
      static Tp(a) {
        let b = new cc;
        var c = a.bCoef,
        d = a.invMass;
        let e = a.damping,
        f = a.acceleration,
        g = a.kickingAcceleration,
        h = a.kickingDamping,
        k = a.kickStrength,
        l = a.gravity,
        n = a.cGroup,
        r = a.radius;
        a = a.kickback;
        null != c &&
        (b.o = w.J(c, E));
        null != d &&
        (b.ca = w.J(d, E));
        null != e &&
        (b.Ea = w.J(e, E));
        null != f &&
        (b.Qe = w.J(f, E));
        null != g &&
        (b.gf = w.J(g, E));
        null != h &&
        (b.hf = w.J(h, E));
        null != k &&
        (b.ef = w.J(k, E));
        null != l &&
        (c = b.ra, d = w.J(l[1], E), c.x = w.J(l[0], E), c.y = d);
        null != n &&
        (b.B = q.Kc(n));
        null != r &&
        (b.V = w.J(r, E));
        null != a &&
        (b.ff = w.J(a, E));
        return b
      }
      static So(a, b) {
        let c = {};
        if (a.a.x != b.a.x || a.a.y != b.a.y) c.pos = [
          a.a.x,
          a.a.y
        ];
        if (a.G.x != b.G.x || a.G.y != b.G.y) c.speed = [
          a.G.x,
          a.G.y
        ];
        if (a.ra.x != b.ra.x || a.ra.y != b.ra.y) c.gravity = [
          a.ra.x,
          a.ra.y
        ];
        q.pa(c, 'radius', a.V, b.V);
        q.pa(c, 'bCoef', a.o, b.o);
        q.pa(c, 'invMass', a.ca, b.ca);
        q.pa(c, 'damping', a.Ea, b.Ea);
        q.Eg(c, a.S, b.S);
        q.Pc(c, 'cMask', a.i, b.i);
        q.Pc(c, 'cGroup', a.B, b.B);
        return c
      }
      static fl(a, b) {
        var c = a.pos,
        d = a.speed;
        let e = a.gravity,
        f = a.radius,
        g = a.bCoef,
        h = a.invMass,
        k = a.damping,
        l = a.color,
        n = a.cMask;
        a = a.cGroup;
        if (null != c) {
          let r = b.a;
          r.x = c[0];
          r.y = c[1]
        }
        null != d &&
        (c = b.G, c.x = d[0], c.y = d[1]);
        null != e &&
        (d = b.ra, d.x = e[0], d.y = e[1]);
        null != f &&
        (b.V = w.J(f, E));
        null != g &&
        (b.o = w.J(g, E));
        null != h &&
        (b.ca = w.J(h, E));
        null != k &&
        (b.Ea = w.J(k, E));
        null != l &&
        (b.S = q.pg(l));
        null != n &&
        (b.i = q.Kc(n));
        null != a &&
        (b.B = q.Kc(a));
        return b
      }
      static pa(a, b, c, d) {
        c != d &&
        (a[b] = c)
      }
    }
    class za {
      static h(a, b, c) {
        null != a &&
        a(b, c)
      }
    }
    class U {
      constructor() {
      }
      ts() {
        return 'idkey.' + this.qj + '.' + this.rj + '.' + this.uk
      }
      hs(a) {
        try {
          let b = A.ka(1024);
          b.m(1);
          let c = b.a;
          b.Xb(0);
          let d = b.a;
          b.oc(this.qj);
          b.oc(this.rj);
          b.Lb(a);
          let e = b.a - d;
          b.s.setUint16(c, e, b.Ua);
          let f = new Uint8Array(b.s.buffer, b.s.byteOffset + d, e);
          return window.crypto.subtle.sign(U.Lm, this.Zl, f).then(function (g) {
            b.Yg(g);
            return b.Wb()
          })
        } catch (b) {
          return Promise.reject(v.Mb(b).Fb())
        }
      }
      static ep() {
        try {
          return window.crypto.subtle.generateKey(U.yh, !0, [
            'sign',
            'verify'
          ]).then(
            function (a) {
              let b = a.privateKey;
              return window.crypto.subtle.exportKey('jwk', b).then(
                function (c) {
                  let d = c.y,
                  e = c.d,
                  f = new U;
                  f.qj = c.x;
                  f.rj = d;
                  f.uk = e;
                  f.Zl = b;
                  return f
                }
              )
            }
          )
        } catch (a) {
          return Promise.reject(v.Mb(a).Fb())
        }
      }
      static cp(a) {
        a = a.split('.');
        if (4 != a.length || 'idkey' !=
        a[0]) return Promise.reject('Invalid id format');
        let b = a[1],
        c = a[2],
        d = a[3];
        return U.Js(b, c, d).then(function (e) {
          let f = new U;
          f.qj = b;
          f.rj = c;
          f.uk = d;
          f.Zl = e;
          return f
        })
      }
      static Cs(a, b) {
        try {
          let c = new J(new DataView(a.buffer, a.byteOffset, a.byteLength), !1);
          c.F();
          let d = c.sb(c.Sb()),
          e = c.sb(),
          f = new J(new DataView(d.buffer, d.byteOffset, d.byteLength), !1),
          g = f.kc(),
          h = f.kc(),
          k = f.sb();
          if (k.byteLength != b.byteLength) return Promise.reject(null);
          a = 0;
          let l = k.byteLength;
          for (; a < l; ) {
            let n = a++;
            if (k[n] != b[n]) return Promise.reject(null)
          }
          return U.Is(g, h).then(function (n) {
            return window.crypto.subtle.verify(U.Lm, n, e, d)
          }).then(function (n) {
            if (!n) throw v.C(null);
            return g
          })
        } catch (c) {
          return Promise.reject(v.Mb(c).Fb())
        }
      }
      static Js(a, b, c) {
        try {
          return window.crypto.subtle.importKey(
            'jwk',
            {
              crv: 'P-256',
              ext: !0,
              key_ops: [
                'sign'
              ],
              kty: 'EC',
              d: c,
              x: a,
              y: b
            },
            U.yh,
            !0,
            [
              'sign'
            ]
          )
        } catch (d) {
          return Promise.reject(v.Mb(d).Fb())
        }
      }
      static Is(a, b) {
        try {
          return window.crypto.subtle.importKey(
            'jwk',
            {
              crv: 'P-256',
              ext: !0,
              key_ops: [
                'verify'
              ],
              kty: 'EC',
              x: a,
              y: b
            },
            U.yh,
            !0,
            [
              'verify'
            ]
          )
        } catch (c) {
          return Promise.reject(v.Mb(c).Fb())
        }
      }
    }
    class ib {
      static delete (a) {
        return null == window.indexedDB ? Promise.reject('IndexedDB not supported by browser.') : new Promise(
          function (b, c) {
            let d = window.indexedDB.open('stadiums', 1);
            d.onblocked = d.onerror = c;
            d.onupgradeneeded = function (e) {
              let f = d.result;
              f.onerror = c;
              1 > e.oldVersion &&
              (
                f.createObjectStore('files', {
                  autoIncrement: !0
                }),
                f.createObjectStore('meta', {
                  keyPath: 'id'
                })
              )
            };
            d.onsuccess = function () {
              let e = d.result;
              e.onerror = c;
              let f = e.transaction(['meta',
              'files'], 'readwrite');
              f.onerror = f.onabort = function (g) {
                c(g);
                e.close()
              };
              f.oncomplete = function () {
                b(0);
                e.close()
              };
              f.objectStore('files').delete(a);
              f.objectStore('meta').delete(a)
            }
          }
        )
      }
      static get(a) {
        return null == window.indexedDB ? Promise.reject('IndexedDB not supported by browser.') : new Promise(
          function (b, c) {
            let d = window.indexedDB.open('stadiums', 1);
            d.onblocked = d.onerror = c;
            d.onupgradeneeded = function (e) {
              let f = d.result;
              f.onerror = c;
              1 > e.oldVersion &&
              (
                f.createObjectStore('files', {
                  autoIncrement: !0
                }),
                f.createObjectStore('meta', {
                  keyPath: 'id'
                })
              )
            };
            d.onsuccess = function () {
              let e = d.result;
              e.onerror = c;
              let f = e.transaction(['files']);
              f.onerror = f.onabort = function (g) {
                c(g);
                e.close()
              };
              f.oncomplete = function () {
                e.close()
              };
              Rb.rh(f.objectStore('files').get(a)).then(
                function (g) {
                  try {
                    let h = new q;
                    h.el(g);
                    b(h)
                  } catch (h) {
                    g = v.Mb(h).Fb(),
                    c(g)
                  }
                },
                c
              )
            }
          }
        )
      }
      static getAll() {
        return null == window.indexedDB ? Promise.reject('IndexedDB not supported by browser.') : new Promise(
          function (a, b) {
            let c = window.indexedDB.open('stadiums', 1);
            c.onblocked = c.onerror = b;
            c.onupgradeneeded = function (d) {
              let e = c.result;
              e.onerror = b;
              1 > d.oldVersion &&
              (
                e.createObjectStore('files', {
                  autoIncrement: !0
                }),
                e.createObjectStore('meta', {
                  keyPath: 'id'
                })
              )
            };
            c.onsuccess = function () {
              let d = c.result;
              d.onerror = b;
              let e = d.transaction(['meta']);
              e.onerror = e.onabort = function (f) {
                b(f);
                d.close()
              };
              e.oncomplete = function () {
                d.close()
              };
              Rb.rh(e.objectStore('meta').getAll()).then(a, b)
            }
          }
        )
      }
      static qt() {
        let a = pa.navigator.storage;
        if (null == a || null == a.persist) return Promise.resolve(!1);
        try {
          return a.persisted().then(function (b) {
            return b ? !0 : a.persist()
          }).catch(function () {
            return !1
          })
        } catch (b) {
          return Promise.resolve(!1)
        }
      }
      static add(a) {
        return null ==
        window.indexedDB ? Promise.reject('IndexedDB not supported by browser.') : new Promise(
          function (b, c) {
            let d = window.indexedDB.open('stadiums', 1);
            d.onblocked = d.onerror = c;
            d.onupgradeneeded = function (e) {
              let f = d.result;
              f.onerror = c;
              1 > e.oldVersion &&
              (
                f.createObjectStore('files', {
                  autoIncrement: !0
                }),
                f.createObjectStore('meta', {
                  keyPath: 'id'
                })
              )
            };
            d.onsuccess = function () {
              let e = d.result;
              e.onerror = c;
              let f = e.transaction(['files',
              'meta'], 'readwrite');
              f.onerror = f.onabort = function (g) {
                c(g);
                e.close()
              };
              f.oncomplete = function () {
                b(0);
                e.close()
              };
              try {
                Rb.rh(f.objectStore('files').add(a.Ce())).then(
                  function (g) {
                    g = {
                      name: a.D,
                      id: g
                    };
                    return Rb.rh(f.objectStore('meta').add(g))
                  }
                ).catch(c)
              } catch (g) {
                c(0)
              }
            }
          }
        )
      }
    }
    class ec {
    }
    class ra {
      constructor() {
        this.jc = - 1;
        this.ic = null;
        this.Il = 0;
        this.i = this.B = 63;
        this.dk = 0;
        this.S = 16777215;
        this.Ea = 0.99;
        this.ca = 1;
        this.o = 0.5;
        this.V = 10;
        this.ra = new P(0, 0);
        this.G = new P(0, 0);
        this.a = new P(0, 0)
      }
      ga(a) {
        var b = this.a;
        a.u(b.x);
        a.u(b.y);
        b = this.G;
        a.u(b.x);
        a.u(b.y);
        b = this.ra;
        a.u(b.x);
        a.u(b.y);
        a.u(this.V);
        a.u(this.o);
        a.u(this.ca);
        a.u(this.Ea);
        a.tb(this.S);
        a.R(this.i);
        a.R(this.B)
      }
      ma(a) {
        var b = this.a;
        b.x = a.w();
        b.y = a.w();
        b = this.G;
        b.x = a.w();
        b.y = a.w();
        b = this.ra;
        b.x = a.w();
        b.y = a.w();
        this.V = a.w();
        this.o = a.w();
        this.ca = a.w();
        this.Ea = a.w();
        this.S = a.jb();
        this.i = a.N();
        this.B = a.N()
      }
      wo(a) {
        var b = this.a,
        c = a.a,
        d = b.x - c.x;
        b = b.y - c.y;
        var e = a.V + this.V,
        f = d * d + b * b;
        if (0 < f && f <= e * e) {
          f = Math.sqrt(f);
          d /= f;
          b /= f;
          c = this.ca / (this.ca + a.ca);
          e -= f;
          f = e * c;
          var g = this.a,
          h = this.a;
          g.x = h.x + d * f;
          g.y = h.y + b * f;
          h = g = a.a;
          e -= f;
          g.x = h.x - d * e;
          g.y = h.y - b * e;
          e = this.G;
          f = a.G;
          e = d * (e.x - f.x) +
          b * (e.y - f.y);
          0 > e &&
          (
            e *= this.o * a.o + 1,
            c *= e,
            g = f = this.G,
            f.x = g.x - d * c,
            f.y = g.y - b * c,
            a = f = a.G,
            c = e - c,
            f.x = a.x + d * c,
            f.y = a.y + b * c
          )
        }
      }
      xo(a) {
        if (0 != 0 * a.vb) {
          var b = a.$.a;
          var c = a.ea.a;
          var d = c.x - b.x;
          var e = c.y - b.y,
          f = this.a;
          var g = f.x - c.x;
          c = f.y - c.y;
          f = this.a;
          if (0 >= (f.x - b.x) * d + (f.y - b.y) * e || 0 <= g * d + c * e) return;
          d = a.ya;
          b = d.x;
          d = d.y;
          g = b * g + d * c
        } else {
          d = a.fe;
          g = this.a;
          b = g.x - d.x;
          d = g.y - d.y;
          g = a.Sg;
          c = a.Tg;
          if ((0 < g.x * b + g.y * d && 0 < c.x * b + c.y * d) == 0 >= a.vb) return;
          c = Math.sqrt(b * b + d * d);
          if (0 == c) return;
          g = c - a.tk;
          b /= c;
          d /= c
        }
        c = a.Hc;
        if (0 == c) 0 > g &&
        (g = - g, b = - b, d = - d);
         else if (0 > c && (c = - c, g = - g, b = - b, d = - d), g < - c) return;
        g >= this.V ||
        (
          g = this.V - g,
          e = c = this.a,
          c.x = e.x + b * g,
          c.y = e.y + d * g,
          g = this.G,
          g = b * g.x + d * g.y,
          0 > g &&
          (g *= this.o * a.o + 1, c = a = this.G, a.x = c.x - b * g, a.y = c.y - d * g)
        )
      }
      uc() {
        let a = qa.Cc,
        b = this.ic;
        this.jc != a &&
        (null == b && (this.ic = b = new ra), this.jc = a, ra.zd(b, this));
        return b
      }
      static zd(a, b) {
        a.V = b.V;
        a.o = b.o;
        a.ca = b.ca;
        a.Ea = b.Ea;
        a.S = b.S;
        a.dk = b.dk;
        a.i = b.i;
        a.B = b.B;
        var c = a.a,
        d = b.a;
        c.x = d.x;
        c.y = d.y;
        c = a.G;
        d = b.G;
        c.x = d.x;
        c.y = d.y;
        a = a.ra;
        b = b.ra;
        a.x = b.x;
        a.y = b.y
      }
    }
    class Xb {
      static h(a, b, c, d, e) {
        null != a &&
        a(b, c, d, e)
      }
    }
    class dc {
      constructor(a, b) {
        this.Zj = [];
        this.rr = /[#@][^\s@#]*$/;
        this.Qb = a;
        this.Aq = b;
        a.hidden = !0
      }
      bi() {
        this.kj(null)
      }
      oo(a, b) {
        b = this.rr.exec(O.substr(a, 0, b));
        if (null != b) {
          var c = b[0],
          d = O.substr(c, 1, null).split(''),
          e = dc.ap,
          f = Array(d.length);
          let g = 0,
          h = d.length;
          for (; g < h; ) {
            let l = g++;
            f[l] = e(d[l])
          }
          let k = new RegExp(f.join('.*?'), 'i');
          this.Yk = '#' == c.charAt(0);
          this.Ii = b.index;
          this.Er = c.length;
          this.lm = a;
          a = function (l) {
            l = k.exec(l.D);
            return null == l ? - 1 : l.index + l[0].length
          };
          b = [];
          c = 0;
          for (d = this.Zj; c < d.length; ) e = d[c],
          ++c,
          f = a(e),
          0 <= f &&
          b.push({
            Hn: f,
            item: e
          });
          b.sort(function (l, n) {
            return l.Hn - n.Hn
          });
          this.kj(b)
        } else this.kj(null)
      }
      Gk(a) {
        a = this.Yk ? '#' + a.ba : '@' + aa.replace(a.D, ' ', '_');
        this.Aq(
          O.substr(this.lm, 0, this.Ii) + a + ' ' + O.substr(this.lm, this.Ii + this.Er, null),
          this.Ii + a.length + 1
        )
      }
      kj(a) {
        var b = null != a &&
        0 != a.length;
        this.Qb.hidden ||
        x.Qf(this.Qb);
        this.dd = null;
        this.Qb.hidden = !b;
        if (b) {
          var c = this;
          b = [];
          for (var d = 0; d < a.length; ) {
            var e = a[d++];
            let f = window.document.createElement('div'),
            g = e.item;
            e = g.D;
            this.Yk &&
            (e = '(' + g.ba +
            ') ' + e);
            f.textContent = e;
            this.Qb.appendChild(f);
            f.onclick = function () {
              c.Gk(g)
            };
            b.push({
              item: g,
              La: f
            })
          }
          this.dd = b;
          this.dd[0].La.classList.toggle('selected', !0);
          this.zc = 0
        }
      }
      hk(a) {
        if (null != this.dd) {
          var b = this.zc;
          this.zc += a;
          a = this.dd.length - 1;
          0 > this.zc ? this.zc = a : this.zc > a &&
          (this.zc = 0);
          a = this.dd[this.zc];
          b != this.zc &&
          (
            a.La.classList.toggle('selected', !0),
            this.dd[b].La.classList.toggle('selected', !1)
          );
          a = a.La;
          b = a.offsetTop;
          a = b + a.offsetHeight;
          var c = this.Qb.scrollTop + this.Qb.clientHeight;
          b < this.Qb.scrollTop ? this.Qb.scrollTop = b : a > c &&
          (this.Qb.scrollTop = a - this.Qb.clientHeight)
        }
      }
      Wo() {
        null != this.dd &&
        (this.Gk(this.dd[this.zc].item), this.bi())
      }
      static ap(a) {
        return - 1 != '.$^{[(|)*+?\\'.indexOf(a) ? '\\' + a : a
      }
    }
    class G {
      constructor() {
        this.Dd = 0;
        this.B = 32;
        this.i = 63;
        this.o = 1;
        this.a = new P(0, 0)
      }
      ga(a) {
        let b = this.a;
        a.u(b.x);
        a.u(b.y);
        a.u(this.o);
        a.R(this.i);
        a.R(this.B)
      }
      ma(a) {
        let b = this.a;
        b.x = a.w();
        b.y = a.w();
        this.o = a.w();
        this.i = a.N();
        this.B = a.N()
      }
    }
    class pb {
      constructor(a, b) {
        this.ek = a;
        this.ij = b;
        this.qc = a;
        this.jf = window.performance.now()
      }
      bn() {
        var a;
        null == a &&
        (a = 1);
        this.A();
        return a <= this.qc ? (this.qc -= a, !0) : !1
      }
      os() {
        this.A();
        let a = 1 - this.qc;
        if (0 >= a) return 0;
        let b = window.performance.now();
        return this.jf + a * this.ij - b
      }
      Go(a) {
        let b = this.os();
        --this.qc;
        window.setTimeout(a, b | 0)
      }
      A() {
        let a = window.performance.now(),
        b = Math.floor((a - this.jf) / this.ij);
        this.jf += b * this.ij;
        this.qc += b;
        this.qc >= this.ek &&
        (this.qc = this.ek, this.jf = a)
      }
    }
    class Bb {
      constructor(a) {
        this.f = x.Ia(Bb.O);
        var b = x.Ba(this.f);
        this.Fh = b.get('cancel');
        this.rk = b.get('create');
        this.pf = b.get('name');
        this.Jl = b.get('pass');
        this.ri = b.get('max-pl');
        this.dn = b.get('unlisted');
        this.pf.maxLength = 40;
        this.pf.value = a;
        let c = this;
        this.pf.oninput = function () {
          c.A()
        };
        this.Jl.maxLength = 30;
        this.dn.onclick = function () {
          c.Xj(!c.en)
        };
        this.Fh.onclick = function () {
          H.h(c.ti)
        };
        this.rk.onclick = function () {
          if (c.Ic()) {
            let d = c.Jl.value;
            '' == d &&
            (d = null);
            D.h(
              c.rq,
              {
                name: c.pf.value,
                password: d,
                dt: c.ri.selectedIndex + 2,
                vt: c.en
              }
            )
          }
        };
        for (a = 2; 21 > a; ) b = window.document.createElement('option'),
        b.textContent = '' + a++,
        this.ri.appendChild(b);
        this.ri.selectedIndex = 10;
        this.Xj(!1);
        this.A()
      }
      Xj(a) {
        this.en = a;
        this.dn.textContent = 'Show in room list: ' + (a ? 'No' : 'Yes')
      }
      Ic() {
        let a = this.pf.value;
        return 40 >= a.length ? 0 < a.length : !1
      }
      A() {
        this.rk.disabled = !this.Ic()
      }
    }
    class A {
      constructor(a, b) {
        null == b &&
        (b = !1);
        this.s = a;
        this.Ua = b;
        this.a = 0
      }
      Vg() {
        let a = new ArrayBuffer(this.a),
        b = new Uint8Array(this.s.buffer, this.s.byteOffset, this.a);
        (new Uint8Array(a)).set(b);
        return a
      }
      Wb() {
        return new Uint8Array(this.s.buffer, this.s.byteOffset, this.a)
      }
      Qd() {
        return new DataView(this.s.buffer, this.s.byteOffset, this.a)
      }
      rs() {
        return new J(this.Qd(), this.Ua)
      }
      tc(a) {
        this.s.byteLength < a &&
        this.Hr(2 * this.s.byteLength >= a ? 2 * this.s.byteLength : a)
      }
      Hr(a) {
        if (1 > a) throw v.C('Can\'t resize buffer to a capacity lower than 1');
        if (this.s.byteLength < a) {
          let b = new Uint8Array(this.s.buffer);
          a = new ArrayBuffer(a);
          (new Uint8Array(a)).set(b);
          this.s = new DataView(a)
        }
      }
      m(a) {
        let b = this.a++;
        this.tc(this.a);
        this.s.setUint8(b, a)
      }
      oj(a) {
        let b = this.a;
        this.a += 2;
        this.tc(this.a);
        this.s.setInt16(b, a, this.Ua)
      }
      Xb(a) {
        let b = this.a;
        this.a += 2;
        this.tc(this.a);
        this.s.setUint16(b, a, this.Ua)
      }
      R(a) {
        let b = this.a;
        this.a += 4;
        this.tc(this.a);
        this.s.setInt32(b, a, this.Ua)
      }
      tb(a) {
        let b = this.a;
        this.a += 4;
        this.tc(this.a);
        this.s.setUint32(b, a, this.Ua)
      }
      nj(a) {
        let b = this.a;
        this.a += 4;
        this.tc(this.a);
        this.s.setFloat32(b, a, this.Ua)
      }
      u(a) {
        let b = this.a;
        this.a += 8;
        this.tc(this.a);
        this.s.setFloat64(b, a, this.Ua)
      }
      Lb(a) {
        let b = this.a;
        this.a += a.byteLength;
        this.tc(this.a);
        (
          new Uint8Array(this.s.buffer, this.s.byteOffset, this.s.byteLength)
        ).set(a, b)
      }
      Fs(a) {
        a = new Uint8Array(a.buffer, a.byteOffset, a.byteLength);
        this.Lb(a)
      }
      Yg(a) {
        this.Lb(new Uint8Array(a))
      }
      oc(a) {
        this.nb(A.Eh(a));
        this.pj(a)
      }
      Eb(a) {
        null == a ? this.nb(0) : (this.nb(A.Eh(a) + 1), this.pj(a))
      }
      jn(a) {
        a = (new TextEncoder).encode(a);
        let b = a.length;
        if (255 < b) throw v.C(null);
        this.m(b);
        this.Fs(a)
      }
      Zg(a) {
        this.oc(JSON.stringify(a))
      }
      pj(a) {
        let b = this.a;
        this.tc(b + A.Eh(a));
        let c = a.length,
        d = 0;
        for (; d < c; ) b += A.$o(O.tj(a, d++), this.s, b);
        this.a = b
      }
      nb(a) {
        let b = this.a;
        a >>>= 0;
        this.tc(b + A.mo(a));
        this.s.setUint8(b, a | 128);
        128 <= a ? (
          this.s.setUint8(b + 1, a >> 7 | 128),
          16384 <= a ? (
            this.s.setUint8(b + 2, a >> 14 | 128),
            2097152 <= a ? (
              this.s.setUint8(b + 3, a >> 21 | 128),
              268435456 <= a ? (this.s.setUint8(b + 4, a >> 28 & 127), a = 5) : (this.s.setUint8(b + 3, this.s.getUint8(b + 3) & 127), a = 4)
            ) : (this.s.setUint8(b + 2, this.s.getUint8(b + 2) & 127), a = 3)
          ) : (this.s.setUint8(b + 1, this.s.getUint8(b + 1) & 127), a = 2)
        ) : (this.s.setUint8(b, this.s.getUint8(b) & 127), a = 1);
        this.a += a
      }
      static ka(a, b) {
        null == b &&
        (b = !1);
        null == a &&
        (a = 16);
        return new A(new DataView(new ArrayBuffer(a)), b)
      }
      static $o(a, b, c) {
        let d = c;
        if (0 > a) throw v.C('Cannot encode UTF8 character: charCode (' +
        a + ') is negative');
        if (128 > a) b.setUint8(c, a & 127),
        ++c;
         else if (2048 > a) b.setUint8(c, a >> 6 & 31 | 192),
        b.setUint8(c + 1, a & 63 | 128),
        c += 2;
         else if (65536 > a) b.setUint8(c, a >> 12 & 15 | 224),
        b.setUint8(c + 1, a >> 6 & 63 | 128),
        b.setUint8(c + 2, a & 63 | 128),
        c += 3;
         else if (2097152 > a) b.setUint8(c, a >> 18 & 7 | 240),
        b.setUint8(c + 1, a >> 12 & 63 | 128),
        b.setUint8(c + 2, a >> 6 & 63 | 128),
        b.setUint8(c + 3, a & 63 | 128),
        c += 4;
         else if (67108864 > a) b.setUint8(c, a >> 24 & 3 | 248),
        b.setUint8(c + 1, a >> 18 & 63 | 128),
        b.setUint8(c + 2, a >> 12 & 63 | 128),
        b.setUint8(c + 3, a >> 6 & 63 | 128),
        b.setUint8(c + 4, a & 63 | 128),
        c += 5;
         else if ( - 2147483648 > a) b.setUint8(c, a >> 30 & 1 | 252),
        b.setUint8(c + 1, a >> 24 & 63 | 128),
        b.setUint8(c + 2, a >> 18 & 63 | 128),
        b.setUint8(c + 3, a >> 12 & 63 | 128),
        b.setUint8(c + 4, a >> 6 & 63 | 128),
        b.setUint8(c + 5, a & 63 | 128),
        c += 6;
         else throw v.C(
          'Cannot encode UTF8 character: charCode (' + a + ') is too large (>= 0x80000000)'
        );
        return c - d
      }
      static lo(a) {
        if (0 > a) throw v.C(
          'Cannot calculate length of UTF8 character: charCode (' + a + ') is negative'
        );
        if (128 > a) return 1;
        if (2048 > a) return 2;
        if (65536 > a) return 3;
        if (2097152 > a) return 4;
        if (67108864 >
        a) return 5;
        if ( - 2147483648 > a) return 6;
        throw v.C(
          'Cannot calculate length of UTF8 character: charCode (' + a + ') is too large (>= 0x80000000)'
        );
      }
      static Eh(a) {
        let b = 0,
        c = a.length,
        d = 0;
        for (; d < c; ) b += A.lo(O.tj(a, d++));
        return b
      }
      static mo(a) {
        a >>>= 0;
        return 128 > a ? 1 : 16384 > a ? 2 : 2097152 > a ? 3 : 268435456 > a ? 4 : 5
      }
    }
    class aa {
      static Zs(a, b) {
        a = O.tj(a, b);
        return 8 < a &&
        14 > a ? !0 : 32 == a
      }
      static st(a) {
        let b = a.length,
        c = 0;
        for (; c < b && aa.Zs(a, b - c - 1); ) ++c;
        return 0 < c ? O.substr(a, 0, b - c) : a
      }
      static Of(a) {
        var b;
        let c = '';
        for (b = 2 - a.length; c.length < b; ) c +=
        '0';
        return c + (null == a ? 'null' : '' + a)
      }
      static replace(a, b, c) {
        return a.split(b).join(c)
      }
      static hh(a, b) {
        let c = '';
        do c = '0123456789ABCDEF'.charAt(a & 15) + c,
        a >>>= 4;
        while (0 < a);
        if (null != b) for (; c.length < b; ) c = '0' + c;
        return c
      }
    }
    class zc {
      constructor() {
        this.hash = 0
      }
      Ls(a) {
        let b = 0,
        c = a.length;
        for (; b < c; ) this.hash = (this.hash += a[b++]) + (this.hash << 10),
        this.hash ^= this.hash >>> 6
      }
    }
    class T {
      constructor(a) {
        this.hd = window.performance.now();
        this.Ug = new Map;
        this.nd = new Map;
        this.te = 1;
        this.Dh = 100;
        this.Wg = 35;
        this.Ld = 0;
        this.Ig = 1.5;
        this.Ya = new P(0, 0);
        this.Xk = !1;
        this.Cd = new wc;
        this.Fp = a;
        this.na = window.document.createElement('canvas');
        this.na.mozOpaque = !0;
        this.c = this.na.getContext('2d', {
          alpha: !1,
          desynchronized: a
        });
        this.rp = this.c.createPattern(m.qp, null);
        this.Do = this.c.createPattern(m.Co, null);
        this.Bo = this.c.createPattern(m.Ao, null)
      }
      vp(a, b) {
        a = this.nd.get(a.Z);
        if (null != a) switch (b) {
          case 0:
            a.mg = !0;
            break;
          case 1:
            a.mg = !1
        }
      }
      Bs() {
        if (null != this.na.parentElement) {
          var a = window.devicePixelRatio * this.te;
          let b = this.na.getBoundingClientRect(),
          c = Math.round(b.width * a);
          a = Math.round(b.height * a);
          if (this.na.width != c || this.na.height != a) this.na.width = c,
          this.na.height = a
        }
      }
      Rc(a, b) {
        var c = window.performance.now();
        let d = (c - this.hd) / 1000;
        this.hd = c;
        this.Ug.clear();
        this.Bs();
        T.Wi(this.c, !0);
        this.c.resetTransform();
        if (null != a.M) {
          c = a.M;
          var e = c.va,
          f = a.oa(b),
          g = null != f ? f.I : null,
          h = 0 != this.Ld ? this.na.height / this.Ld : this.Ig * window.devicePixelRatio * this.te;
          b = this.Wg * this.te;
          var k = this.Dh * this.te,
          l = c.T.mf,
          n = this.na.width / h;
          0 < l &&
          n > l &&
          (n = l, h = this.na.width / l);
          l = (this.na.height - b - k) / h;
          this.ys(c, g, n, l, d);
          for (var r = 0, t = a.K; r < t.length; ) {
            let z = t[r];
            ++r;
            if (null == z.I) continue;
            let K = this.nd.get(z.Z);
            null == K &&
            (K = new tb, this.nd.set(z.Z, K));
            K.A(z, a);
            this.Ug.set(z.I, K)
          }
          this.c.translate(this.na.width / 2, (this.na.height + b - k) / 2);
          this.c.scale(h, h);
          this.c.translate( - this.Ya.x, - this.Ya.y);
          this.c.lineWidth = 3;
          this.Br(c.T);
          this.Ar(c.T);
          h = e.H;
          r = 0;
          for (t = e.qb; r < t.length; ) this.vr(t[r++], h);
          this.ur(a, n, l);
          this.wr(a, f);
          null != g &&
          this.yr(g.a);
          this.c.lineWidth = 2;
          f = 0;
          for (g = a.K; f < g.length; ) l = g[f],
          ++f,
          n = l.I,
          null != n &&
          (l = this.nd.get(l.Z), this.km(n, l));
          f = 0;
          for (e = e.H; f < e.length; ) if (g = e[f], ++f, null == this.Ug.get(g)) {
            if (0 > g.V) break;
            this.km(g, null)
          }
          this.c.lineWidth = 3;
          this.c.resetTransform();
          this.c.translate(this.na.width / 2, b + (this.na.height - b - k) / 2);
          this.xr(c);
          0 >= c.Ta &&
          (this.Cd.A(d), this.Cd.Rc(this.c));
          this.Ug.clear();
          this.tr(a)
        }
      }
      tr(a) {
        let b = new Set;
        var c = 0;
        for (a = a.K; c < a.length; ) b.add(a[c++].Z);
        c = this.nd.keys();
        for (a = c.next(); !a.done; ) {
          let d = a.value;
          a = c.next();
          b.has(d) ||
          this.nd.delete(d)
        }
      }
      ys(a, b, c, d, e) {
        if (null != b && 1 == a.T.Ue) {
          var f = b.a;
          var g = f.x;
          f = f.y;
          null == f &&
          (f = 0);
          null == g &&
          (g = 0)
        } else if (f = a.va.H[0].a, g = f.x, f = f.y, null != b) {
          var h = b.a;
          g = 0.5 * (g + h.x);
          f = 0.5 * (f + h.y);
          var k = c;
          b = d;
          null == d &&
          (b = 0);
          null == c &&
          (k = 0);
          var l = 0.5 * k;
          let n = 0.5 * b;
          b = h.x - l + 50;
          k = h.y - n + 50;
          l = h.x + l - 50;
          h = h.y + n - 50;
          g = g > l ? l : g < b ? b : g;
          f = f > h ? h : f < k ? k : f
        }
        e *= 60;
        1 < e &&
        (e = 1);
        b = g;
        b == b ? (b = f, b = b == b) : b = !1;
        b &&
        (k = b = this.Ya, e *= 0.04, h = k.x, k = k.y, b.x = h + (g - h) * e, b.y = k + (f - k) * e);
        this.Eo(c, d, a.T)
      }
      Eo(a, b, c) {
        a > 2 * c.bc ? this.Ya.x = 0 : this.Ya.x + 0.5 * a > c.bc ? this.Ya.x = c.bc - 0.5 * a : this.Ya.x - 0.5 * a < - c.bc &&
        (this.Ya.x = - c.bc +
        0.5 * a);
        b > 2 * c.sc ? this.Ya.y = 0 : this.Ya.y + 0.5 * b > c.sc ? this.Ya.y = c.sc - 0.5 * b : this.Ya.y - 0.5 * b < - c.sc &&
        (this.Ya.y = - c.sc + 0.5 * b)
      }
      yr(a) {
        this.c.beginPath();
        this.c.strokeStyle = 'white';
        this.c.globalAlpha = 0.3;
        this.c.arc(a.x, a.y, 25, 0, 2 * Math.PI, !1);
        this.c.stroke();
        this.c.globalAlpha = 1
      }
      xr(a) {
        let b = 0 < a.Ta;
        this.Wr(b);
        b &&
        (
          120 != a.Ta &&
          (
            a = a.Ta / 120 * 200,
            this.c.fillStyle = 'white',
            this.c.fillRect(0.5 * - a, 100, a, 20)
          ),
          this.Cd.Nq.Cr(this.c)
        )
      }
      Wr(a) {
        this.Xk != a &&
        (this.na.style.filter = a ? 'grayscale(70%)' : '', this.Xk = a)
      }
      um(a, b, c, d, e, f) {
        d = b + d;
        e = c +
        e;
        a.beginPath();
        a.moveTo(d - f, c);
        a.arcTo(d, c, d, c + f, f);
        a.lineTo(d, e - f);
        a.arcTo(d, e, d - f, e, f);
        a.lineTo(b + f, e);
        a.arcTo(b, e, b, e - f, f);
        a.lineTo(b, c + f);
        a.arcTo(b, c, b + f, c, f);
        a.closePath()
      }
      Br(a) {
        T.Wi(this.c, !1);
        var b = a.be;
        let c = a.ae,
        d = this;
        if (1 == a.ud) this.c.save(),
        this.c.resetTransform(),
        this.c.fillStyle = T.nc(a.td),
        this.c.fillRect(0, 0, this.na.width, this.na.height),
        this.c.restore(),
        this.c.strokeStyle = '#C7E6BD',
        this.c.fillStyle = this.rp,
        this.um(this.c, - b, - c, 2 * b, 2 * c, a.Gc),
        this.c.save(),
        this.c.scale(2, 2),
        this.c.fill(),
        this.c.restore(),
        this.c.moveTo(0, - c),
        this.c.lineTo(0, c),
        this.c.stroke(),
        this.c.beginPath(),
        this.c.arc(0, 0, a.bd, 0, 2 * Math.PI),
        this.c.stroke();
         else if (2 == a.ud) {
          this.c.strokeStyle = '#E9CC6E';
          this.c.save();
          this.c.beginPath();
          this.c.rect(this.Ya.x - 10000, this.Ya.y - 10000, 20000, 20000);
          this.c.scale(2, 2);
          this.c.fillStyle = this.Bo;
          this.c.fill();
          this.c.restore();
          this.c.save();
          this.um(this.c, - b, - c, 2 * b, 2 * c, a.Gc);
          this.c.scale(2, 2);
          this.c.fillStyle = this.Do;
          this.c.fill();
          this.c.restore();
          this.c.stroke();
          this.c.beginPath();
          this.c.moveTo(0, - c);
          this.c.setLineDash([15,
          15]);
          this.c.lineTo(0, c);
          this.c.stroke();
          this.c.setLineDash([]);
          var e = a.Te;
          b -= e;
          e < a.Gc &&
          (b = 0);
          e = function (f, g, h) {
            d.c.beginPath();
            d.c.strokeStyle = f;
            d.c.arc(0, 0, a.bd, - 1.5707963267948966, 1.5707963267948966, h);
            0 != g &&
            (d.c.moveTo(g, - c), d.c.lineTo(g, c));
            d.c.stroke()
          };
          e('#85ACF3', b, !1);
          e('#E18977', - b, !0)
        } else this.c.save(),
        this.c.resetTransform(),
        this.c.fillStyle = T.nc(a.td),
        this.c.fillRect(0, 0, this.na.width, this.na.height),
        this.c.restore();
        T.Wi(this.c, !0)
      }
      wr(a, b) {
        let c = m.j.Uk.v(),
        d = 0;
        for (a = a.K; d < a.length; ) {
          let f = a[d];
          ++d;
          var e = f.I;
          if (null == e) continue;
          e = e.a;
          let g = this.nd.get(f.Z);
          c &&
          g.mg &&
          this.c.drawImage(m.cn, e.x - 0.5 * m.cn.width, e.y - 35);
          f != b &&
          g.Yo(this.c, e.x, e.y + 50)
        }
      }
      km(a, b) {
        0 > a.V ||
        (
          this.c.beginPath(),
          null == b ? (this.c.fillStyle = T.nc(a.S), this.c.strokeStyle = 'black') : (this.c.fillStyle = b.$j, this.c.strokeStyle = b.Ro),
          this.c.beginPath(),
          this.c.arc(a.a.x, a.a.y, a.V, 0, 2 * Math.PI, !1),
          null != b ? (
            this.c.save(),
            b = a.V / 32,
            this.c.translate(a.a.x, a.a.y),
            this.c.scale(b, b),
            this.c.translate( - 32, - 32),
            this.c.fill(),
            this.c.restore()
          ) : - 1 != (a.S | 0) &&
          this.c.fill(),
          this.c.stroke()
        )
      }
      Ar(a) {
        if (null != a) {
          var b = 0;
          for (a = a.X; b < a.length; ) this.zr(a[b++])
        }
      }
      vr(a, b) {
        if (!(0 > a.S)) {
          this.c.beginPath();
          this.c.strokeStyle = T.nc(a.S);
          var c = b[a.ge];
          a = b[a.he];
          null != c &&
          null != a &&
          (
            c = c.a,
            a = a.a,
            this.c.moveTo(c.x, c.y),
            this.c.lineTo(a.x, a.y),
            this.c.stroke()
          )
        }
      }
      zr(a) {
        if (a.bb) {
          this.c.beginPath();
          this.c.strokeStyle = T.nc(a.S);
          var b = a.$.a,
          c = a.ea.a;
          if (0 != 0 * a.vb) this.c.moveTo(b.x, b.y),
          this.c.lineTo(c.x, c.y);
           else {
            a = a.fe;
            let d = b.x - a.x;
            b = b.y -
            a.y;
            this.c.arc(
              a.x,
              a.y,
              Math.sqrt(d * d + b * b),
              Math.atan2(b, d),
              Math.atan2(c.y - a.y, c.x - a.x)
            )
          }
          this.c.stroke()
        }
      }
      ur(a, b, c) {
        var d = a.M;
        if (null != d) for (d = d.va.H[0], this.Ik(d.a, d.S, b, c), d = 0, a = a.K; d < a.length; ) {
          let e = a[d];
          ++d;
          null != e.I &&
          this.Ik(e.I.a, e.fa.S, b, c)
        }
      }
      Ik(a, b, c, d) {
        c = 0.5 * c - 25;
        var e = 0.5 * d - 25;
        null == e &&
        (e = 0);
        null == c &&
        (c = 0);
        d = c;
        c = e;
        var f = this.Ya;
        e = a.x - f.x;
        f = a.y - f.y;
        let g = - d,
        h = - c,
        k = this.Ya;
        d = k.x + (e > d ? d : e < g ? g : e);
        c = k.y + (f > c ? c : f < h ? h : f);
        e = a.x - d;
        a = a.y - c;
        900 < e * e + a * a &&
        (
          this.c.fillStyle = 'rgba(0,0,0,0.5)',
          this.Jk(d + 2, c + 2, Math.atan2(a, e)),
          this.c.fillStyle = T.nc(b),
          this.Jk(d - 2, c - 2, Math.atan2(a, e))
        )
      }
      Jk(a, b, c) {
        this.c.save();
        this.c.translate(a, b);
        this.c.rotate(c);
        this.c.beginPath();
        this.c.moveTo(15, 0);
        this.c.lineTo(0, 7);
        this.c.lineTo(0, - 7);
        this.c.closePath();
        this.c.fill();
        this.c.restore()
      }
      Gr() {
        let a = this.nd.values(),
        b = a.next();
        for (; !b.done; ) {
          let c = b.value;
          b = a.next();
          c.mg = !1
        }
      }
      static nc(a) {
        return 'rgba(' + [(a & 16711680) >>> 16,
        (a & 65280) >>> 8,
        a & 255].join() + ',255)'
      }
      static Wi(a, b) {
        a.imageSmoothingEnabled = b;
        a.mozImageSmoothingEnabled = b
      }
    }
    class mc {
      constructor(a, b) {
        this.r = new RegExp(a, b.split('u').join(''))
      }
      match(a) {
        this.r.global &&
        (this.r.lastIndex = 0);
        this.r.pc = this.r.exec(a);
        this.r.ph = a;
        return null != this.r.pc
      }
      xn(a) {
        if (null != this.r.pc && 0 <= a && a < this.r.pc.length) return this.r.pc[a];
        throw v.C('EReg::matched');
      }
      ct() {
        if (null == this.r.pc) throw v.C('No string matched');
        return {
          Dj: this.r.pc.index,
          $s: this.r.pc[0].length
        }
      }
      bt(a, b) {
        var c;
        null == c &&
        (c = - 1);
        if (this.r.global) {
          this.r.lastIndex = b;
          this.r.pc = this.r.exec(0 > c ? a : O.substr(a, 0, b + c));
          if (b = null !=
          this.r.pc) this.r.ph = a;
          return b
        }
        if (c = this.match(0 > c ? O.substr(a, b, null) : O.substr(a, b, c))) this.r.ph = a,
        this.r.pc.index += b;
        return c
      }
    }
    class Z {
      static om(a, b, c, d, e) {
        return new Promise(
          function (f, g) {
            let h = new XMLHttpRequest;
            h.open(b, a);
            h.responseType = c;
            h.onload = function () {
              200 <= h.status &&
              300 > h.status ? null != h.response ? f(h.response) : g(null) : g('status: ' + h.status)
            };
            h.onerror = function (k) {
              g(k)
            };
            null != e &&
            h.setRequestHeader('Content-type', e);
            h.send(d)
          }
        )
      }
      static v(a, b) {
        return Z.om(a, 'GET', b, null)
      }
      static Nk(a) {
        return Z.v(a, 'json').then(
          function (b) {
            let c = b.error;
            if (null != c) throw v.C(c);
            return b.data
          }
        )
      }
      static Vq(a, b, c) {
        return Z.om(a, 'POST', 'json', b, c)
      }
      static Yl(a, b, c) {
        return Z.Vq(a, b, c).then(
          function (d) {
            let e = d.error;
            if (null != e) throw v.C(e);
            return d.data
          }
        )
      }
    }
    class fc {
      constructor(a, b, c, d, e, f) {
        this.zh = this.Kh = !1;
        this.ua = new Ja(0, b, d);
        let g = this;
        this.ua.kd = function () {
          g.ie(ia.Zd)
        };
        this.ua.Hd = function () {
          null != g.Hd &&
          g.Hd(new Yb(g.ua));
          g.ua = null;
          g.nk()
        };
        (
          async function () {
            try {
              let h = await g.ua.Lo();
              g.aa = new WebSocket(a + 'client?id=' +
              c + (null == f ? '' : '&token=' + f));
              g.aa.binaryType = 'arraybuffer';
              g.aa.onclose = function (k) {
                g.Kh ||
                g.ie(ia.Ne(k.code))
              };
              g.aa.onerror = function () {
                g.Kh ||
                g.ie(ia.Error)
              };
              g.aa.onmessage = M(g, g.ai);
              g.aa.onopen = function () {
                null != g.Fl &&
                g.Fl();
                g.ua.cj();
                g.Ri(h, g.ua.ig, e);
                g.ua.xg = M(g, g.Oi);
                g.ua.jg.then(function () {
                  g.Uc(0, null)
                })
              }
            } catch (h) {
              g.ie(ia.Zd)
            }
          }
        ) ()
      }
      no() {
        this.ie(ia.Me)
      }
      nk() {
        null != this.aa &&
        (
          this.aa.onclose = null,
          this.aa.onmessage = null,
          this.aa.onerror = null,
          this.aa.onopen = null,
          this.aa.close(),
          this.aa = null
        );
        null != this.ua &&
        (this.ua.la(), this.ua = null)
      }
      ie(a) {
        null != this.kd &&
        this.kd(a);
        this.nk()
      }
      ai(a) {
        var b = new J(new DataView(a.data));
        a = b.F();
        0 < b.s.byteLength - b.a &&
        (b = new J(new DataView(pako.inflateRaw(b.sb()).buffer), !1));
        switch (a) {
          case 1:
            a = b.kc();
            b = b.Jg();
            let c = [],
            d = 0;
            for (; d < b.length; ) c.push(new RTCIceCandidate(b[d++]));
            this.$h(a, c);
            break;
          case 4:
            this.Zh(new RTCIceCandidate(b.Jg()))
        }
      }
      $h(a, b) {
        this.ua.cj(this.zh ? 10000 : 4000);
        this.Kh = !0;
        null != this.wl &&
        this.wl();
        let c = this;
        this.ua.Sa.setRemoteDescription(new RTCSessionDescription({
          sdp: a,
          type: 'answer'
        })).then(
          function () {
            let d = 0;
            for (; d < b.length; ) c.ua.Sa.addIceCandidate(b[d++])
          }
        ).catch(function () {
          c.ie(ia.Error)
        })
      }
      Zh(a) {
        this.ua.Sa.addIceCandidate(a)
      }
      Uc(a, b) {
        if (null != this.aa) {
          var c = A.ka(32, !1);
          c.m(a);
          null != b &&
          (a = pako.deflateRaw(b.Wb()), c.Lb(a));
          this.aa.send(c.Qd())
        }
      }
      Ri(a, b, c) {
        let d = A.ka(32, !1);
        d.m(this.zh ? 1 : 0);
        d.oc(a.sdp);
        d.Zg(b);
        null != c &&
        d.Lb(c.Wb());
        this.Uc(1, d)
      }
      Oi(a) {
        let b = A.ka(32, !1);
        b.Zg(a);
        this.Uc(4, b)
      }
      static jp(a) {
        switch (a.pb) {
          case 0:
            return 'Failed';
          case 1:
            return Lc.description(a.code);
          case 2:
            return '';
          case 3:
            return 'Master connection error'
        }
      }
    }
    class qb {
      constructor(a, b) {
        this.f = x.Ia(qb.O);
        let c = x.Ba(this.f);
        this.nf = c.get('name');
        this.Xf = c.get('admin');
        this.df = c.get('kick');
        this.wd = c.get('close');
        let d = this;
        this.Xf.onclick = function () {
          za.h(d.kq, d.Rb, !d.Pl)
        };
        this.df.onclick = function () {
          D.h(d.ui, d.Rb)
        };
        this.wd.onclick = function () {
          H.h(d.rb)
        };
        this.Rb = a.Z;
        this.Wj(a.D);
        this.Vj(a.fb);
        this.Xf.disabled = !b ||
        0 == this.Rb;
        this.df.disabled = !b ||
        0 == this.Rb
      }
      A(a, b) {
        a = a.oa(this.Rb);
        null == a ? H.h(this.rb) : (
          this.zs(a),
          this.Xf.disabled = !b ||
          0 == this.Rb,
          this.df.disabled = !b ||
          0 == this.Rb
        )
      }
      zs(a) {
        this.pe != a.D &&
        this.Wj(a.D);
        this.Pl != a.fb &&
        this.Vj(a.fb)
      }
      Wj(a) {
        this.pe = a;
        this.nf.textContent = a
      }
      Vj(a) {
        this.Pl = a;
        this.Xf.textContent = a ? 'Remove Admin' : 'Give Admin'
      }
    }
    class cb extends p {
      constructor() {
        super ()
      }
      apply(a) {
        a.zo(this.dh)
      }
      wa(a) {
        a.nb(this.dh.byteLength);
        a.Yg(this.dh)
      }
      xa(a) {
        this.dh = a.bm(a.Bb())
      }
    }
    class oa extends W {
      constructor(a) {
        W.yb ? super () : (W.yb = !0, super (), W.yb = !1, this.Za(a))
      }
      Za(a) {
        this.hj = new db;
        this.De = this.ec = 0;
        this.ve = new db;
        this.xc = this.dc = this.Ad = 0;
        this.Ec = 0.06;
        this.vh = 16.666666666666668;
        this.Vf = 120;
        super.Za(a)
      }
      ta() {
        throw v.C('missing implementation');
      }
      hg() {
        throw v.C('missing implementation');
      }
      A() {
        throw v.C('missing implementation');
      }
      Rj(a) {
        let b = this.ve.list,
        c = 0,
        d = b.length,
        e = 0;
        for (; e < a; ) {
          for (++e; c < d; ) {
            let f = b[c];
            if (f.ob != this.Y) break;
            f.apply(this.U);
            null != this.hc &&
            this.hc(f);
            this.ec++;
            ++c
          }
          this.U.A(1);
          this.De += this.ec;
          this.ec = 0;
          this.Y++
        }
        for (; c < d; ) {
          a = b[c];
          if (a.ob != this.Y || a.Dc != this.ec) break;
          a.apply(this.U);
          null != this.hc &&
          this.hc(a);
          this.ec++;
          ++c
        }
        b.splice(0, c)
      }
      Pg(a) {
        a.ob == this.Y &&
        a.Dc <= this.ec ? (a.Dc = this.ec++, a.apply(this.U), null != this.hc && this.hc(a)) : this.ve.rn(a)
      }
      Qk(a, b) {
        if (0 >= a) return this.U;
        a > this.Vf &&
        (a = this.Vf);
        qa.Cc++;
        let c = this.U.uc();
        null != b ? (this.hj.Os(this.ve, b), b = this.hj) : b = this.ve;
        b = b.list;
        let d = 0,
        e = b.length,
        f = this.Y,
        g = a | 0,
        h = f + g;
        for (; f <= h; ) {
          for (; d < e; ) {
            let k = b[d];
            if (k.ob > f) break;
            k.Ge.Ca &&
            k.apply(c);
            ++d
          }
          c.A(f != h ? 1 : a - g);
          ++f
        }
        for (a = this.hj.list; 0 < a.length; ) a.pop();
        return c
      }
      Vr(a) {
        300 < a &&
        (a = 300);
        0 > a &&
        (a = 0);
        this.dc = this.Ec * a | 0
      }
      Fm(a) {
        this.Ad = this.Ec * ( - 200 > a ? - 200 : 1000 < a ? 1000 : a)
      }
    }
    class Oa extends oa {
      constructor(a, b) {
        W.yb = !0;
        super ();
        W.yb = !1;
        this.Za(a, b)
      }
      Za(a, b) {
        this.Ti = [];
        this.Fi = [];
        this.Hg = new db;
        this.hq = 1;
        this.yd = this.Xm = 0;
        this.gj = new Qb(50);
        this.Gg = new Qb(50);
        this.Pn = 500;
        this.zk = '';
        super.Za(b.state);
        this.gi = b.xt;
        this.Xe = b.Rs;
        let c = null,
        d = this;
        c = function (e) {
          d.If(0);
          let f = A.ka();
          f.Xb(b.version);
          f.Eb(b.password);
          d.rc = new fc(b.Aj, b.iceServers, a, oc.channels, f, b.Kn);
          d.rc.zh = e;
          d.rc.Hd = function (h) {
            d.rc = null;
            d.ua = h;
            h.zg = function (k) {
              k = new J(new DataView(k));
              d.cr(k)
            };
            h.tf = function () {
              3 != d.yd &&
              D.h(d.uf, ja.Tf('Connection closed'));
              d.la()
            };
            h = window.setTimeout(function () {
              D.h(d.uf, ja.Tf('Game state timeout'));
              d.la()
            }, 10000);
            d.Be = h;
            d.If(2)
          };
          d.rc.Fl = function () {
            d.If(1)
          };
          let g = !1;
          d.rc.wl = function () {
            g = !0
          };
          d.rc.kd = function (h) {
            if (!e && 1 == d.yd && g) H.h(d.Bq),
            c(!0);
             else {
              let k = fc.jp(h);
              switch (h.pb) {
                case 0:
                  h = ja.Zd;
                  break;
                case 1:
                  h = ja.Ne(h.code);
                  break;
                case 2:
                  h = ja.Me;
                  break;
                default:
                  h = ja.Tf(k)
              }
              D.h(d.uf, h);
              d.la(k)
            }
          }
        };
        c(null != b.En && b.En)
      }
      la(a) {
        null !=
        this.rc &&
        (this.rc.kd = null, this.rc.no(), this.rc = null);
        window.clearTimeout(this.Be);
        null != this.ua &&
        (this.ua.tf = null, this.ua.la(), this.ua = null);
        this.zk = null == a ? 'Connection closed' : a;
        this.If(4)
      }
      If(a) {
        this.yd != a &&
        (this.yd = a, null != this.Id && this.Id(a))
      }
      Ed() {
        return 3 == this.yd
      }
      A() {
        this.Ed() &&
        window.performance.now() - this.Xm > this.Pn &&
        this.Pi();
        this.ed = window.performance.now() * this.Ec + this.gj.mh() - this.Y;
        this.fk()
      }
      hg() {
        return this.Ed() ? (
          0 > this.dc &&
          (this.dc = 0),
          this.Qk(
            window.performance.now() * this.Ec + this.gj.mh() -
            this.Y + this.dc + this.Ad,
            this.Hg
          )
        ) : this.U
      }
      fk() {
        0 > this.ed &&
        (this.ed = 0);
        this.ed > this.Vf &&
        (this.ed = this.Vf)
      }
      cr(a) {
        switch (a.F()) {
          case 0:
            this.$q(a);
            break;
          case 1:
            this.Zq(a);
            break;
          case 2:
            this.Wq(a);
            break;
          case 3:
            this.er(a);
            break;
          case 4:
            this.br(a);
            break;
          case 5:
            this.Yq(a);
            break;
          case 6:
            this.dr(a)
        }
      }
      $q(a) {
        a = a.sb(a.Bb());
        let b = Promise.resolve(null);
        null != this.Xe &&
        (b = this.Xe.hs(a));
        let c = this;
        b.catch(function () {
          return null
        }).then(function (d) {
          c.Sr(d)
        })
      }
      Zq(a) {
        a = pako.inflateRaw(a.sb());
        a = new J(new DataView(a.buffer, a.byteOffset, a.byteLength));
        this.xc = a.Sb();
        this.Y = a.jb();
        this.De = a.jb();
        this.ec = a.Bb();
        this.ed = 10;
        for (this.U.ma(a); 0 < a.s.byteLength - a.a; ) this.Pg(this.fn(a));
        window.clearTimeout(this.Be);
        this.If(3)
      }
      Sr(a) {
        let b = A.ka();
        b.m(0);
        null != a ? (b.nb(a.byteLength), b.Lb(a)) : b.nb(0);
        b.nb(this.gi.byteLength);
        b.Yg(this.gi);
        this.Vb(b);
        this.gi = null
      }
      Vb(a, b) {
        null == b &&
        (b = 0);
        this.ua.Vb(b, a)
      }
      fn(a) {
        let b = a.jb(),
        c = a.Bb(),
        d = a.Sb(),
        e = a.jb();
        a = p.th(a);
        a.P = d;
        a.Fe = e;
        a.ob = b;
        a.Dc = c;
        return a
      }
      Wq(a) {
        a = this.fn(a);
        this.Pg(a);
        a.P == this.xc &&
        this.Hg.pt(a.Fe);
        this.$l()
      }
      dr(a) {
        a = p.th(a);
        a.P = 0;
        a.Fe = 0;
        a.apply(this.U);
        null != this.hc &&
        this.hc(a)
      }
      er(a) {
        let b = a.jb();
        a = a.jb();
        this.Fi.push({
          frame: b,
          Nf: a
        });
        this.$l()
      }
      $l() {
        if (3 == this.yd) {
          for (var a = 0, b = this.Fi; a < b.length; ) {
            var c = b[a];
            ++a;
            c.frame <= this.Y ||
            c.Nf == this.De + this.ec + this.ve.Ps(c.frame) &&
            this.Yn(c.frame - this.Y)
          }
          a = 0;
          b = this.Fi;
          c = 0;
          for (var d = b.length; c < d; ) {
            let e = b[c++];
            e.frame > this.Y &&
            (b[a] = e, ++a)
          }
          for (; b.length > a; ) b.pop();
          this.Hg.ot(this.Y)
        }
      }
      Yq(a) {
        let b = 0 != a.F(),
        c = a.kc(),
        d = '';
        0 < a.s.byteLength -
        a.a &&
        (d = a.kc());
        a = b ? 'You were banned' : 'You were kicked';
        '' != d &&
        (a += ' by ' + d);
        '' != c &&
        (a += ' (' + c + ')');
        this.la(a)
      }
      br(a) {
        var b = a.w();
        a = a.w();
        let c = window.performance.now() - a;
        this.gj.add(b - a * this.Ec);
        this.Gg.add(c);
        let d = b = 0,
        e = this.Ti;
        for (; d < e.length; ) {
          let f = e[d];
          ++d;
          if (f > a) break;
          f < a ? D.h(this.Cl, - 1) : D.h(this.Cl, c);
          ++b
        }
        this.Ti.splice(0, b)
      }
      Pi() {
        let a = window.performance.now();
        this.Xm = a;
        this.Ti.push(a);
        let b = this.Gg.mh() | 0,
        c = A.ka();
        c.m(2);
        c.u(a);
        c.nb(b);
        this.Vb(c, 2)
      }
      Yn(a) {
        this.Rj(a);
        this.ed -= a;
        this.fk()
      }
      ta(a) {
        if (3 ==
        this.yd) {
          var b = this.hq++,
          c = 0;
          0 > this.dc &&
          (this.dc = 0);
          a.Ge.delay &&
          (c = this.Y + (this.ed | 0) + this.dc);
          var d = A.ka();
          d.m(1);
          d.tb(c);
          d.tb(b);
          p.Cj(a, d);
          this.Vb(d);
          a.Ge.Ca &&
          (a.Fe = b, a.P = this.xc, a.ob = c, this.Hg.rn(a))
        }
      }
      static Jh(a) {
        switch (a.pb) {
          case 0:
            return 'Cancelled';
          case 1:
            return 'Failed to connect to peer.';
          case 2:
            return Lc.description(a.reason);
          case 3:
            return a.description
        }
      }
    }
    class Zb extends oa {
      constructor(a) {
        W.yb = !0;
        super ();
        W.yb = !1;
        this.Za(a)
      }
      Za(a) {
        this.bk = new Map;
        this.Jb = null;
        this.tg = 32;
        this.We = new Map;
        this.cc = [];
        this.Od = 2;
        this.to = 600;
        super.Za(a.state);
        this.aq = a.Aj;
        this.Ds = a.version;
        this.bq = 1;
        this.cl = this.xc = 0;
        this.bj = window.performance.now();
        this.Oc = new Jb(this.aq, a.iceServers, oc.channels, a.Kn);
        this.Oc.qk = M(this, this.up);
        let b = this;
        this.Oc.Al = function (c) {
          b.uq(c)
        };
        this.Oc.yg = function (c) {
          D.h(b.yg, c)
        };
        this.Oc.vf = function (c, d) {
          null != b.vf &&
          b.vf(c, d)
        }
      }
      la() {
        this.Oc.la();
        let a = 0,
        b = this.cc;
        for (; a < b.length; ) {
          let c = b[a++].ua;
          c.tf = null;
          c.zg = null;
          c.la()
        }
      }
      Zo(a, b, c, d) {
        let e = this.We.get(a);
        if (null != e) {
          if (d) {
            let f = this.Oc.co(e.ua);
            this.bk.set(a, f)
          }
          a = A.ka();
          a.m(5);
          a.m(d ? 1 : 0);
          a.oc(b);
          null == c &&
          (c = '');
          a.oc(c);
          e.Vb(a);
          e.ua.la()
        }
      }
      ce() {
        this.Oc.ce();
        this.bk.clear()
      }
      Vi(a) {
        this.Oc.Vi(a)
      }
      Ui(a) {
        this.Oc.Ui(a)
      }
      ta(a) {
        a.P = 0;
        let b = this.Y + this.Od + this.dc;
        a.Ge.delay ||
        (b = this.Y);
        a.ob = b;
        this.Pg(a);
        this.Si();
        0 < this.cc.length &&
        this.Qg(this.oi(a), 1)
      }
      A() {
        let a = ((window.performance.now() - this.bj) * this.Ec | 0) - this.Y;
        0 < a &&
        this.Rj(a);
        7 <= this.Y - this.dl &&
        this.Si();
        this.Y - this.cl >= this.to &&
        (this.Si(), this.Qr())
      }
      hg() {
        0 > this.dc &&
        (this.dc = 0);
        return this.Qk(
          (window.performance.now() -
          this.bj) * this.Ec - this.Y + this.Od + this.dc + this.Ad
        )
      }
      up(a, b) {
        if (this.cc.length >= this.tg) return fb.Uf(4100);
        try {
          if (b.Sb() != this.Ds) throw v.C(null);
        } catch (c) {
          return fb.Uf(4103)
        }
        try {
          let c = b.Ab();
          if (null != this.Jb && c != this.Jb) throw v.C(null);
        } catch (c) {
          return fb.Uf(4101)
        }
        return fb.Kj
      }
      uq(a) {
        if (this.cc.length >= this.tg) a.la();
         else {
          var b = new tc(a);
          this.cc.push(b);
          var c = this;
          a.zg = function (d) {
            c.Xq(d, b)
          };
          a.tf = function () {
            O.remove(c.cc, b);
            c.We.delete(b.ba);
            D.h(c.qq, b.ba)
          };
          a = A.ka(1 + b.Ve.byteLength);
          a.m(0);
          a.nb(b.Ve.byteLength);
          a.Lb(b.Ve);
          b.Vb(a)
        }
      }
      oi(a) {
        let b = A.ka();
        b.m(2);
        this.Hl(a, b);
        return b
      }
      Hl(a, b) {
        b.tb(a.ob);
        b.nb(a.Dc);
        b.Xb(a.P);
        b.tb(a.Fe);
        p.Cj(a, b)
      }
      Si() {
        if (!(0 >= this.Y - this.dl) && 0 != this.cc.length) {
          var a = A.ka();
          a.m(3);
          a.tb(this.Y);
          a.tb(this.De);
          this.Qg(a, 2);
          this.dl = this.Y
        }
      }
      Qg(a, b) {
        null == b &&
        (b = 0);
        let c = 0,
        d = this.cc;
        for (; c < d.length; ) {
          let e = d[c];
          ++c;
          e.Lg &&
          e.Vb(a, b)
        }
      }
      Rr(a) {
        let b = A.ka();
        b.m(1);
        let c = A.ka();
        c.Xb(a.ba);
        c.tb(this.Y);
        c.tb(this.De);
        c.nb(this.ec);
        this.U.ga(c);
        let d = this.ve.list,
        e = 0,
        f = d.length;
        for (; e < f; ) this.Hl(d[e++], c);
        b.Lb(pako.deflateRaw(c.Wb()));
        a.Vb(b)
      }
      Qr() {
        this.cl = this.Y;
        if (0 != this.cc.length) {
          var a = new cb;
          a.ob = this.Y;
          a.Dc = this.ec++;
          a.P = 0;
          a.dh = this.U.gp();
          this.Qg(this.oi(a))
        }
      }
      gr(a, b) {
        let c = a.sb(a.Bb()),
        d = a.sb(a.Bb());
        a = b.Ve;
        b.Ve = null;
        let e = this;
        U.Cs(c, a).catch(function () {
          return null
        }).then(
          function (f) {
            try {
              if ( - 1 != e.cc.indexOf(b)) {
                b.yt = f;
                var g = e.bq++;
                b.ba = g;
                e.We.set(g, b);
                za.h(
                  e.pq,
                  g,
                  new J(new DataView(d.buffer, d.byteOffset, d.byteLength), !1)
                );
                b.Lg = !0;
                e.Rr(b)
              }
            } catch (h) {
              f = v.Mb(h).Fb(),
              e.Rk(b, f)
            }
          }
        )
      }
      Xq(a, b) {
        this.A();
        try {
          let c = new J(new DataView(a));
          if (!b.np.bn()) throw v.C(1);
          let d = c.F();
          if (b.Lg) switch (d) {
            case 1:
              this.hr(c, b);
              break;
            case 2:
              this.ar(c, b);
              break;
            default:
              throw v.C(0);
          } else if (0 == d) this.gr(c, b);
           else throw v.C(0);
          if (0 < c.s.byteLength - c.a) throw v.C(2);
        } catch (c) {
          this.Rk(b, v.Mb(c).Fb())
        }
      }
      Rk(a, b) {
        pa.console.log(b);
        this.We.delete(a.ba);
        O.remove(this.cc, a);
        a.Lg &&
        null != this.yl &&
        this.yl(a.ba);
        a.ua.la()
      }
      ar(a, b) {
        let c = a.w();
        b.zb = a.Bb();
        a = A.ka();
        a.m(4);
        a.u((window.performance.now() - this.bj) * this.Ec + this.Od);
        a.u(c);
        b.Vb(a, 2)
      }
      hr(a, b) {
        var c = a.jb();
        let d = a.jb();
        a = p.th(a);
        var e = a.Ge.nh;
        if (null != e) {
          var f = b.Pj.get(e);
          null == f &&
          (f = new pb(e.bh, e.sh), b.Pj.set(e, f));
          if (!f.bn()) throw v.C(3);
        }
        e = this.Y + this.Od;
        f = this.Y;
        var g = this.Y + 20;
        f = c < f ? f : c > g ? g : c;
        g = c - e;
        if (a.Ge.delay) {
          if (g < - this.Od - 3) f = e;
           else {
            let h = - this.Od,
            k = this.Od;
            b.rl.Pa(g < h ? h : g > k ? k : g)
          }
          f < e &&
          - 0.85 > b.rl.ao() &&
          (f = e);
          f < b.ci &&
          (f = b.ci);
          b.ci = f
        }
        a.Fn = g;
        c = f - c;
        a.Gn = 0 < c ? c : 0;
        a.Fe = d;
        a.P = b.ba;
        a.ob = f;
        a.Bn(this.U) &&
        (this.Pg(a), this.Qg(this.oi(a), 1))
      }
    }
    class $b extends oa {
      constructor(a, b, c) {
        W.yb = !0;
        super ();
        W.yb = !1;
        this.Za(a, b, c)
      }
      Za(a, b, c) {
        this.ol = [];
        this.Ol = 5;
        this.Pd = - 1;
        this.vg = this.Ub = this.ii = this.Mk = 0;
        super.Za(b);
        a = new J(new DataView(a.buffer), !1);
        if (1212305970 != a.jb()) throw v.C('');
        b = a.jb();
        if (c != b) throw v.C(new ac(b));
        this.Bf = a.jb();
        c = pako.inflateRaw(a.sb());
        this.Sc = new J(new DataView(c.buffer, c.byteOffset, c.byteLength));
        this.kr(this.Sc);
        c = this.Sc.sb();
        this.Sc = new J(new DataView(c.buffer, c.byteOffset, c.byteLength), !1);
        this.Ki();
        this.ii = window.performance.now();
        this.xc = - 1
      }
      kr(a) {
        let b = a.Sb(),
        c = 0,
        d = 0;
        for (; d < b; ) {
          ++d;
          c += a.Bb();
          let e = a.F();
          this.ol.push({
            Dj: c / this.Bf,
            kind: e
          })
        }
      }
      cm() {
        var a = this.Sc;
        0 < a.s.byteLength - a.a ? (
          a = this.Sc.Bb(),
          this.vg += a,
          a = this.Sc.Sb(),
          this.ug = p.th(this.Sc),
          this.ug.P = a
        ) : this.ug = null
      }
      mp() {
        return this.Y / this.Bf
      }
      ta() {
      }
      hg() {
        this.A();
        qa.Cc++;
        let a = this.U.uc();
        a.A(this.Mk);
        return a
      }
      A() {
        var a = window.performance.now(),
        b = a - this.ii;
        this.ii = a;
        0 < this.Pd ? (this.Ub += 10000, this.Ub > this.Pd && (this.Ub = this.Pd, this.Pd = - 1)) : this.Ub += b * this.Ol;
        a = this.Bf * this.vh;
        this.Ub > a &&
        (this.Ub = a);
        b = this.Ub * this.Ec;
        a = b | 0;
        for (this.Mk = b - a; this.Y < a; ) {
          for (; null != this.ug && this.vg == this.Y; ) b = this.ug,
          b.apply(this.U),
          null != this.hc &&
          this.hc(b),
          this.cm();
          this.Y++;
          this.U.A(1)
        }
      }
      Or(a) {
        this.Pd = a;
        a < this.Ub &&
        this.Ki()
      }
      Ki() {
        this.vg = 0;
        this.Ub = this.Y = this.Sc.a = 0;
        this.U.ma(this.Sc);
        this.cm()
      }
    }
    class Da extends p {
      constructor() {
        super ()
      }
      apply(a) {
        let b = a.oa(this.P);
        null != b &&
        this.kh != b.Td &&
        (b.Td = this.kh, D.h(a.Rl, b))
      }
      wa(a) {
        a.m(this.kh ? 1 : 0)
      }
      xa(a) {
        this.kh = 0 != a.F()
      }
      static qa(a) {
        let b = new Da;
        b.kh = a;
        return b
      }
    }
    class Eb extends p {
      constructor() {
        super ()
      }
      apply(a) {
        0 ==
        this.P &&
        Xb.h(a.tm, this.$c, this.color, this.style, this.Jn)
      }
      wa(a) {
        a.oc(ha.Xc(this.$c, 1000));
        a.R(this.color);
        a.m(this.style);
        a.m(this.Jn)
      }
      xa(a) {
        this.$c = a.kc();
        if (1000 < this.$c.length) throw v.C('message too long');
        this.color = a.N();
        this.style = a.F();
        this.Jn = a.F()
      }
    }
    class Xa extends p {
      constructor() {
        super ()
      }
      apply(a) {
        if (a.Pb(this.P)) {
          for (var b = a.oa(this.P), c = a.K, d = [], e = 0, f = 0, g = 0; g < c.length; ) {
            let h = c[g];
            ++g;
            h.fa == u.Oa &&
            d.push(h);
            h.fa == u.ia ? ++e : h.fa == u.Da &&
            ++f
          }
          c = d.length;
          0 != c &&
          (
            f == e ? 2 > c ||
            (a.ag(b, d[0], u.ia), a.ag(b, d[1], u.Da)) : a.ag(b, d[0], f > e ? u.ia : u.Da)
          )
        }
      }
      wa() {
      }
      xa() {
      }
    }
    class va extends p {
      constructor() {
        super ()
      }
      apply(a) {
        if (a.Pb(this.P) && null == a.M) switch (this.Gj) {
          case 0:
            var b = this.newValue;
            a.kb = 0 > b ? 0 : 99 < b ? 99 : b;
            break;
          case 1:
            b = this.newValue,
            a.Ga = 0 > b ? 0 : 99 < b ? 99 : b
        }
      }
      wa(a) {
        a.R(this.Gj);
        a.R(this.newValue)
      }
      xa(a) {
        this.Gj = a.N();
        this.newValue = a.N()
      }
      static qa(a, b) {
        let c = new va;
        c.Gj = a;
        c.newValue = b;
        return c
      }
    }
    class Ga extends p {
      constructor() {
        super ()
      }
      apply(a) {
        if (a.Pb(this.P)) {
          var b = a.oa(this.P),
          c = a.oa(this.Ud);
          null != c &&
          0 != c.Z &&
          c.fb != this.jh &&
          (c.fb = this.jh, null != a.yi && a.yi(b, c))
        }
      }
      wa(a) {
        a.R(this.Ud);
        a.m(this.jh ? 1 : 0)
      }
      xa(a) {
        this.Ud = a.N();
        this.jh = 0 != a.F()
      }
      static qa(a, b) {
        let c = new Ga;
        c.Ud = a;
        c.jh = b;
        return c
      }
    }
    class Qa extends p {
      constructor() {
        super ()
      }
      apply(a) {
        a = a.oa(this.P);
        null != a &&
        (a.Zb = this.ac)
      }
      wa(a) {
        a.Eb(this.ac)
      }
      xa(a) {
        this.ac = a.Ab();
        null != this.ac &&
        (this.ac = ha.Xc(this.ac, 2))
      }
      static qa(a) {
        let b = new Qa;
        b.ac = a;
        return b
      }
    }
    class fa extends p {
      constructor() {
        super ()
      }
      apply(a) {
        let b = a.oa(this.Ud);
        if (null != b) {
          var c = a.oa(this.P),
          d = a.Pb(this.P);
          (d = d || b == c && !a.Ac && null == a.M) &&
          a.ag(c, b, this.Bj)
        }
      }
      wa(a) {
        a.R(this.Ud);
        a.m(this.Bj.ba)
      }
      xa(a) {
        this.Ud = a.N();
        a = a.zf();
        this.Bj = 1 == a ? u.ia : 2 == a ? u.Da : u.Oa
      }
      static qa(a, b) {
        let c = new fa;
        c.Ud = a;
        c.Bj = b;
        return c
      }
    }
    class Ea extends p {
      constructor() {
        super ()
      }
      apply(a) {
        if (a.Pb(this.P)) {
          var b = a.oa(this.P);
          null == a.M &&
          (a.T = this.Xd, null != a.Zi && a.Zi(b, this.Xd))
        }
      }
      wa(a) {
        var b = A.ka();
        this.Xd.ga(b);
        b = pako.deflateRaw(b.Wb());
        a.Xb(b.byteLength);
        a.Lb(b)
      }
      xa(a) {
        a = pako.inflateRaw(a.sb(a.Sb()));
        this.Xd = q.ma(new J(new DataView(a.buffer, a.byteOffset, a.byteLength)))
      }
      static qa(a) {
        let b = new Ea;
        b.Xd = a;
        return b
      }
    }
    class bb extends p {
      constructor() {
        super ()
      }
      apply(a) {
        a.Pb(this.P) &&
        this.fa != u.Oa &&
        (a.mb[this.fa.ba] = this.eh)
      }
      wa(a) {
        a.m(this.fa.ba);
        this.eh.ga(a)
      }
      xa(a) {
        let b = a.zf();
        this.fa = 1 == b ? u.ia : 2 == b ? u.Da : u.Oa;
        this.eh = new wa;
        this.eh.ma(a)
      }
    }
    class Fa extends p {
      constructor() {
        super ()
      }
      apply(a) {
        if (a.Pb(this.P)) {
          var b = a.Ac;
          a.Ac = this.newValue;
          b != this.newValue &&
          za.h(a.At, a.oa(this.P), this.newValue)
        }
      }
      wa(a) {
        a.m(this.newValue ? 1 : 0)
      }
      xa(a) {
        this.newValue = 0 !=
        a.F()
      }
      static qa(a) {
        let b = new Fa;
        b.newValue = a;
        return b
      }
    }
    class Na extends p {
      constructor() {
        super ()
      }
      apply(a) {
        if (0 == this.P) {
          var b = new ya;
          b.Z = this.Z;
          b.D = this.name;
          b.country = this.uj;
          b.Zb = this.Zb;
          a.K.push(b);
          a = a.Sl;
          null != a &&
          a(b)
        }
      }
      wa(a) {
        a.R(this.Z);
        a.Eb(this.name);
        a.Eb(this.uj);
        a.Eb(this.Zb)
      }
      xa(a) {
        this.Z = a.N();
        this.name = a.Ab();
        this.uj = a.Ab();
        this.Zb = a.Ab()
      }
      static qa(a, b, c, d) {
        let e = new Na;
        e.Z = a;
        e.name = b;
        e.uj = c;
        e.Zb = d;
        return e
      }
    }
    class Gb extends p {
      constructor() {
        super ()
      }
      apply(a) {
        a = a.oa(this.Ke);
        null != a &&
        0 == this.P &&
        (a.Sd = this.ac)
      }
      wa(a) {
        a.Eb(this.ac);
        a.R(this.Ke)
      }
      xa(a) {
        this.ac = a.Ab();
        this.Ke = a.N();
        null != this.ac &&
        (this.ac = ha.Xc(this.ac, 2))
      }
    }
    class Za extends p {
      constructor() {
        super ()
      }
      apply(a) {
        let b = a.M;
        if (null != b && a.Pb(this.P)) {
          var c = a.oa(this.P),
          d = 120 == b.Ta,
          e = 0 < b.Ta;
          this.Pf ? b.Ta = 120 : 120 == b.Ta &&
          (b.Ta = 119);
          d != this.Pf &&
          hc.h(a.Ll, c, this.Pf, e)
        }
      }
      wa(a) {
        a.m(this.Pf ? 1 : 0)
      }
      xa(a) {
        this.Pf = 0 != a.F()
      }
    }
    class Ya extends p {
      constructor() {
        super ()
      }
      Bn(a) {
        if (null != a.Qq) {
          let b = a.oa(this.P);
          return null == b ? !1 : a.Qq(b, this.$c)
        }
        return !0
      }
      apply(a) {
        let b = a.oa(this.P);
        null != b &&
        za.h(a.Ql, b, this.$c)
      }
      wa(a) {
        a.oc(ha.Xc(this.$c, 140))
      }
      xa(a) {
        this.$c = a.kc();
        if (140 < this.$c.length) throw v.C('message too long');
      }
    }
    class La extends p {
      constructor() {
        super ()
      }
      apply(a) {
        let b = a.oa(this.P);
        if (null != b) {
          var c = this.input;
          0 == (b.W & 16) &&
          0 != (c & 16) &&
          (b.Yb = !0);
          b.W = c;
          null != a.Rq &&
          null != b.I &&
          a.Rq(b, this.input, this.Fn, this.Gn)
        }
      }
      wa(a) {
        a.tb(this.input)
      }
      xa(a) {
        this.input = a.jb()
      }
    }
    class Ha extends p {
      constructor() {
        super ()
      }
      apply(a) {
        let b = a.oa(this.P);
        null != b &&
        za.h(a.Vl, b, this.Hj)
      }
      wa(a) {
        a.m(this.Hj)
      }
      xa(a) {
        this.Hj = a.F()
      }
      static qa(a) {
        let b = new Ha;
        b.Hj = a;
        return b
      }
    }
    class ma extends p {
      constructor() {
        p.yb = !0;
        super ();
        p.yb = !1;
        this.Za()
      }
      Za() {
        this.ah = !1;
        super.Za()
      }
      apply(a) {
        if (0 != this.Z && a.Pb(this.P)) {
          var b = a.oa(this.Z);
          if (null != b) {
            var c = a.oa(this.P);
            O.remove(a.K, b);
            null != a.M &&
            O.remove(a.M.va.H, b.I);
            Xb.h(a.Tl, b, this.qd, this.ah, c)
          }
        }
      }
      wa(a) {
        null != this.qd &&
        (this.qd = ha.Xc(this.qd, 100));
        a.R(this.Z);
        a.Eb(this.qd);
        a.m(this.ah ? 1 : 0)
      }
      xa(a) {
        this.Z = a.N();
        this.qd = a.Ab();
        this.ah = 0 != a.F();
        if (null != this.qd && 100 < this.qd.length) throw v.C('string too long');
      }
      static qa(a, b, c) {
        let d = new ma;
        d.Z = a;
        d.qd = b;
        d.ah = c;
        return d
      }
    }
    class Fb extends p {
      constructor() {
        super ()
      }
      apply(a) {
        if (0 == this.P) {
          for (var b = new Map, c = 0, d = a.K; c < d.length; ) {
            var e = d[c];
            ++c;
            b.set(e.Z, e)
          }
          c = [];
          d = 0;
          for (e = this.lh; d < e.length; ) {
            var f = e[d];
            ++d;
            let g = b.get(f);
            null != g &&
            (b.delete(f), c.push(g))
          }
          d = [];
          b = b.values();
          for (e = b.next(); !e.done; ) f = e.value,
          e = b.next(),
          d.push(f);
          a.K = this.An ? c.concat(d) : d.concat(c)
        }
      }
      wa(a) {
        a.m(this.An ? 1 : 0);
        a.m(this.lh.length);
        let b = 0,
        c = this.lh;
        for (; b < c.length; ) a.R(c[b++])
      }
      xa(a) {
        this.An = 0 != a.F();
        let b = a.F();
        this.lh = [];
        let c = 0;
        for (; c < b; ) ++c,
        this.lh.push(a.N())
      }
    }
    class Hb extends p {
      constructor() {
        super ()
      }
      apply(a) {
        if (0 == this.P) {
          var b = a.M;
          if (null != b) {
            if (this.sn) {
              a = a.oa(this.Ke);
              if (null == a) return;
              a = a.I
            } else a = b.va.H[this.Ke];
            null != a &&
            (
              null != this.Ma[0] &&
              (a.a.x = this.Ma[0]),
              null != this.Ma[1] &&
              (a.a.y = this.Ma[1]),
              null != this.Ma[2] &&
              (a.G.x = this.Ma[2]),
              null != this.Ma[3] &&
              (a.G.y = this.Ma[3]),
              null != this.Ma[4] &&
              (a.ra.x = this.Ma[4]),
              null != this.Ma[5] &&
              (a.ra.y = this.Ma[5]),
              null != this.Ma[6] &&
              (a.V = this.Ma[6]),
              null != this.Ma[7] &&
              (a.o = this.Ma[7]),
              null != this.Ma[8] &&
              (a.ca = this.Ma[8]),
              null != this.Ma[9] &&
              (a.Ea = this.Ma[9]),
              null != this.Yc[0] &&
              (a.S = this.Yc[0]),
              null != this.Yc[1] &&
              (a.i = this.Yc[1]),
              null != this.Yc[2] &&
              (a.B = this.Yc[2])
            )
          }
        }
      }
      wa(a) {
        a.R(this.Ke);
        a.m(this.sn ? 1 : 0);
        let b = a.a;
        a.Xb(0);
        let c = 0;
        for (var d = 1, e = 0, f = this.Ma; e < f.length; ) {
          var g = f[e];
          ++e;
          null != g &&
          (c |= d, a.nj(g));
          d <<= 1
        }
        e = 0;
        for (f = this.Yc; e < f.length; ) g = f[e],
        ++e,
        null != g &&
        (c |= d, a.R(g)),
        d <<= 1;
        d = a.a;
        a.a = b;
        a.Xb(c);
        a.a = d
      }
      xa(a) {
        this.Ke = a.N();
        this.sn = 0 != a.F();
        let b = a.Sb();
        this.Ma = [];
        for (var c = 0; 10 > c; ) {
          var d = c++;
          this.Ma[d] = null;
          0 != (b & 1) &&
          (this.Ma[d] = a.Ci());
          b >>>= 1
        }
        this.Yc = [];
        for (c = 0; 3 > c; ) d = c++,
        this.Yc[d] = null,
        0 != (b & 1) &&
        (this.Yc[d] = a.N()),
        b >>>= 1
      }
    }
    class Pa extends p {
      constructor() {
        super ()
      }
      apply(a) {
        a.Pb(this.P) &&
        a.Xr(a.oa(this.P), this.min, this.rate, this.sj)
      }
      wa(a) {
        a.R(this.min);
        a.R(this.rate);
        a.R(this.sj)
      }
      xa(a) {
        this.min = a.N();
        this.rate = a.N();
        this.sj = a.N()
      }
      static qa(a, b, c) {
        let d = new Pa;
        d.min = a;
        d.rate = b;
        d.sj = c;
        return d
      }
    }
    class Va extends p {
      constructor() {
        super ()
      }
      apply(a) {
        a.Pb(this.P) &&
        a.ks(a.oa(this.P))
      }
      wa() {
      }
      xa() {
      }
    }
    class Wa extends p {
      constructor() {
        super ()
      }
      apply(a) {
        if (a.Pb(this.P)) {
          var b = a.oa(this.P);
          if (null != a.M) {
            a.M = null;
            let c = 0,
            d = a.K;
            for (; c < d.length; ) {
              let e = d[c];
              ++c;
              e.I = null;
              e.Nb = 0
            }
            null != a.Kf &&
            a.Kf(b)
          }
        }
      }
      wa() {
      }
      xa() {
      }
    }
    class Ma extends p {
      constructor() {
        super ()
      }
      apply(a) {
        if (0 == this.P) {
          a = a.K;
          for (var b = 0, c = a.length; b < c; ) {
            let d = b++;
            if (d >= this.Ie.length) break;
            a[d].zb = this.Ie[d]
          }
        }
      }
      wa(a) {
        a.nb(this.Ie.length);
        let b = 0,
        c = this.Ie;
        for (; b < c.length; ) a.nb(c[b++])
      }
      xa(a) {
        this.Ie = [];
        let b = a.Bb(),
        c = 0;
        for (; c < b; ) ++c,
        this.Ie.push(a.Bb())
      }
      static qa(a) {
        let b = new Ma,
        c = a.U.K,
        d = [],
        e = 0;
        for (; e < c.length; ) {
          let f = a.We.get(c[e++].Z);
          d.push(null == f ? 0 : f.zb)
        }
        b.Ie = d;
        return b
      }
    }
    class v extends Error {
      constructor(a, b, c) {
        super (a);
        this.message = a;
        this.Oj = null != c ? c : this
      }
      Fb() {
        return this.Oj
      }
      static Mb(a) {
        return a instanceof v ? a : a instanceof Error ? new v(a.message, null, a) : new Mb(a, null, a)
      }
      static C(a) {
        return a instanceof v ? a.Oj : a instanceof Error ? a : new Mb(a)
      }
    }
    class Mb extends v {
      constructor(a, b, c) {
        super (String(a), b, c);
        this.value = a
      }
      Fb() {
        return this.value
      }
    }
    var Ib = Ib ||
    {
    },
    X;
    mc.b = !0;
    Object.assign(mc.prototype, {
      g: mc
    });
    O.b = !0;
    Math.b = !0;
    Ac.b = !0;
    Q.b = !0;
    aa.b = !0;
    ha.b = !0;
    zc.b = !0;
    Object.assign(zc.prototype, {
      g: zc
    });
    var ia = Ib['bas.basnet.FailReason'] = {
      Wf: !0,
      $d: null,
      Zd: {
        wc: 'PeerFailed',
        pb: 0,
        Gb: 'bas.basnet.FailReason',
        toString: ka
      },
      Ne: (
        X = function (a) {
          return {
            pb: 1,
            code: a,
            Gb: 'bas.basnet.FailReason',
            toString: ka
          }
        },
        X.wc = 'Rejected',
        X.Oe = [
          'code'
        ],
        X
      ),
      Me: {
        wc: 'Cancelled',
        pb: 2,
        Gb: 'bas.basnet.FailReason',
        toString: ka
      },
      Error: {
        wc: 'Error',
        pb: 3,
        Gb: 'bas.basnet.FailReason',
        toString: ka
      }
    };
    ia.$d = [
      ia.Zd,
      ia.Ne,
      ia.Me,
      ia.Error
    ];
    fc.b = !0;
    Object.assign(fc.prototype, {
      g: fc
    });
    Hc.b = !0;
    Hc.xh = !0;
    Ja.b = !0;
    Ja.ad = [
      Hc
    ];
    Object.assign(Ja.prototype, {
      g: Ja
    });
    var fb = Ib['bas.basnet.ConnectionRequestResponse'] = {
      Wf: !0,
      $d: null,
      Kj: {
        wc: 'Accept',
        pb: 0,
        Gb: 'bas.basnet.ConnectionRequestResponse',
        toString: ka
      },
      Uf: (
        X = function (a) {
          return {
            pb: 1,
            reason: a,
            Gb: 'bas.basnet.ConnectionRequestResponse',
            toString: ka
          }
        },
        X.wc = 'Reject',
        X.Oe = [
          'reason'
        ],
        X
      )
    };
    fb.$d = [
      fb.Kj,
      fb.Uf
    ];
    Jb.b = !0;
    Object.assign(Jb.prototype, {
      g: Jb
    });
    Kc.b = !0;
    Yb.b = !0;
    Object.assign(Yb.prototype, {
      g: Yb
    });
    J.b = !0;
    Object.assign(J.prototype, {
      g: J
    });
    A.b = !0;
    Object.assign(A.prototype, {
      g: A
    });
    U.b = !0;
    Object.assign(U.prototype, {
      g: U
    });
    vb.b = !0;
    hb.b = !0;
    Nb.b = !0;
    Ob.b = !0;
    Object.assign(Ob.prototype, {
      g: Ob
    });
    x.b = !0;
    Rb.b = !0;
    Ec.b = !0;
    p.b = !0;
    Object.assign(p.prototype, {
      g: p
    });
    db.b = !0;
    Object.assign(db.prototype, {
      g: db
    });
    W.b = !0;
    Object.assign(W.prototype, {
      g: W
    });
    cb.b = !0;
    cb.ja = p;
    Object.assign(cb.prototype, {
      g: cb
    });
    ec.b = !0;
    ec.xh = !0;
    Object.assign(ec.prototype, {
      g: ec
    });
    Qb.b = !0;
    Object.assign(Qb.prototype, {
      g: Qb
    });
    lc.b = !0;
    Object.assign(lc.prototype, {
      g: lc
    });
    pc.b = !0;
    Object.assign(pc.prototype, {
      g: pc
    });
    Ia.b = !0;
    Ia.xh = !0;
    qa.b = !0;
    oa.b = !0;
    oa.ja = W;
    Object.assign(oa.prototype, {
      g: oa
    });
    var ja = Ib['bas.marf.net.ConnFailReason'] = {
      Wf: !0,
      $d: null,
      Me: {
        wc: 'Cancelled',
        pb: 0,
        Gb: 'bas.marf.net.ConnFailReason',
        toString: ka
      },
      Zd: {
        wc: 'PeerFailed',
        pb: 1,
        Gb: 'bas.marf.net.ConnFailReason',
        toString: ka
      },
      Ne: (
        X = function (a) {
          return {
            pb: 2,
            reason: a,
            Gb: 'bas.marf.net.ConnFailReason',
            toString: ka
          }
        },
        X.wc = 'Rejected',
        X.Oe = [
          'reason'
        ],
        X
      ),
      Tf: (
        X = function (a) {
          return {
            pb: 3,
            description: a,
            Gb: 'bas.marf.net.ConnFailReason',
            toString: ka
          }
        },
        X.wc = 'Other',
        X.Oe = [
          'description'
        ],
        X
      )
    };
    ja.$d = [
      ja.Me,
      ja.Zd,
      ja.Ne,
      ja.Tf
    ];
    Oa.b = !0;
    Oa.ja = oa;
    Object.assign(Oa.prototype, {
      g: Oa
    });
    Zb.b = !0;
    Zb.ja = oa;
    Object.assign(Zb.prototype, {
      g: Zb
    });
    tc.b = !0;
    Object.assign(tc.prototype, {
      g: tc
    });
    kc.b = !0;
    Object.assign(kc.prototype, {
      g: kc
    });
    oc.b = !0;
    ac.b = !0;
    Object.assign(ac.prototype, {
      g: ac
    });
    $b.b = !0;
    $b.ja = oa;
    Object.assign($b.prototype, {
      g: $b
    });
    Tb.b = !0;
    Object.assign(Tb.prototype, {
      g: Tb
    });
    Bc.b = !0;
    Object.assign(Bc.prototype, {
      g: Bc
    });
    P.b = !0;
    Object.assign(P.prototype, {
      g: P
    });
    Z.b = !0;
    H.b = !0;
    D.b = !0;
    za.b = !0;
    hc.b = !0;
    Xb.b = !0;
    pb.b = !0;
    Object.assign(pb.prototype, {
      g: pb
    });
    Dc.b = !0;
    Vb.b = !0;
    Object.assign(Vb.prototype, {
      g: Vb
    });
    Ra.b = !0;
    Ca.b = !0;
    Object.assign(Ca.prototype, {
      g: Ca
    });
    Wb.b = !0;
    Object.assign(Wb.prototype, {
      g: Wb
    });
    Ub.b = !0;
    Object.assign(Ub.prototype, {
      g: Ub
    });
    la.b = !0;
    Object.assign(la.prototype, {
      g: la
    });
    uc.b = !0;
    Object.assign(uc.prototype, {
      g: uc
    });
    Cc.b = !0;
    ta.b = !0;
    Object.assign(ta.prototype, {
      g: ta
    });
    sa.b = !0;
    Object.assign(sa.prototype, {
      g: sa
    });
    m.b = !0;
    nc.b = !0;
    Object.assign(nc.prototype, {
      g: nc
    });
    B.b = !0;
    C.b = !0;
    qc.b = !0;
    Object.assign(qc.prototype, {
      g: qc
    });
    Sb.b = !0;
    Object.assign(Sb.prototype, {
      g: Sb
    });
    Pb.b = !0;
    ib.b = !0;
    jc.b = !0;
    Object.assign(jc.prototype, {
      g: jc
    });
    vc.b = !0;
    Object.assign(vc.prototype, {
      g: vc
    });
    Aa.b = !0;
    Object.assign(Aa.prototype, {
      g: Aa
    });
    Y.b = !0;
    Y.ad = [
      Ia
    ];
    Object.assign(Y.prototype, {
      g: Y
    });
    Kb.b = !0;
    Object.assign(Kb.prototype, {
      g: Kb
    });
    cc.b = !0;
    Object.assign(cc.prototype, {
      g: cc
    });
    Sa.b = !0;
    Object.assign(Sa.prototype, {
      g: Sa
    });
    q.b = !0;
    Object.assign(q.prototype, {
      g: q
    });
    wa.b = !0;
    Object.assign(wa.prototype, {
      g: wa
    });
    u.b = !0;
    Object.assign(u.prototype, {
      g: u
    });
    xa.b = !0;
    xa.ad = [
      Ia,
      ec
    ];
    Object.assign(xa.prototype, {
      g: xa
    });
    ya.b = !0;
    ya.ad = [
      Ia
    ];
    Object.assign(ya.prototype, {
      g: ya
    });
    Da.b = !0;
    Da.ja = p;
    Object.assign(Da.prototype, {
      g: Da
    });
    Eb.b = !0;
    Eb.ja = p;
    Object.assign(Eb.prototype, {
      g: Eb
    });
    Xa.b = !0;
    Xa.ja = p;
    Object.assign(Xa.prototype, {
      g: Xa
    });
    va.b = !0;
    va.ja = p;
    Object.assign(va.prototype, {
      g: va
    });
    Ga.b = !0;
    Ga.ja = p;
    Object.assign(Ga.prototype, {
      g: Ga
    });
    Qa.b = !0;
    Qa.ja = p;
    Object.assign(Qa.prototype, {
      g: Qa
    });
    fa.b = !0;
    fa.ja = p;
    Object.assign(fa.prototype, {
      g: fa
    });
    Ea.b = !0;
    Ea.ja = p;
    Object.assign(Ea.prototype, {
      g: Ea
    });
    bb.b = !0;
    bb.ja = p;
    Object.assign(bb.prototype, {
      g: bb
    });
    Fa.b = !0;
    Fa.ja = p;
    Object.assign(Fa.prototype, {
      g: Fa
    });
    Na.b = !0;
    Na.ja = p;
    Object.assign(Na.prototype, {
      g: Na
    });
    Gb.b = !0;
    Gb.ja = p;
    Object.assign(Gb.prototype, {
      g: Gb
    });
    Za.b = !0;
    Za.ja = p;
    Object.assign(Za.prototype, {
      g: Za
    });
    Ya.b = !0;
    Ya.ja = p;
    Object.assign(Ya.prototype, {
      g: Ya
    });
    La.b = !0;
    La.ja = p;
    Object.assign(La.prototype, {
      g: La
    });
    Ha.b = !0;
    Ha.ja = p;
    Object.assign(Ha.prototype, {
      g: Ha
    });
    Jc.b = !0;
    ma.b = !0;
    ma.ja = p;
    Object.assign(ma.prototype, {
      g: ma
    });
    Fb.b = !0;
    Fb.ja = p;
    Object.assign(Fb.prototype, {
      g: Fb
    });
    Hb.b = !0;
    Hb.ja = p;
    Object.assign(Hb.prototype, {
      g: Hb
    });
    Pa.b = !0;
    Pa.ja = p;
    Object.assign(Pa.prototype, {
      g: Pa
    });
    Va.b = !0;
    Va.ja = p;
    Object.assign(Va.prototype, {
      g: Va
    });
    Wa.b = !0;
    Wa.ja = p;
    Object.assign(Wa.prototype, {
      g: Wa
    });
    Ma.b = !0;
    Ma.ja = p;
    Object.assign(Ma.prototype, {
      g: Ma
    });
    ra.b = !0;
    ra.ad = [
      Ia
    ];
    Object.assign(ra.prototype, {
      g: ra
    });
    ob.b = !0;
    ob.ad = [
      Ia
    ];
    Object.assign(ob.prototype, {
      g: ob
    });
    Ta.b = !0;
    Ta.ad = [
      Ia
    ];
    Object.assign(Ta.prototype, {
      g: Ta
    });
    R.b = !0;
    Object.assign(R.prototype, {
      g: R
    });
    I.b = !0;
    Object.assign(I.prototype, {
      g: I
    });
    G.b = !0;
    Object.assign(G.prototype, {
      g: G
    });
    T.b = !0;
    Object.assign(T.prototype, {
      g: T
    });
    da.b = !0;
    Object.assign(da.prototype, {
      g: da
    });
    wc.b = !0;
    Object.assign(wc.prototype, {
      g: wc
    });
    tb.b = !0;
    Object.assign(tb.prototype, {
      g: tb
    });
    Ab.b = !0;
    Object.assign(Ab.prototype, {
      g: Ab
    });
    $a.b = !0;
    Object.assign($a.prototype, {
      g: $a
    });
    dc.b = !0;
    Object.assign(dc.prototype, {
      g: dc
    });
    zb.b = !0;
    Object.assign(zb.prototype, {
      g: zb
    });
    ub.b = !0;
    Object.assign(ub.prototype, {
      g: ub
    });
    Bb.b = !0;
    Object.assign(Bb.prototype, {
      g: Bb
    });
    ab.b = !0;
    Object.assign(ab.prototype, {
      g: ab
    });
    jb.b = !0;
    Object.assign(jb.prototype, {
      g: jb
    });
    ic.b = !0;
    Object.assign(ic.prototype, {
      g: ic
    });
    sc.b = !0;
    Object.assign(sc.prototype, {
      g: sc
    });
    ua.b = !0;
    Object.assign(ua.prototype, {
      g: ua
    });
    sb.b = !0;
    Object.assign(sb.prototype, {
      g: sb
    });
    nb.b = !0;
    Object.assign(nb.prototype, {
      g: nb
    });
    gb.b = !0;
    Object.assign(gb.prototype, {
      g: gb
    });
    rc.b = !0;
    Object.assign(rc.prototype, {
      g: rc
    });
    qb.b = !0;
    Object.assign(qb.prototype, {
      g: qb
    });
    yb.b = !0;
    Object.assign(yb.prototype, {
      g: yb
    });
    Ka.b = !0;
    Object.assign(Ka.prototype, {
      g: Ka
    });
    ca.b = !0;
    Object.assign(ca.prototype, {
      g: ca
    });
    Ba.b = !0;
    Object.assign(Ba.prototype, {
      g: Ba
    });
    rb.b = !0;
    Object.assign(rb.prototype, {
      g: rb
    });
    mb.b = !0;
    Object.assign(mb.prototype, {
      g: mb
    });
    Ua.b = !0;
    Object.assign(Ua.prototype, {
      g: Ua
    });
    lb.b = !0;
    Object.assign(lb.prototype, {
      g: lb
    });
    Cb.b = !0;
    Object.assign(Cb.prototype, {
      g: Cb
    });
    xb.b = !0;
    Object.assign(xb.prototype, {
      g: xb
    });
    na.b = !0;
    Object.assign(na.prototype, {
      g: na
    });
    ba.b = !0;
    Object.assign(ba.prototype, {
      g: ba
    });
    wb.b = !0;
    Object.assign(wb.prototype, {
      g: wb
    });
    kb.b = !0;
    Object.assign(kb.prototype, {
      g: kb
    });
    v.b = !0;
    v.ja = Error;
    Object.assign(v.prototype, {
      g: v
    });
    Mb.b = !0;
    Mb.ja = v;
    Object.assign(Mb.prototype, {
      g: Mb
    });
    Fc.b = !0;
    Object.assign(Fc.prototype, {
      g: Fc
    });
    w.b = !0;
    pa.Jj |= 0;
    'undefined' != typeof performance &&
    'function' == typeof performance.now &&
    (O.now = performance.now.bind(performance));
    null == String.fromCodePoint &&
    (
      String.fromCodePoint = function (a) {
        return 65536 > a ? String.fromCharCode(a) : String.fromCharCode((a >> 10) + 55232) + String.fromCharCode((a & 1023) + 56320)
      }
    );
    Object.defineProperty(
      String.prototype,
      '__class__',
      {
        value: String,
        enumerable: !1,
        writable: !0
      }
    );
    String.b = !0;
    Array.b = !0;
    Date.prototype.g = Date;
    Date.b = 'Date';
    var bc = {},
    Nc = {},
    E = Number,
    Gc = Boolean,
    Oc = {},
    Pc = {};
    u.Oa = new u(0, 16777215, 0, - 1, 'Spectators', 't-spec', 0, 0);
    u.ia = new u(1, 15035990, - 1, 8, 'Red', 't-red', 15035990, 2);
    u.Da = new u(2, 5671397, 1, 16, 'Blue', 't-blue', 625603, 4);
    u.Oa.Dg = u.Oa;
    u.ia.Dg = u.Da;
    u.Da.Dg = u.ia;
    w.Vn = {}.toString;
    Ja.Fo = {
      mandatory: {
        OfferToReceiveAudio: !1,
        OfferToReceiveVideo: !1
      }
    };
    U.yh = {
      name: 'ECDSA',
      namedCurve: 'P-256'
    };
    U.Lm = {
      name: 'ECDSA',
      hash: {
        name: 'SHA-256'
      }
    };
    hb.Ap = [
      'click-rail',
      'drag-thumb',
      'wheel',
      'touch'
    ];
    p.yb = !1;
    p.qn = new Map;
    p.Nf = 0;
    W.yb = !1;
    cb.Aa = p.Ha({
      Ca: !1,
      delay: !1
    });
    qa.Cc = 0;
    oc.channels = [
      {
        name: 'ro',
        reliable: !0,
        ordered: !0
      },
      {
        name: 'ru',
        reliable: !0,
        ordered: !1
      },
      {
        name: 'uu',
        reliable: !1,
        ordered: !1
      }
    ];
    Z.Lj = 'application/x-www-form-urlencoded';
    Ra.eb = [
      'Afghanistan',
      'AF',
      33.3,
      65.1,
      'Albania',
      'AL',
      41.1,
      20.1,
      'Algeria',
      'DZ',
      28,
      1.6,
      'American Samoa',
      'AS',
      - 14.2,
      - 170.1,
      'Andorra',
      'AD',
      42.5,
      1.6,
      'Angola',
      'AO',
      - 11.2,
      17.8,
      'Anguilla',
      'AI',
      18.2,
      - 63,
      'Antigua and Barbuda',
      'AG',
      17,
      - 61.7,
      'Argentina',
      'AR',
      - 34.5,
      - 58.4,
      'Armenia',
      'AM',
      40,
      45,
      'Aruba',
      'AW',
      12.5,
      - 69.9,
      'Australia',
      'AU',
      - 25.2,
      133.7,
      'Austria',
      'AT',
      47.5,
      14.5,
      'Azerbaijan',
      'AZ',
      40.1,
      47.5,
      'Bahamas',
      'BS',
      25,
      - 77.3,
      'Bahrain',
      'BH',
      25.9,
      50.6,
      'Bangladesh',
      'BD',
      23.6,
      90.3,
      'Barbados',
      'BB',
      13.1,
      - 59.5,
      'Belarus',
      'BY',
      53.7,
      27.9,
      'Belgium',
      'BE',
      50.5,
      4.4,
      'Belize',
      'BZ',
      17.1,
      - 88.4,
      'Benin',
      'BJ',
      9.3,
      2.3,
      'Bermuda',
      'BM',
      32.3,
      - 64.7,
      'Bhutan',
      'BT',
      27.5,
      90.4,
      'Bolivia',
      'BO',
      - 16.2,
      - 63.5,
      'Bosnia and Herzegovina',
      'BA',
      43.9,
      17.6,
      'Botswana',
      'BW',
      - 22.3,
      24.6,
      'Bouvet Island',
      'BV',
      - 54.4,
      3.4,
      'Brazil',
      'BR',
      - 14.2,
      - 51.9,
      'British Indian Ocean Territory',
      'IO',
      - 6.3,
      71.8,
      'British Virgin Islands',
      'VG',
      18.4,
      - 64.6,
      'Brunei',
      'BN',
      4.5,
      114.7,
      'Bulgaria',
      'BG',
      42.7,
      25.4,
      'Burkina Faso',
      'BF',
      12.2,
      - 1.5,
      'Burundi',
      'BI',
      - 3.3,
      29.9,
      'Cambodia',
      'KH',
      12.5,
      104.9,
      'Cameroon',
      'CM',
      7.3,
      12.3,
      'Canada',
      'CA',
      56.1,
      - 106.3,
      'Cape Verde',
      'CV',
      16,
      - 24,
      'Cayman Islands',
      'KY',
      19.5,
      - 80.5,
      'Central African Republic',
      'CF',
      6.6,
      20.9,
      'Chad',
      'TD',
      15.4,
      18.7,
      'Chile',
      'CL',
      - 35.6,
      - 71.5,
      'China',
      'CN',
      35.8,
      104.1,
      'Christmas Island',
      'CX',
      - 10.4,
      105.6,
      'Colombia',
      'CO',
      4.5,
      - 74.2,
      'Comoros',
      'KM',
      - 11.8,
      43.8,
      'Congo [DRC]',
      'CD',
      - 4,
      21.7,
      'Congo [Republic]',
      'CG',
      - 0.2,
      15.8,
      'Cook Islands',
      'CK',
      - 21.2,
      - 159.7,
      'Costa Rica',
      'CR',
      9.7,
      - 83.7,
      'Croatia',
      'HR',
      45.1,
      15.2,
      'Cuba',
      'CU',
      21.5,
      - 77.7,
      'Cyprus',
      'CY',
      35.1,
      33.4,
      'Czech Republic',
      'CZ',
      49.8,
      15.4,
      'Côte d\'Ivoire',
      'CI',
      7.5,
      - 5.5,
      'Denmark',
      'DK',
      56.2,
      9.5,
      'Djibouti',
      'DJ',
      11.8,
      42.5,
      'Dominica',
      'DM',
      15.4,
      - 61.3,
      'Dominican Republic',
      'DO',
      18.7,
      - 70.1,
      'Ecuador',
      'EC',
      - 1.8,
      - 78.1,
      'Egypt',
      'EG',
      26.8,
      30.8,
      'El Salvador',
      'SV',
      13.7,
      - 88.8,
      'England',
      'ENG',
      55.3,
      - 3.4,
      'Equatorial Guinea',
      'GQ',
      1.6,
      10.2,
      'Eritrea',
      'ER',
      15.1,
      39.7,
      'Estonia',
      'EE',
      58.5,
      25,
      'Ethiopia',
      'ET',
      9.1,
      40.4,
      'Faroe Islands',
      'FO',
      61.8,
      - 6.9,
      'Fiji',
      'FJ',
      - 16.5,
      179.4,
      'Finland',
      'FI',
      61.9,
      25.7,
      'France',
      'FR',
      46.2,
      2.2,
      'French Guiana',
      'GF',
      3.9,
      - 53.1,
      'French Polynesia',
      'PF',
      - 17.6,
      - 149.4,
      'Gabon',
      'GA',
      - 0.8,
      11.6,
      'Gambia',
      'GM',
      13.4,
      - 15.3,
      'Georgia',
      'GE',
      42.3,
      43.3,
      'Germany',
      'DE',
      51.1,
      10.4,
      'Ghana',
      'GH',
      7.9,
      - 1,
      'Gibraltar',
      'GI',
      36.1,
      - 5.3,
      'Greece',
      'GR',
      39,
      21.8,
      'Greenland',
      'GL',
      71.7,
      - 42.6,
      'Grenada',
      'GD',
      12.2,
      - 61.6,
      'Guadeloupe',
      'GP',
      16.9,
      - 62,
      'Guam',
      'GU',
      13.4,
      144.7,
      'Guatemala',
      'GT',
      15.7,
      - 90.2,
      'Guinea',
      'GN',
      9.9,
      - 9.6,
      'Guinea-Bissau',
      'GW',
      11.8,
      - 15.1,
      'Guyana',
      'GY',
      4.8,
      - 58.9,
      'Haiti',
      'HT',
      18.9,
      - 72.2,
      'Honduras',
      'HN',
      15.1,
      - 86.2,
      'Hong Kong',
      'HK',
      22.3,
      114.1,
      'Hungary',
      'HU',
      47.1,
      19.5,
      'Iceland',
      'IS',
      64.9,
      - 19,
      'India',
      'IN',
      20.5,
      78.9,
      'Indonesia',
      'ID',
      - 0.7,
      113.9,
      'Iran',
      'IR',
      32.4,
      53.6,
      'Iraq',
      'IQ',
      33.2,
      43.6,
      'Ireland',
      'IE',
      53.4,
      - 8.2,
      'Israel',
      'IL',
      31,
      34.8,
      'Italy',
      'IT',
      41.8,
      12.5,
      'Jamaica',
      'JM',
      18.1,
      - 77.2,
      'Japan',
      'JP',
      36.2,
      138.2,
      'Jordan',
      'JO',
      30.5,
      36.2,
      'Kazakhstan',
      'KZ',
      48,
      66.9,
      'Kenya',
      'KE',
      - 0,
      37.9,
      'Kiribati',
      'KI',
      - 3.3,
      - 168.7,
      'Kosovo',
      'XK',
      42.6,
      20.9,
      'Kuwait',
      'KW',
      29.3,
      47.4,
      'Kyrgyzstan',
      'KG',
      41.2,
      74.7,
      'Laos',
      'LA',
      19.8,
      102.4,
      'Latvia',
      'LV',
      56.8,
      24.6,
      'Lebanon',
      'LB',
      33.8,
      35.8,
      'Lesotho',
      'LS',
      - 29.6,
      28.2,
      'Liberia',
      'LR',
      6.4,
      - 9.4,
      'Libya',
      'LY',
      26.3,
      17.2,
      'Liechtenstein',
      'LI',
      47.1,
      9.5,
      'Lithuania',
      'LT',
      55.1,
      23.8,
      'Luxembourg',
      'LU',
      49.8,
      6.1,
      'Macau',
      'MO',
      22.1,
      113.5,
      'Macedonia [FYROM]',
      'MK',
      41.6,
      21.7,
      'Madagascar',
      'MG',
      - 18.7,
      46.8,
      'Malawi',
      'MW',
      - 13.2,
      34.3,
      'Malaysia',
      'MY',
      4.2,
      101.9,
      'Maldives',
      'MV',
      3.2,
      73.2,
      'Mali',
      'ML',
      17.5,
      - 3.9,
      'Malta',
      'MT',
      35.9,
      14.3,
      'Marshall Islands',
      'MH',
      7.1,
      171.1,
      'Martinique',
      'MQ',
      14.6,
      - 61,
      'Mauritania',
      'MR',
      21,
      - 10.9,
      'Mauritius',
      'MU',
      - 20.3,
      57.5,
      'Mayotte',
      'YT',
      - 12.8,
      45.1,
      'Mexico',
      'MX',
      23.6,
      - 102.5,
      'Micronesia',
      'FM',
      7.4,
      150.5,
      'Moldova',
      'MD',
      47.4,
      28.3,
      'Monaco',
      'MC',
      43.7,
      7.4,
      'Mongolia',
      'MN',
      46.8,
      103.8,
      'Montenegro',
      'ME',
      42.7,
      19.3,
      'Montserrat',
      'MS',
      16.7,
      - 62.1,
      'Morocco',
      'MA',
      31.7,
      - 7,
      'Mozambique',
      'MZ',
      - 18.6,
      35.5,
      'Myanmar [Burma]',
      'MM',
      21.9,
      95.9,
      'Namibia',
      'NA',
      - 22.9,
      18.4,
      'Nauru',
      'NR',
      - 0.5,
      166.9,
      'Nepal',
      'NP',
      28.3,
      84.1,
      'Netherlands',
      'NL',
      52.1,
      5.2,
      'Netherlands Antilles',
      'AN',
      12.2,
      - 69,
      'New Caledonia',
      'NC',
      - 20.9,
      165.6,
      'New Zealand',
      'NZ',
      - 40.9,
      174.8,
      'Nicaragua',
      'NI',
      12.8,
      - 85.2,
      'Niger',
      'NE',
      17.6,
      8,
      'Nigeria',
      'NG',
      9,
      8.6,
      'Niue',
      'NU',
      - 19,
      - 169.8,
      'Norfolk Island',
      'NF',
      - 29,
      167.9,
      'North Korea',
      'KP',
      40.3,
      127.5,
      'Northern Mariana Islands',
      'MP',
      17.3,
      145.3,
      'Norway',
      'NO',
      60.4,
      8.4,
      'Oman',
      'OM',
      21.5,
      55.9,
      'Pakistan',
      'PK',
      30.3,
      69.3,
      'Palau',
      'PW',
      7.5,
      134.5,
      'Palestinian Territories',
      'PS',
      31.9,
      35.2,
      'Panama',
      'PA',
      8.5,
      - 80.7,
      'Papua New Guinea',
      'PG',
      - 6.3,
      143.9,
      'Paraguay',
      'PY',
      - 23.4,
      - 58.4,
      'Peru',
      'PE',
      - 9.1,
      - 75,
      'Philippines',
      'PH',
      12.8,
      121.7,
      'Pitcairn Islands',
      'PN',
      - 24.7,
      - 127.4,
      'Poland',
      'PL',
      51.9,
      19.1,
      'Portugal',
      'PT',
      39.3,
      - 8.2,
      'Puerto Rico',
      'PR',
      18.2,
      - 66.5,
      'Qatar',
      'QA',
      25.3,
      51.1,
      'Romania',
      'RO',
      45.9,
      24.9,
      'Russia',
      'RU',
      61.5,
      105.3,
      'Rwanda',
      'RW',
      - 1.9,
      29.8,
      'Réunion',
      'RE',
      - 21.1,
      55.5,
      'Saint Helena',
      'SH',
      - 24.1,
      - 10,
      'Saint Kitts',
      'KN',
      17.3,
      - 62.7,
      'Saint Lucia',
      'LC',
      13.9,
      - 60.9,
      'Saint Pierre',
      'PM',
      46.9,
      - 56.2,
      'Saint Vincent',
      'VC',
      12.9,
      - 61.2,
      'Samoa',
      'WS',
      - 13.7,
      - 172.1,
      'San Marino',
      'SM',
      43.9,
      12.4,
      'Saudi Arabia',
      'SA',
      23.8,
      45,
      'Scotland',
      'SCT',
      56.5,
      4.2,
      'Senegal',
      'SN',
      14.4,
      - 14.4,
      'Serbia',
      'RS',
      44,
      21,
      'Seychelles',
      'SC',
      - 4.6,
      55.4,
      'Sierra Leone',
      'SL',
      8.4,
      - 11.7,
      'Singapore',
      'SG',
      1.3,
      103.8,
      'Slovakia',
      'SK',
      48.6,
      19.6,
      'Slovenia',
      'SI',
      46.1,
      14.9,
      'Solomon Islands',
      'SB',
      - 9.6,
      160.1,
      'Somalia',
      'SO',
      5.1,
      46.1,
      'South Africa',
      'ZA',
      - 30.5,
      22.9,
      'South Georgia',
      'GS',
      - 54.4,
      - 36.5,
      'South Korea',
      'KR',
      35.9,
      127.7,
      'Spain',
      'ES',
      40.4,
      - 3.7,
      'Sri Lanka',
      'LK',
      7.8,
      80.7,
      'Sudan',
      'SD',
      12.8,
      30.2,
      'Suriname',
      'SR',
      3.9,
      - 56,
      'Svalbard and Jan Mayen',
      'SJ',
      77.5,
      23.6,
      'Swaziland',
      'SZ',
      - 26.5,
      31.4,
      'Sweden',
      'SE',
      60.1,
      18.6,
      'Switzerland',
      'CH',
      46.8,
      8.2,
      'Syria',
      'SY',
      34.8,
      38.9,
      'São Tomé and Príncipe',
      'ST',
      0.1,
      6.6,
      'Taiwan',
      'TW',
      23.6,
      120.9,
      'Tajikistan',
      'TJ',
      38.8,
      71.2,
      'Tanzania',
      'TZ',
      - 6.3,
      34.8,
      'Thailand',
      'TH',
      15.8,
      100.9,
      'Timor-Leste',
      'TL',
      - 8.8,
      125.7,
      'Togo',
      'TG',
      8.6,
      0.8,
      'Tokelau',
      'TK',
      - 8.9,
      - 171.8,
      'Tonga',
      'TO',
      - 21.1,
      - 175.1,
      'Trinidad and Tobago',
      'TT',
      10.6,
      - 61.2,
      'Tunisia',
      'TN',
      33.8,
      9.5,
      'Turkey',
      'TR',
      38.9,
      35.2,
      'Turkmenistan',
      'TM',
      38.9,
      59.5,
      'Turks and Caicos Islands',
      'TC',
      21.6,
      - 71.7,
      'Tuvalu',
      'TV',
      - 7.1,
      177.6,
      'U.S. Minor Outlying Islands',
      'UM',
      0,
      0,
      'U.S. Virgin Islands',
      'VI',
      18.3,
      - 64.8,
      'Uganda',
      'UG',
      1.3,
      32.2,
      'Ukraine',
      'UA',
      48.3,
      31.1,
      'United Arab Emirates',
      'AE',
      23.4,
      53.8,
      'United Kingdom',
      'GB',
      55.3,
      - 3.4,
      'United States',
      'US',
      37,
      - 95.7,
      'Uruguay',
      'UY',
      - 32.5,
      - 55.7,
      'Uzbekistan',
      'UZ',
      41.3,
      64.5,
      'Vanuatu',
      'VU',
      - 15.3,
      166.9,
      'Vatican City',
      'VA',
      41.9,
      12.4,
      'Venezuela',
      'VE',
      6.4,
      - 66.5,
      'Vietnam',
      'VN',
      14,
      108.2,
      'Wales',
      'WLS',
      55.3,
      - 3.4,
      'Wallis and Futuna',
      'WF',
      - 13.7,
      - 177.1,
      'Western Sahara',
      'EH',
      24.2,
      - 12.8,
      'Yemen',
      'YE',
      15.5,
      48.5,
      'Zambia',
      'ZM',
      - 13.1,
      27.8,
      'Zimbabwe',
      'ZW',
      - 19,
      29.1
    ];
    m.Hs = 'wss://p2p.haxball.com/';
    m.Se = 'https://www.haxball.com/rs/';
    m.kg = [
      {
        urls: 'stun:stun.l.google.com:19302'
      }
    ];
    m.j = new uc;
    Y.ul = function () {
      let a = [];
      {
        let b = 0;
        for (; 256 > b; ) ++b,
        a.push(new P(0, 0))
      }
      return a
    }(this);
    Y.yk = function () {
      let a = [];
      {
        let b = 0;
        for (; 256 > b; ) ++b,
        a.push(0)
      }
      return a
    }(this);
    q.qs = A.ka(1024);
    Da.Aa = p.Ha({
      Ca: !1,
      delay: !1,
      nh: {
        bh: 2,
        sh: 10000
      }
    });
    Eb.Aa = p.Ha({
      Ca: !1,
      delay: !1,
      nh: {
        bh: 10,
        sh: 900
      }
    });
    Xa.Aa = p.Ha({
      Ca: !1,
      delay: !1
    });
    va.Aa = p.Ha({
      Ca: !1,
      delay: !1
    });
    Ga.Aa = p.Ha({
      Ca: !1,
      delay: !1
    });
    Qa.Aa = p.Ha({
      Ca: !1,
      delay: !1
    });
    fa.Aa = p.Ha({
      Ca: !1,
      delay: !1
    });
    Ea.Aa = p.Ha({
      Ca: !1,
      delay: !1,
      nh: {
        bh: 10,
        sh: 2000
      }
    });
    bb.Aa = p.Ha({
      Ca: !1,
      delay: !1
    });
    Fa.Aa = p.Ha({
      Ca: !1,
      delay: !1
    });
    Na.Aa = p.Ha({
      Ca: !1,
      delay: !1
    });
    Gb.Aa = p.Ha({
      Ca: !1,
      delay: !1
    });
    Za.Aa = p.Ha({
    });
    Ya.Aa = p.Ha({
      Ca: !1,
      delay: !1,
      nh: {
        bh: 10,
        sh: 900
      }
    });
    La.Aa = p.Ha({
    });
    Ha.Aa = p.Ha({
      Ca: !1,
      delay: !1
    });
    ma.Aa = p.Ha({
      Ca: !1,
      delay: !1
    });
    Fb.Aa = p.Ha({
      Ca: !1,
      delay: !1
    });
    Hb.Aa = p.Ha({
      Ca: !1,
      delay: !1
    });
    Pa.Aa = p.Ha({
      Ca: !1,
      delay: !1
    });
    Va.Aa = p.Ha({
      Ca: !1,
      delay: !1
    });
    Wa.Aa = p.Ha({
      Ca: !1,
      delay: !1
    });
    Ma.Aa = p.Ha({
      Ca: !1,
      delay: !1
    });
    I.On = 0.17435839227423353;
    I.Nn = 5.934119456780721;
    da.Ln = new Tb([0,
    0,
    2,
    1,
    0,
    0.35,
    1,
    0,
    1,
    0,
    0.7,
    1,
    0,
    0,
    0,
    1]);
    da.Mn = new Tb([0,
    - 1,
    3,
    0,
    0,
    0.35,
    0,
    0,
    0,
    0,
    0.65,
    0,
    0,
    1,
    3,
    1]);
    Ab.O = '<div class=\'dialog change-location-view\'><h1>Change Location</h1><div class=\'splitter\'><div class=\'list\' data-hook=\'list\'></div><div class=\'buttons\'><button data-hook=\'change\'>Change</button><button data-hook=\'cancel\'>Cancel</button></div></div></div>';
    $a.O = '<div class=\'chatbox-view\'><div class=\'chatbox-view-contents\'><div data-hook=\'drag\' class=\'drag\'></div><div data-hook=\'log\' class=\'log subtle-thin-scrollbar\'><div data-hook=\'log-contents\' class=\'log-contents\'><p>Controls:<br/>Move: WASD or Arrows<br/>Kick: X, Space, Ctrl, Shift, Numpad 0<br/>View: Numbers 1 to 4</p></div></div><div class=\'autocompletebox\' data-hook=\'autocompletebox\'></div><div class=\'input\'><input data-hook=\'input\' type=\'text\' /></div></div></div>';
    zb.O = '<div class=\'choose-nickname-view\'><img src="images/haxball.png" /><div class=\'dialog\'><h1>Choose nickname</h1><div class=\'label-input\'><label>Nick:</label><input data-hook=\'input\' type=\'text\' /></div><button data-hook=\'ok\'>Ok</button></div></div>';
    ub.O = '<div class=\'connecting-view\'><div class=\'dialog\'><h1>Connecting</h1><div class=\'connecting-view-log\' data-hook=\'log\'></div><button data-hook=\'cancel\'>Cancel</button></div></div>';
    Bb.O = '<div class=\'create-room-view\'><div class=\'dialog\'><h1>Create room</h1><div class=\'label-input\'><label>Room name:</label><input data-hook=\'name\' required /></div><div class=\'label-input\'><label>Password:</label><input data-hook=\'pass\' /></div><div class=\'label-input\'><label>Max players:</label><select data-hook=\'max-pl\'></select></div><button data-hook=\'unlisted\'></button><div class=\'row\'><button data-hook=\'cancel\'>Cancel</button><button data-hook=\'create\'>Create</button></div></div></div>';
    ab.O = '<div class=\'disconnected-view\'><div class=\'dialog basic-dialog\'><h1>Disconnected</h1><p data-hook=\'reason\'></p><div class=\'buttons\'><button data-hook=\'ok\'>Ok</button><button data-hook=\'replay\'>Save replay</button></div></div></div>';
    jb.O = '<div class=\'game-state-view\'><div class=\'bar-container\'><div class=\'bar\'><div class=\'scoreboard\'><div class=\'teamicon red\'></div><div class=\'score\' data-hook=\'red-score\'>0</div><div>-</div><div class=\'score\' data-hook=\'blue-score\'>0</div><div class=\'teamicon blue\'></div></div><div class="fps-limit-fix"></div><div data-hook=\'timer\'></div></div></div><div class=\'canvas\' data-hook=\'canvas\'></div></div>';
    ua.O = '<div class=\'game-view\' tabindex=\'-1\'><div class=\'gameplay-section\' data-hook=\'gameplay\'></div><div class=\'top-section\' data-hook=\'top-section\'></div><div class=\'bottom-section\'><div data-hook=\'stats\'></div><div data-hook=\'chatbox\'></div><div class=\'bottom-spacer\'></div></div><div class=\'buttons\'><div class=\'sound-button-container\' data-hook="sound"><div class=\'sound-slider\' data-hook=\'sound-slider\'><div class=\'sound-slider-bar-bg\' data-hook=\'sound-bar-bg\'><div class=\'sound-slider-bar\' data-hook=\'sound-bar\'></div></div></div><button data-hook=\'sound-btn\'><i class=\'icon-volume-up\' data-hook=\'sound-icon\'></i></button></div><button data-hook=\'menu\'><i class=\'icon-menu\'></i>Menu<span class=\'tooltip\'>Toggle room menu [Escape]</span></button><button data-hook=\'settings\'><i class=\'icon-cog\'></i></button></div><div data-hook=\'popups\'></div></div>';
    sb.O = '<div class=\'dialog kick-player-view\'><h1 data-hook=\'title\'></h1><div class=label-input><label>Reason: </label><input type=\'text\' data-hook=\'reason\' /></div><button data-hook=\'ban-btn\'><i class=\'icon-block\'></i>Ban from rejoining: <span data-hook=\'ban-text\'></span></button><div class="row"><button data-hook=\'close\'>Cancel</button><button data-hook=\'kick\'>Kick</button></div></div>';
    nb.O = '<div class=\'dialog basic-dialog leave-room-view\'><h1>Leave room?</h1><p>Are you sure you want to leave the room?</p><div class=\'buttons\'><button data-hook=\'cancel\'>Cancel</button><button data-hook=\'leave\'><i class=\'icon-logout\'></i>Leave</button></div></div>';
    gb.O = '<div class=\'dialog pick-stadium-view\'><h1>Pick a stadium</h1><div class=\'splitter\'><div class=\'list\' data-hook=\'list\'></div><div class=\'buttons\'><button data-hook=\'pick\'>Pick</button><button data-hook=\'delete\'>Delete</button><div class=\'file-btn\'><label for=\'stadfile\'>Load</label><input id=\'stadfile\' type=\'file\' accept=\'.hbs,.json,.json5\' data-hook=\'file\'/></div><button data-hook=\'export\'>Export</button><div class=\'spacer\'></div><button data-hook=\'cancel\'>Cancel</button></div></div></div>';
    qb.O = '<div class=\'dialog\' style=\'min-width:200px\'><h1 data-hook=\'name\'></h1><button data-hook=\'admin\'></button><button data-hook=\'kick\'>Kick</button><button data-hook=\'close\'>Close</button></div>';
    yb.O = '<div class=\'player-list-item\'><div data-hook=\'flag\' class=\'flagico\'></div><div data-hook=\'name\'></div><div data-hook=\'ping\'></div></div>';
    Ka.O = '<div class=\'player-list-view\'><div class=\'buttons\'><button data-hook=\'join-btn\'>Join</button><button data-hook=\'reset-btn\' class=\'admin-only\'></button></div><div class=\'list thin-scrollbar\' data-hook=\'list\'></div></div>';
    Ba.O = '<div class=\'replay-controls-view\'><button data-hook=\'reset\'><i class=\'icon-to-start\'></i></button><button data-hook=\'play\'><i data-hook=\'playicon\'></i></button><div data-hook=\'spd\'>1x</div><button data-hook=\'spddn\'>-</button><button data-hook=\'spdup\'>+</button><div data-hook=\'time\'>00:00</div><div class=\'timebar\' data-hook=\'timebar\'><div class=\'barbg\'><div class=\'bar\' data-hook=\'progbar\'></div></div><div class=\'timetooltip\' data-hook=\'timetooltip\'></div></div><button data-hook=\'leave\'>Leave</button></div>';
    rb.O = '<div class=\'dialog basic-dialog room-link-view\'><h1>Room link</h1><p>Use this url to link others directly into this room.</p><input data-hook=\'link\' readonly></input><div class=\'buttons\'><button data-hook=\'close\'>Close</button><button data-hook=\'copy\'>Copy to clipboard</button></div></div>';
    mb.Ij = '<tr><td><span data-hook=\'tag\'></span><span data-hook=\'name\'></span></td><td data-hook=\'players\'></td><td data-hook=\'pass\'></td><td><div data-hook=\'flag\' class=\'flagico\'></div><span data-hook=\'distance\'></span></td></tr>';
    Ua.Ij = '<div class=\'roomlist-view\'><div class=\'notice\' data-hook=\'notice\' hidden><div data-hook=\'notice-contents\'>Testing the notice.</div><div data-hook=\'notice-close\'><i class=\'icon-cancel\'></i></div></div><div class=\'dialog\'><h1>Room list</h1><p>Tip: Join rooms near you to reduce lag.</p><div class=\'splitter\'><div class=\'list\'><table class=\'header\'><colgroup><col><col><col><col></colgroup><thead><tr><td>Name</td><td>Players</td><td>Pass</td><td>Distance</td></tr></thead></table><div class=\'separator\'></div><div class=\'content\' data-hook=\'listscroll\'><table><colgroup><col><col><col><col></colgroup><tbody data-hook=\'list\'></tbody></table></div><div class=\'filters\'><span class=\'bool\' data-hook=\'fil-pass\'>Show locked <i></i></span><span class=\'bool\' data-hook=\'fil-full\'>Show full <i></i></span><span class=\'bool\' data-hook=\'fil-empty\'>Show empty <i></i></span></div></div><div class=\'buttons\'><button data-hook=\'refresh\'><i class=\'icon-cw\'></i><div>Refresh</div></button><button data-hook=\'join\'><i class=\'icon-login\'></i><div>Join Room</div></button><button data-hook=\'create\'><i class=\'icon-plus\'></i><div>Create Room</div></button><div class=\'spacer\'></div><div class=\'file-btn\'><label for=\'replayfile\'><i class=\'icon-play\'></i><div>Replays</div></label><input id=\'replayfile\' type=\'file\' accept=\'.hbr2\' data-hook=\'replayfile\'/></div><button data-hook=\'settings\'><i class=\'icon-cog\'></i><div>Settings</div></button><button data-hook=\'changenick\'><i class=\'icon-cw\'></i><div>Change Nick</div></button></div></div><p data-hook=\'count\'></p></div></div>';
    Cb.O = '<div class=\'room-password-view\'><div class=\'dialog\'><h1>Password required</h1><div class=\'label-input\'><label>Password:</label><input data-hook=\'input\' /></div><div class=\'buttons\'><button data-hook=\'cancel\'>Cancel</button><button data-hook=\'ok\'>Ok</button></div></div></div>';
    xb.O = '<div class=\'room-view\'><div class=\'container\'><h1 data-hook=\'room-name\'></h1><div class=\'header-btns\'><button data-hook=\'rec-btn\'><i class=\'icon-circle\'></i>Rec</button><button data-hook=\'link-btn\'><i class=\'icon-link\'></i>Link</button><button data-hook=\'leave-btn\'><i class=\'icon-logout\'></i>Leave</button></div><div class=\'teams\'><div class=\'tools admin-only\'><button data-hook=\'auto-btn\'>Auto</button><button data-hook=\'rand-btn\'>Rand</button><button data-hook=\'lock-btn\'>Lock</button><button data-hook=\'reset-all-btn\'>Reset</button></div><div data-hook=\'red-list\'></div><div data-hook=\'spec-list\'></div><div data-hook=\'blue-list\'></div><div class=\'spacer admin-only\'></div></div><div class=\'settings\'><div><label class=\'lbl\'>Time limit</label><select data-hook=\'time-limit-sel\'></select></div><div><label class=\'lbl\'>Score limit</label><select data-hook=\'score-limit-sel\'></select></div><div><label class=\'lbl\'>Stadium</label><label class=\'val\' data-hook=\'stadium-name\'>testing the stadium name</label><button class=\'admin-only\' data-hook=\'stadium-pick\'>Pick</button></div></div><div class=\'controls admin-only\'><button data-hook=\'start-btn\'><i class=\'icon-play\'></i>Start game</button><button data-hook=\'stop-btn\'><i class=\'icon-stop\'></i>Stop game</button><button data-hook=\'pause-btn\'><i class=\'icon-pause\'></i>Pause</button></div></div></div>';
    na.O = '<div class=\'dialog settings-view\'><h1>Settings</h1><button data-hook=\'close\'>Close</button><div class=\'tabs\'><button data-hook=\'soundbtn\'>Sound</button><button data-hook=\'videobtn\'>Video</button><button data-hook=\'inputbtn\'>Input</button><button data-hook=\'miscbtn\'>Misc</button></div><div data-hook=\'presskey\' tabindex=\'-1\'><div>Press a key</div></div><div class=\'tabcontents\'><div class=\'section\' data-hook=\'miscsec\'><div class=\'loc\' data-hook=\'loc\'></div><div class=\'loc\' data-hook=\'loc-ovr\'></div><button data-hook=\'loc-ovr-btn\'></button></div><div class=\'section\' data-hook=\'soundsec\'><div data-hook="tsound-main">Sounds enabled</div><div data-hook="tsound-chat">Chat sound enabled</div><div data-hook="tsound-highlight">Nick highlight sound enabled</div><div data-hook="tsound-crowd">Crowd sound enabled</div></div><div class=\'section\' data-hook=\'inputsec\'></div><div class=\'section\' data-hook=\'videosec\'><div>Viewport Mode:<select data-hook=\'viewmode\'><option>Dynamic</option><option>Restricted 840x410</option><option>Full 1x Zoom</option><option>Full 1.25x Zoom</option><option>Full 1.5x Zoom</option><option>Full 1.75x Zoom</option><option>Full 2x Zoom</option><option>Full 2.25x Zoom</option><option>Full 2.5x Zoom</option></select></div><div>FPS Limit:<select data-hook=\'fps\'><option>None (Recommended)</option><option>30</option></select></div><div>Resolution Scaling:<select data-hook=\'resscale\'><option>100%</option><option>75%</option><option>50%</option><option>25%</option></select></div><div data-hook="tvideo-lowlatency">Use low latency canvas</div><div data-hook="tvideo-teamcol">Custom team colors enabled</div><div data-hook="tvideo-showindicators">Show chat indicators</div><div data-hook="tvideo-showavatars">Show player avatars</div><div class="option-row"><div style="margin-right: 10px; flex: 1; max-width: 115px;">Chat opacity </div><div style="width: 40px" data-hook="chatopacity-value">1</div><input class="slider" type="range" min="0.5" max="1" step="0.01" data-hook="chatopacity-range"></div><div class="option-row"><div style="margin-right: 10px; flex: 1; max-width: 115px;">Chat focus height </div><div style="width: 40px" data-hook="chatfocusheight-value">200</div><input class="slider" type="range" min="0" max="400" step="10" data-hook="chatfocusheight-range"></div><div>Chat background width:<select data-hook=\'chatbgmode\'><option>Full</option><option>Compact</option></select></div></div></div></div>';
    na.ym = 0;
    ba.O = '<div class=\'simple-dialog-view\'><div class=\'dialog basic-dialog\'><h1 data-hook=\'title\'></h1><p data-hook=\'content\'></p><div class=\'buttons\' data-hook=\'buttons\'></div></div></div>';
    wb.O = '<div class="stats-view-container"><div class=\'stats-view\'><p data-hook=\'ping\'></p><p data-hook=\'fps\'></p><div data-hook=\'graph\'></div></div></div>';
    kb.O = '<div class=\'unsupported-browser-view\'><div class=\'dialog\'><h1>Unsupported Browser</h1><p>Sorry! Your browser doesn\'t yet implement some features which are required for HaxBall to work.</p><p>The missing features are: <span data-hook=\'features\'></span></p><h2>Recommended browsers:</h2><div><a href="https://www.mozilla.org/firefox/new/"><img src="images/firefox-icon.png"/>Firefox</a></div><div><a href="https://www.google.com/chrome/"><img src="images/chrome-icon.png"/>Chrome</a></div><div><a href="http://www.opera.com/"><img src="images/opera-icon.png"/>Opera</a></div></div></div>';
    B.Yp()
  }
) (
  'undefined' != typeof window ? window : 'undefined' != typeof global ? global : 'undefined' != typeof self ? self : this
);
