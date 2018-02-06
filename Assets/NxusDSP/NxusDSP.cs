using UnityEngine;
using System.Collections;
using System.Runtime.InteropServices;
using System.Collections.Generic;

public class NxusDSP : MonoBehaviour {

	public bool debuggingEnabled = true;
	public string apiKey = "{Your API key here}";

	private static NxusDSP instance = null;

	public NxusDSP () {}

	private NxusDSP (bool debuggingEnabled, string apiKey) {
		this.debuggingEnabled = debuggingEnabled;
		this.apiKey = apiKey;
	}

	void Awake () {
		Debug.Log ("NxusDSP Awake");
		Debug.Log ("Awake - debuggingEnabled: " + debuggingEnabled);
		Debug.Log ("Awake - apiKey: " + apiKey);
		if (NxusDSP.instance == null) {
			NxusDSP.instance = new NxusDSP (debuggingEnabled, apiKey);
			NxusDSP.instance.nxusDspInitializeLibrary ();
		}
	}

	public static void trackEvent(string eventName) {
		Debug.Log ("NxusDSP trackEvent - check instance");
		if (NxusDSP.instance != null) {
			Debug.Log ("NxusDSP trackEvent - instance existing, tracking event");
			NxusDSP.instance.nxusDspTrackEvent(eventName);
		}
	}

	public static void trackEventWithParams(string eventName, Dictionary<string, string> attributes) {
		Debug.Log ("NxusDSP trackEventWithParams - check instance");
		if (NxusDSP.instance != null) {
			Debug.Log ("NxusDSP trackEventWithParams - instance existing, tracking event");
			string attributesString = "";
			foreach(KeyValuePair<string, string> kvp in attributes) {
				attributesString += kvp.Key + "=" + kvp.Value + "\n";
			}
			Debug.Log ("NxusDSP trackEventWithParams attributes: " + attributesString);
			NxusDSP.instance.nxusDspTrackEventWithParams (eventName, attributesString);
		}
	}

	public static void trackEventInstall(Dictionary<string, string> attributes) {
		Debug.Log ("NxusDSP trackEventInstall - check instance");
		if (NxusDSP.instance != null) {
			Debug.Log ("NxusDSP trackEventInstall - instance existing, tracking event");
			string attributesString = "";
			foreach(KeyValuePair<string, string> kvp in attributes) {
				attributesString += kvp.Key + "=" + kvp.Value + "\n";
			}
			Debug.Log ("NxusDSP trackEventInstall attributes: " + attributesString);
			NxusDSP.instance.nxusDspTrackEventInstall (attributesString);
		}
	}

	public static void trackEventOpen(Dictionary<string, string> attributes) {
		Debug.Log ("NxusDSP trackEventOpen - check instance");
		if (NxusDSP.instance != null) {
			Debug.Log ("NxusDSP trackEventOpen - instance existing, tracking event");
			string attributesString = "";
			foreach(KeyValuePair<string, string> kvp in attributes) {
				attributesString += kvp.Key + "=" + kvp.Value + "\n";
			}
			Debug.Log ("NxusDSP trackEventOpen attributes: " + attributesString);
			NxusDSP.instance.nxusDspTrackEventOpen (attributesString);
		}
	}

	public static void trackEventRegistration(Dictionary<string, string> attributes) {
		Debug.Log ("NxusDSP trackEventRegistration - check instance");
		if (NxusDSP.instance != null) {
			Debug.Log ("NxusDSP trackEventRegistration - instance existing, tracking event");
			string attributesString = "";
			foreach(KeyValuePair<string, string> kvp in attributes) {
				attributesString += kvp.Key + "=" + kvp.Value + "\n";
			}
			Debug.Log ("NxusDSP trackEventRegistration attributes: " + attributesString);
			NxusDSP.instance.nxusDspTrackEventRegistration (attributesString);
		}
	}

	public static void trackEventPurchase(Dictionary<string, string> attributes) {
		Debug.Log ("NxusDSP trackEventPurchase - check instance");
		if (NxusDSP.instance != null) {
			Debug.Log ("NxusDSP trackEventPurchase - instance existing, tracking event");
			string attributesString = "";
			foreach(KeyValuePair<string, string> kvp in attributes) {
				attributesString += kvp.Key + "=" + kvp.Value + "\n";
			}
			Debug.Log ("NxusDSP trackEventPurchase attributes: " + attributesString);
			NxusDSP.instance.nxusDspTrackEventPurchase (attributesString);
		}
	}

