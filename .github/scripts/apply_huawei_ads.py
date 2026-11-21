#!/usr/bin/env python3
"""Mathzelio 1.2.1: native, child-directed Huawei Ads. No opt-in/out-of-ads question."""
from pathlib import Path
import sys

base = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path("Mathzelio").resolve()
asset = base/"app/src/main/assets"
app = base/"app"
main = app/"src/main"
java_file = main/"java/com/mhmmad/mathzelio/MainActivity.java"

def replace(path, old, new, label):
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit("Missing patch anchor "+label+": "+str(path))
    path.write_text(text.replace(old, new), encoding="utf-8")

replace(base/"settings.gradle",
        "repositories { google(); mavenCentral() } }",
        "repositories { google(); mavenCentral(); maven { url 'https://developer.huawei.com/repo/' } } }",
        "Huawei Maven")
replace(app/"build.gradle",
        "versionCode 4; versionName '1.2.0'",
        "versionCode 5; versionName '1.2.1'",
        "version")
with (app/"build.gradle").open("a",encoding="utf-8") as out:
    out.write("\n// Official Petal Ads Lite SDK (2026-10-10). Child-only contextual ad requests.\n")
    out.write("dependencies { implementation 'com.huawei.hms:ads-lite:13.4.91.300' }\n")

manifest = main/"AndroidManifest.xml"
src = manifest.read_text(encoding="utf-8")
src = src.replace('<manifest xmlns:android="http://schemas.android.com/apk/res/android">',
    '<manifest xmlns:android="http://schemas.android.com/apk/res/android" xmlns:tools="http://schemas.android.com/tools">\n'
    '    <uses-permission android:name="android.permission.INTERNET"/>\n'
    '    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>\n'
    '    <!-- Do not request an advertising ID for an app directed at young children. -->\n'
    '    <uses-permission android:name="com.google.android.gms.permission.AD_ID" tools:node="remove"/>')
if src == manifest.read_text(encoding="utf-8"):
    raise SystemExit("AndroidManifest.xml start tag not found")
manifest.write_text(src,encoding="utf-8")

