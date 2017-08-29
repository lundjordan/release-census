# Manually sign Focus for Android APKs

There are 2 APKs: one is Focus, the other for the german-speaking population: Klar.

## Create signatures
1. `ssh signing4.srv.releng.scl3.mozilla.com`
1. Download unsigned APKs
1. `jarsigner -keystore /builds/signing/rel-key-signing-server/secrets/focus-jar app-focus-webkit-release-unsigned.apk focus`. Repeat for the Klar APK: only change the path to the file, the certificate alias (`focus`) remains identical. You'll be prompted for the focus passphrase which is stored in the releng private repo. You'll also get an expected warning:
```
Warning:
No -tsa or -tsacert is provided and this jar is not timestamped. Without a timestamp, users may not be able to validate this jar after the signer certificate's expiration date (2044-10-25) or after any future revocation date.
```
1. Verify signatures: `jarsigner -verify -verbose -keystore /builds/signing/rel-key-signing-server/secrets/focus-jar app-focus-webkit-release-unsigned.apk focus`. Repeat for the Klar APK.
1. `mv app-focus-webkit-release-unsigned.apk app-focus-webkit-release-signed.apk`
1. Fetch signed APKs on your local machine.

## Optimize APKs

Google Play refuses non-optimized APKs. The signature changes the structure of the APK archive, which breaks the Zip optimization.

1. Install the latest Android SDK, to get the build tools. For instance, on Mac: `brew cask install android-sdk` (requires `brew tap caskroom/cask`)
1. `zipalign -v 4 app-klar-webkit-release-signed.apk app-klar-webkit-release-signed-aligned.apk`. Repeat for the Klar APK. Zipalign may not be in your PATH. This depends on on your distribution. Please check folder like `/usr/local/bin` or `/opt/android-sdk/build-tools/XX.Y.Z`.
1. Verify optimization. `zipalign -c -v 4 app-focus-webkit-release-signed-aligned.apk`. Repeat for the Klar APK.
