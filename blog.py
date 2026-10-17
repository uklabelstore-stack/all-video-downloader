"""
blog.py - /blog section with 9 practical guides for vdownloder.xyz.
Each article links to the matching free tools. Loaded from main.py.
"""
from html import escape
from flask import abort

PUBLISHED = "2026-10-17"

POSTS = [
    {
        "slug": "youtube-thumbnail-size-and-best-practices",
        "title": "YouTube Thumbnail Size: Best Dimensions and Tips",
        "desc": "The recommended YouTube thumbnail size, format and design tips that help "
                "your videos get more clicks.",
        "tools": ["youtube-thumbnail-downloader", "aspect-ratio-calculator"],
        "body": """
<p>A thumbnail is the first thing viewers see, so getting its size and style right matters.
Here is what to use and how to make it work on small phone screens.</p>

<h2>Recommended thumbnail size</h2>
<ul>
<li><strong>Resolution:</strong> 1280 x 720 pixels (16:9 ratio).</li>
<li><strong>Minimum width:</strong> 640 pixels.</li>
<li><strong>Formats:</strong> JPG, PNG or GIF. YouTube Help lists the current maximum
file size, so check it before you upload because limits can change.</li>
</ul>
<p>Keeping the 16:9 ratio prevents black bars or cropping. If your design is a different
size, the <a href="/tools/aspect-ratio-calculator">Aspect Ratio Calculator</a> helps you
resize it without stretching.</p>

<h2>Design tips that work</h2>
<ul>
<li><strong>Keep text short.</strong> Use 3 to 5 big words at most. Most people see
thumbnails on a phone.</li>
<li><strong>Use strong contrast</strong> between the text, the subject and the background.</li>
<li><strong>Show one clear subject,</strong> such as a face or a single object.</li>
<li><strong>Stay consistent.</strong> Similar colors and fonts make your channel easy to recognize.</li>
<li><strong>Do not mislead.</strong> A thumbnail that does not match the video lowers
watch time and viewer trust.</li>
</ul>

<h2>See the thumbnail of any video</h2>
<p>To study how other creators design thumbnails, paste a link into the
<a href="/tools/youtube-thumbnail-downloader">YouTube Thumbnail Downloader</a> to view
all available sizes. Thumbnails belong to their creators, so use them only for reference
unless you have permission.</p>
"""
    },
    {
        "slug": "best-video-bitrate-for-youtube-1080p-4k",
        "title": "Best Video Bitrate for YouTube: 1080p, 1440p and 4K",
        "desc": "YouTube's recommended upload bitrates for 360p to 4K, plus how to pick "
                "the right bitrate for your video.",
        "tools": ["video-bitrate-calculator", "video-file-size-calculator"],
        "body": """
<p>Bitrate decides how much data each second of video uses. Higher bitrate usually means
better quality and a bigger file. These are the video bitrates YouTube recommends for
standard dynamic range (SDR) uploads.</p>

<h2>Standard frame rates (24, 25, 30 fps)</h2>
<ul>
<li>4K (2160p): 35 to 45 Mbps</li>
<li>1440p: 16 Mbps</li>
<li>1080p: 8 Mbps</li>
<li>720p: 5 Mbps</li>
<li>480p: 2.5 Mbps</li>
<li>360p: 1 Mbps</li>
</ul>

<h2>High frame rates (48, 50, 60 fps)</h2>
<ul>
<li>4K (2160p): 53 to 68 Mbps</li>
<li>1440p: 24 Mbps</li>
<li>1080p: 12 Mbps</li>
<li>720p: 7.5 Mbps</li>
<li>480p: 4 Mbps</li>
<li>360p: 1.5 Mbps</li>
</ul>

<h2>Audio</h2>
<p>YouTube recommends 384 kbps for stereo audio. Audio is a small part of the file
compared with video.</p>

<h2>Tips</h2>
<ul>
<li>These figures come from YouTube's recommendations and can be updated, so check the
YouTube Help page when you export.</li>
<li>YouTube re-encodes every upload, so a very high bitrate does not guarantee better
playback quality.</li>
<li>If you must keep a file under a size limit, use the
<a href="/tools/video-bitrate-calculator">Video Bitrate Calculator</a> to find the
bitrate for your length and target size.</li>
<li>To check how large an export will be, use the
<a href="/tools/video-file-size-calculator">Video File Size Calculator</a>.</li>
</ul>
"""
    },
    {
        "slug": "video-aspect-ratios-youtube-shorts-reels-tiktok",
        "title": "Video Aspect Ratios for YouTube, Shorts, Reels and TikTok",
        "desc": "Which video size and aspect ratio to use for YouTube, Shorts, Instagram "
                "Reels, TikTok and Facebook.",
        "tools": ["aspect-ratio-calculator", "social-media-character-counter"],
        "body": """
<p>Using the right aspect ratio keeps your video from being cropped or shown with black
bars. These are the sizes most creators use.</p>

<h2>Common sizes</h2>
<ul>
<li><strong>16:9 landscape (1920 x 1080):</strong> standard YouTube videos and most
websites.</li>
<li><strong>9:16 vertical (1080 x 1920):</strong> YouTube Shorts, Instagram Reels and
TikTok.</li>
<li><strong>1:1 square (1080 x 1080):</strong> works on most social feeds.</li>
<li><strong>4:5 portrait (1080 x 1350):</strong> takes more screen space in feeds than
square video.</li>
</ul>

<h2>Keep important content in the safe area</h2>
<p>Vertical apps place the caption, buttons and profile name on top of the video. Keep
faces and text away from the edges, especially the bottom, so nothing is hidden.</p>

<h2>Resize without stretching</h2>
<p>Enter your current width and height in the
<a href="/tools/aspect-ratio-calculator">Aspect Ratio Calculator</a> to see the simplified
ratio and the matching height for a new width.</p>

<h2>Write the caption too</h2>
<p>Each platform has a caption limit. Check your text with the
<a href="/tools/social-media-character-counter">Social Media Character Counter</a> before
you post. Platforms can change sizes and limits, so confirm important details in the app.</p>
"""
    },
    {
        "slug": "mbps-vs-mbs-download-speed-explained",
        "title": "Mbps vs MB/s: Why Your Download Looks Slower Than Your Plan",
        "desc": "Learn the difference between Mbps and MB/s, how to convert them and how to "
                "estimate download time.",
        "tools": ["mbps-to-mbs-converter", "download-time-calculator",
                  "data-storage-converter"],
        "body": """
<p>Your internet plan says 100 Mbps but your download shows around 12 MB/s. Nothing is
wrong. The two units measure different things.</p>

<h2>Bits and bytes</h2>
<ul>
<li><strong>Mbps</strong> means megabits per second. Internet providers use it.</li>
<li><strong>MB/s</strong> means megabytes per second. Browsers and download managers
usually show this.</li>
<li>One byte is 8 bits, so <strong>MB/s = Mbps / 8</strong>.</li>
</ul>
<p>So 100 Mbps is at most 12.5 MB/s. Try your own numbers in the
<a href="/tools/mbps-to-mbs-converter">Mbps to MB/s Converter</a>.</p>

<h2>Why real speed is lower</h2>
<ul>
<li>Network overhead uses part of the speed.</li>
<li>Weak Wi-Fi or many devices on the same network slow things down.</li>
<li>The server you download from may be limited or busy.</li>
</ul>

<h2>Estimate the download time</h2>
<p>Time in seconds = file size in MB x 8 / speed in Mbps. For example, a 500 MB file at
20 Mbps takes about 200 seconds, or around 3 minutes and 20 seconds. The
<a href="/tools/download-time-calculator">Download Time Calculator</a> does this for you.</p>

<p>If you also need to convert MB to GB, the
<a href="/tools/data-storage-converter">Data Storage Converter</a> shows both decimal and
binary results.</p>
"""
    },
    {
        "slug": "how-to-add-youtube-chapters-and-timestamps",
        "title": "How to Add YouTube Chapters and Timestamp Links",
        "desc": "Step-by-step guide to adding chapters in your YouTube description and "
                "sharing links that start at an exact time.",
        "tools": ["youtube-timestamp-link-generator", "seconds-to-time-converter"],
        "body": """
<p>Chapters split your video into sections so viewers can jump to the part they want. They
also make long videos easier to browse.</p>

<h2>Rules for chapters</h2>
<ul>
<li>The first timestamp must be <strong>0:00</strong>.</li>
<li>Add at least <strong>three</strong> timestamps in ascending order.</li>
<li>Each chapter should be at least <strong>10 seconds</strong> long.</li>
<li>Write them in the video description, one per line.</li>
</ul>

<h2>Example</h2>
<p>Paste this into your description, changing the times and titles:</p>
<p>0:00 Introduction<br>1:15 Setting up<br>4:40 Main steps<br>9:05 Final tips</p>
<p>If you only have seconds from your editor, the
<a href="/tools/seconds-to-time-converter">Seconds to Time Converter</a> turns them into
the right format.</p>

<h2>Share a link that starts at a specific moment</h2>
<p>Add <code>?t=</code> and the number of seconds to a YouTube link, for example
<code>https://youtu.be/VIDEO_ID?t=90</code> starts at 1 minute 30 seconds. The
<a href="/tools/youtube-timestamp-link-generator">YouTube Timestamp Link Generator</a>
builds this link from any video URL and a time such as 1:30.</p>
"""
    },
    {
        "slug": "how-to-estimate-video-file-size",
        "title": "How to Estimate Video File Size Before You Export",
        "desc": "A simple formula to calculate video file size from bitrate and duration, "
                "with a worked example.",
        "tools": ["video-file-size-calculator", "video-bitrate-calculator",
                  "data-storage-converter"],
        "body": """
<p>You can predict the size of a video before you export it. You only need the bitrate and
the length.</p>

<h2>The formula</h2>
<p><strong>Size in bytes = (video bitrate + audio bitrate) x seconds / 8</strong></p>
<p>Use bits per second for both bitrates, then divide by 8 to get bytes.</p>

<h2>Example</h2>
<p>A 10 minute video with 8 Mbps video and 128 kbps audio:</p>
<ul>
<li>Total bitrate = 8,000,000 + 128,000 = 8,128,000 bits per second</li>
<li>Time = 600 seconds</li>
<li>Bits = 8,128,000 x 600 = 4,876,800,000</li>
<li>Bytes = 4,876,800,000 / 8 = 609,600,000, which is about <strong>610 MB</strong></li>
</ul>

<h2>Things to remember</h2>
<ul>
<li>This is an estimate. Variable bitrate and the container format change the final size
a little.</li>
<li>Storage makers count 1 GB as 1000 MB, while many computers show 1024-based sizes. The
<a href="/tools/data-storage-converter">Data Storage Converter</a> shows both.</li>
</ul>

<p>Skip the maths with the
<a href="/tools/video-file-size-calculator">Video File Size Calculator</a>. If you have a
size limit instead, the
<a href="/tools/video-bitrate-calculator">Video Bitrate Calculator</a> works backwards and
gives you the bitrate to use.</p>
"""
    },
    {
        "slug": "create-whatsapp-click-to-chat-link",
        "title": "How to Create a WhatsApp Click-to-Chat Link",
        "desc": "Make a wa.me link that opens a WhatsApp chat with a ready message. "
                "Format, examples and tips.",
        "tools": ["whatsapp-link-generator"],
        "body": """
<p>A click-to-chat link opens a WhatsApp conversation with one tap, without saving the
number first. It is handy for a bio, a website button or a business card.</p>

<h2>The link format</h2>
<p><code>https://wa.me/PHONENUMBER</code></p>
<ul>
<li>Use the full number with the country code.</li>
<li>Do not use plus signs, zeros at the start, spaces or dashes.</li>
</ul>
<p>Example: the Pakistani number 0300 1234567 becomes <code>923001234567</code>, so the
link is <code>https://wa.me/923001234567</code>.</p>

<h2>Add a ready-made message</h2>
<p>Add <code>?text=</code> and the message. Spaces and special characters must be
URL-encoded, so "Hello there" becomes <code>Hello%20there</code>. Example:
<code>https://wa.me/923001234567?text=Hello%20there</code>.</p>

<h2>Make it in seconds</h2>
<p>The <a href="/tools/whatsapp-link-generator">WhatsApp Link Generator</a> builds the link
and does the encoding for you. Test the link on your phone before you share it.</p>

<h2>Use it politely</h2>
<p>Only message people who expect to hear from you. Sending unwanted bulk messages can get
a number blocked.</p>
"""
    },
    {
        "slug": "seo-title-and-meta-description-length",
        "title": "SEO Title and Meta Description Length: What to Use",
        "desc": "How long a page title and meta description should be, and how to write "
                "them so they show properly in Google.",
        "tools": ["seo-title-meta-length-checker", "meta-tag-generator",
                  "keyword-density-checker"],
        "body": """
<p>Your title and meta description are what people read in search results. If they are too
long they get cut off, and if they are vague people will not click.</p>

<h2>Good lengths to aim for</h2>
<ul>
<li><strong>Title:</strong> about 50 to 60 characters.</li>
<li><strong>Meta description:</strong> about 120 to 160 characters.</li>
</ul>
<p>Google actually measures width in pixels, so these numbers are a guide, not a strict
rule. Google can also rewrite your snippet if it thinks another text fits the search
better.</p>

<h2>How to write them</h2>
<ul>
<li>Give every page its own unique title and description.</li>
<li>Put the main topic near the start of the title.</li>
<li>Describe what the visitor will get, in plain words.</li>
<li>Do not repeat the same keyword again and again.</li>
</ul>

<h2>Check and generate</h2>
<p>Paste your text into the
<a href="/tools/seo-title-meta-length-checker">SEO Title and Meta Description Length
Checker</a> to see the length. When you are happy, the
<a href="/tools/meta-tag-generator">Meta Tag Generator</a> creates the HTML tags for the
head of your page. To see which words you repeat most in an article, try the
<a href="/tools/keyword-density-checker">Keyword Density Checker</a>.</p>
"""
    },
    {
        "slug": "downloading-online-videos-responsibly",
        "title": "Downloading Online Videos Responsibly: A Practical Guide",
        "desc": "What to keep in mind before you save an online video: permission, "
                "copyright, platform rules and safer options.",
        "tools": [],
        "body": """
<p>Saving a video for offline use is common, but it is not always allowed. This guide is
general information and not legal advice, because rules differ between countries and
platforms.</p>

<h2>When saving is usually fine</h2>
<ul>
<li>The video is <strong>your own</strong> content.</li>
<li>The owner has <strong>given you permission</strong>.</li>
<li>The video has a license that allows reuse, such as some Creative Commons licenses.
Check the exact terms and give credit if they require it.</li>
</ul>

<h2>When to be careful</h2>
<ul>
<li>Most platforms' terms of service restrict downloading content without their own
download feature.</li>
<li>Copyright usually stays with the creator even when a video is public.</li>
<li>Re-uploading someone else's video, even with credit, can still be a violation.</li>
</ul>

<h2>Safer options</h2>
<ul>
<li>Use the official offline or download option inside the app, when the platform offers it.</li>
<li>Ask the creator for permission, and keep the message as a record.</li>
<li>Use a link or embed instead of copying the file.</li>
</ul>

<h2>Private content</h2>
<p>Do not try to access private or restricted videos. VDownloader only works with public
links, and our <a href="/how-to-download-facebook-video">step-by-step guide</a> explains
how it works. Read our <a href="/terms">Terms of Service</a> as well.</p>
"""
    },
]

