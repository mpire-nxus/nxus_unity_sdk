using UnityEngine;
using System.Collections;
using System.Runtime.InteropServices;
using System.Collections.Generic;

public class MpireNxusMeasurement : MonoBehaviour {

	public bool debuggingEnabled = true;
	public string apiKey = "{Your API key here}";

	private static MpireNxusMeasurement instance = null;

	public MpireNxusMeasurement () {}

	private MpireNxusMeasurement (bool debuggingEnabled, string apiKey) {
		this.debuggingEnabled = debuggingEnabled;
		this.apiKey = apiKey;
	}

	void Awake () {
		Debug.Log ("MpireNxusMeasurement Awake");
		Debug.Log ("Awake - debuggingEnabled: " + debuggingEnabled);
		Debug.Log ("Awake - apiKey: " + apiKey);
		if (MpireNxusMeasurement.instance == null) {
			MpireNxusMeasurement.instance = new MpireNxusMeasurement (debuggingEnabled, apiKey);
			MpireNxusMeasurement.instance.mpireNxusMeasurementInitializeLibrary ();
		}
	}

	public static void trackEvent(string eventName) {
		Debug.Log ("MpireNxusMeasurement trackEvent - instance existing, tracking event");
		MpireNxusMeasurement.instance.mpireNxusMeasurementTrackEvent(eventName);
	}

	public static void trackEventWithParams(string eventName, Dictionary<string, string> attributes) {
		Debug.Log ("MpireNxusMeasurement trackEventWithParams - instance existing, tracking event");
		string attributesString = "";
		foreach(KeyValuePair<string, string> kvp in attributes) {
			attributesString += kvp.Key + "=" + kvp.Value + "\n";
		}
		Debug.Log ("MpireNxusMeasurement trackEventWithParams attributes: " + attributesString);
		MpireNxusMeasurement.instance.mpireNxusMeasurementTrackEventWithParams (eventName, attributesString);
	}

	public static void trackEventInstall(Dictionary<string, string> attributes) {
		Debug.Log ("MpireNxusMeasurement trackEventInstall - instance existing, tracking event");
		string attributesString = "";
		foreach(KeyValuePair<string, string> kvp in attributes) {
			attributesString += kvp.Key + "=" + kvp.Value + "\n";
		}
		Debug.Log ("MpireNxusMeasurement trackEventInstall attributes: " + attributesString);
		MpireNxusMeasurement.instance.mpireNxusMeasurementTrackEventInstall (attributesString);
	}

	public static void trackEventOpen(Dictionary<string, string> attributes) {
		Debug.Log ("MpireNxusMeasurement trackEventOpen - instance existing, tracking event");
		string attributesString = "";
		foreach(KeyValuePair<string, string> kvp in attributes) {
			attributesString += kvp.Key + "=" + kvp.Value + "\n";
		}
		Debug.Log ("MpireNxusMeasurement trackEventOpen attributes: " + attributesString);
		MpireNxusMeasurement.instance.mpireNxusMeasurementTrackEventOpen (attributesString);
	}

	public static void trackEventRegistration(Dictionary<string, string> attributes) {
		Debug.Log ("MpireNxusMeasurement trackEventRegistration - instance existing, tracking event");
		string attributesString = "";
		foreach(KeyValuePair<string, string> kvp in attributes) {
			attributesString += kvp.Key + "=" + kvp.Value + "\n";
		}
		Debug.Log ("MpireNxusMeasurement trackEventRegistration attributes: " + attributesString);
		MpireNxusMeasurement.instance.mpireNxusMeasurementTrackEventRegistration (attributesString);
	}

	public static void trackEventPurchase(Dictionary<string, string> attributes) {
		Debug.Log ("MpireNxusMeasurement trackEventPurchase - instance existing, tracking event");
		string attributesString = "";
		foreach(KeyValuePair<string, string> kvp in attributes) {
			attributesString += kvp.Key + "=" + kvp.Value + "\n";
		}
		Debug.Log ("MpireNxusMeasurement trackEventPurchase attributes: " + attributesString);
		MpireNxusMeasurement.instance.mpireNxusMeasurementTrackEventPurchase (attributesString);
	}

	public static void trackEventLevel(Dictionary<string, string> attributes) {
		Debug.Log ("MpireNxusMeasurement trackEventLevel - instance existing, tracking event");
		string attributesString = "";
		foreach(KeyValuePair<string, string> kvp in attributes) {
			attributesString += kvp.Key + "=" + kvp.Value + "\n";
		}
		Debug.Log ("MpireNxusMeasurement trackEventLevel attributes: " + attributesString);
		MpireNxusMeasurement.instance.mpireNxusMeasurementTrackEventLevel (attributesString);
	}