	public static void trackEventLevel(Dictionary<string, string> attributes) {
		Debug.Log ("NxusDSP trackEventLevel - check instance");
		if (NxusDSP.instance != null) {
			Debug.Log ("NxusDSP trackEventLevel - instance existing, tracking event");
			string attributesString = "";
			foreach(KeyValuePair<string, string> kvp in attributes) {
				attributesString += kvp.Key + "=" + kvp.Value + "\n";
			}
			Debug.Log ("NxusDSP trackEventLevel attributes: " + attributesString);
			NxusDSP.instance.nxusDspTrackEventLevel (attributesString);
		}
	}

	public static void trackEventTutorial(Dictionary<string, string> attributes) {
		Debug.Log ("NxusDSP trackEventTutorial - check instance");
		if (NxusDSP.instance != null) {
			Debug.Log ("NxusDSP trackEventTutorial - instance existing, tracking event");
			string attributesString = "";
			foreach(KeyValuePair<string, string> kvp in attributes) {
				attributesString += kvp.Key + "=" + kvp.Value + "\n";
			}
			Debug.Log ("NxusDSP trackEventTutorial attributes: " + attributesString);
			NxusDSP.instance.nxusDspTrackEventTutorial (attributesString);
		}
	}

	public static void trackEventAddToCart(Dictionary<string, string> attributes) {
		Debug.Log ("NxusDSP trackEventAddToCart - check instance");
		if (NxusDSP.instance != null) {
			Debug.Log ("NxusDSP trackEventAddToCart - instance existing, tracking event");
			string attributesString = "";
			foreach(KeyValuePair<string, string> kvp in attributes) {
				attributesString += kvp.Key + "=" + kvp.Value + "\n";
			}
			Debug.Log ("NxusDSP trackEventAddToCart attributes: " + attributesString);
			NxusDSP.instance.nxusDspTrackEventAddToCart (attributesString);
		}
	}

	public static void trackEventCheckout(Dictionary<string, string> attributes) {
		Debug.Log ("NxusDSP trackEventCheckout - check instance");
		if (NxusDSP.instance != null) {
			Debug.Log ("NxusDSP trackEventCheckout - instance existing, tracking event");
			string attributesString = "";
			foreach(KeyValuePair<string, string> kvp in attributes) {
				attributesString += kvp.Key + "=" + kvp.Value + "\n";
			}
			Debug.Log ("NxusDSP trackEventCheckout attributes: " + attributesString);
			NxusDSP.instance.nxusDspTrackEventCheckout (attributesString);
		}
	}

	public static void trackEventInvite(Dictionary<string, string> attributes) {
		Debug.Log ("NxusDSP trackEventInvite - check instance");
		if (NxusDSP.instance != null) {
			Debug.Log ("NxusDSP trackEventInvite - instance existing, tracking event");
			string attributesString = "";
			foreach(KeyValuePair<string, string> kvp in attributes) {
				attributesString += kvp.Key + "=" + kvp.Value + "\n";
			}
			Debug.Log ("NxusDSP trackEventInvite attributes: " + attributesString);
			NxusDSP.instance.nxusDspTrackEventInvite (attributesString);
		}
	}

	public static void trackEventAchievement(Dictionary<string, string> attributes) {
		Debug.Log ("NxusDSP trackEventAchievement - check instance");
		if (NxusDSP.instance != null) {
			Debug.Log ("NxusDSP trackEventAchievement - instance existing, tracking event");
			string attributesString = "";
			foreach(KeyValuePair<string, string> kvp in attributes) {
				attributesString += kvp.Key + "=" + kvp.Value + "\n";
			}
			Debug.Log ("NxusDSP trackEventAchievement attributes: " + attributesString);
			NxusDSP.instance.nxusDspTrackEventAchievement (attributesString);
		}
	}

	#if UNITY_EDITOR
	#region Public methods
	public void nxusDspInitializeLibrary () {
		// Empty
	}

	public void nxusDspTrackEvent (string eventName) {
		// Empty
	}

	public void nxusDspTrackEventWithParams (string eventName, string attributes) {
		// Empty
	}

	public void nxusDspTrackEventInstall (string attributes) {
		// Empty
	}