java_file.write_text(r'''package com.mhmmad.mathzelio;

import android.app.Activity;
import android.os.Bundle;
import android.os.SystemClock;
import android.graphics.Color;
import android.view.Gravity;
import android.view.View;
import android.view.WindowInsets;
import android.view.WindowInsetsController;
import android.webkit.JavascriptInterface;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import com.huawei.hms.ads.AdListener;
import com.huawei.hms.ads.AdParam;
import com.huawei.hms.ads.BannerAdSize;
import com.huawei.hms.ads.ContentClassification;
import com.huawei.hms.ads.HwAds;
import com.huawei.hms.ads.NonPersonalizedAd;
import com.huawei.hms.ads.RequestOptions;
import com.huawei.hms.ads.TagForChild;
import com.huawei.hms.ads.UnderAge;
import com.huawei.hms.ads.banner.BannerView;
import com.huawei.hms.ads.InterstitialAd;

public final class MainActivity extends Activity {
    private static final String BANNER_SLOT = "r6ngbhqn6k";
    private static final String INTERSTITIAL_SLOT = "c9tc18kd7o";
    private static final long MIN_INTERSTITIAL_INTERVAL_MS = 4L * 60L * 1000L;
    private static final int COMPLETIONS_BETWEEN_ADS = 5;

    private WebView game;
    private BannerView banner;
    private InterstitialAd interstitial;
    private FrameLayout bannerArea;
    private String currentScreen = "splash";
    private boolean bannerLoaded = false;
    private boolean adReady = false;
    private int levelCompletions = 0;
    private long lastInterstitialMs;

    private int dp(int value) {
        return Math.round(getResources().getDisplayMetrics().density * value);
    }

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().setStatusBarColor(Color.BLACK);
        getWindow().setNavigationBarColor(Color.BLACK);
        lastInterstitialMs = SystemClock.elapsedRealtime();

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setBackgroundColor(0xff38205c);

        game = new WebView(this);
        game.setBackgroundColor(0xff532a9a);
        WebSettings settings = game.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(false);
        settings.setAllowFileAccessFromFileURLs(false);
        settings.setAllowUniversalAccessFromFileURLs(false);
        settings.setBlockNetworkLoads(true); // Ads only through the native SDK.
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        game.setWebViewClient(new WebViewClient() {
            @Override public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest r) {
                return !r.getUrl().toString().startsWith("file:///android_asset/");
            }
            @Override public boolean shouldOverrideUrlLoading(WebView v, String url) {
                return !url.startsWith("file:///android_asset/");
            }
        });
        // Limited to this bundled and network-isolated WebView. No arbitrary web origin.
        game.addJavascriptInterface(new GameAdsBridge(), "MathzelioNativeAds");
        root.addView(game, new LinearLayout.LayoutParams(-1, 0, 1f));

        // Native ad is outside the game surface: never overlaps questions or answer buttons.
        bannerArea = new FrameLayout(this);
        bannerArea.setBackgroundColor(0xff221137);
        bannerArea.setPadding(0, dp(12), 0, dp(10));
        bannerArea.setVisibility(View.GONE);
        root.addView(bannerArea, new LinearLayout.LayoutParams(-1, dp(72)));

        setContentView(root);
        immersive();
        initChildSafeAds();
        game.loadUrl("file:///android_asset/index.html");
    }

    private void initChildSafeAds() {
        try {
            RequestOptions requestOptions = new RequestOptions.Builder()
                .setTagForChildProtection(TagForChild.TAG_FOR_CHILD_PROTECTION_TRUE)
                .setTagForUnderAgeOfPromise(UnderAge.PROMISE_TRUE)
                .setAdContentClassification(ContentClassification.AD_CONTENT_CLASSIFICATION_W)
                .setNonPersonalizedAd(NonPersonalizedAd.ALLOW_NON_PERSONALIZED)
                .build();
            HwAds.setRequestOptions(requestOptions);
            HwAds.init(this);
            adReady = true;

            banner = new BannerView(this);
            banner.setAdId(BANNER_SLOT);
            banner.setBannerAdSize(BannerAdSize.BANNER_SIZE_320_50);
            FrameLayout.LayoutParams params = new FrameLayout.LayoutParams(-2, dp(50), Gravity.CENTER);
            bannerArea.addView(banner, params);
            banner.setBannerRefresh(90);
            banner.setAdListener(new AdListener() {
                @Override public void onAdLoaded() {
                    bannerLoaded = true;
                    updateBanner();
                }
                @Override public void onAdFailed(int errorCode) {
                    bannerLoaded = false;
                    updateBanner();
                }
                @Override public void onAdClosed() {
                    bannerLoaded = false;
                    updateBanner();
                }
            });
            banner.loadAd(new AdParam.Builder().build());

            interstitial = new InterstitialAd(this);
            interstitial.setAdId(INTERSTITIAL_SLOT);
            interstitial.setAdListener(new AdListener() {
                @Override public void onAdClosed() {
                    loadNextInterstitial();
                }
                @Override public void onAdFailed(int errorCode) {
                    // A failed ad must never block game progress or create a dialog.
                }
            });
            loadNextInterstitial();
        } catch (Throwable unavailable) {
            // Huawei Ads may be unavailable on an unsupported device.
            // Continue the game with no ads and no pop-up.
            adReady = false;
            bannerLoaded = false;
            if (bannerArea != null) bannerArea.setVisibility(View.GONE);
        }
    }

    private void loadNextInterstitial() {
        if (!adReady || interstitial == null) return;
        try { interstitial.loadAd(new AdParam.Builder().build()); }
        catch (RuntimeException ignored) { }
    }

    private void updateBanner() {
        boolean menu = "home".equals(currentScreen) || "map".equals(currentScreen)
            || "progress".equals(currentScreen);
        if (bannerArea != null) {
            bannerArea.setVisibility(adReady && bannerLoaded && menu ? View.VISIBLE : View.GONE);
        }
    }

    private void showAfterLevelCompleted() {
        if (!adReady || !"win".equals(currentScreen) || interstitial == null) return;
        if (levelCompletions < COMPLETIONS_BETWEEN_ADS) return;
        if (SystemClock.elapsedRealtime() - lastInterstitialMs < MIN_INTERSTITIAL_INTERVAL_MS) return;
        if (!interstitial.isLoaded()) return;
        levelCompletions = 0;
        lastInterstitialMs = SystemClock.elapsedRealtime();
        try { interstitial.show(this); } catch (RuntimeException ignored) { }
    }

    private final class GameAdsBridge {
        @JavascriptInterface public void screen(String screenName) {
            runOnUiThread(() -> {
                currentScreen = screenName == null ? "" : screenName;
                updateBanner();
                if ("win".equals(currentScreen)) {
                    // Pause after the victory screen; never interrupt a question.
                    if (game != null) game.postDelayed(() -> showAfterLevelCompleted(), 1500);
                }
            });
        }
        @JavascriptInterface public void completedLevel() {
            runOnUiThread(() -> { levelCompletions = Math.min(20, levelCompletions + 1); });
        }
    }

    private void immersive() {
        if (android.os.Build.VERSION.SDK_INT >= 30) {
            WindowInsetsController c = getWindow().getInsetsController();
            if (c != null) {
                c.hide(WindowInsets.Type.systemBars());
                c.setSystemBarsBehavior(WindowInsetsController.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
            }
        } else getWindow().getDecorView().setSystemUiVisibility(5894);
    }

    @Override public void onWindowFocusChanged(boolean focused) {
        super.onWindowFocusChanged(focused);
        if (focused) immersive();
    }
    @Override public void onBackPressed() {
        if (game != null) game.evaluateJavascript("window.gameBack && window.gameBack()", null);
    }
    @Override protected void onPause() {
        if (game != null) game.onPause();
        if (banner != null) banner.pause();
        super.onPause();
    }
    @Override protected void onResume() {
        super.onResume();
        if (game != null) game.onResume();
        if (banner != null) banner.resume();
    }
    @Override protected void onDestroy() {
        if (banner != null) { banner.destroy(); banner = null; }
        interstitial = null;
        if (game != null) { game.destroy(); game = null; }
        super.onDestroy();
    }
}
''',encoding="utf-8")

