"""Writes playnordant.com's pages into the nordant-site repo: python build.py <site dir>."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parts import head, bar, FOOT, PLAY, SITE, LEADERBOARD

OUT = sys.argv[1]
BADGE = f'<a href="{PLAY}"><img alt="Get it on Google Play" src="https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png"></a>'
TIERS = ["Slush", "Frost", "Pine", "Granite", "Agate", "Glacier", "Polar", "Aurora"]
API = "https://api-production-51079.up.railway.app"


def page(name, title, description, path, body, current="", noindex=False):
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(head(title, description, path, noindex) + bar(current) + body + FOOT)


def feature(title, text):
    return f'<div class="feature"><h3>{title}</h3><p>{text}</p></div>'


# The trailer first, played from this site (the user, 2026-10-19: "embedded directly", not
# YouTube); nothing of it is fetched until it's played.
trailer = ('<video class="trailer" controls playsinline preload="none" poster="/assets/shots/trailer-poster.jpg" width="1280" height="720" aria-label="The Nordant trailer">'
           '<source src="/assets/trailer.mp4" type="video/mp4"></video>')
shots = trailer + "".join(f'<img src="/assets/shots/{n}.jpg" alt="{alt}" loading="lazy" width="1280" height="720">' for n, alt in [
    ("01-minnehaha", "A fight at the falls on Minnehaha"),
    ("02-skins", "Polar Tech, Northern Lights and Lumberjack"),
    ("03-locker", "Skins in the Locker: Polar Tech Superior, Northern Lights Fillet Knife, Lumberjack Timberwolf, Northern Lights Mosquito"),
    ("04-bait-shop", "The Bait Shop: the Polar Tech bundle"),
    ("05-season", "Season 1's pass, First Ice: the Fillet Knife, Timberwolf, Muskie and Skipstone"),
    ("06-ranked", "The ranks, Slush to Aurora"),
    ("07-full-time", "Ranked full time: a promotion to Glacier II"),
    ("08-sandstone", "Disarming the core on Sandstone with a second left"),
])

# The skins, each a still until it's tapped, then doing its own thing in a loop (the user,
# 2026-10-26: "Only have them animated when you click on one of them"); one at a time, a tap again
# stops it. Show, don't tell: only their names under them. Nothing is fetched until it's played.
SKINS = [
    ("polar-tech-north-star", "Polar Tech", "North Star"),
    ("polar-tech-superior", "Polar Tech", "Superior"),
    ("polar-tech-loon", "Polar Tech", "Loon"),
    ("northern-lights-knife", "Northern Lights", "Fillet Knife"),
    ("northern-lights-mosquito", "Northern Lights", "Mosquito"),
    ("northern-lights-blizzard", "Northern Lights", "Blizzard"),
    ("lumberjack-timberwolf", "Lumberjack", "Timberwolf"),
    ("lumberjack-taconite", "Lumberjack", "Taconite"),
]
skins = "".join(
    f'<figure class="skin l-{n.split("-")[0]}"><button type="button" class="play" aria-label="Play the {line} {gun}" aria-pressed="false">'
    f'<video muted loop playsinline preload="none" poster="/assets/skins/{n}.jpg" width="960" height="540">'
    f'<source src="/assets/skins/{n}.mp4" type="video/mp4"></video><span class="go" aria-hidden="true"></span></button>'
    f'<figcaption><b>{line}</b><span>{gun}</span></figcaption></figure>'
    for n, line, gun in SKINS)
tiers = "".join(f'<span class="tier t-{t.lower()}">{t}</span>' for t in TIERS)


def point(title, text):
    return f'<div class="point"><h3>{title}</h3><p>{text}</p></div>'


page("index.html", "Nordant", "Nordant is a tactical 5v5 shooter played as a sport: Forwards arm the core, Defensemen hold the line. Climb the ranks, squad up.", "/", f"""<main>
<div class="hero"><img src="/assets/hero.jpg" alt="Nordant: a match on a snowy rooftop" width="1024" height="500"></div>
<section class="pitch">
  <h1>Arm the core. Hold the line.</h1>
  <p>Five a side. One life a round. Every online match ranked. Squad up and climb.</p>
  <div class="badges">{BADGE}</div>
  <p class="soon">Coming to the App Store and Google Play.</p>
