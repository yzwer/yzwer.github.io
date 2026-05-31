/**
 * Text-to-Speech: read article aloud with variable speed
 */
(function () {
    'use strict';

    var syn = window.speechSynthesis;
    var utterance = null;
    var isPlaying = false;
    var isPaused = false;
    var currentRate = 1;

    var btn = document.getElementById('tts-btn');
    var indicator = document.getElementById('tts-indicator');
    var speeds = document.querySelectorAll('.tts-speed');
    var articleContent = document.getElementById('content');

    if (!btn || !articleContent) return;

    // Extract clean text from article content
    function getArticleText() {
        // Clone to avoid modifying the live DOM
        var clone = articleContent.cloneNode(true);
        // Remove UI elements that shouldn't be read
        var removes = clone.querySelectorAll('script, style, pre, code, .highlight, .ic, .wc, .sc, .qc, .post-like, .post-footer, .post-share, .ft, .dv, .table-wrap, button, .toc, .featured-image');
        for (var i = 0; i < removes.length; i++) {
            removes[i].remove();
        }
        var text = clone.textContent || '';
        // Collapse whitespace
        text = text.replace(/\s+/g, ' ').trim();
        return text;
    }

    function findChineseVoice() {
        var voices = syn.getVoices();
        // Prefer zh-CN, fallback to any zh
        var v = voices.find(function (v) { return v.lang === 'zh-CN'; })
              || voices.find(function (v) { return v.lang.startsWith('zh'); });
        return v || null;
    }

    function speak() {
        if (syn.speaking && !isPaused) return;

        if (!isPaused) {
            // Start fresh
            syn.cancel();
            var text = getArticleText();
            if (!text) return;

            utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = currentRate;
            utterance.lang = 'zh-CN';
            var voice = findChineseVoice();
            if (voice) utterance.voice = voice;

            utterance.onstart = function () {
                isPlaying = true;
                isPaused = false;
                updateUI();
            };
            utterance.onend = function () {
                isPlaying = false;
                isPaused = false;
                utterance = null;
                updateUI();
            };
            utterance.onerror = function () {
                isPlaying = false;
                isPaused = false;
                utterance = null;
                updateUI();
            };

            syn.speak(utterance);
        } else {
            // Resume
            syn.resume();
            isPaused = false;
            updateUI();
        }
    }

    function togglePlay() {
        if (isPlaying && !isPaused) {
            // Pause
            syn.pause();
            isPaused = true;
            updateUI();
        } else {
            speak();
        }
    }

    function stop() {
        syn.cancel();
        isPlaying = false;
        isPaused = false;
        utterance = null;
        updateUI();
    }

    function setRate(rate) {
        currentRate = rate;
        if (utterance) {
            utterance.rate = rate;
        }
        // Update active state on speed buttons
        for (var i = 0; i < speeds.length; i++) {
            var val = parseFloat(speeds[i].getAttribute('data-rate'));
            if (val === rate) {
                speeds[i].classList.add('active');
            } else {
                speeds[i].classList.remove('active');
            }
        }
    }

    function updateUI() {
        var icon = btn.querySelector('.tts-icon');
        var label = btn.querySelector('.tts-label');
        if (isPlaying && !isPaused) {
            icon.className = 'tts-icon fas fa-pause';
            label.textContent = '暂停';
            if (indicator) indicator.textContent = '朗读中...';
        } else if (isPaused) {
            icon.className = 'tts-icon fas fa-play';
            label.textContent = '继续';
            if (indicator) indicator.textContent = '已暂停';
        } else {
            icon.className = 'tts-icon fas fa-volume-up';
            label.textContent = '朗读';
            if (indicator) indicator.textContent = '';
        }
    }

    // Event listeners
    btn.addEventListener('click', togglePlay);

    // Stop button
    var stopBtn = document.getElementById('tts-stop');
    if (stopBtn) {
        stopBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            stop();
        });
    }

    // Speed buttons
    for (var i = 0; i < speeds.length; i++) {
        (function (el) {
            el.addEventListener('click', function (e) {
                e.stopPropagation();
                var rate = parseFloat(el.getAttribute('data-rate'));
                setRate(rate);
            });
        })(speeds[i]);
    }

    // Handle voice loading (async)
    if (syn.getVoices().length === 0) {
        syn.addEventListener('voiceschanged', function () {
            findChineseVoice();
        }, { once: true });
    }

    // Set default active speed
    setRate(1);

    // Keyboard shortcut: Escape to stop
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && isPlaying) {
            stop();
        }
    });
})();
