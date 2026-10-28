import json, sys, unicodedata, difflib, datetime, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")
SRC = os.path.join(D, "openfootball")
SHORT = {
 # LaLiga
 "Real Madrid CF":"Real Madrid","FC Barcelona":"Barcelona","Club Atlético de Madrid":"Atlético de Madrid","Athletic Club":"Athletic Club",
 "Villarreal CF":"Villarreal","Real Betis Balompié":"Real Betis","RC Celta de Vigo":"Celta","Real Sociedad de Fútbol":"Real Sociedad",
 "Rayo Vallecano de Madrid":"Rayo Vallecano","CA Osasuna":"Osasuna","Sevilla FC":"Sevilla","Valencia CF":"Valencia","Getafe CF":"Getafe",
 "RCD Espanyol de Barcelona":"Espanyol","Deportivo Alavés":"Alavés","Elche CF":"Elche","Levante UD":"Levante","Málaga CF":"Málaga",
 "Real Racing Club de Santander":"Racing de Santander","RC Deportivo La Coruña":"Deportivo",
 # Premier
 "Arsenal FC":"Arsenal","Liverpool FC":"Liverpool","Manchester City FC":"Manchester City","Chelsea FC":"Chelsea","Aston Villa FC":"Aston Villa",
 "Newcastle United FC":"Newcastle","Tottenham Hotspur FC":"Tottenham","Manchester United FC":"Manchester United","Brighton & Hove Albion FC":"Brighton",
 "AFC Bournemouth":"Bournemouth","Nottingham Forest FC":"Nottingham Forest","Brentford FC":"Brentford","Crystal Palace FC":"Crystal Palace",
 "Fulham FC":"Fulham","Everton FC":"Everton","Leeds United FC":"Leeds United","Sunderland AFC":"Sunderland","Coventry City FC":"Coventry City",
 "Hull City AFC":"Hull City","Ipswich Town FC":"Ipswich Town",
 # Serie A
 "FC Internazionale Milano":"Inter","SSC Napoli":"Napoli","Juventus FC":"Juventus","Atalanta BC":"Atalanta","AC Milan":"Milan","AS Roma":"Roma",
 "Como 1907":"Como","SS Lazio":"Lazio","Bologna FC 1909":"Bologna","ACF Fiorentina":"Fiorentina","Torino FC":"Torino","Udinese Calcio":"Udinese",
 "Genoa CFC":"Genoa","US Sassuolo Calcio":"Sassuolo","Cagliari Calcio":"Cagliari","Parma Calcio 1913":"Parma","US Lecce":"Lecce",
 "AC Monza":"Monza","Frosinone Calcio":"Frosinone","Venezia FC":"Venezia",
 # Bundesliga
 "FC Bayern München":"Bayern München","Borussia Dortmund":"Borussia Dortmund","Bayer 04 Leverkusen":"Bayer Leverkusen","RB Leipzig":"Leipzig",
 "Eintracht Frankfurt":"Eintracht Frankfurt","VfB Stuttgart":"Stuttgart","SC Freiburg":"Freiburg","TSG 1899 Hoffenheim":"Hoffenheim",
 "1. FSV Mainz 05":"Mainz","SV Werder Bremen":"Werder Bremen","Borussia Mönchengladbach":"Mönchengladbach","FC Augsburg":"Augsburg",
 "1. FC Union Berlin":"Union Berlin","1. FC Köln":"Köln","Hamburger SV":"Hamburgo","FC Schalke 04":"Schalke 04","SC Paderborn 07":"Paderborn",
 "SV 07 Elversberg":"Elversberg",
 # Ligue 1
 "Paris Saint-Germain FC":"Paris Saint-Germain","Olympique de Marseille":"Marsella","AS Monaco FC":"Mónaco","Lille OSC":"Lille",
 "Olympique Lyonnais":"Lyon","OGC Nice":"Niza","Racing Club de Lens":"Lens","RC Strasbourg Alsace":"Estrasburgo","Stade Rennais FC 1901":"Rennes",
 "Stade Brestois 29":"Brest","Toulouse FC":"Toulouse","AJ Auxerre":"Auxerre","Angers SCO":"Angers","Le Havre AC":"Le Havre","FC Lorient":"Lorient",
 "Paris FC":"Paris FC","ES Troyes AC":"Troyes","Le Mans FC":"Le Mans",
}
CUP_ALIAS = {"Celta de Vigo":"Celta","Racing de Santander":"Racing de Santander","Málaga":"Málaga"}
LEAGUES = [("laliga","es.1","LaLiga",0),("premier","en.1","Premier League",1),("seriea","it.1","Serie A",0),("bundes","de.1","Bundesliga",0),("ligue1","fr.1","Ligue 1",0)]
CODE = {"es":"laliga","en":"premier","it":"seriea","de":"bundes","fr":"ligue1"}
# horarios conocidos que faltan en la fuente (hora peninsular)
TIMES = {"laliga":{11:{("Villarreal","Espanyol"):("2026-10-30","21:00"),("Levante","Atlético de Madrid"):("2026-10-31","14:00"),
  ("Rayo Vallecano","Celta"):("2026-10-31","16:15"),("Real Betis","Málaga"):("2026-10-31","18:30"),("Barcelona","Alavés"):("2026-10-31","21:00"),
  ("Getafe","Sevilla"):("2026-11-01","14:00"),("Racing de Santander","Real Madrid"):("2026-11-01","16:15"),("Elche","Valencia"):("2026-11-01","18:30"),
  ("Athletic Club","Real Sociedad"):("2026-11-01","21:00"),("Deportivo","Osasuna"):("2026-11-02","21:00")}}}

