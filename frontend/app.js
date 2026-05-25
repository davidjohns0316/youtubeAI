/* ── Video Ideas Data ────────────────────────────────────────────── */
const VIDEO_IDEAS = [
  {
    rank: 1,
    title: "The $1 Trillion Collapse: What Really Happened",
    category: "Finance",
    catClass: "cat-finance",
    description: "Business collapse documentaries are the highest-earning format on YouTube — combining finance CPM ($12–18 RPM) with drama storytelling watch time. Channels covering FTX, Enron, and Lehman Brothers regularly hit 5M–20M views.",
    rpm: "$12–18",
    views: "5M–20M",
    platform: "YouTube",
    ratio: "1280:768",
    duration: 10,
    prompt: "Dramatic cinematic aerial shot of a towering glass skyscraper in a major financial district at golden hour, red stock ticker numbers cascading down the building's windows like falling rain, the structure slowly developing visible cracks, dust and embers drifting outward, ominous storm clouds gathering behind, photorealistic, epic scale, IMAX quality"
  },
  {
    rank: 2,
    title: "AI Just Replaced 100,000 Jobs — What No One Is Telling You",
    category: "AI News",
    catClass: "cat-ai-news",
    description: "Fear-based AI displacement content is the most-shared format in the AI niche. Gets massive organic shares because viewers send it to coworkers and friends. AI advertisers pay $15–22 RPM — one of the highest CPMs on YouTube.",
    rpm: "$15–22",
    views: "3M–12M",
    platform: "YouTube + TikTok",
    ratio: "1280:768",
    duration: 10,
    prompt: "A vast modern open-plan office at twilight, rows of empty ergonomic chairs and dark monitors, holographic AI interfaces glowing blue above each workstation autonomously processing work, lone human silhouette standing at floor-to-ceiling windows overlooking a city, cinematic wide angle, melancholic atmosphere, blue and violet neon lighting"
  },
  {
    rank: 3,
    title: "The Untold Betrayal That Ended [Athlete]'s Career",
    category: "Sports Drama",
    catClass: "cat-sports",
    description: "Betrayal narratives have the highest watch-through rate of any storytelling format ($10–13 RPM). Sports audiences are obsessive — they rewatch, comment, and share. Works for any major athlete with a controversial storyline.",
    rpm: "$10–13",
    views: "4M–18M",
    platform: "YouTube",
    ratio: "1280:768",
    duration: 10,
    prompt: "Cinematic slow motion shot of a lone athlete in a darkened stadium, single spotlight cutting through smoky air, thousands of empty seats surrounding them, championship trophy lying on its side in the foreground, dramatic shadows and volumetric light beams, film noir color grade, desaturated with deep blue shadows and warm amber highlights"
  },
  {
    rank: 4,
    title: "5 Money Rules the Rich Never Talk About",
    category: "Finance",
    catClass: "cat-finance",
    description: "Evergreen aspirational finance content. The 'secret knowledge' hook drives enormous click-through rates. Consistently generates 2M–8M views across channels of all sizes. Perfect for TikTok short-form and YouTube long-form.",
    rpm: "$10–15",
    views: "2M–8M",
    platform: "YouTube + TikTok",
    ratio: "768:1280",
    duration: 5,
    prompt: "Luxurious penthouse living room at night overlooking a glittering city skyline, a mahogany desk covered in financial documents and a single glowing laptop, stacks of banded currency subtly visible, warm amber lamp light casting dramatic shadows, ultra-wealthy aesthetic, cinematic depth of field, photorealistic"
  },
  {
    rank: 5,
    title: "What Happens to Your Money When the Economy Crashes",
    category: "Finance",
    catClass: "cat-finance",
    description: "Economic anxiety content spikes during any market volatility and stays evergreen. High search volume year-round. Finance advertisers (banks, brokerages) pay premium to reach this worried audience.",
    rpm: "$11–16",
    views: "3M–10M",
    platform: "YouTube",
    ratio: "1280:768",
    duration: 10,
    prompt: "Aerial cinematic shot flying over a major city at dusk, buildings flickering as power cuts in and out, red stock market graphs projected massive across skyscraper facades, crowds of tiny figures rushing through streets below, heavy storm clouds crackling with lightning rolling in from the horizon, dramatic and ominous, Blade Runner aesthetic"
  },
  {
    rank: 6,
    title: "I Tested Every Major AI Tool for 30 Days — Honest Results",
    category: "AI News",
    catClass: "cat-ai-news",
    description: "Comparison and review formats dominate AI search traffic. Audiences trust 'honest test' framing. AI companies actively bid to advertise on this content, pushing CPMs to $20+. Evergreen as new tools launch constantly.",
    rpm: "$18–25",
    views: "1M–6M",
    platform: "YouTube",
    ratio: "1280:768",
    duration: 10,
    prompt: "Futuristic minimalist workspace surrounded by floating holographic screens each displaying a different AI tool interface generating art, code, and video in real time, soft blue and white ambient lighting, a single human hand reaching toward one glowing screen, clean and aspirational tech aesthetic, 8K photorealistic"
  },
  {
    rank: 7,
    title: "The Fix That Shocked the World: Sport's Biggest Scandal",
    category: "Sports Drama",
    catClass: "cat-sports",
    description: "Match-fixing and sports scandal content gets massive spikes when stories break and long-tail views for years after. Comments sections explode, which signals the algorithm to push the video hard. $10–13 RPM with massive volume.",
    rpm: "$10–13",
    views: "5M–25M",
    platform: "YouTube",
    ratio: "1280:768",
    duration: 10,
    prompt: "Dramatic film noir style stadium scene at night, floodlights casting harsh shadows on an empty pitch, a shadowy figure in a referee uniform standing alone at center field, newspaper headlines swirling around them in the wind, dark and ominous atmosphere, high contrast black and deep blue color grade with flickers of harsh white light"
  },
  {
    rank: 8,
    title: "AGI Is 18 Months Away — The Timeline They're Hiding",
    category: "AI News",
    catClass: "cat-ai-news",
    description: "Existential AI content drives the highest engagement rates in the AI niche — comment sections go viral on their own. Conspiracy-adjacent framing massively boosts shares. Works in 60-second TikTok format and 15-minute YouTube deep-dives.",
    rpm: "$14–20",
    views: "2M–10M",
    platform: "YouTube + TikTok",
    ratio: "1280:768",
    duration: 10,
    prompt: "A vast cosmic neural network visualization, billions of glowing nodes and synaptic connections spreading across a deep space background, slowly transforming from simple scattered points into an impossibly dense and complex web of pulsing golden light, camera slowly pulling back to reveal the infinite scale, ethereal and awe-inspiring, 8K"
  },
  {
    rank: 9,
    title: "From Broke to $50M: The Rise No One Believed In",
    category: "Sports Drama",
    catClass: "cat-sports",
    description: "Underdog athlete success stories are the most re-watched storytelling format on YouTube. Emotional arc keeps viewers through to the end. Works perfectly as a 12–18 minute YouTube documentary with AI-generated cinematic visuals.",
    rpm: "$9–12",
    views: "6M–30M",
    platform: "YouTube",
    ratio: "1280:768",
    duration: 10,
    prompt: "Cinematic time-lapse montage feel — starting with a dark rain-soaked empty basketball court in a rough neighborhood at night, transitioning to a massive floodlit arena packed with roaring fans, confetti falling in slow motion, a lone athlete raising a championship trophy above their head in triumph, warm golden light flooding the scene, emotional and epic"
  },
  {
    rank: 10,
    title: "The Secret Way the Ultra-Rich Pay Zero Taxes (Legally)",
    category: "Finance",
    catClass: "cat-finance",
    description: "Controversial finance content about wealth inequality goes massively viral. The 'legally' qualifier makes it safe for YouTube monetization while keeping the provocative hook. Finance + controversy = algorithm gold.",
    rpm: "$13–19",
    views: "4M–15M",
    platform: "YouTube + TikTok",
    ratio: "768:1280",
    duration: 10,
    prompt: "Opulent private bank vault interior, gleaming gold and polished marble, stacks of gold bars and banded currency behind reinforced glass, a single suited figure reviewing documents at a grand desk, dramatic chiaroscuro lighting with a single beam of light from above, cinematic and secretive atmosphere, ultra-realistic"
  },
];

