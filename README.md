## Summary
TechMpire nxus platform SDK for Unity developers

## Get Unity SDK
Download the Unity package file from <a href="http://distribution.nxus.mobi/libs/MpireNxusMeasurement_v1_1_2.zip">here</a>
Open your project in the Unity Editor and navigate to <pre>Assets -> Import Package -> Custom Package</pre> and select the downloaded Unity package file.
<img src="http://distribution.nxus.mobi/images/unity/image_1.png">

## Integration into project
To integrate the library into you project, add the prefab <b>MpireNxusMeasurement</b> to your first scene so it's initialized properly. Location of prefab: <pre>Assets/MpireNxusMeasurement/MpireNxusMeasurement.prefab</pre>
Edit the parameters of the MpireNxusMeasurement script in the Inspector menu of the added prefab.

Replace <b>{Your API key here}</b> with your actual API key.
If Debugging is enabled, library actions and events will be visible in the log console.

Once initialisation is done, an <b>app_start</b> event is automatically sent. If the application is started for the first time after installation, instead of <b>app_start</b>, <b>install</b> event is sent.

## Sending custom events
To send a custom event, call the method <b>trackEvent</b> from your code.
```
MpireNxusMeasurement.trackEvent ("event-name");
```

If you have any additional parameters you would like to send, pass in an instance of <b>Dictionary</b>:
```
Dictionary<string, string> params = new Dictionary<string, string>();
params.Add ("key", "value");
MpireNxusMeasurement.trackEventWithParams ("event-name", params);
```

## Sending predefined events
You can send predefined events using the SDK, with following methods:
```
MpireNxusMeasurement.trackEventInstall (params);
MpireNxusMeasurement.trackEventOpen (params);
MpireNxusMeasurement.trackEventRegistration (params);
MpireNxusMeasurement.trackEventPurchase (params);
MpireNxusMeasurement.trackEventLevel (params);
MpireNxusMeasurement.trackEventTutorial (params);
MpireNxusMeasurement.trackEventAddToCart (params);
MpireNxusMeasurement.trackEventCheckout (params);
MpireNxusMeasurement.trackEventInvite (params);
MpireNxusMeasurement.trackEventAchievement (params);
```
Every method takes additional parameters using <b>Dictionary</b>:
```
Dictionary<string, string> params = new Dictionary<string, string>();
params.Add ("key", "value");
```
