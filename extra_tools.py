"""
extra_tools.py - 30 more free browser-based tools for vdownloder.xyz.
Loaded from main.py with 2 lines (see instructions). Nothing here touches
your downloader code.
"""


def add(tool, field, RESULT, COPY_BTN, NOTE):
    def btns(items):
        return '<div class="btns">' + "".join(
            '<button type="button" %s>%s</button>' % (a, b) for a, b in items
        ) + "</div>"

    # shared YouTube id regex used by 3 tools
    YT = r"""const vid=s=>{const m=s.match(/(?:youtu\.be\/|v=|shorts\/|embed\/|live\/)([A-Za-z0-9_-]{11})/);return m?m[1]:null};
"""

    # 1 -------------------------------------------------------------
    tool(
        "frames-to-timecode-converter",
        "Frames to Timecode Converter",
        "Convert a frame count to hh:mm:ss:ff timecode for any frame rate.",
        "Turn frame numbers from your video editor into timecode and seconds." + NOTE,
        "Enter the number of frames and the frame rate (24, 25, 30, 60 and so on). "
        "The result uses non-drop-frame timecode.",
        field("fr", "Frames", "", "number", "1500")
        + field("fps", "Frame rate (fps)", "", "number", "30") + RESULT,
        r"""on('fr,fps',()=>{const f=Math.max(0,Math.floor(+$('fr').value||0)),r=+$('fps').value;
if(!r){$('o').textContent='';return}const fps=Math.round(r);const p=n=>String(n).padStart(2,'0');const s=Math.floor(f/fps);
$('o').textContent='Timecode: '+p(Math.floor(s/3600))+':'+p(Math.floor(s%3600/60))+':'+p(s%60)+':'+p(f%fps)+'\nDuration: '+(f/r).toFixed(2)+' seconds';});"""
    )

    # 2 -------------------------------------------------------------
    tool(
        "slow-motion-calculator",
        "Slow Motion Calculator",
        "Find out how slow your footage will look from the recording and timeline frame rates.",
        "Plan slow-motion shots by comparing the frame rate you film at with the "
        "frame rate of your project." + NOTE,
        "Enter the frame rate you record at (for example 120) and your timeline "
        "or export frame rate (for example 30). You get the slowdown factor and "
        "the playback speed percentage.",
        field("rec", "Recording frame rate (fps)", "", "number", "120")
        + field("tl", "Timeline frame rate (fps)", "", "number", "30") + RESULT,
        r"""on('rec,tl',()=>{const a=+$('rec').value,b=+$('tl').value;if(!a||!b){$('o').textContent='';return}
$('o').textContent='Slow motion: '+(a/b).toFixed(2)+'x slower\nPlayback speed: '+(b/a*100).toFixed(1)+'%\n1 second of real action lasts '+(a/b).toFixed(2)+' seconds';});"""
    )

    # 3 -------------------------------------------------------------
    tool(
        "timelapse-interval-calculator",
        "Timelapse Interval Calculator",
        "Calculate how often to take a photo for a timelapse of a given length.",
        "Work out the photo interval for a timelapse before you start shooting." + NOTE,
        "Enter how long the real event lasts, how long you want the final clip "
        "and the playback frame rate. The tool gives the interval between photos "
        "and the number of photos needed.",
        field("ev", "Real event length (minutes)", "", "number", "60")
        + field("cl", "Final clip length (seconds)", "", "number", "10")
        + field("fp", "Playback frame rate (fps)", "", "number", "30") + RESULT,
        r"""on('ev,cl,fp',()=>{const e=+$('ev').value*60,c=+$('cl').value,f=+$('fp').value;if(!e||!c||!f){$('o').textContent='';return}
const n=c*f;$('o').textContent='Take one photo every '+(e/n).toFixed(2)+' seconds\nTotal photos needed: '+Math.round(n)+'\nSpeed-up: '+(e/c).toFixed(0)+'x';});"""
    )

    # 4 -------------------------------------------------------------
    tool(
        "audio-file-size-calculator",
        "Audio File Size Calculator",
        "Estimate MP3, AAC or WAV file size from bitrate and duration.",
        "Know how much space a song, podcast or voiceover will take." + NOTE,
        "Enter the bitrate in kbps and the length in minutes. Common values: MP3 "
        "128 or 320 kbps, and CD-quality WAV is about 1411 kbps.",
        field("kb", "Bitrate (kbps)", "", "number", "128")
        + field("m", "Duration (minutes)", "", "number", "60") + RESULT,
        r"""on('kb,m',()=>{const b=(+$('kb').value||0)*1000*(+$('m').value||0)*60/8;$('o').textContent='Estimated size: '+(b/1e6).toFixed(2)+' MB';});"""
    )

    # 5 -------------------------------------------------------------
    tool(
        "youtube-timestamp-link-generator",
        "YouTube Timestamp Link Generator",
        "Create a YouTube link that starts at a specific time.",
        "Share a YouTube video at the exact moment you want people to watch." + NOTE,
        "Paste the YouTube link and type the start time as mm:ss or hh:mm:ss. "
        "Copy the new link and share it.",
        field("u", "YouTube link", "https://www.youtube.com/watch?v=...", "url")
        + field("tm", "Start time (mm:ss or hh:mm:ss)", "1:30")
        + field("o", "Link with timestamp", rows=2, ro=True) + COPY_BTN,
        YT + r"""on('u,tm',()=>{const id=vid($('u').value.trim());const a=$('tm').value.split(':').map(Number);
if(!id||!$('tm').value||a.some(isNaN)||a.length>3){$('o').value='';return}while(a.length<3)a.unshift(0);
$('o').value='https://youtu.be/'+id+'?t='+(a[0]*3600+a[1]*60+a[2]);});"""
    )

    # 6 -------------------------------------------------------------
    tool(
        "youtube-embed-code-generator",
        "YouTube Embed Code Generator",
        "Get the iframe embed code for any YouTube video with your own size.",
        "Create ready-to-paste HTML to show a YouTube video on your website." + NOTE,
        "Paste the video link, choose the width and height and copy the iframe "
        "code into your page.",
        field("u", "YouTube link", "https://www.youtube.com/watch?v=...", "url")
        + field("w", "Width (px)", "", "number", "560")
        + field("h", "Height (px)", "", "number", "315")
        + field("o", "Embed code", rows=5, ro=True) + COPY_BTN,
        YT + r"""on('u,w,h',()=>{const id=vid($('u').value.trim());if(!id){$('o').value='';return}
const w=Math.max(100,Math.floor(+$('w').value||560)),h=Math.max(100,Math.floor(+$('h').value||315));
$('o').value='<iframe width="'+w+'" height="'+h+'" src="https://www.youtube.com/embed/'+id+'" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>';});"""
    )

    # 7 -------------------------------------------------------------
    tool(
        "whatsapp-link-generator",
        "WhatsApp Link Generator",
        "Create a click-to-chat WhatsApp link with a ready message.",
        "Make a wa.me link that opens a WhatsApp chat with your message already typed." + NOTE,
        "Enter the phone number with the country code and no plus sign or spaces "
        "(for example 923001234567). Add an optional message and copy the link.",
        field("ph", "Phone number with country code", "923001234567", "tel")
        + field("msg", "Message (optional)", "Hello, I want to know more", rows=3)
        + field("o", "WhatsApp link", rows=2, ro=True) + COPY_BTN,
        r"""on('ph,msg',()=>{const p=$('ph').value.replace(/\D/g,'');if(!p){$('o').value='';return}
const m=$('msg').value.trim();$('o').value='https://wa.me/'+p+(m?'?text='+encodeURIComponent(m):'');});"""
    )

    # 8 -------------------------------------------------------------
    tool(
        "data-storage-converter",
        "Data Storage Converter (MB to GB and more)",
        "Convert between bytes, KB, MB, GB, TB and PB using decimal and binary units.",
        "Convert file sizes between MB, GB, TB and other units, with both 1000 "
        "and 1024 based results." + NOTE,
        "Type a number and pick its unit. The tool shows the value in every unit. "
        "Storage makers use decimal units (1 KB = 1000 B) while many operating "
        "systems use binary (1 KiB = 1024 B), so both are shown.",
        field("v", "Value", "", "number", "1")
        + '<label class="lbl" for="fu">From unit</label><select id="fu">'
          '<option>B</option><option>KB</option><option selected>MB</option>'
          '<option>GB</option><option>TB</option><option>PB</option></select>'
        + RESULT,
        r"""const U=['B','KB','MB','GB','TB','PB'];const fm=x=>x.toLocaleString('en-US',{maximumFractionDigits:6});
on('v,fu',()=>{if($('v').value===''){$('o').textContent='';return}const v=+$('v').value,i=U.indexOf($('fu').value);
let t='Decimal (1 KB = 1000 B):\n';const b=v*Math.pow(1000,i);U.forEach((u,k)=>{t+=fm(b/Math.pow(1000,k))+' '+u+'\n';});
const c=v*Math.pow(1024,i);t+='\nBinary (1 KiB = 1024 B):\n';U.forEach((u,k)=>{t+=fm(c/Math.pow(1024,k))+' '+u+'\n';});$('o').textContent=t;});"""
    )

    # 9 -------------------------------------------------------------
    tool(
        "mbps-to-mbs-converter",
        "Mbps to MB/s Converter",
        "Convert internet speed from megabits per second to megabytes per second and back.",
        "Your internet plan is in Mbps but downloads show MB/s. Convert between them here." + NOTE,
        "Type your speed in Mbps to see MB/s, or type MB/s to see Mbps. One byte "
        "is 8 bits, so divide Mbps by 8 to get MB/s.",
        field("mb", "Speed in Mbps (megabits per second)", "", "number", "100") + RESULT
        + field("ms", "Speed in MB/s (megabytes per second)", "", "number", "12.5")
        + '<div id="o2" class="result" aria-live="polite"></div>',
        r"""on('mb',()=>{$('o').textContent=((+$('mb').value||0)/8).toFixed(3)+' MB/s';});
on('ms',()=>{$('o2').textContent=((+$('ms').value||0)*8).toFixed(2)+' Mbps';});"""
    )

    # 10 ------------------------------------------------------------
    tool(
        "engagement-rate-calculator",
        "Social Media Engagement Rate Calculator",
        "Calculate engagement rate from likes, comments, shares and followers.",
        "Measure how well your posts perform compared with your audience size." + NOTE,
        "Enter your follower count and the likes, comments and shares of a post. "
        "Engagement rate is total interactions divided by followers, times 100.",
        field("f", "Followers", "", "number", "10000")
        + field("l", "Likes", "", "number", "450")
        + field("c", "Comments", "", "number", "35")
        + field("sh", "Shares (optional)", "", "number", "20") + RESULT,
        r"""on('f,l,c,sh',()=>{const f=+$('f').value;if(!f){$('o').textContent='';return}
const t=(+$('l').value||0)+(+$('c').value||0)+(+$('sh').value||0);
$('o').textContent='Engagement rate: '+(t/f*100).toFixed(2)+'%\nTotal interactions: '+t;});"""
    )

    # 11 ------------------------------------------------------------
    tool(
        "video-ad-revenue-calculator",
        "Video Ad Revenue Calculator (RPM)",
        "Estimate video ad earnings from views and RPM.",
        "Get a rough idea of how much a video could earn from ads." + NOTE,
        "Enter the number of views and your RPM (revenue per 1000 views). RPM "
        "differs a lot by country and topic, so use your own analytics value. "
        "This is only an estimate.",
        field("v", "Views", "", "number", "100000")
        + field("r", "RPM (USD per 1000 views)", "", "number", "2") + RESULT,
        r"""on('v,r',()=>{const x=(+$('v').value||0)/1000*(+$('r').value||0);$('o').textContent='Estimated earnings: $'+x.toFixed(2);});"""
    )

    # 12 ------------------------------------------------------------
    tool(
        "meta-tag-generator",
        "Meta Tag Generator",
        "Generate title, description, canonical and Open Graph meta tags for your page.",
        "Create the SEO and social sharing tags your page needs, ready to paste "
        "into the head section." + NOTE,
        "Fill in your title, description, page URL and an optional image URL. "
        "Copy the generated HTML into the head of your page.",
        field("t", "Page title", "Your page title")
        + field("d", "Meta description", "Short description of the page", rows=3)
        + field("u", "Page URL (optional)", "https://example.com/page", "url")
        + field("i", "Image URL (optional)", "https://example.com/image.jpg", "url")
        + field("o", "Meta tags", rows=9, ro=True) + COPY_BTN,
        r"""const esc=s=>s.replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
on('t,d,u,i',()=>{const t=esc($('t').value),d=esc($('d').value),u=esc($('u').value),i=esc($('i').value);
let h='<title>'+t+'</title>\n<meta name="description" content="'+d+'">\n';
if(u)h+='<link rel="canonical" href="'+u+'">\n';
h+='<meta property="og:title" content="'+t+'">\n<meta property="og:description" content="'+d+'">\n';
if(u)h+='<meta property="og:url" content="'+u+'">\n';
if(i)h+='<meta property="og:image" content="'+i+'">\n';
h+='<meta name="twitter:card" content="summary_large_image">';$('o').value=h;});"""
    )

    # 13 ------------------------------------------------------------
    tool(
        "robots-txt-generator",
        "Robots.txt Generator",
        "Create a robots.txt file with disallow rules and your sitemap link.",
        "Build a simple robots.txt for your website in seconds." + NOTE,
        "List the paths you want to block, one per line (for example /admin/). "
        "Leave it empty to allow everything. Add your sitemap URL, then copy the "
        "result into a file named robots.txt at the root of your site.",
        field("dp", "Paths to block (one per line)", "/admin/", rows=4)
        + field("sm", "Sitemap URL (optional)", "https://example.com/sitemap.xml", "url")
        + field("o", "robots.txt", rows=7, ro=True) + COPY_BTN,
        r"""on('sm,dp',()=>{let t='User-agent: *\n';const d=$('dp').value.split('\n').map(s=>s.trim()).filter(Boolean);
if(d.length){d.forEach(x=>{t+='Disallow: '+x+'\n';});}else{t+='Allow: /\n';}
const s=$('sm').value.trim();if(s)t+='\nSitemap: '+s+'\n';$('o').value=t;});"""
    )

    # 14 ------------------------------------------------------------
    tool(
        "keyword-density-checker",
        "Keyword Density Checker",
        "Find the most used words in your text and their density percentage.",
        "Check which words you repeat most before you publish an article or description." + NOTE,
        "Paste your text. The tool lists the top 10 words (common filler words "
        "are ignored) with their count and percentage of all words.",
        field("t", "Your text", "Paste your article or description here", rows=10) + RESULT,
        r"""const SW=new Set('the and for are but not you all any can had her was one our out has have this that with from they will would there their what about which when your said each she how its than them these some into more other been were then also just very over'.split(' '));
on('t',()=>{const w=($('t').value.toLowerCase().match(/[\p{L}\p{N}']+/gu)||[]);const tot=w.length;const m={};
w.forEach(x=>{if(x.length>2&&!SW.has(x))m[x]=(m[x]||0)+1;});
const top=Object.entries(m).sort((a,b)=>b[1]-a[1]).slice(0,10);
$('o').textContent=tot?('Total words: '+tot+'\n\n'+(top.map(([k,v])=>k+': '+v+' ('+(v/tot*100).toFixed(1)+'%)').join('\n')||'No keywords found.')):'';});"""
    )

    # 15 ------------------------------------------------------------
    tool(
        "readability-score-checker",
        "Readability Score Checker (Flesch)",
        "Check how easy your English text is to read with the Flesch Reading Ease score.",
        "See whether your writing is easy enough for a wide audience." + NOTE,
        "Paste English text of at least a few sentences. A higher score is easier "
        "to read: 60 to 70 is plain English, and below 30 is very difficult. The "
        "syllable count is an estimate.",
        field("t", "Your English text", "Paste your text here", rows=10) + RESULT,
        r"""const syl=w=>{w=w.toLowerCase().replace(/[^a-z]/g,'');if(!w)return 0;if(w.length<=3)return 1;
w=w.replace(/(?:[^laeiouy]es|ed|[^laeiouy]e)$/,'').replace(/^y/,'');const m=w.match(/[aeiouy]{1,2}/g);return m?m.length:1;};
on('t',()=>{const v=$('t').value;const words=v.match(/[A-Za-z']+/g)||[];const sen=Math.max(1,(v.match(/[.!?]+(\s|$)/g)||[]).length);
if(words.length<5){$('o').textContent=v?'Enter at least a few sentences.':'';return}
const sy=words.reduce((a,w)=>a+syl(w),0);const s=206.835-1.015*(words.length/sen)-84.6*(sy/words.length);
const sc=Math.max(0,Math.min(100,s));const lvl=sc>=90?'Very easy':sc>=70?'Easy':sc>=60?'Plain English':sc>=50?'Fairly difficult':sc>=30?'Difficult':'Very difficult';
$('o').textContent='Flesch Reading Ease: '+sc.toFixed(1)+' ('+lvl+')\nWords: '+words.length+'\nSentences: '+sen;});"""
    )

    # 16 ------------------------------------------------------------
    tool(
        "reverse-text-generator",
        "Reverse Text Generator",
        "Reverse text by letters, words or lines online.",
        "Flip your text backwards in one click." + NOTE,
        "Paste your text and choose whether to reverse the letters, the order of "
        "the words or the order of the lines.",
        field("t", "Your text", "Type or paste your text", rows=5)
        + btns([('data-r="c"', "Reverse letters"), ('data-r="w"', "Reverse words"),
                ('data-r="l"', "Reverse lines")])
        + field("o", "Result", rows=5, ro=True) + COPY_BTN,
        r"""const R={c:s=>[...s].reverse().join(''),w:s=>s.split(/\s+/).reverse().join(' '),l:s=>s.split('\n').reverse().join('\n')};
document.querySelectorAll('[data-r]').forEach(b=>{b.onclick=()=>{$('o').value=R[b.dataset.r]($('t').value);};});"""
    )

    # 17 ------------------------------------------------------------
    tool(
        "remove-line-breaks",
        "Remove Line Breaks from Text",
        "Remove line breaks and extra spaces to turn text into one paragraph.",
        "Clean text copied from PDFs, emails or captions by joining all lines." + NOTE,
        "Paste your text. Every line break is replaced with a single space and "
        "double spaces are removed.",
        field("t", "Your text", "Paste text with line breaks", rows=8)
        + field("o", "Clean text", rows=8, ro=True) + COPY_BTN,
        r"""on('t',()=>{$('o').value=$('t').value.replace(/\s*[\r\n]+\s*/g,' ').replace(/ {2,}/g,' ').trim();});"""
    )

    # 18 ------------------------------------------------------------
    tool(
        "sort-lines-alphabetically",
        "Sort Lines Alphabetically",
        "Sort a list of lines from A to Z, Z to A or by length.",
        "Put any list in order: names, keywords, links or tags." + NOTE,
        "Paste your list with one item per line, then choose A to Z, Z to A or "
        "shortest first. Empty lines are removed.",
        field("t", "Your list", "One item per line", rows=8)
        + btns([('data-s="az"', "A to Z"), ('data-s="za"', "Z to A"),
                ('data-s="len"', "Shortest first")])
        + field("o", "Sorted list", rows=8, ro=True) + COPY_BTN,
        r"""const S={az:a=>a.sort((x,y)=>x.localeCompare(y)),za:a=>a.sort((x,y)=>y.localeCompare(x)),len:a=>a.sort((x,y)=>x.length-y.length)};
document.querySelectorAll('[data-s]').forEach(b=>{b.onclick=()=>{$('o').value=S[b.dataset.s]($('t').value.split('\n').filter(x=>x.trim())).join('\n');};});"""
    )

    # 19 ------------------------------------------------------------
    tool(
        "extract-urls-from-text",
        "Extract URLs from Text",
        "Find and list all http and https links inside any text.",
        "Pull every link out of a long text, email or page source." + NOTE,
        "Paste your text. All unique links starting with http or https are listed "
        "below, one per line.",
        field("t", "Your text", "Paste text that contains links", rows=8)
        + field("o", "Links found", rows=8, ro=True) + COPY_BTN,
        r"""on('t',()=>{const m=$('t').value.match(/https?:\/\/[^\s<>"')]+/g)||[];$('o').value=[...new Set(m)].join('\n');});"""
    )

    # 20 ------------------------------------------------------------
    tool(
        "extract-emails-from-text",
        "Extract Emails from Text",
        "Find and list all email addresses inside any text.",
        "Collect email addresses from a block of text quickly." + NOTE,
        "Paste your text. All unique email addresses are listed below, one per "
        "line. Only use collected addresses in ways that follow privacy and "
        "anti-spam laws.",
        field("t", "Your text", "Paste text that contains emails", rows=8)
        + field("o", "Emails found", rows=8, ro=True) + COPY_BTN,
        r"""on('t',()=>{const m=$('t').value.match(/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g)||[];$('o').value=[...new Set(m)].join('\n');});"""
    )

    # 21 ------------------------------------------------------------
    tool(
        "lorem-ipsum-generator",
        "Lorem Ipsum Generator",
        "Generate placeholder lorem ipsum paragraphs for designs and mockups.",
        "Fill your website or design mockup with dummy text." + NOTE,
        "Choose how many paragraphs you need (1 to 20) and copy the text.",
        field("n", "Number of paragraphs (1 to 20)", "", "number", "3")
        + field("o", "Lorem ipsum", rows=10, ro=True) + COPY_BTN,
        r"""const W='lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo consequat duis aute irure in reprehenderit voluptate velit esse cillum fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt culpa qui officia deserunt mollit anim id est laborum'.split(' ');
function para(k){const s=[];for(let i=0;i<4+(k%3);i++){const n=8+((i*5+k*3)%9);const w=[];for(let j=0;j<n;j++)w.push(W[(i*7+j*3+k*11)%W.length]);const t=w.join(' ');s.push(t.charAt(0).toUpperCase()+t.slice(1)+'.');}return s.join(' ');}
on('n',()=>{const n=Math.min(20,Math.max(1,Math.floor(+$('n').value||3)));const a=[];for(let i=0;i<n;i++)a.push(para(i));$('o').value=a.join('\n\n');});"""
    )

    # 22 ------------------------------------------------------------
    tool(
        "percentage-calculator",
        "Percentage Calculator",
        "Calculate percent of a number, what percent one number is of another, and percent change.",
        "Three common percentage calculations in one simple tool." + NOTE,
        "Fill in the three rows. Row 1 finds X% of Y, row 2 finds what percent X "
        "is of Y, and row 3 gives the percent increase or decrease from the first "
        "number to the second.",
        field("a1", "1) What is this percent ...", "", "number", "20")
        + field("b1", "... of this number?", "", "number", "150")
        + field("a2", "2) This number ...", "", "number", "30")
        + field("b2", "... is what percent of this number?", "", "number", "120")
        + field("a3", "3) Change from this number ...", "", "number", "80")
        + field("b3", "... to this number", "", "number", "100") + RESULT,
        r"""on('a1,b1,a2,b2,a3,b3',()=>{const n=id=>$(id).value===''?NaN:+$(id).value;
const f=x=>(isNaN(x)||!isFinite(x))?'-':(+x.toFixed(4)).toString();
$('o').textContent='1) '+$('a1').value+'% of '+$('b1').value+' = '+f(n('a1')*n('b1')/100)+'\n2) '+$('a2').value+' is '+f(n('a2')/n('b2')*100)+'% of '+$('b2').value+'\n3) Change from '+$('a3').value+' to '+$('b3').value+' = '+f((n('b3')-n('a3'))/n('a3')*100)+'%';});"""
    )

    # 23 ------------------------------------------------------------
    tool(
        "age-calculator",
        "Age Calculator",
        "Calculate your exact age in years, months and days from your date of birth.",
        "Find your exact age and the days left until your next birthday." + NOTE,
        "Pick your date of birth. The age is calculated using today's date from "
        "your device.",
        field("d", "Date of birth", "", "date") + RESULT,
        r"""on('d',()=>{const v=$('d').value;if(!v){$('o').textContent='';return}
const b=new Date(v+'T00:00:00'),t=new Date();if(b>t){$('o').textContent='The date is in the future.';return}
let y=t.getFullYear()-b.getFullYear(),m=t.getMonth()-b.getMonth(),dd=t.getDate()-b.getDate();
if(dd<0){m--;dd+=new Date(t.getFullYear(),t.getMonth(),0).getDate();}if(m<0){y--;m+=12;}
const days=Math.floor((t-b)/864e5);let nb=new Date(t.getFullYear(),b.getMonth(),b.getDate());
if(nb<=t)nb.setFullYear(t.getFullYear()+1);const left=Math.ceil((nb-t)/864e5);
$('o').textContent='Age: '+y+' years, '+m+' months, '+dd+' days\nTotal days lived: '+days.toLocaleString('en-US')+'\nNext birthday in '+left+' days';});"""
    )

    # 24 ------------------------------------------------------------
    tool(
        "days-between-dates-calculator",
        "Days Between Dates Calculator",
        "Count the number of days, weeks and months between two dates.",
        "Find how many days there are between any two dates." + NOTE,
        "Pick a start date and an end date. The result is the number of days "
        "between them, also shown in weeks and approximate months.",
        field("d1", "Start date", "", "date") + field("d2", "End date", "", "date") + RESULT,
        r"""on('d1,d2',()=>{if(!$('d1').value||!$('d2').value){$('o').textContent='';return}
const a=new Date($('d1').value+'T00:00:00'),b=new Date($('d2').value+'T00:00:00');
const d=Math.round(Math.abs(b-a)/864e5);$('o').textContent='Days between: '+d+'\nWeeks: '+(d/7).toFixed(1)+'\nApprox. months: '+(d/30.44).toFixed(1);});"""
    )

    # 25 ------------------------------------------------------------
    tool(
        "hex-to-rgb-converter",
        "HEX to RGB Color Converter",
        "Convert a HEX color code to RGB and preview the color.",
        "Turn a color code like #1a2b3c into RGB values and see the color." + NOTE,
        "Type a 3 or 6 digit HEX code with or without the # sign. The RGB value "
        "and a color preview appear below.",
        field("hx", "HEX color", "#2563eb", "text", "#2563eb") + RESULT,
        r"""on('hx',()=>{let h=$('hx').value.trim().replace('#','');if(h.length===3)h=h.split('').map(c=>c+c).join('');
if(!/^[0-9a-fA-F]{6}$/.test(h)){$('o').textContent=$('hx').value?'Enter a valid HEX color like #1a2b3c':'';return}
const r=parseInt(h.slice(0,2),16),g=parseInt(h.slice(2,4),16),b=parseInt(h.slice(4,6),16);
$('o').textContent='RGB: rgb('+r+', '+g+', '+b+')\nHEX: #'+h.toLowerCase();
const s=document.createElement('div');s.style.cssText='height:60px;border-radius:8px;margin-top:10px;background:#'+h;$('o').append(s);});"""
    )

    # 26 ------------------------------------------------------------
    tool(
        "number-to-words-converter",
        "Number to Words Converter",
        "Convert any number into English words, for cheques and documents.",
        "Write numbers in words, like 1250 becomes one thousand two hundred fifty." + NOTE,
        "Type a whole number (up to 12 digits). The English words appear below.",
        field("n", "Number", "", "text", "1250") + RESULT + COPY_BTN,
        r"""const A=['zero','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen'],T=['','','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety'];
function hh(n){let s='';if(n>=100){s+=A[Math.floor(n/100)]+' hundred';n%=100;if(n)s+=' ';}if(n>=20){s+=T[Math.floor(n/10)];if(n%10)s+='-'+A[n%10];}else if(n>0||!s){s+=A[n];}return s;}
function ww(n){if(n===0)return 'zero';const P=[[1e9,'billion'],[1e6,'million'],[1e3,'thousand']];const s=[];for(const [v,nm] of P){if(n>=v){s.push(hh(Math.floor(n/v))+' '+nm);n%=v;}}if(n>0)s.push(hh(n));return s.join(' ');}
on('n',()=>{const v=$('n').value.trim();if(!/^-?\d{1,12}$/.test(v)){$('o').textContent=v?'Enter a whole number up to 12 digits.':'';return}const n=+v;$('o').textContent=(n<0?'minus ':'')+ww(Math.abs(n));});"""
    )

    # 27 ------------------------------------------------------------
    tool(
        "morse-code-translator",
        "Morse Code Translator",
        "Translate text to Morse code and Morse code back to text.",
        "Convert letters and numbers to dots and dashes and back." + NOTE,
        "To encode, type text and press Encode. To decode, paste Morse code with "
        "spaces between letters and / between words, then press Decode.",
        field("t", "Input", "Type text or Morse code", rows=5)
        + btns([('id="enc"', "Text to Morse"), ('id="dec"', "Morse to Text")])
        + field("o", "Result", rows=5, ro=True) + COPY_BTN,
        r"""const M={A:'.-',B:'-...',C:'-.-.',D:'-..',E:'.',F:'..-.',G:'--.',H:'....',I:'..',J:'.---',K:'-.-',L:'.-..',M:'--',N:'-.',O:'---',P:'.--.',Q:'--.-',R:'.-.',S:'...',T:'-',U:'..-',V:'...-',W:'.--',X:'-..-',Y:'-.--',Z:'--..',0:'-----',1:'.----',2:'..---',3:'...--',4:'....-',5:'.....',6:'-....',7:'--...',8:'---..',9:'----.'};
const RM=Object.fromEntries(Object.entries(M).map(([k,v])=>[v,k]));
$('enc').onclick=()=>{$('o').value=$('t').value.toUpperCase().split('').map(c=>c===' '?'/':(M[c]||'')).filter(x=>x!=='').join(' ');};
$('dec').onclick=()=>{$('o').value=$('t').value.trim().split(/\s+/).map(c=>c==='/'?' ':(RM[c]||'?')).join('');};"""
    )

    # 28 ------------------------------------------------------------
    tool(
        "binary-to-text-converter",
        "Binary to Text Converter",
        "Convert text to binary code and binary code back to text.",
        "Translate between readable text and 8-bit binary." + NOTE,
        "To encode, type text and press Text to Binary. To decode, paste binary "
        "groups of 8 digits separated by spaces and press Binary to Text.",
        field("t", "Input", "Type text or paste binary", rows=5)
        + btns([('id="enc"', "Text to Binary"), ('id="dec"', "Binary to Text")])
        + field("o", "Result", rows=5, ro=True) + COPY_BTN,
        r"""$('enc').onclick=()=>{$('o').value=[...new TextEncoder().encode($('t').value)].map(b=>b.toString(2).padStart(8,'0')).join(' ');};
$('dec').onclick=()=>{try{const b=$('t').value.trim().split(/\s+/).map(x=>{if(!/^[01]{1,8}$/.test(x))throw 0;return parseInt(x,2);});
$('o').value=new TextDecoder().decode(Uint8Array.from(b));}catch(e){$('o').value='Enter binary groups of 0 and 1 separated by spaces.';}};"""
    )

    # 29 ------------------------------------------------------------
    tool(
        "unix-timestamp-converter",
        "Unix Timestamp Converter",
        "Convert Unix timestamps to a readable date and dates to Unix time.",
        "Read Unix timestamps from logs and APIs, or create one from a date." + NOTE,
        "Type a timestamp in seconds or milliseconds to see the date, or pick a "
        "date and time below to get its Unix timestamp.",
        field("ts", "Unix timestamp (seconds or milliseconds)", "", "text", "1760000000")
        + btns([('id="now"', "Use current time")]) + RESULT
        + field("dt", "Date and time", "", "datetime-local")
        + '<div id="o2" class="result" aria-live="polite"></div>',
        r"""on('ts',()=>{const v=$('ts').value.trim();if(!/^\d+$/.test(v)){$('o').textContent='';return}
let n=+v;if(v.length>=13)n=Math.floor(n/1000);const d=new Date(n*1000);
if(isNaN(d.getTime())){$('o').textContent='Number is too large.';return}
$('o').textContent='UTC: '+d.toUTCString()+'\nLocal: '+d.toString()+'\nISO: '+d.toISOString();});
$('now').onclick=()=>{$('ts').value=Math.floor(Date.now()/1000);$('ts').dispatchEvent(new Event('input'));};
$('dt').addEventListener('input',()=>{const d=new Date($('dt').value);$('o2').textContent=isNaN(d.getTime())?'':'Unix timestamp: '+Math.floor(d.getTime()/1000);});"""
    )

    # 30 ------------------------------------------------------------
    tool(
        "uuid-generator",
        "UUID Generator",
        "Generate random version 4 UUIDs online, one or many at a time.",
        "Create unique IDs for databases, apps and testing." + NOTE,
        "Choose how many UUIDs you need (1 to 100) and press Generate. They are "
        "created in your browser using its secure random generator.",
        field("n", "How many (1 to 100)", "", "number", "5")
        + btns([('id="g"', "Generate")])
        + field("o", "UUIDs", rows=8, ro=True) + COPY_BTN,
        r"""function gen(){if(crypto.randomUUID)return crypto.randomUUID();
return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,c=>{const r=crypto.getRandomValues(new Uint8Array(1))[0]%16;return(c==='x'?r:(r&3|8)).toString(16);});}
$('g').onclick=()=>{const n=Math.min(100,Math.max(1,Math.floor(+$('n').value||1)));const a=[];for(let i=0;i<n;i++)a.push(gen());$('o').value=a.join('\n');};$('g').click();"""
    )