/* ── State ───────────────────────────────────────────────────────── */
let activeTab = 'generate';
let selectedVideoId = null;
let pollInterval = null;
let authStatus = { youtube: false, tiktok: false, runway: false };

/* ── Init ────────────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  setupNavigation();
  setupGenerateForm();
  setupImageDrop();
  setupAdvancedToggle();
  setupPublishPanel();
  setupPlatformTabs();
  setupIdeasTab();
  checkAuthStatus();
  handleOAuthCallback();
});

/* ── Navigation ──────────────────────────────────────────────────── */
function setupNavigation() {
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => switchTab(btn.dataset.tab));
  });
}

function switchTab(tabName) {
  activeTab = tabName;
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.toggle('active', b.dataset.tab === tabName));
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.id === `tab-${tabName}`));
  if (tabName === 'library') loadLibrary();
  if (tabName === 'settings') checkAuthStatus();
}

/* ── Ideas Tab ───────────────────────────────────────────────────── */
function setupIdeasTab() {
  renderIdeas('all');

  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderIdeas(btn.dataset.filter);
    });
  });
}

function renderIdeas(filter) {
  const list = document.getElementById('ideas-list');
  list.innerHTML = '';

  const filtered = filter === 'all'
    ? VIDEO_IDEAS
    : VIDEO_IDEAS.filter(i => i.category === filter);

  filtered.forEach((idea, idx) => {
    const card = document.createElement('div');
    card.className = 'idea-card';
    card.dataset.category = idea.category;

    const ratioLabel = idea.ratio === '768:1280' ? '9:16 Portrait' : '16:9 Landscape';
    const platformIcon = idea.platform.includes('TikTok') && idea.platform.includes('YouTube') ? '▶ + ♪' :
                         idea.platform.includes('TikTok') ? '♪ TikTok' : '▶ YouTube';

    card.innerHTML = `
      <div class="idea-rank">${idea.rank}</div>
      <div class="idea-body">
        <div class="idea-top">
          <span class="idea-title">${escHtml(idea.title)}</span>
          <span class="idea-category ${idea.catClass}">${idea.category}</span>
        </div>
        <div class="idea-desc">${escHtml(idea.description)}</div>
        <div class="idea-stats">
          <span class="idea-stat">💰 <strong>${idea.rpm} RPM</strong></span>
          <span class="idea-stat">👁 <strong>${idea.views} views</strong></span>
          <span class="idea-stat">📐 <strong>${ratioLabel}</strong></span>
          <span class="idea-stat">📱 <strong>${platformIcon}</strong></span>
        </div>
        <div class="idea-prompt-preview" id="prompt-preview-${idx}">
          <strong style="color:var(--text2);font-style:normal">Runway prompt:</strong><br>${escHtml(idea.prompt)}
        </div>
      </div>
      <div class="idea-actions">
        <button class="btn-use-prompt" onclick="useIdeaPrompt(${VIDEO_IDEAS.indexOf(idea)})">
          ✨ Use This Prompt
        </button>
        <button class="btn-preview-prompt" onclick="togglePromptPreview('prompt-preview-${idx}', this)">
          Preview Prompt
        </button>
      </div>
    `;

    list.appendChild(card);
  });
}