POSTS_BY_SLUG = {p["slug"]: p for p in POSTS}


def register(app, render_page, tools_by_slug, site_url):
    @app.route("/blog")
    def blog_index():
        items = "".join(
            '<article style="margin-top:22px"><h2 style="margin-bottom:4px">'
            '<a href="/blog/%s">%s</a></h2><p style="margin-top:0">%s</p></article>'
            % (p["slug"], escape(p["title"]), escape(p["desc"]))
            for p in POSTS
        )
        body = (
            '<section class="content"><h1>VDownloader Blog</h1>'
            "<p>Practical guides for video creators and website owners: sizes, "
            "bitrates, links and SEO basics, each with a free tool you can try.</p>"
            + items + "</section>"
        )
        return render_page(
            "Blog: Guides for Video Creators | VDownloader",
            "Simple guides on video size, bitrate, aspect ratio, YouTube chapters, "
            "WhatsApp links and SEO basics.",
            body, "/blog"
        )

    @app.route("/blog/<slug>")
    def blog_post(slug):
        p = POSTS_BY_SLUG.get(slug)
        if not p:
            abort(404)

        path = "/blog/" + slug

        tools_html = ""
        linked = [tools_by_slug[s] for s in p["tools"] if s in tools_by_slug]
        if linked:
            tools_html = (
                "<h2>Free tools for this guide</h2><div class=\"tool-grid\">"
                + "".join(
                    '<a href="/tools/%s">%s</a>' % (t["slug"], escape(t["h1"]))
                    for t in linked
                )
                + "</div>"
            )

        others = [q for q in POSTS if q["slug"] != slug][:3]
        more = (
            "<h2>More guides</h2><ul>"
            + "".join(
                '<li><a href="/blog/%s">%s</a></li>' % (q["slug"], escape(q["title"]))
                for q in others
            )
            + "</ul>"
        )

        body = (
            '<section class="content"><p><a href="/blog">&larr; All guides</a></p>'
            "<h1>" + escape(p["title"]) + "</h1>"
            '<p class="subtitle">Published ' + PUBLISHED + " by VDownloader</p>"
            + p["body"] + tools_html + more + "</section>"
        )
        schema = [{
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": p["title"],
            "description": p["desc"],
            "datePublished": PUBLISHED,
            "dateModified": PUBLISHED,
            "mainEntityOfPage": site_url + path,
            "author": {"@type": "Organization", "name": "VDownloader"},
            "publisher": {"@type": "Organization", "name": "VDownloader",
                          "url": site_url}
        }]
        return render_page(p["title"] + " | VDownloader", p["desc"], body, path, schema)