	public static void trackEventTutorial(Dictionary<string, string> attributes) {
		Debug.Log ("MpireNxusMeasurement trackEventTutorial - instance existing, tracking event");
		string attributesString = "";
		foreach(KeyValuePair<string, string> kvp in attributes) {
			attributesString += kvp.Key + "=" + kvp.Value + "\n";
		}
		Debug.Log ("MpireNxusMeasurement trackEventTutorial attributes: " + attributesString);
		MpireNxusMeasurement.instance.mpireNxusMeasurementTrackEventTutorial (attributesString);
	}

	public static void trackEventAddToCart(Dictionary<string, string> attributes) {
		Debug.Log ("MpireNxusMeasurement trackEventAddToCart - instance existing, tracking event");
		string attributesString = "";
		foreach(KeyValuePair<string, string> kvp in attributes) {
			attributesString += kvp.Key + "=" + kvp.Value + "\n";
		}
		Debug.Log ("MpireNxusMeasurement trackEventAddToCart attributes: " + attributesString);
		MpireNxusMeasurement.instance.mpireNxusMeasurementTrackEventAddToCart (attributesString);
	}

	public static void trackEventCheckout(Dictionary<string, string> attributes) {
		Debug.Log ("MpireNxusMeasurement trackEventCheckout - instance existing, tracking event");
		string attributesString = "";
		foreach(KeyValuePair<string, string> kvp in attributes) {
			attributesString += kvp.Key + "=" + kvp.Value + "\n";
		}
		Debug.Log ("MpireNxusMeasurement trackEventCheckout attributes: " + attributesString);
		MpireNxusMeasurement.instance.mpireNxusMeasurementTrackEventCheckout (attributesString);
	}

	public static void trackEventInvite(Dictionary<string, string> attributes) {
		Debug.Log ("MpireNxusMeasurement trackEventInvite - instance existing, tracking event");
		string attributesString = "";
		foreach(KeyValuePair<string, string> kvp in attributes) {
			attributesString += kvp.Key + "=" + kvp.Value + "\n";
		}
		Debug.Log ("MpireNxusMeasurement trackEventInvite attributes: " + attributesString);
		MpireNxusMeasurement.instance.mpireNxusMeasurementTrackEventInvite (attributesString);
	}

	public static void trackEventAchievement(Dictionary<string, string> attributes) {
		Debug.Log ("MpireNxusMeasurement trackEventAchievement - instance existing, tracking event");
		string attributesString = "";
		foreach(KeyValuePair<string, string> kvp in attributes) {
			attributesString += kvp.Key + "=" + kvp.Value + "\n";
		}
		Debug.Log ("MpireNxusMeasurement trackEventAchievement attributes: " + attributesString);
		MpireNxusMeasurement.instance.mpireNxusMeasurementTrackEventAchievement (attributesString);
	}

	#if UNITY_EDITOR
	#region Public methods
	public void mpireNxusMeasurementInitializeLibrary () {
		// Empty
	}

	public void mpireNxusMeasurementTrackEvent (string eventName) {
		// Empty
	}

	public void mpireNxusMeasurementTrackEventWithParams (string eventName, string attributes) {
		// Empty
	}

	public void mpireNxusMeasurementTrackEventInstall (string attributes) {
		// Empty
	}

	public void mpireNxusMeasurementTrackEventOpen (string attributes) {
		// Empty
	}

	public void mpireNxusMeasurementTrackEventRegistration (string attributes) {
		// Empty
	}

	public void mpireNxusMeasurementTrackEventPurchase (string attributes) {
		// Empty
	}

	public void mpireNxusMeasurementTrackEventLevel (string attributes) {
		// Empty
	}

	public void mpireNxusMeasurementTrackEventTutorial (string attributes) {
		// Empty
	}

	public void mpireNxusMeasurementTrackEventAddToCart (string attributes) {
		// Empty
	}

	public void mpireNxusMeasurementTrackEventCheckout (string attributes) {
		// Empty
	}

	public void mpireNxusMeasurementTrackEventInvite (string attributes) {
		// Empty
	}

	public void mpireNxusMeasurementTrackEventAchievement (string attributes) {
		// Empty
	}
    #endregion

	#elif UNITY_IOS
    #region External methods
	[DllImport("__Internal")]
	private static extern void mpire_nxus_measurement_set_sdk_platform (string platform);

	[DllImport("__Internal")]
	private static extern void mpire_nxus_measurement_debugging_enabled (bool enabled);