</section>

<div class="wrap">
<section class="section">
  <div class="shots">{shots}</div>
</section>

<section class="section">
  <h2>How it plays</h2>
  <div class="points">
    {point("Ranked from match one", "Every online match counts. Climb eight tiers, Slush to Aurora, with your squad beside you.")}
    {point("Arm it. Retake it.", "Forwards carry the core into a zone and arm it. Defensemen hold, retake, and disarm it before it blows. Sides swap at halftime.")}
    {point("Your money, your call", "Win rounds, earn cash, buy your loadout: rifles, snipers, armor, smokes and flashes. Save when you're broke. Go big when you're not.")}
    {point("Arenas that fight back", "A quarry rink with a Zamboni that clears the ice (and you), a firefight round the falls, a city in winter. Every map has moving parts.")}
  </div>
</section>

<section class="section" id="skins">
  <p class="kicker">Skins</p>
  <h2>Polar Tech. Northern Lights. Lumberjack.</h2>
  <div class="skins">{skins}</div>
</section>

<section class="section">
  <p class="kicker">Season pass</p>
  <h2>Season 1: First Ice</h2>
  <img class="art" src="/assets/art/season-1.jpg" alt="Season 1 pass, First Ice: the Fillet Knife at tier 50, the Timberwolf at 35, the Muskie at 30, the Skipstone at 15" loading="lazy" width="1920" height="1080">
</section>

<section class="section">
  <p class="kicker">Ranked</p>
  <h2>Slush to Aurora</h2>
  <img class="art" src="/assets/art/ranked.jpg" alt="The eight ranks, Slush to Aurora" loading="lazy" width="1920" height="1080">
  {'<p class="muted">See who' + chr(39) + 's on top this season, and of all time, on <a href="/leaderboard">the leaderboard</a>.</p>' if LEADERBOARD else ""}
</section>
</div>

<section class="cta">
  <h2>Drop in.</h2>
  <div class="badges">{BADGE}</div>
</section>
</main>
<script>
(function () {{
  // A skin plays when it's tapped, and stops when it's tapped again or another one is.
  var buttons = document.querySelectorAll(".skin .play");
  function stop(b) {{
    var v = b.querySelector("video");
    v.pause();
    b.classList.remove("playing");
    b.setAttribute("aria-pressed", "false");
  }}
  buttons.forEach(function (b) {{
    b.addEventListener("click", function () {{
      var v = b.querySelector("video");
      if (b.classList.contains("playing")) {{ stop(b); return; }}
      buttons.forEach(function (other) {{ if (other !== b && other.classList.contains("playing")) stop(other); }});
      v.preload = "auto";
      v.currentTime = 0;
      b.classList.add("playing");
      b.setAttribute("aria-pressed", "true");
      v.play().catch(function () {{ stop(b); }});
    }});
  }});
}})();
</script>
""")

# (Hidden: its page only sends people home, and search engines are told to leave it out.)
if not LEADERBOARD:
    page("leaderboard.html", "Leaderboard", "Nordant's leaderboard is coming back soon.", "/leaderboard",
         '<main class="prose"><h1>Leaderboard</h1><p class="muted">Coming back soon. <a href="/">Back to Nordant</a>.</p></main>'
         '<script>location.replace("/");</script>', noindex=True)
else:
  page("leaderboard.html", "Leaderboard", "The best-ranked Nordant players this season and of all time, by tier.", "/leaderboard", f"""<main class="prose" style="max-width:860px">
<h1>Leaderboard</h1>
<nav class="views" aria-label="Leaderboard">
  <a href="/leaderboard" data-view="season" aria-current="page">Season</a>
  <a href="/leaderboard?view=alltime" data-view="alltime">All time</a>
