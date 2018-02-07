## Summary
TechMpire nxus platform SDK for Unity developers

## Get Unity SDK
Download the Unity package file from <a href="http://distribution.nxus.mobi/libs/unity-nxus-sdk-v1_0_20.unitypackage">here</a>
Open your project in the Unity Editor and navigate to <pre>Assets -> Import Package -> Custom Package</pre> and select the downloaded Unity package file.
<img src="http://distribution.nxus.mobi/images/unity/image_1.png">

## Integration into project
To integrate the library into you project, add the prefab <b>NxusDSP</b> to your first scene so it's initialized properly. Location of prefab: <pre>Assets/NxusDSP/NxusDSP.prefab</pre>
Edit the parameters of the NxusDSP script in the Inspector menu of the added prefab.
<img src="http://distribution.nxus.mobi/images/unity/image_2.png">

Replace <b>{Your API key here}</b> with your actual API key.
If Debugging is enabled, library actions and events will be visible in the log console.

Once initialisation is done, an <b>app_start</b> event is automatically sent. If the application is started for the first time after installation, instead of <b>app_start</b>, <b>first_app_launch</b> is sent.

## Sending custom events
To send a custom event, call the method <b>trackEvent</b> from your code.
```
NxusDSP.trackEvent ("event-name");
```

If you have any additional parameters you would like to send, pass in an instance of <b>Dictionary</b>:
```
Dictionary<string, string> params = new Dictionary<string, string>();
params.Add ("key", "value");
NxusDSP.trackEventWithParams ("event-name", params);
```

## Sending predefined events
You can send predefined events using the SDK, with following methods:
```
NxusDSP.trackEventInstall (params);
NxusDSP.trackEventOpen (params);
NxusDSP.trackEventRegistration (params);
NxusDSP.trackEventPurchase (params);
NxusDSP.trackEventLevel (params);
NxusDSP.trackEventTutorial (params);
NxusDSP.trackEventAddToCart (params);
NxusDSP.trackEventCheckout (params);
NxusDSP.trackEventInvite (params);
NxusDSP.trackEventAchievement (params);
```
Every method takes additional parameters using <b>Dictionary</b>:
```
Dictionary<string, string> params = new Dictionary<string, string>();
params.Add ("key", "value");
```