function togglePromptPreview(previewId, btn) {
  const el = document.getElementById(previewId);
  const open = el.classList.toggle('open');
  btn.textContent = open ? 'Hide Prompt' : 'Preview Prompt';
}

function useIdeaPrompt(ideaIndex) {
  const idea = VIDEO_IDEAS[ideaIndex];

  // Switch to Generate tab
  switchTab('generate');

  // Fill in the form
  document.getElementById('prompt').value = idea.prompt;
  document.getElementById('ratio').value = idea.ratio;
  document.getElementById('duration').value = idea.duration;

  // Highlight the prompt field
  const promptEl = document.getElementById('prompt');
  promptEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
  promptEl.focus();
  promptEl.style.borderColor = 'var(--accent)';
  promptEl.style.boxShadow = '0 0 0 3px var(--accent-glow)';
  setTimeout(() => {
    promptEl.style.borderColor = '';
    promptEl.style.boxShadow = '';
  }, 2000);

  toast(`Loaded: "${idea.title}"`, 'success');
}

window.useIdeaPrompt = useIdeaPrompt;
window.togglePromptPreview = togglePromptPreview;

/* ── OAuth callback handler ──────────────────────────────────────── */
function handleOAuthCallback() {
  const params = new URLSearchParams(window.location.search);
  if (params.get('yt') === 'connected') {
    toast('YouTube connected successfully!', 'success');
    switchTab('settings');
    history.replaceState({}, '', '/');
  } else if (params.get('yt') === 'error') {
    toast(`YouTube auth failed: ${params.get('msg') || 'unknown error'}`, 'error');
    history.replaceState({}, '', '/');
  }
  if (params.get('tt') === 'connected') {
    toast('TikTok connected successfully!', 'success');
    switchTab('settings');
    history.replaceState({}, '', '/');
  } else if (params.get('tt') === 'error') {
    toast(`TikTok auth failed: ${params.get('msg') || 'unknown error'}`, 'error');
    history.replaceState({}, '', '/');
  }
}

