# Manually sign Focus for Android APKs

There are 2 APKs: one is Focus, the other for the german-speaking population: Klar.

## Create signatures
1. `ssh signing4.srv.releng.scl3.mozilla.com`
1. Download unsigned APKs
1. `jarsigner -keystore /builds/signing/rel-key-signing-server/secrets/focus-jar app-focus-webkit-release-unsigned.apk focus`. Repeat for Klar: only change the name of the APK, the certificate alias (`focus`) remains identical.
1. Verify signatures: `jarsigner -verify -verbose -keystore /builds/signing/rel-key-signing-server/secrets/focus-jar app-focus-webkit-release-unsigned.apk focus`. Repeat for Klar.
1. `mv app-focus-webkit-release-unsigned.apk app-focus-webkit-release-signed.apk`
1. Fetch signed APKs on your local machine.

## Optimize APKs

Google Play refuses non-optimized APKs. The signature changes the structure of the APK archive, which breaks the Zip optimization.

1. Install the latest Android SDK, to get the build tools. For instance, on Mac: `brew cask install android-sdk` (requires `brew tap caskroom/cask`)
1. `/opt/android-sdk/build-tools/26.0.1/zipalign -v 4 app-klar-webkit-release-signed.apk app-klar-webkit-release-signed-aligned.apk`. Repeat for Klar.
1. Verify optimization. `/opt/android-sdk/build-tools/26.0.1/zipalign -c -v 4 app-focus-webkit-release-signed-aligned.apk`. Release for Klar.
