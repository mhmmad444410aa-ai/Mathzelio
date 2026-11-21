# Mathzelio Math Games — Android 1.2.0

**Android package:** `com.mhmmad.mathzelio` · **versionCode:** `4` · **minSdk:** `23` · **targetSdk:** `36`.

The complete source archive **Mathzelio-1.2.0-Source.zip** is already in the repository root. It contains an Android Java/WebView app, offline assets (including pre-rendered 3D-style backgrounds), six worlds, 300 generated levels and ten maths skills. British English, Arabic RTL and Brazilian Portuguese are supported. No ads SDK, telemetry, network permission or music in this version.

## Builds and verification
Visit [GitHub Actions](../../actions/workflows/android.yml) and choose **Build Mathzelio Android**. Pushing the source archive or changing the workflow starts a fresh run.

The workflow extracts the archive, checks that the correct application is present, corrects the in-app About version label, rebuilds offline assets, runs 3,600 maths engine checks, compiles and lints Debug and Release variants, and uploads:

- `Mathzelio-1.2.0-Debug-APK` — signed with GitHub's temporary debug key; **for testing only**.
- `Mathzelio-1.2.0-Unsigned-Release` — unsigned Release APK and AAB that must be signed before publishing.
- `Mathzelio-1.2.0-Signed-Release` — created when all four existing signing secrets are configured.
- Android build/lint reports.

The **first production Release APK/AAB** and a **new permanent certificate** were generated and checked independently in the private ChatGPT project session; neither signing keys nor passwords were uploaded to this public GitHub repository. **Save the original private key and password backup** before submission. If an earlier store release used a different certificate, do not replace that certificate.

To enable later signed builds, set these four GitHub **Actions Secrets**, using the *same permanent key*:

- `ANDROID_KEYSTORE_BASE64`
- `ANDROID_STORE_PASSWORD`
- `ANDROID_KEY_ALIAS`
- `ANDROID_KEY_PASSWORD`

Never paste secret values into files, commits, GitHub Issues or screenshots.

Certificate SHA-256 for the new proposed first-release key:
`41:A5:F9:48:BB:5E:62:65:EB:C2:51:EB:2B:7E:A8:9A:85:DC:A5:84:AE:AF:9D:81:AC:32:62:4C:13:BB:11:06`

## Store listing and privacy
Read the [Privacy Policy](PRIVACY.md) (English, Arabic and Brazilian Portuguese). The app is intended for children aged 4–10. The store listing must accurately disclose the absence of ads, tracking, external transmission and purchases. Provide verified developer contact information before publication. Screenshots must be from the actual running app, not generated mockups.

A genuine Android Gradle Release was built, signed and checked for package identity and signature integrity. **Physical-device install and interaction tests have not yet been carried out**; publication and approval have not been confirmed. Test on real devices before submitting it to any store.