/* ── Auth Status ─────────────────────────────────────────────────── */
async function checkAuthStatus() {
  await Promise.all([checkRunwayStatus(), checkYouTubeStatus(), checkTikTokStatus()]);
}

async function checkRunwayStatus() {
  try {
    const res = await fetch('/health');
    // Runway status is inferred from whether API key is set; we check via a lightweight endpoint
    // We'll just mark it based on the generate endpoint's 400 vs non-400
    setStatus('runway', 'configured', true); // optimistic — validated on generate
  } catch {
    setStatus('runway', 'unavailable', false);
  }
}

async function checkYouTubeStatus() {
  try {
    const res = await fetch('/api/auth/youtube/status');
    const data = await res.json();
    authStatus.youtube = data.connected;
    setStatus('yt', data.connected ? 'Connected' : 'Not connected', data.connected);
    document.getElementById('yt-connect-btn').style.display = data.connected ? 'none' : '';
    document.getElementById('yt-disconnect-btn').style.display = data.connected ? '' : 'none';
  } catch {
    setStatus('yt', 'Error checking status', false);
  }
}

async function checkTikTokStatus() {
  try {
    const res = await fetch('/api/auth/tiktok/status');
    const data = await res.json();
    authStatus.tiktok = data.connected;
    setStatus('tt', data.connected ? 'Connected' : 'Not connected', data.connected);
    document.getElementById('tt-connect-btn').style.display = data.connected ? 'none' : '';
    document.getElementById('tt-disconnect-btn').style.display = data.connected ? '' : 'none';
  } catch {
    setStatus('tt', 'Error checking status', false);
  }
}

function setStatus(prefix, text, ok) {
  const dot = document.getElementById(`${prefix}-dot`);
  const label = document.getElementById(`${prefix}-status`);
  if (!dot || !label) return;
  dot.className = 'status-dot ' + (ok ? 'green' : 'red');
  label.textContent = text;
}

async function disconnectYouTube() {
  if (!confirm('Disconnect YouTube?')) return;
  await fetch('/api/auth/youtube/disconnect', { method: 'POST' });
  authStatus.youtube = false;
  checkYouTubeStatus();
  toast('YouTube disconnected', 'info');
}

async function disconnectTikTok() {
  if (!confirm('Disconnect TikTok?')) return;
  await fetch('/api/auth/tiktok/disconnect', { method: 'POST' });
  authStatus.tiktok = false;
  checkTikTokStatus();
  toast('TikTok disconnected', 'info');
}

// Expose for inline onclick
window.disconnectYouTube = disconnectYouTube;
window.disconnectTikTok = disconnectTikTok;
window.switchTab = switchTab;

/* ── Image Drop ──────────────────────────────────────────────────── */
function setupImageDrop() {
  const drop = document.getElementById('image-drop');
  const input = document.getElementById('image-input');
  const preview = document.getElementById('file-preview');
  const previewImg = document.getElementById('preview-img');
  const dropUi = document.getElementById('file-drop-ui');
  const removeBtn = document.getElementById('remove-image');

  input.addEventListener('change', () => showPreview(input.files[0]));
  removeBtn.addEventListener('click', e => { e.stopPropagation(); clearImage(); });

  drop.addEventListener('dragover', e => { e.preventDefault(); drop.classList.add('drag-over'); });
  drop.addEventListener('dragleave', () => drop.classList.remove('drag-over'));
  drop.addEventListener('drop', e => {
    e.preventDefault();
    drop.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      input.files = e.dataTransfer.files;
      showPreview(file);
    }
  });

  function showPreview(file) {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = ev => {
      previewImg.src = ev.target.result;
      dropUi.style.display = 'none';
      preview.style.display = 'block';
      // File input must remain accessible for FormData
    };
    reader.readAsDataURL(file);
  }

  function clearImage() {
    input.value = '';
    previewImg.src = '';
    preview.style.display = 'none';
    dropUi.style.display = 'flex';
  }
}

