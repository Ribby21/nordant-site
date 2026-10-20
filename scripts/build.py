"""Writes playnordant.com's pages into the nordant-site repo: python build.py <site dir>."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parts import head, bar, FOOT, PLAY, SITE

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
    ("01-zone", "A 5v5 fight for a zone on Minnehaha"),
    ("02-rank", "Full time in ranked: your numbers and your rank going up"),
    ("03-disarm", "Disarming the core with a second on the clock"),
    ("04-buy", "Buying your loadout at the start of a round"),
    ("05-ranked", "Queueing ranked with your party"),
    ("06-stats", "Your stats: K/D, damage a round, accuracy"),
])
tiers = "".join(f'<span class="tier t-{t.lower()}">{t}</span>' for t in TIERS)


def point(title, text):
    return f'<div class="point"><h3>{title}</h3><p>{text}</p></div>'


page("index.html", "Nordant", "Nordant is a tactical 5v5 shooter played as a sport: Forwards arm the core, Defensemen hold the line. Climb the ranks, squad up.", "/", f"""<main>
<div class="hero"><img src="/assets/hero.jpg" alt="Nordant: a match on a snowy rooftop" width="1024" height="500"></div>
<section class="pitch">
  <h1>Arm the core. Hold the line.</h1>
  <p>Two clubs, five a side, first to six rounds. Climb the ranks, squad up.</p>
  <div class="badges">{BADGE}</div>
  <p class="soon">Launching soon on Google Play.</p>
</section>

<div class="wrap">
<section class="section">
  <div class="shots">{shots}</div>
</section>

<section class="section">
  <h2>How it plays</h2>
  <div class="points">
    {point("Ranked", "Every online match is ranked. Climb eight tiers with your friends.")}
    {point("Forwards and Defensemen", "Forwards carry the core into a zone and arm it. Defensemen hold the zones and stop them. Sides swap at halftime.")}
    {point("Every round counts", "Buy your gear each round with what you've earned. Save, or spend.")}
    {point("Three arenas", "A quarry rink with a Zamboni, a fight round the falls, and a city in winter.")}
  </div>
</section>

<section class="section">
  <h2>Climb the ranks</h2>
  <div class="tiers">{tiers}</div>
  <p class="muted">A new season every three months, with a free track, a premium pass, and daily and weekly challenges. See who's on top on <a href="/leaderboard">the leaderboard</a>.</p>
</section>
</div>

<section class="cta">
  <h2>Drop in.</h2>
  <div class="badges">{BADGE}</div>
</section>
</main>
""")

page("leaderboard.html", "Leaderboard", "The best-ranked Nordant players right now, by tier.", "/leaderboard", f"""<main class="prose" style="max-width:860px">
<h1>Leaderboard</h1>
<p class="muted">The top 100 ranked players who've finished their five placement matches. Updated every minute.</p>
<div id="board"><p class="note">Loading&hellip;</p></div>
<p class="note">Ranks run Slush, Frost, Pine, Granite, Agate, Glacier and Polar, three divisions each, then Aurora at the top.</p>
</main>
<script>
(function () {{
  var box = document.getElementById("board");
  var roman = ["", " I", " II", " III"];
  function esc(s) {{ return String(s).replace(/[&<>"']/g, function (c) {{ return {{"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}}[c]; }}); }}
  fetch("{API}/v1/leaderboard").then(function (r) {{ if (!r.ok) throw new Error(r.status); return r.json(); }}).then(function (data) {{
    var players = data.players || [];
    if (!players.length) {{ box.innerHTML = '<div class="box">No one has finished their placement matches yet. Play five ranked matches and you could be first.</div>'; return; }}
    var rows = players.map(function (p) {{
      var cls = "t-" + String(p.tier).toLowerCase().replace(/[^a-z]/g, "");
      return "<tr><td class=\\"place\\">" + Number(p.place) + "</td><td class=\\"name\\">" + esc(p.name) + "</td>" +
        "<td><span class=\\"rank " + cls + "\\"><i></i>" + esc(p.tier) + (roman[p.division] || "") + "</span></td>" +
        "<td class=\\"num\\">" + Number(p.wins) + "</td><td class=\\"num hide-sm\\">" + Number(p.games) + "</td></tr>";
    }}).join("");
    box.innerHTML = '<table class="board"><thead><tr><th>#</th><th>Player</th><th>Rank</th><th class="num">Wins</th><th class="num hide-sm">Matches</th></tr></thead><tbody>' + rows + "</tbody></table>";
  }}).catch(function () {{
    box.innerHTML = '<div class="box">The leaderboard couldn\\'t be loaded just now. Try again in a minute.</div>';
  }});
}})();
</script>
""", current="/leaderboard")

page("get.html", "Get the game", "Download Nordant for Android.", "/get", f"""<main class="prose" style="text-align:center">
<h1>Get Nordant</h1>
<p class="muted">Arm the core. Hold the line.</p>
<div class="badges" style="margin-top:24px">{BADGE.replace('<a href=', '<a id="play" href=')}</div>
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
<p>Found a bug, missing Nords, or have an idea? Write to <a href="mailto:support@playnordant.com">support@playnordant.com</a>. Say which phone you play on, the name you play under, and what happened, and we'll get back to you.</p>

