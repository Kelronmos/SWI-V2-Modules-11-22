# Implementation limitations

1. Non-Android environments cannot claim camera/face/hand/mic/biometric PASS.
2. Face = presence only, never recognition/identity.
3. Finger counts never hardcoded to five.
4. Speaker PASS requires human confirmation of hearing.
5. Network reachability ≠ SWI authorization.
6. Device facts ≠ human identity.
7. Termux shared storage must be verified before write.
8. V2 governing_permit remains the only permit engine.