/* ── Advanced Toggle ─────────────────────────────────────────────── */
function setupAdvancedToggle() {
  const btn = document.getElementById('advanced-toggle');
  const body = document.getElementById('advanced-body');
  const chevron = btn.querySelector('.chevron');
  btn.addEventListener('click', () => {
    const open = body.style.display !== 'none';
    body.style.display = open ? 'none' : 'block';
    chevron.classList.toggle('open', !open);
  });
}

/* ── Generate Form ───────────────────────────────────────────────── */
function setupGenerateForm() {
  const form = document.getElementById('generate-form');
  form.addEventListener('submit', async e => {
    e.preventDefault();
    await startGeneration(form);
  });

  // Duration warning
  const durationSel = document.getElementById('duration');
  const warningEl = document.createElement('p');
  warningEl.className = 'duration-warning';
  warningEl.style.cssText = 'font-size:12px;color:var(--yellow);margin-top:6px;display:none';
  durationSel.parentElement.appendChild(warningEl);

  durationSel.addEventListener('change', () => {
    const val = parseInt(durationSel.value);
    const clips = Math.ceil(val / 10);
    if (clips > 1) {
      warningEl.style.display = 'block';
      warningEl.textContent = `⚠ Uses ${clips} Runway API calls (~${clips * 1}–${clips * 3} min total)`;
    } else {
      warningEl.style.display = 'none';
    }
  });
}

async function startGeneration(form) {
  const btn = document.getElementById('generate-btn');
  const btnText = document.getElementById('generate-btn-text');
  const progressCard = document.getElementById('progress-card');
  const progressBar = document.getElementById('progress-bar');
  const progressStatus = document.getElementById('progress-status');
  const progressPrompt = document.getElementById('progress-prompt');

  btn.disabled = true;
  btnText.textContent = 'Generating...';

  const formData = new FormData(form);
  const seedVal = formData.get('seed');
  if (!seedVal) formData.delete('seed');

  // Remove image field if empty
  const imageInput = document.getElementById('image-input');
  if (!imageInput.files.length) formData.delete('image');

  try {
    const res = await fetch('/api/generate', { method: 'POST', body: formData });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Generation failed');
    }
    const data = await res.json();
    const clipsTotal = data.clips_total || 1;

    progressPrompt.textContent = `"${formData.get('prompt')}"`;
    progressCard.style.display = 'block';
    progressBar.style.width = '3%';
    progressStatus.textContent = clipsTotal > 1
      ? `Starting clip 1 of ${clipsTotal}...`
      : 'Queued — Runway is processing your request...';
    document.getElementById('progress-note').textContent = clipsTotal > 1
      ? `${clipsTotal} clips × 1–3 min each — clips auto-stitch when done`
      : 'Gen-3 Alpha Turbo takes 1–3 min per clip';

    startPolling(data.video_id, clipsTotal);
  } catch (err) {
    toast(err.message, 'error');
    btn.disabled = false;
    btnText.textContent = '✨ Generate Video';
  }
}

function startPolling(videoId, clipsTotal) {
  clearInterval(pollInterval);

  pollInterval = setInterval(async () => {
    try {
      const res = await fetch(`/api/tasks/${videoId}`);
      const video = await res.json();

      const progressBar = document.getElementById('progress-bar');
      const progressStatus = document.getElementById('progress-status');
      const progressNote = document.getElementById('progress-note');

      if (video.status === 'completed') {
        clearInterval(pollInterval);
        progressBar.style.width = '100%';
        progressStatus.textContent = clipsTotal > 1 ? 'Stitching clips into final video...' : 'Complete! Loading your video...';

        setTimeout(() => {
          document.getElementById('progress-card').style.display = 'none';
          const btn = document.getElementById('generate-btn');
          btn.disabled = false;
          document.getElementById('generate-btn-text').textContent = '✨ Generate Video';
          document.getElementById('generate-form').reset();
          document.getElementById('file-drop-ui').style.display = 'flex';
          document.getElementById('file-preview').style.display = 'none';
          toast('Video generated! Opening library...', 'success');
          switchTab('library');
        }, 1000);

      } else if (video.status === 'failed') {
        clearInterval(pollInterval);
        progressStatus.textContent = video.error || 'Generation failed. Please try again.';
        progressBar.style.background = 'var(--red)';
        const btn = document.getElementById('generate-btn');
        btn.disabled = false;
        document.getElementById('generate-btn-text').textContent = '✨ Generate Video';
        toast('Video generation failed', 'error');

      } else {
        // Multi-clip: use clips_done / clips_total for real progress
        const clipsTotal = video.clips_total || 1;
        const clipsDone = video.clips_done || 0;
        const realPct = clipsTotal > 1
          ? (clipsDone / clipsTotal) * 100
          : (video.progress || 0) * 100;

        // Nudge forward slightly so bar never looks stuck
        const displayPct = Math.min(realPct + 2, 95);
        progressBar.style.width = `${displayPct}%`;

        // Status label
        progressStatus.textContent = video.status_label ||
          (clipsTotal > 1
            ? `Generating clip ${clipsDone + 1} of ${clipsTotal}...`
            : 'Runway is generating your video...');

        // Update note for multi-clip
        if (clipsTotal > 1) {
          progressNote.textContent = `${clipsTotal} clips × 1–3 min each — clips auto-stitch when done`;
        }
      }
    } catch {
      // Network hiccup — keep polling
    }
  }, 5000);
}

