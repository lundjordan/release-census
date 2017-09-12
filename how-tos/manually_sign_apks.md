# Manually sign Android APKs (like Focus for Android or Rocket)

Currently, 2 products are concerned:
    * Firefox Rocket
    * Firefox Focus for Android. :warning: This product has 2 APKs: one is Focus, the other for the german-speaking population: Klar.


## Create signatures
1. `ssh signing4.srv.releng.scl3.mozilla.com`
1. Download unsigned APK(s).
1. `keystore='/builds/signing/rel-key-signing-server/secrets/focus-jar'` for Focus/Klar. `keystore='/builds/signing/rel-key-signing-server/secrets/rocket-jar'` for Rocket.
1. `alias='focus'` for Focus/Klar. `alias='rocket'` for Rocket.
1. `jarsigner -keystore "$keystore" unsigned.apk "$alias"`. Repeat for the Klar APK: only change the path to the file, the certificate alias (`focus`) remains identical. You'll be prompted for the focus passphrase which is stored in the releng private repo. You'll also get an expected warning:
```
Warning:
No -tsa or -tsacert is provided and this jar is not timestamped. Without a timestamp, users may not be able to validate this jar after the signer certificate's expiration date (2044-10-25) or after any future revocation date.
```
1. `mv unsigned.apk signed.apk`
1. Verify signatures: `jarsigner -verify -verbose -keystore "$keystore" signed.apk "$alias"`. Repeat for the Klar APK.
1. If your product has several APKs, repeat the 3 previous steps.
1. Fetch signed APK(s) on your local machine.

### Can't sign APKs

Sometimes, APKs aren't correctly formatted. For instance, CI may have already signed an APK with a dev key. In this case, you may see:
```sh
$ jarsigner -verbose -keystore "$keystore" unsigned.apk "$alias"
Enter Passphrase for keystore:
jarsigner: unable to sign jar: java.util.zip.ZipException: invalid entry compressed size (expected 34549 but got 35093 bytes)
```

The fix is just to strip the signature from the package:
```sh
$ zip -d unsigned.apk META-INF/\*
deleting: META-INF/CERT.RSA
deleting: META-INF/CERT.SF
deleting: META-INF/MANIFEST.MF
```

Then you can resume signing.


## Optimize APKs

Google Play refuses non-optimized APKs. The signature changes the structure of the APK archive, which breaks the Zip optimization.

1. Install the latest Android SDK, to get the build tools. For instance, on Mac: `brew cask install android-sdk` (requires `brew tap caskroom/cask`)
1. `zipalign -v 4 signed.apk signed-aligned.apk`. Zipalign may not be in your PATH. This depends on on your distribution. Please check folder like `/usr/local/bin` or `/opt/android-sdk/build-tools/XX.Y.Z`.
1. Verify optimization. `zipalign -c -v 4 signed-aligned.apk`.
1. If your product has several APKs, repeat the 2 previous steps.
