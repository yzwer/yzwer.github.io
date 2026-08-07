# YouTube Pipeline Run: v3Evq0LTnuo

**Date:** 2026-08-07
**Video:** v3Evq0LTnuo
**Title:** 境外保单征税来了：香港保险的末日，还是公平税负的开始？
**Pipeline version:** v2.4

## Status: COMPLETE

## Steps Completed

1. **Pipeline download:** SOCKS5 x3 failed (rc=1), cached f140.m4a already existed (12.35MB)
2. **Audio extract:** ffmpeg m4a -> wav (25MB, 13:20, pcm_s16le, 16000Hz mono, speed=897x)
3. **Transcription:** C:\Python314\python.exe + openai-whisper base, 3859 chars, 198 segments, saved v3Evq0LTnuo.json
4. **Gen script:** gen_v3Evq0LTnuo.py (3799B) - Python unicode escape fixed by using raw Chinese strings
5. **Article HTML:** v3Evq0LTnuo_wechat_article.html (5866B, 4 sections, red-black gradient template)
6. **Hugo post:** content/posts/v3Evq0LTnuo/index.md (4580B, 4 chapters)
7. **Cover:** yt-dlp thumbnail converted to v3Evq0LTnuo_cover.jpg (72KB)
8. **Commit:** 68133ac (4 files: index.md, json, wechat_article.html, cover)
9. **Push:** 2nd attempt succeeded (773c1bf..68133ac)
10. **last_video.txt:** Updated to v3Evq0LTnuo, committed 961ba50, pushed (68133ac..961ba50)

## Article Summary (4 chapters)

1. 一、征税风暴突然落地 (内地税务在北京、杭州两地率先动手，CRS十年大数据积累，锁定了香港保单的分红派息及预缴保费利息收入，税率20%)
2. 二、境外保单还值不值得买？ (瑞穗/高盛：即便全面征税，港险演示回报6-6.5%仍远高于内地3%，扣税后仍有优势；美元计价提供货币分散)
3. 三、已持有的人怎么办？ (不恐慌退保；分清保障型[免税]vs投资型[征税]；保单贷款需谨慎；整理缴费记录；大额资产找专业顾问)
4. 四、境外征税密集落地：口袋紧了才是真相 (境外炒股补税、券商账户20%、离岸信托7月被两部门发文征税——土地财政断崖、地方债务压力最大之时；公平是外包装，缺钱才是本质)

## Notes

- WeChat draft upload still blocked by IP whitelist (errcode 40164)
- Proxy instability persists (schannel SSL failures), push needed retry
- Pipeline internal last-video tracking lag bug (still present, not fixed)
- Python source encoding: avoid unicode escapes with invalid chars, use raw UTF-8 Chinese strings instead
- gen script: use CSS string concatenation (+) instead of f-strings with braces to avoid template conflicts