</nav>
<p class="muted" id="about">This season's top 100 ranked players. Updated every minute.</p>
<div id="board"><p class="note">Loading&hellip;</p></div>
<p class="note">Ranks run Slush, Frost, Pine, Granite, Agate, Glacier and Polar, three divisions each, then Aurora at the top. Each new season, every rank moves halfway back toward where everyone starts, and three placement matches put you back on the board.</p>
</main>
<script>
(function () {{
  var box = document.getElementById("board"), about = document.getElementById("about");
  var links = document.querySelectorAll(".views a");
  var roman = ["", " I", " II", " III"];
  var asked = 0;
  function esc(s) {{ return String(s).replace(/[&<>"']/g, function (c) {{ return {{"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}}[c]; }}); }}
  // Season: this season's ratings and record. All time: everyone's best rank ever, and their whole record.
  function show(view) {{
    var mine = ++asked;
    for (var i = 0; i < links.length; i++) {{
      if (links[i].getAttribute("data-view") === view) links[i].setAttribute("aria-current", "page");
      else links[i].removeAttribute("aria-current");
    }}
    about.textContent = view === "alltime" ? "The top 100 by the best rank they've ever reached. Updated every minute." : "This season's top 100 ranked players. Updated every minute.";
    box.innerHTML = '<p class="note">Loading&hellip;</p>';
    fetch("{API}/v1/leaderboard?view=" + view).then(function (r) {{ if (!r.ok) throw new Error(r.status); return r.json(); }}).then(function (data) {{
      if (mine !== asked) return;
      if (view === "season" && data.season && data.season.name) about.textContent = data.season.name + "'s top 100 ranked players. Updated every minute.";
      var players = data.players || [];
      if (!players.length) {{
        box.innerHTML = '<div class="box">' + (view === "alltime" ? "No one has finished their placement matches yet." : "No one has finished their placement matches this season yet.") + " Play yours and you could be first.</div>";
        return;
      }}
      var rows = players.map(function (p) {{
        var cls = "t-" + String(p.tier).toLowerCase().replace(/[^a-z]/g, "");
        return "<tr><td class=\\"place\\">" + Number(p.place) + "</td><td class=\\"name\\">" + esc(p.name) + "</td>" +
          "<td><span class=\\"rank " + cls + "\\"><i></i>" + esc(p.tier) + (roman[p.division] || "") + "</span></td>" +
          "<td class=\\"num\\">" + Number(p.wins) + "</td><td class=\\"num hide-sm\\">" + Number(p.games) + "</td></tr>";
      }}).join("");
      box.innerHTML = '<table class="board"><thead><tr><th>#</th><th>Player</th><th>' + (view === "alltime" ? "Best rank" : "Rank") + '</th><th class="num">Wins</th><th class="num hide-sm">Matches</th></tr></thead><tbody>' + rows + "</tbody></table>";
    }}).catch(function () {{
      if (mine !== asked) return;
      box.innerHTML = '<div class="box">The leaderboard couldn\\'t be loaded just now. Try again in a minute.</div>';
    }});
  }}
  // (The tabs are links, so a view can be shared; switching between them here doesn't reload the page.)
  for (var i = 0; i < links.length; i++) links[i].addEventListener("click", function (e) {{
    e.preventDefault();
    var view = this.getAttribute("data-view");
    history.replaceState(null, "", this.getAttribute("href"));
    show(view);
  }});
  show(/[?&]view=alltime(&|$)/.test(location.search) ? "alltime" : "season");
}})();
</script>
""", current="/leaderboard")

page("get.html", "Get the game", "Get Nordant on Android and iPhone.", "/get", f"""<main class="prose" style="text-align:center">
<h1>Get Nordant</h1>
<p class="muted">Arm the core. Hold the line.</p>
<div class="badges" style="margin-top:24px">{BADGE.replace('<a href=', '<a id="play" href=')}</div>
<p class="muted">Coming to the App Store too.</p>
</main>
<script>
(function () {{
  // On an Android phone, straight to Play; ?src=<tag> says where the link was found (a flyer, a post).
  var src = new URLSearchParams(location.search).get("src") || "get-page";
  var play = "{PLAY}&referrer=" + encodeURIComponent("utm_source=" + src + "&utm_medium=link");
  document.getElementById("play").href = play;
  if (/android/i.test(navigator.userAgent || "")) location.replace(play);
}})();
</script>
""", current="/get")

page("support.html", "Support", "Help with Nordant: how to play, Nords and purchases, the season pass, ranked play, and deleting your account.", "/support", """<main class="prose">
<h1>Support</h1>
<p class="muted">Help with the game, from ribby.dev.</p>

<h2>Get in touch</h2>
<p>Found a bug, or have an idea? Write to <a href="mailto:support@playnordant.com">support@playnordant.com</a>. Say which phone you play on, the name you play under, and what happened, and we'll get back to you.</p>

