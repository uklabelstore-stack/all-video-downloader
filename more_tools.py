"""
more_tools.py - the 7 tool pages that blog posts link to but did not exist.
Same format as extra_tools.py. Put this file next to main.py and add these
2 lines in main.py, right after the line `extra_tools.add(tool, field, RESULT, COPY_BTN, NOTE)`:

    import more_tools
    more_tools.add(tool, field, RESULT, COPY_BTN, NOTE)
"""


def add(tool, field, RESULT, COPY_BTN, NOTE):
    def btns(items):
        return '<div class="btns">' + "".join(
            '<button type="button" %s>%s</button>' % (a, b) for a, b in items
        ) + "</div>"

    def faq(items):
        return "<h2>Frequently asked questions</h2>" + "".join(
            "<h3>%s</h3><p>%s</p>" % (q, a) for q, a in items
        )

    def select(i, label, opts):
        o = "".join(
            '<option value="%s"%s>%s</option>' % (v, " selected" if s else "", t)
            for v, t, s in opts
        )
        return '<label class="lbl" for="%s">%s</label><select id="%s">%s</select>' % (i, label, i, o)

    # 1 -------------------------------------------------------------
    tool(
        "aspect-ratio-calculator",
        "Aspect Ratio Calculator",
        "Calculate the aspect ratio of any image or video and resize to a new width or height without stretching. Includes 16:9, 9:16, 1:1 and 4:5 presets.",
        "Find the aspect ratio of an image or video and resize it without stretching "
        "or squashing it. Enter the original width and height to see the simplified "
        "ratio, such as 16:9 for YouTube videos or 9:16 for Shorts, Reels and TikTok. "
        "Then type a new width or a new height and the matching size is calculated "
        "for you. This is useful for thumbnails, banners, social media posts, "
        "website images and video exports where the proportions must stay the same." + NOTE,
        "Enter the original width and height, or tap a preset such as 16:9. Type "
        "either a new width or a new height and the other side is filled in "
        "automatically. The ratio is shown in its simplest form together with its "
        "decimal value.",
        field("ow", "Original width (px)", "", "number", "1920")
        + field("oh", "Original height (px)", "", "number", "1080")
        + btns([('data-p="16:9"', "16:9"), ('data-p="9:16"', "9:16"),
                ('data-p="1:1"', "1:1"), ('data-p="4:5"', "4:5")])
        + field("nw", "New width (px)", "", "number")
        + field("nh", "New height (px)", "", "number") + RESULT
        + faq([
            ("What is an aspect ratio?",
             "It is the proportion between the width and the height of a picture or "
             "video, written as two numbers like 16:9. A 1920 x 1080 video has a 16:9 ratio."),
            ("Which aspect ratio should I use for YouTube Shorts, Reels and TikTok?",
             "Vertical videos use 9:16, for example 1080 x 1920 pixels. Normal YouTube "
             "videos use 16:9, and square posts use 1:1."),
            ("Why does my picture look stretched after resizing?",
             "It happens when the new width and height do not follow the original ratio. "
             "Change only one side here and use the calculated value for the other side."),
        ]),
        r"""const g=(a,b)=>b?g(b,a%b):a;
function show(){const w=Math.round(+$('ow').value),h=Math.round(+$('oh').value);if(!w||!h){$('o').textContent='Enter the original width and height.';return}
const d=g(w,h);$('o').textContent='Aspect ratio: '+(w/d)+':'+(h/d)+'\nDecimal: '+(w/h).toFixed(4)+(($('nw').value&&$('nh').value)?'\nNew size: '+$('nw').value+' x '+$('nh').value+' px':'');}
$('ow').oninput=$('oh').oninput=()=>{const w=+$('ow').value,h=+$('oh').value;if(w&&h&&$('nw').value!=='')$('nh').value=Math.round($('nw').value*h/w);show();};
$('nw').oninput=()=>{const w=+$('ow').value,h=+$('oh').value;$('nh').value=(w&&h&&$('nw').value!=='')?Math.round($('nw').value*h/w):'';show();};
$('nh').oninput=()=>{const w=+$('ow').value,h=+$('oh').value;$('nw').value=(w&&h&&$('nh').value!=='')?Math.round($('nh').value*w/h):'';show();};
document.querySelectorAll('[data-p]').forEach(b=>{b.onclick=()=>{const p=b.dataset.p.split(':');$('ow').value=p[0];$('oh').value=p[1];$('ow').oninput();};});
show();"""
    )

    # 2 -------------------------------------------------------------
    tool(
        "video-file-size-calculator",
        "Video File Size Calculator",
        "Estimate video file size from bitrate and duration. Enter video and audio bitrate to see the final size in MB and GB before you export.",
        "Estimate how big a video file will be before you export or upload it. Enter "
        "the video bitrate, the audio bitrate and the length of the video and the "
        "calculator shows the approximate file size in megabytes and gigabytes. This "
        "helps you plan storage space, stay under upload limits and choose export "
        "settings for YouTube, WhatsApp, email or your own website. Try a few "
        "bitrates to see how much size you save." + NOTE,
        "Type the video bitrate and choose Mbps or kbps. Add the audio bitrate "
        "(128 kbps is common) and the duration in minutes. The size updates as you "
        "type. The result is an estimate, because containers and metadata add a "
        "small amount.",
        field("vb", "Video bitrate", "", "number", "8")
        + select("vu", "Video bitrate unit", [("1e6", "Mbps", True), ("1e3", "kbps", False)])
        + field("ab", "Audio bitrate (kbps)", "", "number", "128")
        + field("m", "Duration (minutes)", "", "number", "10") + RESULT
        + faq([
            ("How is video file size calculated?",
             "File size is the total bitrate (video plus audio) multiplied by the "
             "duration, divided by 8 to turn bits into bytes."),
            ("Is the result exact?",
             "No. It is a close estimate. Variable bitrate, the file container and "
             "metadata can change the final size slightly."),
            ("How can I make a video file smaller?",
             "Lower the video bitrate, reduce the resolution or frame rate, or trim "
             "the video. Use the bitrate calculator to find a bitrate for a target size."),
        ]),
        r"""on('vb,vu,ab,m',()=>{const v=(+$('vb').value||0)*(+$('vu').value),a=(+$('ab').value||0)*1e3,s=(+$('m').value||0)*60;
const b=(v+a)*s/8;if(!b){$('o').textContent='';return}
$('o').textContent='Estimated size: '+(b/1e6).toFixed(1)+' MB ('+(b/1e9).toFixed(2)+' GB)\nTotal bitrate: '+((v+a)/1e6).toFixed(2)+' Mbps';});"""
    )

    # 3 -------------------------------------------------------------
    tool(
        "video-bitrate-calculator",
        "Video Bitrate Calculator",
        "Find the video bitrate you need to hit a target file size. Enter the size, duration and audio bitrate to get the result in kbps and Mbps.",
        "Work out the video bitrate you need so your file ends up at a target size. "
        "This is handy when a platform or email has a size limit, for example when "
        "you must keep a video under 500 MB or 25 MB. Enter the size you want, the "
        "length of the video and the audio bitrate, and the calculator returns the "
        "average video bitrate in kbps and Mbps to use in your video editor or "
        "converter." + NOTE,
        "Enter the target file size in MB, the duration in minutes and the audio "
        "bitrate in kbps. The tool subtracts the audio and shows the video bitrate "
        "left. If the number is too small, the video will look poor, so consider a "
        "bigger size or a shorter video.",
        field("sz", "Target file size (MB)", "", "number", "500")
        + field("m", "Duration (minutes)", "", "number", "10")
        + field("ab", "Audio bitrate (kbps)", "", "number", "128") + RESULT
        + faq([
            ("What bitrate should I use for 1080p video?",
             "Many creators use roughly 8 Mbps for 1080p at 30 fps. Higher frame rates "
             "and fast motion need more. Check the recommended settings of your platform."),
            ("Does the audio bitrate matter?",
             "Yes. Audio takes part of the file size, so the video gets what is left "
             "after the audio is removed from the total."),
            ("Why is the result called average bitrate?",
             "Most encoders vary the bitrate during a video. This tool gives the "
             "average you should aim for to reach the target size."),
        ]),
        r"""on('sz,m,ab',()=>{const s=+$('sz').value,t=(+$('m').value||0)*60,a=+$('ab').value||0;if(!s||!t){$('o').textContent='';return}
const k=s*8000/t-a;if(k<=0){$('o').textContent='The size is too small for this duration and audio bitrate. Increase the size or lower the audio bitrate.';return}
$('o').textContent='Video bitrate: '+Math.round(k)+' kbps ('+(k/1000).toFixed(2)+' Mbps)\nAudio bitrate: '+a+' kbps\nTotal: '+Math.round(k+a)+' kbps';});"""
    )

    # 4 -------------------------------------------------------------
    tool(
        "social-media-character-counter",
        "Social Media Character Counter",
        "Count characters for X, Instagram, TikTok, LinkedIn and YouTube. See how many characters are left for every platform as you type.",
        "Check the length of your post before you publish it. Type or paste your "
        "text and the counter shows the number of characters and words, and how many "
        "characters are left for X (Twitter), Instagram, TikTok, LinkedIn and "
        "YouTube titles and descriptions. It is useful for captions, bios, tweets, "
        "video titles and descriptions, so your text is not cut off. Writers, marketers "
        "and creators can use it to shorten long text and keep every platform within its limit." + NOTE,
        "Paste or type your text in the box. Every platform shows used and allowed "
        "characters, and tells you how many are left or by how much you are over. "
        "Emojis and special letters are counted as one character each.",
        field("t", "Your text", "Type or paste your caption, tweet or title", rows=6) + RESULT
        + faq([
            ("What are the character limits?",
             "This tool uses 280 for X, 2200 for Instagram and TikTok captions, 3000 "
             "for LinkedIn posts, 100 for YouTube titles and 5000 for YouTube "
             "descriptions. Platforms can change their limits."),
            ("Do links count the same way everywhere?",
             "Not always. X shortens links and counts them differently, so the real "
             "count on X can be a little different from this simple counter."),
            ("Are spaces and emojis counted?",
             "Yes. Spaces, line breaks and each emoji are counted as characters."),
        ]),
        r"""const L=[['X (Twitter) post',280],['Instagram caption',2200],['TikTok caption',2200],['LinkedIn post',3000],['YouTube title',100],['YouTube description',5000]];
on('t',()=>{const v=$('t').value,n=[...v].length;
$('o').textContent='Characters: '+n+'\nWords: '+((v.trim().match(/\S+/g)||[]).length)+'\n\n'+L.map(([k,m])=>k+': '+n+' / '+m+(n<=m?' ('+(m-n)+' left)':' (over by '+(n-m)+')')).join('\n');});"""
    )

    # 5 -------------------------------------------------------------
    tool(
        "download-time-calculator",
        "Download Time Calculator",
        "Calculate how long a file takes to download from its size and your internet speed in Mbps. Also shows the speed in MB/s.",
        "Find out how long a download will take before you start it. Enter the size "
        "of the file and your internet speed in Mbps, and the calculator shows the "
        "time in days, hours, minutes and seconds. It also converts your speed to "
        "MB/s, which is the number your browser shows while downloading. Use it for "
        "games, movies, software updates, backups and large video files. It also helps you "
        "decide whether to wait, upgrade your plan or download at a quieter time of day." + NOTE,
        "Type the file size and pick MB, GB or TB. Enter your internet speed in "
        "Mbps, as written on your plan or shown by a speed test. The estimated time "
        "appears at once. Real downloads can be slower than the plan speed.",
        field("sz", "File size", "", "number", "1.5")
        + select("su", "Size unit", [("1e6", "MB", False), ("1e9", "GB", True), ("1e12", "TB", False)])
        + field("sp", "Internet speed (Mbps)", "", "number", "50") + RESULT
        + faq([
            ("What is the difference between Mbps and MB/s?",
             "Mbps means megabits per second and MB/s means megabytes per second. "
             "One byte has 8 bits, so divide Mbps by 8 to get MB/s."),
            ("Why is my real download slower than the estimate?",
             "Wi-Fi quality, other devices, the server speed and network traffic can "
             "all reduce the speed you actually get."),
            ("How can I find my internet speed?",
             "Run a speed test on your device, or check the speed of your plan with "
             "your internet provider."),
        ]),
        r"""const fmt=s=>{s=Math.round(s);const d=Math.floor(s/86400),h=Math.floor(s%86400/3600),m=Math.floor(s%3600/60),x=s%60;return [d&&d+' d',(d||h)&&h+' h',(d||h||m)&&m+' min',x+' s'].filter(Boolean).join(' ');};
on('sz,su,sp',()=>{const b=(+$('sz').value||0)*(+$('su').value),r=(+$('sp').value||0)*1e6/8;if(!b||!r){$('o').textContent='';return}
$('o').textContent='Download time: '+fmt(b/r)+'\nSpeed: '+(r/1e6).toFixed(2)+' MB/s\nReal-world speed is usually a bit lower than the plan speed.';});"""
    )

    # 6 -------------------------------------------------------------
    tool(
        "seconds-to-time-converter",
        "Seconds to Time Converter",
        "Convert seconds to hh:mm:ss time and back to seconds. Handy for YouTube timestamps, chapters, video editing and timecodes.",
        "Turn a number of seconds into a readable time like 01:02:05, or turn a time "
        "back into seconds. This is useful when you write YouTube chapters and "
        "timestamps, cut videos, set start times in links, or read durations from "
        "video editors, logs and APIs that show only seconds. Both converters work "
        "instantly in your browser, with no sign-up and no limits. Bookmark the page and "
        "use it every time you edit a video or write a description." + NOTE,
        "To convert seconds, type the number in the first box and read the time "
        "below it. To convert a time to seconds, type it in the second box as "
        "hh:mm:ss or mm:ss. The YouTube style line shows the format used in video "
        "descriptions for chapters.",
        field("s", "Seconds", "", "number", "3725") + RESULT
        + field("t", "Time (hh:mm:ss or mm:ss)", "", "text", "1:02:05")
        + '<div id="o2" class="result" aria-live="polite"></div>'
        + faq([
            ("How do I convert seconds to minutes?",
             "Divide the seconds by 60. For example, 150 seconds is 2 minutes and "
             "30 seconds, or 02:30."),
            ("What format do YouTube chapters use?",
             "Write the time at the start of a line in the description, such as "
             "0:00 Intro or 1:02:05 Main topic. The first chapter must start at 0:00."),
            ("Can I convert more than 24 hours?",
             "Yes. Hours keep counting, so 100000 seconds becomes 27 hours, 46 "
             "minutes and 40 seconds."),
        ]),
        r"""const p=n=>String(n).padStart(2,'0');
on('s',()=>{const v=$('s').value;if(v===''||+v<0){$('o').textContent='';return}const s=Math.floor(+v),h=Math.floor(s/3600),m=Math.floor(s%3600/60),x=s%60;
$('o').textContent='hh:mm:ss: '+p(h)+':'+p(m)+':'+p(x)+'\nYouTube style: '+(h?h+':'+p(m):m)+':'+p(x)+'\n'+h+' hours, '+m+' minutes, '+x+' seconds';});
on('t',()=>{const v=$('t').value.trim();const a=v.split(':').map(Number);if(!v||a.length>3||a.some(n=>isNaN(n)||n<0)){$('o2').textContent=v?'Enter a time like 1:02:05 or 12:30':'';return}
while(a.length<3)a.unshift(0);$('o2').textContent='Total seconds: '+(a[0]*3600+a[1]*60+a[2]);});"""
    )

    # 7 -------------------------------------------------------------
    tool(
        "seo-title-meta-length-checker",
        "SEO Title and Meta Description Length Checker",
        "Check your SEO title and meta description length in characters and estimated pixels, with clear warnings before Google cuts them off.",
        "Check if your page title and meta description will fit in Google search "
        "results. Type or paste both and the tool shows the length in characters and "
        "an estimated width in pixels, with a clear status for each. Titles are "
        "usually safe at about 30 to 60 characters, and meta descriptions at about "
        "120 to 155 characters. Fix the length before you publish to avoid cut-off "
        "text and to improve how your page looks in search." + NOTE,
        "Paste your title in the first box and your meta description in the second. "
        "The counts and status update as you type. Pixel widths are estimates, "
        "because Google measures the real width of the letters, and its snippets "
        "can still change.",
        field("t", "SEO title", "Your page title")
        + field("d", "Meta description", "Your page description", rows=4) + RESULT
        + faq([
            ("How long should an SEO title be?",
             "Aim for about 30 to 60 characters, or under roughly 600 pixels. Longer "
             "titles are often cut off with three dots in search results."),
            ("How long should a meta description be?",
             "Aim for about 120 to 155 characters. Too short wastes space, and too "
             "long gets cut off."),
            ("Will Google always show my meta description?",
             "No. Google sometimes writes its own snippet from your page text, but a "
             "good description still helps people decide to click."),
        ]),
        r"""const cv=document.createElement('canvas').getContext('2d');
const px=(s,f)=>{cv.font=f+' Arial, sans-serif';return Math.round(cv.measureText(s).width);};
on('t,d',()=>{const t=$('t').value,d=$('d').value,tl=[...t].length,dl=[...d].length,tp=px(t,'20px'),dp=px(d,'14px');
const ts=!tl?'-':(tl>60||tp>600)?'Too long (may be cut off)':tl<30?'A bit short':'Good';
const ds=!dl?'-':(dl>155||dp>960)?'Too long (may be cut off)':dl<120?'Too short':'Good';
$('o').textContent='Title: '+tl+' characters, about '+tp+' px\nStatus: '+ts+'\n\nMeta description: '+dl+' characters, about '+dp+' px\nStatus: '+ds;});"""
    )