	public void nxusDspTrackEventOpen (string attributes) {
		// Empty
	}

	public void nxusDspTrackEventRegistration (string attributes) {
		// Empty
	}

	public void nxusDspTrackEventPurchase (string attributes) {
		// Empty
	}

	public void nxusDspTrackEventLevel (string attributes) {
		// Empty
	}

	public void nxusDspTrackEventTutorial (string attributes) {
		// Empty
	}

	public void nxusDspTrackEventAddToCart (string attributes) {
		// Empty
	}

	public void nxusDspTrackEventCheckout (string attributes) {
		// Empty
	}

	public void nxusDspTrackEventInvite (string attributes) {
		// Empty
	}

	public void nxusDspTrackEventAchievement (string attributes) {
		// Empty
	}
    #endregion

	#elif UNITY_IOS
    #region External methods
	[DllImport("__Internal")]
	private static extern void nxus_dsp_set_sdk_platform (string platform);

	[DllImport("__Internal")]
	private static extern void nxus_dsp_debugging_enabled (bool enabled);

	[DllImport("__Internal")]
	private static extern void nxus_dsp_initialize_library (string key);

	[DllImport("__Internal")]
	private static extern void nxus_dsp_track_event (string eventName);

	[DllImport("__Internal")]
	private static extern void nxus_dsp_track_event_with_params (string eventName, string attributes);

	[DllImport("__Internal")]
	private static extern void nxus_dsp_track_event_install (string attributes);

	[DllImport("__Internal")]
	private static extern void nxus_dsp_track_event_open (string attributes);

	[DllImport("__Internal")]
	private static extern void nxus_dsp_track_event_registration (string attributes);

	[DllImport("__Internal")]
	private static extern void nxus_dsp_track_event_purchase (string attributes);

	[DllImport("__Internal")]
	private static extern void nxus_dsp_track_event_level (string attributes);

	[DllImport("__Internal")]
	private static extern void nxus_dsp_track_event_tutorial (string attributes);

	[DllImport("__Internal")]
	private static extern void nxus_dsp_track_event_add_to_cart (string attributes);

	[DllImport("__Internal")]
	private static extern void nxus_dsp_track_event_checkout (string attributes);

	[DllImport("__Internal")]
	private static extern void nxus_dsp_track_event_invite (string attributes);

	[DllImport("__Internal")]
	private static extern void nxus_dsp_track_event_achievement (string attributes);
    #endregion

    #region Public methods
	public void nxusDspInitializeLibrary () {
		Debug.Log ("NxusDSP instance == null. Initializing...");
		nxus_dsp_set_sdk_platform("ios_unity");
		nxus_dsp_debugging_enabled(this.debuggingEnabled);
		nxus_dsp_initialize_library(this.apiKey);
	}

	public void nxusDspTrackEvent (string eventName) {
		nxus_dsp_track_event(eventName);
	}

	public void nxusDspTrackEventWithParams (string eventName, string attributes) {
		nxus_dsp_track_event_with_params(eventName, attributes);
	}

	public void nxusDspTrackEventInstall (string attributes) {
		nxus_dsp_track_event_install(attributes);
	}

	public void nxusDspTrackEventOpen (string attributes) {
		nxus_dsp_track_event_open(attributes);
	}

	public void nxusDspTrackEventRegistration (string attributes) {
		nxus_dsp_track_event_registration(attributes);
	}

	public void nxusDspTrackEventPurchase (string attributes) {
		nxus_dsp_track_event_purchase(attributes);
	}

	public void nxusDspTrackEventLevel (string attributes) {
		nxus_dsp_track_event_level(attributes);
	}

	public void nxusDspTrackEventTutorial (string attributes) {
		nxus_dsp_track_event_tutorial(attributes);
	}

	public void nxusDspTrackEventAddToCart (string attributes) {
		nxus_dsp_track_event_add_to_cart(attributes);
	}

	public void nxusDspTrackEventCheckout (string attributes) {
		nxus_dsp_track_event_checkout(attributes);
	}

	public void nxusDspTrackEventInvite (string attributes) {
		nxus_dsp_track_event_invite(attributes);
	}

	public void nxusDspTrackEventAchievement (string attributes) {
		nxus_dsp_track_event_achievement(attributes);
	}
    #endregion

