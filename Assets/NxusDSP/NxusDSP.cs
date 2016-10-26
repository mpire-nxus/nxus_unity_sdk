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
    #endregion

	#elif UNITY_WEBGL
    #region Public methods
    public void nxusDspInitializeLibrary()
    {
        // Empty
    }

    public void nxusDspTrackEvent(string eventName)
    {
        // Empty
    }

    public void nxusDspTrackEventWithParams(string eventName, string attributes)
    {
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
    #endregion
	#endif

}