	[DllImport("__Internal")]
	private static extern void mpire_nxus_measurement_initialize_library (string key);

	[DllImport("__Internal")]
	private static extern void mpire_nxus_measurement_track_event (string eventName);

	[DllImport("__Internal")]
	private static extern void mpire_nxus_measurement_track_event_with_params (string eventName, string attributes);

	[DllImport("__Internal")]
	private static extern void mpire_nxus_measurement_track_event_install (string attributes);

	[DllImport("__Internal")]
	private static extern void mpire_nxus_measurement_track_event_open (string attributes);

	[DllImport("__Internal")]
	private static extern void mpire_nxus_measurement_track_event_registration (string attributes);

	[DllImport("__Internal")]
	private static extern void mpire_nxus_measurement_track_event_purchase (string attributes);

	[DllImport("__Internal")]
	private static extern void mpire_nxus_measurement_track_event_level (string attributes);

	[DllImport("__Internal")]
	private static extern void mpire_nxus_measurement_track_event_tutorial (string attributes);

	[DllImport("__Internal")]
	private static extern void mpire_nxus_measurement_track_event_add_to_cart (string attributes);

	[DllImport("__Internal")]
	private static extern void mpire_nxus_measurement_track_event_checkout (string attributes);

	[DllImport("__Internal")]
	private static extern void mpire_nxus_measurement_track_event_invite (string attributes);

	[DllImport("__Internal")]
	private static extern void mpire_nxus_measurement_track_event_achievement (string attributes);
    #endregion

    #region Public methods
	public void mpireNxusMeasurementInitializeLibrary () {
		Debug.Log ("NxusDSP instance == null. Initializing...");
		mpire_nxus_measurement_set_sdk_platform("ios_unity");
		mpire_nxus_measurement_debugging_enabled(this.debuggingEnabled);
		mpire_nxus_measurement_initialize_library(this.apiKey);
	}

	public void mpireNxusMeasurementTrackEvent (string eventName) {
		mpire_nxus_measurement_track_event(eventName);
	}

	public void mpireNxusMeasurementTrackEventWithParams (string eventName, string attributes) {
		mpire_nxus_measurement_track_event_with_params(eventName, attributes);
	}

	public void mpireNxusMeasurementTrackEventInstall (string attributes) {
		mpire_nxus_measurement_track_event_install(attributes);
	}

	public void mpireNxusMeasurementTrackEventOpen (string attributes) {
		mpire_nxus_measurement_track_event_open(attributes);
	}

	public void mpireNxusMeasurementTrackEventRegistration (string attributes) {
		mpire_nxus_measurement_track_event_registration(attributes);
	}

	public void mpireNxusMeasurementTrackEventPurchase (string attributes) {
		mpire_nxus_measurement_track_event_purchase(attributes);
	}

	public void mpireNxusMeasurementTrackEventLevel (string attributes) {
		mpire_nxus_measurement_track_event_level(attributes);
	}

	public void mpireNxusMeasurementTrackEventTutorial (string attributes) {
		mpire_nxus_measurement_track_event_tutorial(attributes);
	}

	public void mpireNxusMeasurementTrackEventAddToCart (string attributes) {
		mpire_nxus_measurement_track_event_add_to_cart(attributes);
	}

	public void mpireNxusMeasurementTrackEventCheckout (string attributes) {
		mpire_nxus_measurement_track_event_checkout(attributes);
	}

	public void mpireNxusMeasurementTrackEventInvite (string attributes) {
		mpire_nxus_measurement_track_event_invite(attributes);
	}

	public void mpireNxusMeasurementTrackEventAchievement (string attributes) {
		mpire_nxus_measurement_track_event_achievement(attributes);
	}
    #endregion

	#elif UNITY_ANDROID
    #region Public methods
	public void mpireNxusMeasurementInitializeLibrary () {
		Debug.Log ("MpireNxusMeasurement instance == null. Initializing...");
		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.measurement.MpireNxusMeasurement");
		AndroidJavaClass unityPlayer = new AndroidJavaClass ("com.unity3d.player.UnityPlayer");
		AndroidJavaObject mCurrentActivity = unityPlayer.GetStatic<AndroidJavaObject> ("currentActivity");
		nxusDspTrackerClass.CallStatic("setSdkPlatform", "android_unity");
		nxusDspTrackerClass.CallStatic("setDebugginEnabled", this.debuggingEnabled);
		nxusDspTrackerClass.CallStatic("initializeLibraryWithApiKey", mCurrentActivity, this.apiKey);
	}