	#elif UNITY_ANDROID
    #region Public methods
	public void nxusDspInitializeLibrary () {
		Debug.Log ("NxusDSP instance == null. Initializing...");
		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.dsp.NxusDSPTracker");
		AndroidJavaClass unityPlayer = new AndroidJavaClass ("com.unity3d.player.UnityPlayer");
		AndroidJavaObject mCurrentActivity = unityPlayer.GetStatic<AndroidJavaObject> ("currentActivity");
		nxusDspTrackerClass.CallStatic("setSdkPlatform", "android_unity");
		nxusDspTrackerClass.CallStatic("setDebugginEnabled", this.debuggingEnabled);
		nxusDspTrackerClass.CallStatic("initializeLibraryWithApiKey", mCurrentActivity, this.apiKey);
	}

	public void nxusDspTrackEvent (string eventName) {
		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.dsp.NxusDSPTracker");
		nxusDspTrackerClass.CallStatic("trackEvent", eventName);
	}

	public void nxusDspTrackEventWithParams (string eventName, string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.dsp.tracking.TrackingParams");

		string[] attrs = attributes.Split (new string[] {"\n"}, System.StringSplitOptions.None);
		foreach (string att in attrs) {
			string[] attDetails = att.Split (new string[] {"="}, System.StringSplitOptions.None);
			trackingParamsClass.Call ("put", attDetails[0], attDetails[1]);
			Debug.Log ("NxusDSP Android Tracking Param: key=" + attDetails[0] + "; value=" + attDetails[1]);
		}

		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.dsp.NxusDSPTracker");
		nxusDspTrackerClass.CallStatic("trackEvent", eventName, trackingParamsClass);
	}

	public void nxusDspTrackEventInstall (string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.dsp.tracking.TrackingParams");

		string[] attrs = attributes.Split (new string[] {"\n"}, System.StringSplitOptions.None);
		foreach (string att in attrs) {
			string[] attDetails = att.Split (new string[] {"="}, System.StringSplitOptions.None);
			trackingParamsClass.Call ("put", attDetails[0], attDetails[1]);
			Debug.Log ("NxusDSP Android Tracking Param: key=" + attDetails[0] + "; value=" + attDetails[1]);
		}

		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.dsp.NxusDSPTracker");
		nxusDspTrackerClass.CallStatic("trackEventInstall", trackingParamsClass);
	}

	public void nxusDspTrackEventOpen (string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.dsp.tracking.TrackingParams");

		string[] attrs = attributes.Split (new string[] {"\n"}, System.StringSplitOptions.None);
		foreach (string att in attrs) {
			string[] attDetails = att.Split (new string[] {"="}, System.StringSplitOptions.None);
			trackingParamsClass.Call ("put", attDetails[0], attDetails[1]);
			Debug.Log ("NxusDSP Android Tracking Param: key=" + attDetails[0] + "; value=" + attDetails[1]);
		}

		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.dsp.NxusDSPTracker");
		nxusDspTrackerClass.CallStatic("trackEventOpen", trackingParamsClass);
	}

	public void nxusDspTrackEventRegistration (string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.dsp.tracking.TrackingParams");

		string[] attrs = attributes.Split (new string[] {"\n"}, System.StringSplitOptions.None);
		foreach (string att in attrs) {
			string[] attDetails = att.Split (new string[] {"="}, System.StringSplitOptions.None);
			trackingParamsClass.Call ("put", attDetails[0], attDetails[1]);
			Debug.Log ("NxusDSP Android Tracking Param: key=" + attDetails[0] + "; value=" + attDetails[1]);
		}

		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.dsp.NxusDSPTracker");
		nxusDspTrackerClass.CallStatic("trackEventRegistration", trackingParamsClass);
	}

	public void nxusDspTrackEventPurchase (string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.dsp.tracking.TrackingParams");

		string[] attrs = attributes.Split (new string[] {"\n"}, System.StringSplitOptions.None);
		foreach (string att in attrs) {
			string[] attDetails = att.Split (new string[] {"="}, System.StringSplitOptions.None);
			trackingParamsClass.Call ("put", attDetails[0], attDetails[1]);
			Debug.Log ("NxusDSP Android Tracking Param: key=" + attDetails[0] + "; value=" + attDetails[1]);
		}

		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.dsp.NxusDSPTracker");
		nxusDspTrackerClass.CallStatic("trackEventPurchase", trackingParamsClass);
	}