<h2>How do I play?</h2>
<p>Drag in the bottom-left corner of the screen to move. Tap anywhere else to aim and shoot, and hold to keep firing. With a sniper, touch to line up your shot and lift to fire; flick along your aim to scope in, and back the other way to scope out. The tutorial (How to play, on the menu) walks you through a round, and the practice range is there to warm up.</p>

<h2>What are Nords?</h2>
<p>The game's own currency, spent in the Bait Shop on skins (worn from the Locker) and on the premium season pass. You get them from the season pass's free track by playing, or buy them in packs on the Get Nords screen. Skins remake the look of you and your guns, right down to their animations and sounds. All style, no edge: they never change how you play.</p>

<h2>Buying Nords</h2>
<p>Nords you buy land in your account within seconds. If a purchase ever hasn't arrived (a payment Google Play is still processing, or a phone that went offline mid-purchase), open the game again while you're online and it catches up. Anything else, write to us with your Google Play order number (it starts with GPA, and it's in the email Google sent you) and we'll sort it out. For a refund, ask through Google Play; Nords from a refunded purchase are taken back.</p>

<h2>How does the season pass work?</h2>
<p>Each season lasts about three months and has 50 tiers. Matches earn XP (more for a win), and so do the three daily and three weekly challenges. Free-track rewards are yours as you reach each tier. Get the premium pass with Nords to unlock the premium track too, including every premium reward up to the tier you've already reached.</p>

<h2>How does ranked play work?</h2>
<p>Every online match is ranked. Your first five matches place you; after that, winning moves you up through the tiers, from Slush to Aurora, and losing moves you down. Leaving a ranked match early counts as a loss. Each new season moves every rank halfway back toward where everyone starts, with three matches to place again.""" + (' The best players this season, and the best ever, are on <a href="/leaderboard">the leaderboard</a>.' if LEADERBOARD else "") + """</p>

<h2>Moving to a new phone</h2>
<p>Sign in with Google (in Settings) and your account, with your rank, friends, Nords and skins, comes with you: sign in with the same Google account on the new phone.</p>

<h2>Deleting your account</h2>
<p>In the game, open Settings and tap Delete account. See <a href="/delete-account">deleting your account</a> for what's deleted, or to ask us to do it for you.</p>
</main>
""", current="/support")

page("delete-account.html", "Delete your account", "How to delete your Nordant account and the data kept with it.", "/delete-account", """<main class="prose">
<h1>Delete your account</h1>
<p class="muted">Nordant, by ribby.dev LLC</p>

<h2>In the game</h2>
<ol>
  <li>Open Nordant and tap <strong>Settings</strong> on the menu.</li>
  <li>Under Account, tap <strong>Delete account</strong>, and confirm.</li>
</ol>
<p>Your account is deleted from our server straight away, and the game starts you over as a new player.</p>

<h2>By email</h2>
<p>Can't open the game? Write to <a href="mailto:support@playnordant.com?subject=Delete%20my%20Nordant%20account">support@playnordant.com</a> with the subject "Delete my Nordant account". Tell us the name you play under and, if you signed in with Google, the Google account's email address. We'll confirm it's yours and delete it within 30 days, usually much sooner.</p>

<h2>What's deleted</h2>
<ul>
  <li>Your account and its sign-in sessions, and the Google account link if you signed in with Google.</li>
  <li>Your name and tag, your look, the skins you own and your Nords.</li>
  <li>Your rank, ranked results, season progress and challenges, and the matches recorded for them.</li>
  <li>Your friends, friend requests and parties.</li>
  <li>Our records of your purchases.</li>
</ul>
<p>Deleted Nords, skins and season passes can't be brought back, and aren't refunded. Our server's request logs, kept for a limited time for security, aren't part of your account and expire on their own. Google keeps its own record of anything you bought through Google Play, in your Google Play order history. RevenueCat, which checks purchases for us, keeps its record of them under your account's ID only.</p>
</main>
""", current="/delete-account")

page("privacy.html", "Privacy policy", "What Nordant collects, why, and what you can do about it.", "/privacy", """<main class="prose">
<h1>Privacy policy</h1>
<p class="muted">Effective October 26, 2026</p>

<p>Nordant is a game made by ribby.dev LLC ("we"). This page says what the game collects, why, and what you can do about it. The short version: no ads, no tracking, no selling your data, and no real name or location asked for. An email address is kept only if you choose to sign in with Google.</p>

<h2>What the game collects</h2>
<ul>
  <li><strong>A player account.</strong> When you first open the game it makes an anonymous account for you: a random ID, and when it was made and last used. It isn't tied to your name, email, phone number or contacts.</li>
  <li><strong>Your display name</strong>, the name other players see in matches and on the leaderboard, if you choose one, and your <strong>tag</strong> (six letters and numbers after it) that friends add you by.</li>
  <li><strong>Google sign-in, if you use it.</strong> Signing in with Google is optional; it lets your account follow you to a new phone. If you do, we keep your Google account's ID and its email address, to link your account to it and show you which account you're signed in with. We don't get your password or anything else from your Google account.</li>
  <li><strong>Friends and parties.</strong> The players you're friends with, friend requests and party invitations you send or receive, and whether you're online or in a match, which your friends can see.</li>
  <li><strong>Ranked play.</strong> Your rating and rank, and the results of the ranked matches you play (who was in them and how they went), to match you with players of a similar level. Your name, rank and record appear on the public leaderboard once you've played your placement matches; your rating number doesn't.</li>
  <li><strong>The season pass.</strong> Your XP and tier, whether you have the premium pass, the rewards you've been given, and your progress on challenges. To count that progress, the game reports what you did in each match: how many knockouts (and with which guns), trick shots, rounds as the star, clutches and rounds won.</li>
  <li><strong>Your stats and match history.</strong> For each match you finish, your numbers in it (knockouts, times knocked out, damage dealt and taken, shots fired and hit, trick shots, rounds won and played) are added to your stats, kept for each season and all time, online and against bots, so the game can show them to you. And your last 100 matches of each kind, each with its full-time scoreboard: the score, and the names and numbers of everyone in it. So the other players in a match you played see your name and numbers in their own history, as you see theirs.</li>
  <li><strong>Your game items</strong>: your Nords balance (the game's own currency, bought, or given by the season pass), the skins you own and wear, and a record of the matches you start and finish.</li>
  <li><strong>Purchases.</strong> If you buy Nords, a record of each purchase: what you bought, when, the store's order number, and which game account it was for. See Purchases, below.</li>
  <li><strong>Sign-in tokens</strong>, so the game remembers your account. They're kept on your device, and our server keeps only a scrambled (hashed) copy.</li>
  <li><strong>Connection details.</strong> Like any online service, our server and the multiplayer service see your device's IP address when the game connects. Our server's logs record requests, including IP addresses, for security (such as stopping abuse) and fixing problems. They're kept for a limited time and not used for anything else.</li>
</ul>

<h2>What the game doesn't do</h2>
<ul>
  <li>No advertising, and no advertising IDs.</li>
  <li>No analytics or tracking across other apps and websites.</li>
  <li>No selling or renting of your information to anyone.</li>
  <li>No access to your contacts, photos, microphone, camera or location.</li>
</ul>

<h2>Purchases</h2>
<p>Nords are sold in packs through Google Play, which handles the payment: we never see your card or payment details. We use RevenueCat to check each purchase with Google Play and tell our server, which then adds the Nords to your account. RevenueCat and our server keep a record of each purchase (the product, the time, the store's order number and your game account's ID) to credit your Nords, handle refunds and answer questions about a purchase. Nords from a refunded purchase are taken back.</p>

<h2>Who else handles it</h2>
<p>Only the services the game runs on, and only to run it:</p>
<ul>
  <li><strong>Railway</strong> hosts our server and its database.</li>
  <li><strong>Photon</strong> (Exit Games) connects players' devices for matches.</li>
  <li><strong>Edgegap</strong> runs the servers ranked matches are played on, and picks one near you from your connection.</li>
  <li><strong>Google</strong>, for Google Play purchases, and if you sign in with Google.</li>
  <li><strong>RevenueCat</strong> checks purchases, as above.</li>
  <li><strong>Unity</strong>, the engine the game is built with.</li>
</ul>
<p>We'd share information otherwise only if the law required it.</p>

<h2>Children</h2>
<p>Nordant isn't made for children under 13, and we don't knowingly collect information from them. If you think a child has given us information, contact us and we'll delete it.</p>

<h2>Deleting your account</h2>
<p>You can delete your account and everything kept with it at any time, right in the game: Settings, then Delete account. It's removed from our server straight away. You can also write to us and we'll delete it for you. See <a href="/delete-account">deleting your account</a> for the details, including what Google and RevenueCat keep. Uninstalling the game removes its sign-in from your device, but doesn't delete the account on our server.</p>

<h2>Changes</h2>
<p>If this policy changes, the new version will be posted here with a new date.</p>

<h2>Contact</h2>
<p>ribby.dev LLC, Inver Grove Heights, Minnesota, USA &middot; <a href="mailto:support@playnordant.com">support@playnordant.com</a></p>
</main>
""")

page("terms.html", "Terms of service", "The terms for playing Nordant: your account, Nords and skins, the season pass, and fair play.", "/terms", """<main class="prose">
<h1>Terms of service</h1>
<p class="muted">Effective October 19, 2026</p>

<p>These terms are between you and ribby.dev LLC ("we"), the maker of Nordant. By playing the game you agree to them. If you don't agree, please don't play.</p>

<h2>Your account</h2>
<p>The game makes an account for you when you first open it. Keep your phone and your Google account (if you sign in with it) secure: what's done with your account is your responsibility. You must be at least 13 to play. We may suspend or delete accounts that break these terms.</p>

<h2>Nords, skins and the season pass</h2>
<ul>
  <li>Nords, skins and season passes are virtual items for use in the game. Buying or earning them gives you a personal, non-transferable license to use them in Nordant; you don't own them, and they have no cash value.</li>
  <li>They can't be sold, traded, transferred to another account or exchanged for real money or anything outside the game.</li>
  <li>Purchases are made through Google Play, under its terms and refund policy. Except where the law or Google Play's policy says otherwise, purchases are final. Nords from a refunded or charged-back purchase are taken back, and the account's balance may go down accordingly.</li>
  <li>A season pass applies to its own season. Rewards are given as tiers are reached during that season; progress and tiers not reached don't carry over to the next one.</li>
  <li>We may change prices, items and rewards, and retire items, from time to time. We won't take away items you already own except as these terms allow (refunds, cheating, or a closed account).</li>
  <li>If we ever close the game, we'll say so in the game at least 60 days before, and stop selling Nords when we do.</li>
</ul>

<h2>Fair play</h2>
<p>Don't cheat. That means no hacks, modified versions of the game, bots or scripts that play for you, exploiting bugs to win or get items, or deliberately throwing ranked matches. Don't use a name that's offensive, impersonates someone, or harasses anyone; we may change such names. Don't try to break, overload or get unauthorized access to the game or its servers. We may reset rank, take back items, or suspend or close accounts that do any of this.</p>

<h2>The game itself</h2>
<p>The game, its art, sounds, code and names belong to ribby.dev LLC. Online play needs our servers and those of the services the game runs on, and may sometimes be unavailable. We update the game, and may add, change or remove features. The game is provided "as is", without warranties of any kind, to the extent the law allows.</p>

<h2>Limits on liability</h2>
<p>To the extent the law allows, ribby.dev LLC isn't liable for indirect, incidental or consequential damages, or for lost data or items, arising from the game; and our total liability to you for anything to do with the game is limited to what you paid us in the 12 months before the claim. Some places don't allow these limits, so they may not apply to you.</p>

<h2>Privacy</h2>
<p>How we handle your information is in the <a href="/privacy">privacy policy</a>.</p>

<h2>Changes and law</h2>
<p>We may update these terms; the new version will be posted here with a new date, and playing after that means you accept it. These terms are governed by the laws of the State of Minnesota, USA.</p>

<h2>Contact</h2>
<p>ribby.dev LLC, Inver Grove Heights, Minnesota, USA &middot; <a href="mailto:support@playnordant.com">support@playnordant.com</a></p>
</main>
""")

page("404.html", "Not found", "That page isn't here.", "/404", """<main class="prose" style="text-align:center">
<h1>Off the map</h1>
<p class="muted">That page isn't here. Head back to <a href="/">the home page</a>.</p>
</main>
""", noindex=True)
print("pages written")