/* ── Library ─────────────────────────────────────────────────────── */
async function loadLibrary() {
  const grid = document.getElementById('library-grid');
  const empty = document.getElementById('library-empty');

  try {
    const res = await fetch('/api/videos');
    const videos = await res.json();

    // Clear existing cards (keep empty state node)
    grid.querySelectorAll('.video-card').forEach(el => el.remove());

    if (!videos.length) {
      empty.style.display = 'flex';
      return;
    }

    empty.style.display = 'none';

    videos.forEach(video => {
      const card = buildVideoCard(video);
      grid.appendChild(card);
    });
  } catch {
    toast('Failed to load library', 'error');
  }
}

function buildVideoCard(video) {
  const card = document.createElement('div');
  card.className = 'video-card';
  card.dataset.videoId = video.id;

  const statusBadge = {
    generating: '<span class="badge badge-generating">Generating</span>',
    completed: '<span class="badge badge-completed">Ready</span>',
    failed: '<span class="badge badge-failed">Failed</span>',
  }[video.status] || '';

  const ytBadge = video.youtube_url ? '<span class="badge badge-yt">YT</span>' : '';
  const ttBadge = video.tiktok_publish_id ? '<span class="badge badge-tt">TT</span>' : '';

  const date = new Date(video.created_at).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit',
  });

  const thumbContent = video.status === 'completed' && video.filename
    ? `<video src="/api/videos/${video.filename}" muted preload="metadata"></video>
       <div class="thumb-overlay"><div class="play-icon">▶</div></div>`
    : video.status === 'generating'
    ? '<div style="color:var(--text3);font-size:13px">Generating...</div>'
    : '<div style="font-size:32px">🎬</div>';

  card.innerHTML = `
    <div class="video-card-thumb">${thumbContent}</div>
    <div class="video-card-info">
      <div class="video-card-prompt">${escHtml(video.prompt)}</div>
      <div class="video-card-meta">
        <div class="video-card-badges">${statusBadge}${ytBadge}${ttBadge}</div>
        <span>${date}</span>
      </div>
    </div>
    <div class="video-card-actions">
      ${video.status === 'completed'
        ? `<button class="btn btn-primary" onclick="openPublishPanel('${video.id}')">Publish</button>`
        : ''}
      <button class="btn btn-danger" onclick="deleteVideo('${video.id}', event)" style="flex:0;padding:7px 12px">🗑</button>
    </div>
  `;

  if (video.status === 'completed') {
    card.addEventListener('click', e => {
      if (e.target.tagName === 'BUTTON') return;
      openPublishPanel(video.id);
    });
  }

  return card;
}

function escHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

async function deleteVideo(videoId, e) {
  e.stopPropagation();
  if (!confirm('Delete this video?')) return;
  try {
    await fetch(`/api/videos/${videoId}`, { method: 'DELETE' });
    toast('Video deleted', 'info');
    loadLibrary();
    if (selectedVideoId === videoId) closePublishPanel();
  } catch {
    toast('Delete failed', 'error');
  }
}

window.deleteVideo = deleteVideo;
window.openPublishPanel = openPublishPanel;