	public void mpireNxusMeasurementTrackEvent (string eventName) {
		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.measurement.MpireNxusMeasurement");
		nxusDspTrackerClass.CallStatic("trackEvent", eventName);
	}

	public void mpireNxusMeasurementTrackEventWithParams (string eventName, string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.measurement.tracking.TrackingParams");
		AndroidJavaObject trackingParams = trackingParamsClass.CallStatic<AndroidJavaObject>("instantiateFromString", attributes);
		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.measurement.MpireNxusMeasurement");
		nxusDspTrackerClass.CallStatic("trackEvent", eventName, trackingParamsClass);
	}

	public void mpireNxusMeasurementTrackEventInstall (string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.measurement.tracking.TrackingParams");
		AndroidJavaObject trackingParams = trackingParamsClass.CallStatic<AndroidJavaObject>("instantiateFromString", attributes);
		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.measurement.MpireNxusMeasurement");
		nxusDspTrackerClass.CallStatic("trackEventInstall", trackingParams);
	}

	public void mpireNxusMeasurementTrackEventOpen (string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.measurement.tracking.TrackingParams");
		AndroidJavaObject trackingParams = trackingParamsClass.CallStatic<AndroidJavaObject>("instantiateFromString", attributes);
		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.measurement.MpireNxusMeasurement");
		nxusDspTrackerClass.CallStatic("trackEventOpen", trackingParams);
	}

	public void mpireNxusMeasurementTrackEventRegistration (string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.measurement.tracking.TrackingParams");
		AndroidJavaObject trackingParams = trackingParamsClass.CallStatic<AndroidJavaObject>("instantiateFromString", attributes);
		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.measurement.MpireNxusMeasurement");
		nxusDspTrackerClass.CallStatic("trackEventRegistration", trackingParams);
	}

	public void mpireNxusMeasurementTrackEventPurchase (string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.measurement.tracking.TrackingParams");
		AndroidJavaObject trackingParams = trackingParamsClass.CallStatic<AndroidJavaObject>("instantiateFromString", attributes);
		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.measurement.MpireNxusMeasurement");
		nxusDspTrackerClass.CallStatic("trackEventPurchase", trackingParams);
	}

	public void mpireNxusMeasurementTrackEventLevel (string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.measurement.tracking.TrackingParams");
		AndroidJavaObject trackingParams = trackingParamsClass.CallStatic<AndroidJavaObject>("instantiateFromString", attributes);
		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.measurement.MpireNxusMeasurement");
		nxusDspTrackerClass.CallStatic("trackEventLevel", trackingParams);
	}

	public void mpireNxusMeasurementTrackEventTutorial (string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.measurement.tracking.TrackingParams");
		AndroidJavaObject trackingParams = trackingParamsClass.CallStatic<AndroidJavaObject>("instantiateFromString", attributes);
		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.measurement.MpireNxusMeasurement");
		nxusDspTrackerClass.CallStatic("trackEventTutorial", trackingParams);
	}

	public void mpireNxusMeasurementTrackEventAddToCart (string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.measurement.tracking.TrackingParams");
		AndroidJavaObject trackingParams = trackingParamsClass.CallStatic<AndroidJavaObject>("instantiateFromString", attributes);
		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.measurement.MpireNxusMeasurement");
		nxusDspTrackerClass.CallStatic("trackEventAddToCart", trackingParams);
	}

	public void mpireNxusMeasurementTrackEventCheckout (string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.measurement.tracking.TrackingParams");
		AndroidJavaObject trackingParams = trackingParamsClass.CallStatic<AndroidJavaObject>("instantiateFromString", attributes);
		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.measurement.MpireNxusMeasurement");
		nxusDspTrackerClass.CallStatic("trackEventCheckout", trackingParams);
	}

	public void mpireNxusMeasurementTrackEventInvite (string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.measurement.tracking.TrackingParams");
		AndroidJavaObject trackingParams = trackingParamsClass.CallStatic<AndroidJavaObject>("instantiateFromString", attributes);
		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.measurement.MpireNxusMeasurement");
		nxusDspTrackerClass.CallStatic("trackEventInvite", trackingParams);
	}

	public void mpireNxusMeasurementTrackEventAchievement (string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.measurement.tracking.TrackingParams");
		AndroidJavaObject trackingParams = trackingParamsClass.CallStatic<AndroidJavaObject>("instantiateFromString", attributes);
		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.measurement.MpireNxusMeasurement");
		nxusDspTrackerClass.CallStatic("trackEventAchievement", trackingParams);
	}
    #endregion
	#endif

}