def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode().lower().replace("-"," ")
    drop = {"fc","cf","ac","ss","ssc","as","us","afc","rc","rcd","cd","ud","sc","club","de","la","1907","1909","1913","05","04","07","29","1899","1901","1.","fsv","vfb","tsg","sv","calcio","balompie","futbol","ogc","osc","sco","estac","es","aj","bc","acf","cfc","&","04"}
    return " ".join(w for w in s.split() if w not in drop)
def sim(a,b):
    a,b = norm(a),norm(b)
    r = difflib.SequenceMatcher(None,a,b).ratio()
    if a in b or b in a: r += .5
    return r

def plus1(t):
    h,m = map(int,t.split(":")); return f"{(h+1)%24:02d}:{m:02d}"

out = {"updated": datetime.date.today().isoformat(), "comps": {}}
res = {}
for line in open(os.path.join(D,"results.txt"),encoding="utf8"):
    line=line.strip()
    if not line: continue
    c,r,h,a,s = line.split("|"); res.setdefault((CODE[c],int(r)),[]).append((h,a,s))

for key,f,name,bst in LEAGUES:
    m = json.load(open(os.path.join(SRC,f+".json"),encoding="utf8"))["matches"]
    rounds = {}
    for x in m:
        n = int(x["round"].split()[-1]); h,a = SHORT[x["team1"]],SHORT[x["team2"]]
        t = x.get("time")
        if t and bst: t = plus1(t)
        sc = x.get("score"); sc = sc.get("ft") if isinstance(sc,dict) else sc
        rounds.setdefault(n,[]).append([x["date"],t,h,a,sc[0] if sc else None,sc[1] if sc else None])
    for n,ms in rounds.items():
        for (rh,ra,s) in res.get((key,n),[]):
            best = max(ms,key=lambda q: sim(rh,q[2])+sim(ra,q[3]))
            hs,as_ = map(int,s.split("-")); best[4],best[5] = hs,as_
        for (th,ta),(d,t) in TIMES.get(key,{}).get(n,{}).items():
            for q in ms:
                if q[2]==th and q[3]==ta: q[0],q[1]=d,t
        ms.sort(key=lambda q:(q[0],q[1] or "99"))
    out["comps"][key] = {"n":name,"rounds":[{"n":n,"m":rounds[n]} for n in sorted(rounds)]}

cups = {"ucl":{"n":"Champions League","rounds":{}},"copa":{"n":"Copa del Rey","rounds":{}},"super":{"n":"Supercopa de España","rounds":{}}}
for line in open(os.path.join(D,"cups.txt"),encoding="utf8"):
    line=line.strip()
    if not line: continue
    c,r,d,t,h,a,s = line.split("|"); h,a = CUP_ALIAS.get(h,h),CUP_ALIAS.get(a,a)
    hs = as_ = None
    if s: hs,as_ = map(int,s.split("-"))
    cups[c]["rounds"].setdefault(int(r),[]).append([d,t,h,a,hs,as_])
