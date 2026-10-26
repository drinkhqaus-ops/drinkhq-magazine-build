<?php
/**
 * Plugin Name: DrinkHQ Contribute
 * Description: Public contributor page at /contribute/ for DrinkHQ Magazine: write for us, send photos and the bartender interview. Entries go straight to HubSpot (forms in portal 443540288) and notify the team. Uses the site's own header and footer from the Contact page.
 * Version: 1.0.0
 * Author: DrinkHQ
 * Requires PHP: 7.4
 */

if (!defined('ABSPATH')) exit;

define('DHQC_PORTAL', '443540288');
define('DHQC_FORMS', [
	'write'     => '4496b826-b402-4a82-8af1-5a9736f7cbb5',
	'photos'    => 'f0046255-8881-48ae-bf72-0c91378e5ab3',
	'interview' => 'f47cab99-defd-4b77-9d54-5a70f2f7b82a',
]);

add_action('init', function () {
	$path = trim((string) parse_url($_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH), '/');
	if ($path !== 'contribute') return;
	if (!empty($_SERVER['REQUEST_METHOD']) && $_SERVER['REQUEST_METHOD'] !== 'GET' && $_SERVER['REQUEST_METHOD'] !== 'HEAD') return;
	nocache_headers();
	status_header(200);
	header('Content-Type: text/html; charset=utf-8');
	echo dhqc_page();
	exit;
}, 1);

function dhqc_shell() {
	$cached = get_transient('dhqc_shell_v2');
	if ($cached) return $cached;
	$res = wp_remote_get(home_url('/contact/'), ['timeout' => 8]);
	$html = is_wp_error($res) ? '' : (string) wp_remote_retrieve_body($res);
	if (strpos($html, '<main id="main">') === false || strpos($html, '</main>') === false) return '';
	set_transient('dhqc_shell_v2', $html, HOUR_IN_SECONDS);
	return $html;
}

function dhqc_page() {
	$shell = dhqc_shell();
	$main  = dhqc_main();
	$title = 'Contribute to DrinkHQ Magazine';
	$desc  = 'Write for DrinkHQ Magazine, send us your photos, or answer the bartender interview.';
	$url   = home_url('/contribute/');
	if (!$shell) {
		return '<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' . esc_html($title) . '</title>' . dhqc_css(true) . '</head><body>' . $main . '</body></html>';
	}
	$a = strpos($shell, '<main id="main">');
	$b = strpos($shell, '</main>', $a) + strlen('</main>');
	$out = substr($shell, 0, $a) . $main . substr($shell, $b);
	$out = preg_replace('~<title>.*?</title>~s', '<title>' . esc_html($title) . ' | DrinkHQ Media</title>', $out, 1);
	$out = preg_replace('~(<meta name="description" content=")[^"]*(")~', '${1}' . esc_attr($desc) . '${2}', $out, 1);
	$out = preg_replace('~(<link rel="canonical" href=")[^"]*(")~', '${1}' . esc_url($url) . '${2}', $out, 1);
	$out = preg_replace('~(<meta property="og:url" content=")[^"]*(")~', '${1}' . esc_url($url) . '${2}', $out, 1);
	$out = preg_replace('~(<meta property="og:title" content=")[^"]*(")~', '${1}' . esc_attr($title) . '${2}', $out, 1);
	$out = str_replace(' aria-current="page"', '', $out);
	$out = str_replace('</head>', dhqc_css(false) . '</head>', $out);
	return $out;
}