/* ── Publish Panel ───────────────────────────────────────────────── */
function setupPublishPanel() {
  document.getElementById('close-publish').addEventListener('click', closePublishPanel);
  document.getElementById('publish-overlay').addEventListener('click', e => {
    if (e.target === e.currentTarget) closePublishPanel();
  });
  document.getElementById('publish-yt-btn').addEventListener('click', publishToYouTube);
  document.getElementById('publish-tt-btn').addEventListener('click', publishToTikTok);
}

async function openPublishPanel(videoId) {
  selectedVideoId = videoId;

  const res = await fetch('/api/videos');
  const videos = await res.json();
  const video = videos.find(v => v.id === videoId);
  if (!video || !video.filename) return;

  document.getElementById('publish-preview').src = `/api/videos/${video.filename}`;
  document.getElementById('pub-title').value = video.prompt.slice(0, 100);
  document.getElementById('pub-description').value = `AI-generated video\nPrompt: ${video.prompt}`;

  // Auth warnings
  document.getElementById('yt-auth-warning').style.display = authStatus.youtube ? 'none' : 'flex';
  document.getElementById('tt-auth-warning').style.display = authStatus.tiktok ? 'none' : 'flex';

  document.getElementById('publish-overlay').style.display = 'flex';
}

function closePublishPanel() {
  document.getElementById('publish-overlay').style.display = 'none';
  const vid = document.getElementById('publish-preview');
  vid.pause();
  vid.src = '';
  selectedVideoId = null;
}

async function publishToYouTube() {
  if (!selectedVideoId) return;
  const btn = document.getElementById('publish-yt-btn');
  btn.disabled = true;
  btn.textContent = 'Uploading...';

  const title = document.getElementById('pub-title').value.trim() || 'AI Generated Video';
  const description = document.getElementById('pub-description').value.trim();
  const tagsRaw = document.getElementById('pub-yt-tags').value;
  const tags = tagsRaw.split(',').map(t => t.trim()).filter(Boolean);
  const privacy = document.getElementById('pub-yt-privacy').value;
  const categoryId = document.getElementById('pub-yt-category').value;

  try {
    const res = await fetch('/api/publish/youtube', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ video_id: selectedVideoId, title, description, tags, privacy, category_id: categoryId }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail);
    }
    const data = await res.json();
    toast(`Uploaded to YouTube! ${data.url}`, 'success');
    closePublishPanel();
    loadLibrary();
  } catch (err) {
    toast(`YouTube upload failed: ${err.message}`, 'error');
  } finally {
    btn.disabled = false;
    btn.textContent = 'Upload to YouTube';
  }
}

async function publishToTikTok() {
  if (!selectedVideoId) return;
  const btn = document.getElementById('publish-tt-btn');
  btn.disabled = true;
  btn.textContent = 'Uploading...';

  const title = document.getElementById('pub-title').value.trim() || 'AI Generated Video';
  const hashtagsRaw = document.getElementById('pub-tt-hashtags').value;
  const hashtags = hashtagsRaw.split(',').map(t => t.trim()).filter(Boolean);
  const privacy = document.getElementById('pub-tt-privacy').value;

  try {
    const res = await fetch('/api/publish/tiktok', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ video_id: selectedVideoId, title, hashtags, privacy }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail);
    }
    toast('Submitted to TikTok for publishing!', 'success');
    closePublishPanel();
    loadLibrary();
  } catch (err) {
    toast(`TikTok upload failed: ${err.message}`, 'error');
  } finally {
    btn.disabled = false;
    btn.textContent = 'Upload to TikTok';
  }
}

/* ── Platform Tab Switching ──────────────────────────────────────── */
function setupPlatformTabs() {
  document.querySelectorAll('.platform-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.platform-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const platform = tab.dataset.platform;
      document.getElementById('youtube-fields').style.display = platform === 'youtube' ? 'flex' : 'none';
      document.getElementById('tiktok-fields').style.display = platform === 'tiktok' ? 'flex' : 'none';
    });
  });
}

/* ── Toasts ──────────────────────────────────────────────────────── */
function toast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  const el = document.createElement('div');
  el.className = `toast toast-${type}`;

  const icon = { success: '✓', error: '✕', info: 'ℹ' }[type] || 'ℹ';
  el.innerHTML = `<span style="font-weight:700">${icon}</span><span>${escHtml(message)}</span>`;

  container.appendChild(el);

  setTimeout(() => {
    el.classList.add('fade-out');
    el.addEventListener('animationend', () => el.remove());
  }, type === 'error' ? 6000 : 4000);
}
