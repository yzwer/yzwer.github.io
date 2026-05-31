/**
 * Interaction features: anonymous likes, WeChat QR share
 * Uses LeanCloud REST API (same app as Valine)
 */
(function () {
    'use strict';

    const config = window.config && window.config.like;
    if (!config) return;

    const appId = config.appId;
    const appKey = config.appKey;
    // Derive API base from appId (remove region suffix after '-', use first 8 chars)
    var appPrefix = appId.split('-')[0];
    if (appPrefix.length > 8) appPrefix = appPrefix.slice(0, 8);
    var apiBase = config.serverURLs;
    if (!apiBase) {
        // Try TAB (lncldapi.com) first, fall back to legacy (lncld.com)
        apiBase = 'https://' + appPrefix + '.api.lncldapi.com';
    }
    const headers = {
        'X-LC-Id': appId,
        'X-LC-Key': appKey,
        'Content-Type': 'application/json'
    };

    const likeBtn = document.getElementById('like-btn');
    const likeIcon = document.getElementById('like-icon');
    const likeCount = document.getElementById('like-count');
    const likeText = document.getElementById('like-text');
    const url = document.getElementById('post-like')
        ? document.getElementById('post-like').getAttribute('data-url')
        : null;

    if (!likeBtn || !url) return;

    // ---- Like feature ----

    function api(path, method, body) {
        return fetch(apiBase + path, {
            method: method || 'GET',
            headers: headers,
            body: body ? JSON.stringify(body) : undefined
        }).then(function (r) { return r.json(); });
    }

    // Load current like count
    var currentObjId = null;

    function loadCount() {
        var q = encodeURIComponent(JSON.stringify({ url: url }));
        api('/1.1/classes/LikeCounter?where=' + q).then(function (data) {
            if (data.results && data.results.length > 0) {
                var obj = data.results[0];
                currentObjId = obj.objectId;
                likeCount.textContent = obj.count || 0;
                // Check if already liked (from localStorage)
                var liked = localStorage.getItem('liked_' + btoa(url));
                if (liked) {
                    setLikedState(true, false);
                }
            }
        }).catch(function (err) {
            console.warn('Failed to load like count:', err);
        });
    }

    function setLikedState(liked, animate) {
        if (liked) {
            likeIcon.className = 'like-icon fas fa-heart liked';
            likeText.textContent = '已赞';
            likeBtn.disabled = true;
        } else {
            likeIcon.className = 'like-icon far fa-heart';
            likeText.textContent = '赞';
            likeBtn.disabled = false;
        }
    }

    function handleLike() {
        if (likeBtn.disabled) return;

        // Check localStorage first
        var storageKey = 'liked_' + btoa(url);
        if (localStorage.getItem(storageKey)) {
            setLikedState(true, false);
            return;
        }

        likeBtn.disabled = true;
        likeText.textContent = '...';

        // Get client IP via ipify
        var clientIp = '';
        fetch('https://api.ipify.org?format=json', { mode: 'cors' })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                clientIp = data.ip || '';
            })
            .catch(function () {
                // IP detection failed, proceed without it
            })
            .then(function () {
                return doLike(clientIp);
            })
            .catch(function (err) {
                console.warn('Like failed:', err);
                likeBtn.disabled = false;
                likeText.textContent = '赞';
            });
    }

    function doLike(clientIp) {
        if (currentObjId) {
            // Update existing record: atomically increment count and add IP
            var updateBody = {
                count: { '__op': 'Increment', 'amount': 1 }
            };
            if (clientIp) {
                updateBody.ips = { '__op': 'AddUnique', 'objects': [clientIp] };
            }
            return api('/1.1/classes/LikeCounter/' + currentObjId, 'PUT', updateBody)
                .then(function (data) {
                    var newCount = (typeof data.count === 'number') ? data.count : parseInt(likeCount.textContent, 10) + 1;
                    likeCount.textContent = newCount;
                    setLikedState(true, true);
                    localStorage.setItem('liked_' + btoa(url), '1');
                });
        } else {
            // Create new record
            var createBody = {
                url: url,
                count: 1,
                ips: clientIp ? [clientIp] : []
            };
            return api('/1.1/classes/LikeCounter', 'POST', createBody)
                .then(function (data) {
                    currentObjId = data.objectId;
                    likeCount.textContent = '1';
                    setLikedState(true, true);
                    localStorage.setItem('liked_' + btoa(url), '1');
                });
        }
    }

    loadCount();
    likeBtn.addEventListener('click', handleLike);

    // ---- WeChat QR share modal ----

    window.showWechatModal = function (postUrl) {
        var modal = document.getElementById('wechat-modal');
        var qrDiv = document.getElementById('wechat-qr');
        if (!modal || !qrDiv) return;
        var fullUrl = 'https://yzwer.github.io' + postUrl;
        qrDiv.innerHTML = '<img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=' + encodeURIComponent(fullUrl) + '" alt="QR Code" style="width:200px;height:200px;">';
        modal.style.display = 'flex';
    };

    window.closeWechatModal = function (event) {
        if (event && event.target !== event.currentTarget) return;
        var modal = document.getElementById('wechat-modal');
        if (modal) modal.style.display = 'none';
    };

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            var modal = document.getElementById('wechat-modal');
            if (modal) modal.style.display = 'none';
        }
    });
})();