	public void nxusDspTrackEventLevel (string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.dsp.tracking.TrackingParams");

		string[] attrs = attributes.Split (new string[] {"\n"}, System.StringSplitOptions.None);
		foreach (string att in attrs) {
			string[] attDetails = att.Split (new string[] {"="}, System.StringSplitOptions.None);
			trackingParamsClass.Call ("put", attDetails[0], attDetails[1]);
			Debug.Log ("NxusDSP Android Tracking Param: key=" + attDetails[0] + "; value=" + attDetails[1]);
		}

		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.dsp.NxusDSPTracker");
		nxusDspTrackerClass.CallStatic("trackEventLevel", trackingParamsClass);
	}

	public void nxusDspTrackEventTutorial (string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.dsp.tracking.TrackingParams");

		string[] attrs = attributes.Split (new string[] {"\n"}, System.StringSplitOptions.None);
		foreach (string att in attrs) {
			string[] attDetails = att.Split (new string[] {"="}, System.StringSplitOptions.None);
			trackingParamsClass.Call ("put", attDetails[0], attDetails[1]);
			Debug.Log ("NxusDSP Android Tracking Param: key=" + attDetails[0] + "; value=" + attDetails[1]);
		}

		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.dsp.NxusDSPTracker");
		nxusDspTrackerClass.CallStatic("trackEventTutorial", trackingParamsClass);
	}

	public void nxusDspTrackEventAddToCart (string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.dsp.tracking.TrackingParams");

		string[] attrs = attributes.Split (new string[] {"\n"}, System.StringSplitOptions.None);
		foreach (string att in attrs) {
			string[] attDetails = att.Split (new string[] {"="}, System.StringSplitOptions.None);
			trackingParamsClass.Call ("put", attDetails[0], attDetails[1]);
			Debug.Log ("NxusDSP Android Tracking Param: key=" + attDetails[0] + "; value=" + attDetails[1]);
		}

		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.dsp.NxusDSPTracker");
		nxusDspTrackerClass.CallStatic("trackEventAddToCart", trackingParamsClass);
	}

	public void nxusDspTrackEventCheckout (string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.dsp.tracking.TrackingParams");

		string[] attrs = attributes.Split (new string[] {"\n"}, System.StringSplitOptions.None);
		foreach (string att in attrs) {
			string[] attDetails = att.Split (new string[] {"="}, System.StringSplitOptions.None);
			trackingParamsClass.Call ("put", attDetails[0], attDetails[1]);
			Debug.Log ("NxusDSP Android Tracking Param: key=" + attDetails[0] + "; value=" + attDetails[1]);
		}

		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.dsp.NxusDSPTracker");
		nxusDspTrackerClass.CallStatic("trackEventCheckout", trackingParamsClass);
	}

	public void nxusDspTrackEventInvite (string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.dsp.tracking.TrackingParams");

		string[] attrs = attributes.Split (new string[] {"\n"}, System.StringSplitOptions.None);
		foreach (string att in attrs) {
			string[] attDetails = att.Split (new string[] {"="}, System.StringSplitOptions.None);
			trackingParamsClass.Call ("put", attDetails[0], attDetails[1]);
			Debug.Log ("NxusDSP Android Tracking Param: key=" + attDetails[0] + "; value=" + attDetails[1]);
		}

		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.dsp.NxusDSPTracker");
		nxusDspTrackerClass.CallStatic("trackEventInvite", trackingParamsClass);
	}

	public void nxusDspTrackEventAchievement (string attributes) {
		AndroidJavaClass trackingParamsClass = new AndroidJavaClass("com.nxus.dsp.tracking.TrackingParams");

		string[] attrs = attributes.Split (new string[] {"\n"}, System.StringSplitOptions.None);
		foreach (string att in attrs) {
			string[] attDetails = att.Split (new string[] {"="}, System.StringSplitOptions.None);
			trackingParamsClass.Call ("put", attDetails[0], attDetails[1]);
			Debug.Log ("NxusDSP Android Tracking Param: key=" + attDetails[0] + "; value=" + attDetails[1]);
		}

		AndroidJavaClass nxusDspTrackerClass = new AndroidJavaClass("com.nxus.dsp.NxusDSPTracker");
		nxusDspTrackerClass.CallStatic("trackEventAchievement", trackingParamsClass);
	}
    #endregion
	#endif

}
