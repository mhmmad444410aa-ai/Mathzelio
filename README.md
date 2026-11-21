# Mathzelio Math Games — Android

**Current development version:** 1.2.1 (versionCode 5) · **Package:** `com.mhmmad.mathzelio` · Android minSdk 23, targetSdk 36.

## Repository structure

The `Mathzelio-1.2.0-Source.zip` file contains the original game: 6 worlds, 300 levels, 10 interactive skills, saved progress, and three languages (British English, Arabic RTL, Brazilian Portuguese). The **1.2.1 child-safe Petal Ads integration is an actual source patch** at `.github/scripts/apply_huawei_ads.py`. CI extracts the original ZIP, applies the patch, packs the offline game assets, compiles Android, and publishes a separate **Mathzelio-1.2.1-Source** ZIP with the updated source files. This avoids uploading signing secrets or huge generated archives to the public repository.

## Advertisements — child-directed and contextual only

The 1.2.1 integration uses `com.huawei.hms:ads-lite:13.4.91.300` and the user's two ad slots:
- Banner: `r6ngbhqn6k` — only displayed in home, world map, or progress menus, in a separate non-overlapping native view.
- Interstitial: `c9tc18kd7o` — only after five completed adventure levels, on a victory screen, at least four minutes after the prior interstitial/startup.

All ad requests set **TagForChild=TRUE**, **UnderAge=PROMISE_TRUE**, **NonPersonalizedAd=ALLOW_NON_PERSONALIZED**, and **ContentClassification=W** before SDK initialization. No optional "Do you want ads?" dialog, ad enable/disable toggle, splash ad, rewarded ad, or ad during a maths question. The game still works offline; advertising requires network access. No advertising SDK is embedded in the WebView; it runs natively and the game's WebView remains network isolated.

AppGallery/publisher settings must also match child-directed delivery and appropriate ads. The SDK itself can display built-in disclosures, and mandatory legal privacy or guardian consent must be respected. This source does not attempt to bypass mandatory consent.

**Privacy notice:** [PRIVACY.md](PRIVACY.md) — updated English, Arabic, and Brazilian Portuguese policy. The publisher must disclose the new SDK, network usage, and advertising accurately in store submissions. Ads and links must be appropriate for children.

## Building and signing

Visit [GitHub Actions](../../actions/workflows/android.yml). The build runs on `main` changes to the workflow, source archive or 1.2.1 source patch. A successful run provides `Mathzelio-1.2.1-Debug-APK`, unsigned Release APK/AAB and a downloadable updated source ZIP. A **signed** Release is produced only if you configure the four existing permanent signing secrets at GitHub Settings → Secrets and variables → Actions:

- `ANDROID_KEYSTORE_BASE64`
- `ANDROID_STORE_PASSWORD`
- `ANDROID_KEY_ALIAS`
- `ANDROID_KEY_PASSWORD`

**Never upload keystores or passwords into this public repository.** If 1.2.0 was already uploaded to Huawei, keep the exact same app signing certificate to submit 1.2.1. The previously generated release certificate fingerprint is `41:A5:F9:48:BB:5E:62:65:EB:C2:51:EB:2B:7E:A8:9A:85:DC:A5:84:AE:AF:9D:81:AC:32:62:4C:13:BB:11:06`. Do not replace it for an update.

## Verification and remaining limitations

CI performs **real** Gradle compilation/lint and 3,600 questions checks. Tests with Huawei HMS Core, live ad availability, absence of SDK/system consent prompts, interstitial callback ordering, accidental-ad-tap avoidance, real-device performance and final AppGallery acceptance require physical devices or emulators. **Do not treat a compiled APK alone as production-QA approval.**