game = asset/"game.js"
replace(game,
    "window.scrollTo(0,0);}",
    "window.scrollTo(0,0);try{window.MathzelioNativeAds?.screen(screen);}catch(e){} }",
    "screen reporting")
replace(game,
    "save();show('win');confetti();}",
    "save();try{if(run.type==='level')window.MathzelioNativeAds?.completedLevel();}catch(e){}show('win');confetti();}",
    "interstitial level-boundary")

translations = asset/"translations.js"
replace(translations, "No advertisements in this version",
        "Child-appropriate, non-personalised ads may be shown. No ads appear during questions.",
        "privacy English")
replace(translations, "لا إعلانات في هذا الإصدار",
        "قد تظهر إعلانات غير مخصّصة ومناسبة للأطفال، ولا تظهر أثناء حل الأسئلة.",
        "privacy Arabic")
replace(translations, "Sem anúncios nesta versão",
        "Podem aparecer anúncios não personalizados e adequados para crianças, nunca durante as questões.",
        "privacy Portuguese")
replace(translations,
        "Mathzelio works offline. It stores learning progress, settings and a parent PIN verifier only on this device. No accounts, personal information, location, tracking, advertisements or external links are used in this version. Clear app data in device settings to delete local information.",
        "Maths activities and progress work offline. Huawei Petal Ads may use network access to display child-appropriate, non-personalised ads. Game records, settings and the parent PIN verifier remain on this device; we do not send game scores to advertisers. For SDK data processing, see the public privacy policy. Clear app data to delete local records.",
        "English privacy notice")
replace(translations,
        "تعمل ماثزيليو دون إنترنت، وتخزن التقدم التعليمي والإعدادات وبيانات التحقق من رمز الوالدين على الجهاز فقط. لا حسابات ولا معلومات شخصية ولا موقع ولا تتبع ولا إعلانات أو روابط خارجية في هذا الإصدار. لمسح المعلومات احذف بيانات التطبيق من إعدادات الجهاز.",
        "تعمل أنشطة الحساب وحفظ التقدم دون اتصال. قد يستخدم نظام إعلانات هواوي الإنترنت لعرض إعلانات غير مخصّصة ومناسبة للأطفال. تبقى النتائج والإعدادات ورمز الوالدين محفوظة محليًا، ولا نرسل نتائج اللعب إلى المعلنين. راجع سياسة الخصوصية المنشورة لمعلومات معالجة بيانات SDK. امسح بيانات التطبيق لحذف البيانات المحلية.",
        "Arabic privacy notice")
replace(translations,
        "Mathzelio funciona sem internet e guarda o progresso, as configurações e o verificador do PIN apenas no aparelho. Esta versão não usa contas, informações pessoais, localização, rastreamento, anúncios ou links externos. Limpe os dados do app nas configurações para excluí-los.",
        "As atividades e o progresso funcionam sem internet. O Petal Ads da Huawei pode usar a rede para mostrar anúncios não personalizados e adequados para crianças. O progresso, as configurações e o PIN ficam no aparelho; não enviamos resultados aos anunciantes. Consulte a política de privacidade pública para saber mais sobre o SDK. Limpe os dados do app para apagar registros locais.",
        "Portuguese privacy notice")
replace(translations, "1.1.0", "1.2.1", "about screen version")
(asset/"ad-policy.js").write_text(
"""/* Ads are implemented ONLY in the native Huawei SDK.
   No choice-to-enable-ads dialog. No JavaScript ad requests or ad settings.
   Child protection + non-personalised + W-rated filtering enforced natively.
   Mandatory legal disclosures remain in the parent-gated privacy area. */
window.MathzelioAds=Object.freeze({native:true,eligible:['home','map','progress','win']});
""", encoding="utf-8")
print("Patched Mathzelio for Petal Ads: 1.2.1 (5), child-directed/non-personalised, no ads toggle.")
