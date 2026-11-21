# Mathzelio Math Games — Android

Android app: `com.mhmmad.mathzelio` • **1.2.0 (versionCode 4)**.

**The repository currently has only its release automation. You must upload the project's existing ZIP archive before an APK can be built.**

## Upload once from your phone
1. Download **Mathzelio-1.2.0-Source.zip** from the ChatGPT conversation.
2. In this repository, tap **Add file → Upload files**.
3. Upload the ZIP as **Mathzelio-1.2.0-Source.zip** at the repository root (do not rename or extract it).
4. Commit directly to **main**. This starts the GitHub Actions workflow automatically.
5. Open **Actions → Build Mathzelio Android → latest run → Artifacts**.

**Artifacts:**
- `Mathzelio-1.2.0-Debug-APK` — installable test APK, **not for store**.
- `Mathzelio-1.2.0-Signed-Release` — signed APK and AAB, created **only if the original, permanent signing key and all four secrets are provided**.

## Signing
Set GitHub **Settings → Secrets and variables → Actions → New repository secret**:
- `ANDROID_KEYSTORE_BASE64`
- `ANDROID_STORE_PASSWORD`
- `ANDROID_KEY_ALIAS`
- `ANDROID_KEY_PASSWORD`

If this app was published previously, preserve its original certificate; do not generate a replacement key. If it has never been published, generate one permanent release key once and back it up securely. Never upload the keystore or any password into a public repository.

This is an offline kids' maths game (six worlds, 300 levels, 10 modes, English, Arabic, Portuguese). It currently has **no ads SDK or Internet permission**. The design uses pre-rendered 3D sprites, not real-time 3D. GitHub Actions builds the actual Android source rather than repackaging the prior TEST APK. Browser testing is not Android device QA.

**Before store submission:** install and test the signed APK, check the publisher signing certificate and target SDK, provide a working privacy-policy URL and developer contact, verify child-safety/store requirements, and ensure all screenshots describe real in-app functionality.
