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
  checkAuthStatus();
  handleOAuthCallback();

  // Load library on start
  if (activeTab === 'library') loadLibrary();
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

    progressPrompt.textContent = `"${formData.get('prompt')}"`;
    progressCard.style.display = 'block';
    progressBar.style.width = '5%';
    progressStatus.textContent = 'Queued — Runway is processing your request...';

    startPolling(data.video_id);
  } catch (err) {
    toast(err.message, 'error');
    btn.disabled = false;
    btnText.textContent = '✨ Generate Video';
  }
}

function startPolling(videoId) {
  clearInterval(pollInterval);
  let fakeProgress = 5;

  pollInterval = setInterval(async () => {
    try {
      const res = await fetch(`/api/tasks/${videoId}`);
      const video = await res.json();

      const progressBar = document.getElementById('progress-bar');
      const progressStatus = document.getElementById('progress-status');

      if (video.status === 'completed') {
        clearInterval(pollInterval);
        progressBar.style.width = '100%';
        progressStatus.textContent = 'Complete! Loading your video...';

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
        }, 800);

      } else if (video.status === 'failed') {
        clearInterval(pollInterval);
        progressStatus.textContent = 'Generation failed. Please try again.';
        progressBar.style.background = 'var(--red)';
        const btn = document.getElementById('generate-btn');
        btn.disabled = false;
        document.getElementById('generate-btn-text').textContent = '✨ Generate Video';
        toast('Video generation failed', 'error');

      } else {
        // Still generating — advance fake progress
        const realProgress = (video.progress || 0) * 100;
        fakeProgress = Math.max(fakeProgress + 3, realProgress);
        fakeProgress = Math.min(fakeProgress, 90);
        progressBar.style.width = `${fakeProgress}%`;
        progressStatus.textContent = realProgress > 0
          ? `Processing... ${Math.round(realProgress)}%`
          : 'Runway is generating your video...';
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