<h2>How do I play?</h2>
<p>Drag anywhere on the left half of the screen to move. On the right, run your thumb round the ring of the aim wheel to turn your aim (the line from your gun), and tap FIRE in its middle to shoot; hold it to keep firing. Aim sensitivity in Settings sets how far the ring turns your aim. The tutorial (How to play, on the menu) walks you through a round, and the practice range is there to warm up.</p>

<h2>What are Nords?</h2>
<p>The game's own currency, spent in the Bait Shop on skins (worn from the Locker) and on the premium season pass. You get them from the season pass's free track by playing, or buy them in packs on the Get Nords screen. Skins only change how you look.</p>

<h2>I bought Nords and they haven't shown up</h2>
<p>They usually arrive within a few seconds. If they haven't, close the game and open it again while you're online. Still missing after a few minutes? Write to us with your Google Play order number (it starts with GPA, and it's in the email Google sent you) and we'll sort it out. For a refund, ask through Google Play; Nords from a refunded purchase are taken back.</p>

<h2>How does the season pass work?</h2>
<p>Each season lasts about three months and has 50 tiers. Matches earn XP (more for a win), and so do the three daily and three weekly challenges. Free-track rewards are yours as you reach each tier. Get the premium pass with Nords to unlock the premium track too, including every premium reward up to the tier you've already reached.</p>

<h2>How does ranked play work?</h2>
<p>Every online match is ranked. Your first five matches place you; after that, winning moves you up through the tiers, from Slush to Aurora, and losing moves you down. Leaving a ranked match early counts as a loss. The best players are on <a href="/leaderboard">the leaderboard</a>.</p>

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
<p class="muted">Effective October 19, 2026</p>

<p>Nordant is a game made by ribby.dev LLC ("we"). This page says what the game collects, why, and what you can do about it. The short version: no ads, no tracking, no selling your data, and no real name or location asked for. An email address is kept only if you choose to sign in with Google.</p>

<h2>What the game collects</h2>
<ul>
  <li><strong>A player account.</strong> When you first open the game it makes an anonymous account for you: a random ID, and when it was made and last used. It isn't tied to your name, email, phone number or contacts.</li>
  <li><strong>Your display name</strong>, the name other players see in matches and on the leaderboard, if you choose one, and your <strong>tag</strong> (six letters and numbers after it) that friends add you by.</li>
  <li><strong>Google sign-in, if you use it.</strong> Signing in with Google is optional; it lets your account follow you to a new phone. If you do, we keep your Google account's ID and its email address, to link your account to it and show you which account you're signed in with. We don't get your password or anything else from your Google account.</li>
  <li><strong>Friends and parties.</strong> The players you're friends with, friend requests and party invitations you send or receive, and whether you're online or in a match, which your friends can see.</li>
  <li><strong>Ranked play.</strong> Your rating and rank, and the results of the ranked matches you play (who was in them and how they went), to match you with players of a similar level. Your name, rank and record appear on the public leaderboard once you've played your placement matches; your rating number doesn't.</li>
  <li><strong>The season pass.</strong> Your XP and tier, whether you have the premium pass, the rewards you've been given, and your progress on challenges. To count that progress, the game reports what you did in each match: how many knockouts (and with which guns), trick shots, rounds as the star, clutches and rounds won.</li>
  <li><strong>Your game items</strong>: your Nords balance (the game's own currency, earned by playing or bought), the skins you own and wear, and a record of the matches you start and finish.</li>
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