function dhqc_css($standalone) {
	$base = $standalone ? 'body{margin:0;font-family:Raleway,sans-serif;background:#F6F1E8;color:#0B2049}.in{max-width:900px;margin:0 auto;padding:40px 20px}' : '';
	return '<style id="dhqc">' . $base . '
.dhqc-tabs{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 24px}
.dhqc-tabs a{display:inline-block;padding:10px 16px;border:1.5px solid currentColor;text-decoration:none;font-weight:700;font-size:13px;letter-spacing:.08em;text-transform:uppercase}
.dhqc-tabs a[aria-selected="true"]{background:#FFC000;border-color:#FFC000;color:#0B2049}
.dhqc-panel[hidden]{display:none}
.dhqc-panel .note{font-size:14px;opacity:.8;margin:-4px 0 18px}
.dhqc-panel label small{display:block;font-weight:400;opacity:.75;font-size:12.5px;margin-top:2px}
.dhqc-ok{display:none;padding:18px 20px;border-left:4px solid #FFC000;background:#fff;font-weight:600}
.dhqc-err{display:none;color:#b00020;font-weight:600;margin-top:10px}
.dhqc-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:18px}
.dhqc-cards a{display:block;padding:18px;border-left:4px solid #FFC000;background:rgba(255,255,255,.06);text-decoration:none;color:inherit}
.dhqc-cards b{display:block;font-family:"Playfair Display",serif;font-size:20px;margin-bottom:4px}
</style>';
}

function dhqc_sections($with_feature = true) {
	$s = ['Feature Article', 'Bars in Brief', 'Bartender Interview', 'Cocktail Mastery Championship', 'Trade Connect / Sponsor Feature', 'Connoisseurs Club', 'General / Other'];
	if (!$with_feature) array_shift($s);
	$o = '<option value="">Choose a section</option>';
	foreach ($s as $x) $o .= '<option value="' . esc_attr($x) . '">' . esc_html($x) . '</option>';
	return $o;
}

function dhqc_main() {
	$privacy = 'https://thedrinkhqexperience.com.au/privacy-policy/';
	ob_start(); ?>
<main id="main">
<section class="hero short"><div class="in">
<p class="eyebrow">DrinkHQ Magazine</p>
<h1>Contribute to <em>the magazine</em></h1>
<p class="lead">Got a story, a camera or a bar worth talking about? Send it in. Every submission is read by the editorial team.</p>
<div class="dhqc-cards">
<a href="#write"><b>Write for us</b>Pitch a story or send a finished piece.</a>
<a href="#photos"><b>Send photos</b>Round nights, bars, drinks and the people behind them.</a>
<a href="#interview"><b>Bartender interview</b>Seven questions for bartenders who want to be featured.</a>
</div>
</div></section>

<section class="band paper" id="forms"><div class="in narrow">
<nav class="dhqc-tabs" role="tablist">
<a href="#write" role="tab" data-tab="write">Write for us</a>
<a href="#photos" role="tab" data-tab="photos">Send photos</a>
<a href="#interview" role="tab" data-tab="interview">Bartender interview</a>
</nav>

<div class="dhqc-panel" id="panel-write" data-form="write">
<h2>Write for us</h2>
<p class="note">Send a pitch or a finished article. Put your Word document and any images in a shared folder and paste the link below.</p>
<form class="form" novalidate>
<div class="grid2">
<label>First name*<input type="text" name="firstname" required autocomplete="given-name"></label>
<label>Last name<input type="text" name="lastname" autocomplete="family-name"></label>
<label>Email*<input type="email" name="email" required autocomplete="email"></label>
<label>Phone<input type="tel" name="phone" autocomplete="tel"></label>
</div>
<label>Website or portfolio<input type="url" name="website" placeholder="https://"></label>
<label>Section*<select name="magazine_section" required><?php echo dhqc_sections(true); ?></select></label>
<label>Short bio for publication*<textarea name="author_bio" rows="3" required></textarea></label>
<label>Link to your files*<small>Google Drive, Dropbox or WeTransfer. Make sure anyone with the link can open it.</small><input type="url" name="submission_files_link" required placeholder="https://"></label>
<label>Story ideas<textarea name="content_suggestions" rows="3"></textarea></label>
<label>Anything else we should know<textarea name="message" rows="3"></textarea></label>
<label class="check"><input type="checkbox" name="consent" required> I confirm this work is my own and not previously published, and I agree that DrinkHQ may keep my details to review this submission and contact me about it. If it is published, I grant DrinkHQ the right to publish and distribute it. See the <a href="<?php echo esc_url($privacy); ?>">Privacy Policy</a>.</label>
<button class="btn" type="submit">Send submission</button>
<p class="dhqc-err" role="alert"></p>
</form>
<p class="dhqc-ok" role="status">Thanks, we have your submission. The editorial team will be in touch.</p>
</div>

<div class="dhqc-panel" id="panel-photos" data-form="photos">
<h2>Send photos</h2>
<p class="note">High-resolution JPEG, TIFF or PNG in a shared folder. Tell us where and when they were taken, and how you'd like to be credited.</p>
<form class="form" novalidate>
<div class="grid2">
<label>First name*<input type="text" name="firstname" required autocomplete="given-name"></label>
<label>Last name<input type="text" name="lastname" autocomplete="family-name"></label>
<label>Email*<input type="email" name="email" required autocomplete="email"></label>
<label>Credit me as<input type="text" name="photo_credit_name"></label>
</div>
<label>Instagram or website<input type="text" name="social" placeholder="@handle or https://"></label>
<label>Section*<select name="magazine_section" required><?php echo dhqc_sections(false); ?></select></label>
<label>About the photos<small>Location, date and who or what is in them.</small><textarea name="image_description" rows="3"></textarea></label>
<label>Link to your files*<small>Google Drive, Dropbox or WeTransfer. Make sure anyone with the link can open it.</small><input type="url" name="submission_files_link" required placeholder="https://"></label>
<label>Anything else we should know<textarea name="message" rows="3"></textarea></label>
<label class="check"><input type="checkbox" name="consent" required> I own the copyright to these images and have the releases needed for anyone identifiable in them. I grant DrinkHQ Magazine the right to publish and use them for editorial purposes, with credit, and I agree that DrinkHQ may keep my details to review this submission and contact me about it. See the <a href="<?php echo esc_url($privacy); ?>">Privacy Policy</a>.</label>
<button class="btn" type="submit">Send photos</button>
<p class="dhqc-err" role="alert"></p>
</form>
<p class="dhqc-ok" role="status">Thanks, we have your photos. We'll be in touch if we use them.</p>
</div>

<div class="dhqc-panel" id="panel-interview" data-form="interview">
<h2>Bartender interview</h2>
<p class="note">Answer as much or as little as you like in each box. We edit for length and may follow up before publishing.</p>
<form class="form" novalidate>
<div class="grid2">
<label>First name*<input type="text" name="firstname" required autocomplete="given-name"></label>
<label>Last name<input type="text" name="lastname" autocomplete="family-name"></label>
<label>Email*<input type="email" name="email" required autocomplete="email"></label>
<label>Phone*<input type="tel" name="phone" required autocomplete="tel"></label>
<label>Instagram*<input type="text" name="instagram_handle" required placeholder="@yourhandle"></label>
<label>Where do you work?*<input type="text" name="home_venue__bar" required placeholder="Venue, city"></label>
</div>
<label>Your signature cocktail, and what inspired it*<textarea name="interview_signature_cocktail" rows="3" required></textarea></label>
<label>The most memorable moment you've had behind the bar*<textarea name="interview_memorable_moment" rows="3" required></textarea></label>
<label>Your go-to drink for guests who say they don't like cocktails*<textarea name="interview_go_to_drink" rows="3" required></textarea></label>
<label>How you stay up to date with trends and techniques*<textarea name="interview_staying_updated" rows="3" required></textarea></label>
<label>The craziest ingredient you've used, and how it turned out*<textarea name="interview_craziest_ingredient" rows="3" required></textarea></label>
<label>A cocktail that sums up your personality: name and ingredients*<textarea name="interview_personality_cocktail" rows="3" required></textarea></label>
<label>Your advice for someone starting out behind the bar*<textarea name="interview_advice" rows="3" required></textarea></label>
<label class="check"><input type="checkbox" name="consent" required> I agree that DrinkHQ Magazine may keep my details and answers to prepare my interview feature and contact me about it, and may publish my answers, edited for length, with my name and venue. See the <a href="<?php echo esc_url($privacy); ?>">Privacy Policy</a>.</label>
<button class="btn" type="submit">Send my answers</button>
<p class="dhqc-err" role="alert"></p>
</form>
<p class="dhqc-ok" role="status">Thanks, we have your answers. We'll be in touch before anything is published.</p>
</div>
</div></section>
</main>
<script>
(function(){
var PORTAL=<?php echo json_encode(DHQC_PORTAL); ?>, FORMS=<?php echo json_encode(DHQC_FORMS); ?>;
var TYPE={write:'Editorial',photos:'Image',interview:'Bartender interview'};

var tabs=[].slice.call(document.querySelectorAll('.dhqc-tabs a')), panels=[].slice.call(document.querySelectorAll('.dhqc-panel'));
function show(k,scroll){if(!FORMS[k])k='write';tabs.forEach(function(t){t.setAttribute('aria-selected',t.dataset.tab===k?'true':'false')});panels.forEach(function(p){p.hidden=p.dataset.form!==k});if(scroll){var f=document.getElementById('forms');if(f)f.scrollIntoView({behavior:'smooth'})}}
function fromHash(scroll){var h=(location.hash||'').slice(1);show(FORMS[h]?h:'write',scroll&&!!FORMS[h])}
window.addEventListener('hashchange',function(){fromHash(true)});
document.querySelectorAll('a[href^="#"]').forEach(function(a){a.addEventListener('click',function(e){var k=a.getAttribute('href').slice(1);if(FORMS[k]){e.preventDefault();history.replaceState(null,'','#'+k);show(k,true)}})});
fromHash(true);
function cookie(n){var m=document.cookie.match(new RegExp('(?:^|; )'+n+'=([^;]*)'));return m?decodeURIComponent(m[1]):''}
panels.forEach(function(p){
 var k=p.dataset.form, form=p.querySelector('form'), ok=p.querySelector('.dhqc-ok'), err=p.querySelector('.dhqc-err'), btn=form.querySelector('button');
 form.addEventListener('submit',function(e){
  e.preventDefault(); err.style.display='none';
  if(!form.checkValidity()){form.reportValidity();return}
  var fields=[], els=form.elements;
  for(var i=0;i<els.length;i++){var el=els[i];if(!el.name||el.name==='consent'||el.type==='submit')continue;var v=String(el.value||'').trim();if(!v)continue;
   if(el.name==='social'){if(/^https?:\/\//i.test(v))fields.push({objectTypeId:'0-1',name:'website',value:v});else fields.push({objectTypeId:'0-1',name:'instagram_handle',value:v});continue}
   fields.push({objectTypeId:'0-1',name:el.name,value:v})}
  var consentText=form.querySelector('[name=consent]').parentElement.textContent.replace(/\s+/g,' ').trim();
  fields.push({objectTypeId:'0-1',name:'magazine_submission_type',value:TYPE[k]});
  if(k==='interview'){fields.push({objectTypeId:'0-1',name:'message',value:'Consent given: '+consentText})}
  else{var m=fields.find(function(f){return f.name==='message'});var c='Consent given: '+consentText;if(m)m.value+='\n\n'+c;else fields.push({objectTypeId:'0-1',name:'message',value:c})}
  var ctx={pageUri:location.href,pageName:document.title};var hutk=cookie('hubspotutk');if(hutk)ctx.hutk=hutk;
  btn.disabled=true;var label=btn.textContent;btn.textContent='Sending…';
  fetch('https://api.hsforms.com/submissions/v3/integration/submit/'+PORTAL+'/'+FORMS[k],{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({fields:fields,context:ctx})})
  .then(function(r){return r.json().catch(function(){return {}}).then(function(j){if(!r.ok)throw new Error((j.errors&&j.errors[0]&&j.errors[0].message)||'Something went wrong');return j})})
  .then(function(){form.style.display='none';ok.style.display='block';ok.scrollIntoView({behavior:'smooth',block:'center'})})
  .catch(function(x){err.textContent='Sorry, that didn\'t send. Please check the form and try again, or email hello@thedrinkhqexperience.com.au. ('+x.message+')';err.style.display='block'})
  .finally(function(){btn.disabled=false;btn.textContent=label});
 });
});
})();
</script>
<?php
	return ob_get_clean();
}
