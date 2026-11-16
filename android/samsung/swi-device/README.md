# SWI Samsung Device — initial Android shell

Target device: Samsung SM-A127F, Android 13 / API 33.
Compile platform: Android API 35.
Application ID: bw.trustsmotion.swi.

Includes:
- SWI identity activity
- Quick Settings tile
- Home-screen widget
- Boot-completed notification

Limitations:
- A normal application cannot insert a custom page into Samsung system Settings.
  SWI appears as an installed app in Android Settings > Apps.
- Android background-start restrictions prevent guaranteeing a full-screen
  launch after reboot. This project uses a notification instead.
- Boot notification requires the user to launch the app and grant notification
  permission first.
- No device attestation, Knox SDK integration, governing-spine connection,
  execution authority, or production authorization is implemented here.
- This is an initial source scaffold, not a built or tested APK.
