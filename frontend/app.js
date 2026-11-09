/* Mazhai Cover — React 18 (CDN, createElement, no build). Flat design + free Unsplash photos. */
(function () {
  const h = React.createElement;
  const { useState, useEffect } = React;

  const API_ORIGIN = window.location.origin.startsWith("http") ? window.location.origin : "http://127.0.0.1:5000";
  const API_PATH = "/api/report";
  const ADMIN_PATH = "/api/admin";
  const PROVIDER_PATH = "/api/report?source=http://127.0.0.1:9000/provider";
  const DEMO_TOKEN = "demo-token-1234";

  /* Free images (Unsplash, hot-link allowed). Nature / monsoon vibes. */
  const PHOTOS = [
    { src: "https://images.unsplash.com/photo-1428592953211-077101b2021b?auto=format&fit=crop&w=600&q=80", tag: "Monsoon rain" },
    { src: "https://images.unsplash.com/photo-1504893524553-b855bce32c67?auto=format&fit=crop&w=600&q=80", tag: "River & hills" },
    { src: "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=600&q=80", tag: "Green forest" },
    { src: "https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?auto=format&fit=crop&w=600&q=80", tag: "Sunset beach" }
  ];
  const HERO_SRC = "https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?auto=format&fit=crop&w=900&q=80";

  function mergePrefs(target, source) { Object.assign(target, source); return target; }

  function ZoneTable(props) {
    return h("table", null,
      h("thead", null, h("tr", null,
        h("th", null, "Zone"), h("th", null, "Risk"), h("th", null, "Members"),
        h("th", null, "Payout"), h("th", null, "Premium"))),
      h("tbody", null, props.zones.map(z =>
        h("tr", { key: z.zone_id },
          h("td", null, z.zone_name), h("td", null, z.risk_score), h("td", null, z.members),
          h("td", null, "Rs. " + z.payout), h("td", null, "Rs. " + z.premium)))));
  }

  function App() {
    const [report, setReport] = useState(null);
    const [sim, setSim] = useState(null);
    const [status, setStatus] = useState("Loading report...");
    let prefs = {};
    try { prefs = mergePrefs({}, JSON.parse(localStorage.getItem("mazhai.prefs") || "{}")); } catch (e) {}

    useEffect(function () {
      fetch(API_ORIGIN + API_PATH + "?token=" + DEMO_TOKEN)
        .then(function (r) { return r.json(); })
        .then(function (d) { setReport(d); setStatus("Report loaded"); })
        .catch(function (e) { setStatus("Report failed: " + e.message); });
      fetch(API_ORIGIN + ADMIN_PATH).then(function (r) { return r.json(); })
        .then(function (d) { console.log("admin", d); }).catch(function () {});
    }, []);

    function runSim() {
      setStatus("Simulating...");
      fetch(API_ORIGIN + "/api/simulate")
        .then(function (r) { return r.json(); })
        .then(function (d) { setSim(d); setStatus("Simulation done"); })
        .catch(function (e) { setStatus("Simulate failed: " + e.message); });
    }

    return h("div", null,
      h("nav", { className: "nav" },
        h("div", { className: "wrap" },
          h("span", { className: "logo" }, "Mazhai Cover"),
          h("div", { className: "links" },
            h("span", null, "Dashboard"), h("span", null, "Zones"), h("span", null, "Simulate")))),
      h("header", { className: "hero" },
        h("div", { className: "wrap hero-grid" },
          h("div", null,
            h("span", { className: "eyebrow" }, "Chennai • Rider cover"),
            h("h1", null, "Rain today. ", h("span", null, "Riding tomorrow.")),
            h("p", { className: "lead" }, "Flat, fast cover for gig riders in the monsoon. Live data from ", h("code", null, "/api/report"), "."),
            h("div", { className: "actions" },
              h("button", { className: "btn-solid", onClick: runSim }, "Run simulation"),
              h("button", { className: "btn-outline", onClick: function () { window.scrollTo({ top: 900, behavior: "smooth" }); } }, "See zones"))),
          h("div", { className: "hero-photo" },
            h("img", { src: HERO_SRC, alt: "Rain and a rider in the city" }),
            h("div", { className: "cap" }, "Monsoon in Chennai — freedom to ride"))),
      h("section", { className: "shapes" },
        h("div", { className: "wrap row" },
          h("div", { className: "shape s1" }, "● SUN"),
          h("div", { className: "shape s2" }, "■ RIDE"),
          h("div", { className: "shape s3" }, "▲ NATURE"),
          h("div", { className: "shape s4" }, "◆ SAFETY"))),
      h("main", { className: "wrap shell" },
        h("section", { className: "stats" },
          h("div", { className: "stat" }, h("div", { className: "num" }, report ? "Rs. " + report.total_payout : "—"), h("div", { className: "lbl" }, "Total payouts")),
          h("div", { className: "stat alt" }, h("div", { className: "num" }, report ? report.events : "—"), h("div", { className: "lbl" }, "Triggers")),
          h("div", { className: "stat" }, h("div", { className: "num" }, report ? report.riders : "—"), h("div", { className: "lbl" }, "Riders"))),
        h("section", { className: "gallery" },
          h("h2", null, "Natural vibes"),
          h("p", { className: "hint" }, "Free photos from Unsplash — rain, rivers, forests and sunset. Flat cards, light pages."),
          h("div", { className: "ph-grid" },
            PHOTOS.map(function (p, i) {
              return h("div", { className: "ph", key: i },
                h("img", { src: p.src, alt: p.tag, loading: "lazy" }),
                h("div", { className: "tag" }, p.tag));
            }))),
        h("section", { className: "grid" },
          h("div", { className: "card" },
            h("h2", null, "Zones"),
            h("p", null, "Premiums stay within 2.5×. Every zone gets the same horizon."),
            h("span", { className: "status" }, status),
            report && h(ZoneTable, { zones: report.zones }),
            !report && h("p", null, "Loading...")),
          h("div", { className: "card dark" },
            h("h2", null, "Simulate"),
            h("p", null, "Monte-Carlo storm path. Flat UI, serious maths."),
            h("button", { className: "btn-solid", onClick: runSim }, "Run simulation"),
            sim && h("pre", null, JSON.stringify(sim.portfolio, null, 2)),
            h("p", { style: { fontSize: 13, marginTop: 12 } }, "Prefs: ", JSON.stringify(prefs)))),
        h("footer", null, "Mazhai (மழை) = rain. Cover that keeps Chennai moving. Live API, flat design."))));
  }

  ReactDOM.createRoot(document.getElementById("root")).render(h(App));
})();