for c,v in cups.items():
    out["comps"][c] = {"n":v["n"],"rounds":[{"n":n,"m":v["rounds"][n]} for n in sorted(v["rounds"])]}


# plantillas y goleadores
squads={}
for fn in ["squads_es.txt","squads_ucl.txt"]:
    team=None
    for line in open(os.path.join(D,fn),encoding="utf8"):
        line=line.strip()
        if not line: continue
        if line.startswith("#"): team=line[1:]; squads[team]=[]; continue
        n,pos=line.rsplit(",",1); squads[team].append([n,pos,None])
def key(s): return unicodedata.normalize("NFKD",s).encode("ascii","ignore").decode().lower()
for fn in ["scorers_es.txt"]:
    for line in open(os.path.join(D,fn),encoding="utf8"):
        line=line.strip()
        if not line: continue
        n,t,g=line.split("|"); sq=squads[t]; k=key(n)
        hit=[p for p in sq if key(p[0])==k] or [p for p in sq if k in key(p[0]) or key(p[0]) in k] or [p for p in sq if key(p[0]).split()[-1]==k.split()[-1]]
        if len(hit)!=1: print("NO MATCH",n,t,[h[0] for h in hit]); continue
        hit[0][2]=int(g)
allteams={m[2] for c in out["comps"].values() for r in c["rounds"] for m in r["m"]}|{m[3] for c in out["comps"].values() for r in c["rounds"] for m in r["m"]}
for t in squads: assert t in allteams, t
out["visible"]=["laliga","copa","super","ucl"]
out["squads"]=squads
out["scorersAsOf"]="2026-10-27"

# cuotas 1X2 de mercado (OddsPortal)
ALIAS={"atl. madrid":"Atlético de Madrid","ath bilbao":"Athletic Club","dep. a coruna":"Deportivo","celta vigo":"Celta","betis":"Real Betis","malaga":"Málaga","alaves":"Alavés","racing santander":"Racing de Santander","manchester utd":"Manchester United","as roma":"Roma","bayern munich":"Bayern München","bodo/glimt":"Bodø/Glimt","slavia prague":"Slavia Praha","psv":"PSV Eindhoven","club brugge kv":"Club Brugge","fc porto":"Porto","rb leipzig":"Leipzig","sabah fc":"Sabah","fenerbahce":"Fenerbahçe","psg":"Paris Saint-Germain","dortmund":"Borussia Dortmund","anaitasuna ft":"Anaitasuna","tarancon":"Tarancón"}
odds={}
for line in open(os.path.join(D,"odds.txt"),encoding="utf8"):
    line=line.strip()
    if not line: continue
    c,d,h,a,o1,ox,o2=line.split("|")
    h=ALIAS.get(h.lower(),h); a=ALIAS.get(a.lower(),a)
    ms=[m for r in out["comps"][c]["rounds"] for m in r["m"] if abs((datetime.date.fromisoformat(m[0])-datetime.date.fromisoformat(d)).days)<=3]
    best=max(ms,key=lambda m: sim(h,m[2])+sim(a,m[3]))
    sc=sim(h,best[2])+sim(a,best[3])
    if sc<1.5: print("NO MATCH ODDS",c,h,a,best[2],best[3],round(sc,2)); continue
    odds[best[2]+"|"+best[3]]=[float(o1),float(ox),float(o2)]
out["odds"]=odds; out["oddsAsOf"]="2026-10-28"; out["oddsSrc"]="OddsPortal"
print("odds",len(odds))

data = json.dumps(out,ensure_ascii=False,separators=(",",":"))
tpl = open(os.path.join(ROOT,"scripts","template.html"),encoding="utf8").read()
assert "</" not in data
html = tpl.replace("__GB_DATA__", data)
HEAD = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#13211d">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="GerardBet">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
"""
SW = """<script>if("serviceWorker" in navigator){window.addEventListener("load",()=>navigator.serviceWorker.register("sw.js").catch(()=>{}))}</script>
"""
# la plantilla empieza con <title>, <meta> y <style>; van al <head>, el resto al <body>
i = html.index("<header")
page = HEAD + html[:i] + "</head>\n<body>\n" + html[i:] + "\n" + SW + "</body>\n</html>\n"
open(os.path.join(ROOT,"index.html"),"w",encoding="utf8").write(page)
print("ok", len(data), "bytes of data")
