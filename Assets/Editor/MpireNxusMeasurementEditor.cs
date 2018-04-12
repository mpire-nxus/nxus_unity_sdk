using System;
using System.IO;
using System.Collections;
using System.Diagnostics;
using System.Text.RegularExpressions;

using UnityEngine;
using UnityEditor;
using UnityEditor.Callbacks;

using System.Runtime.InteropServices;
using System.Collections.Generic;

public class MpireNxusMeasurementEditor : MonoBehaviour
{
    static bool isEnabled = true;
    static string iOSBuildPath = "";

    [PostProcessBuild]
    public static void OnPostprocessBuild (BuildTarget target, string pathToBuiltProject)
    {
        if (!isEnabled)
        {
            return;
        }
			
        var exitCode = RunPostBuildScript (target: target, preBuild: false, pathToBuiltProject: pathToBuiltProject);

        if (exitCode == -1)
        {
            return;
        }

        if (exitCode != 0)
        {
            var errorMessage = GenerateErrorScriptMessage (target, exitCode);
            UnityEngine.Debug.LogError ("MpireNxusMeasurement: " + errorMessage);
        }
    }

    [MenuItem ("Assets/MpireNxusMeasurement/Fix AndroidManifest.xml")]
    static void FixAndroidManifest ()
    {
#if UNITY_ANDROID
        var exitCode = RunPostBuildScript (target: BuildTarget.Android, preBuild: true);

        if (exitCode == 1)
        {
            EditorUtility.DisplayDialog ("MpireNxusMeasurement", 
                                         string.Format("AndroidManifest.xml changed or created at {0}/Plugins/Android/ .", Application.dataPath),
                                         "OK");
        }
        else if (exitCode == 0)
        {
            EditorUtility.DisplayDialog ("MpireNxusMeasurement", "AndroidManifest.xml did not needed to be changed.", "OK");
        }
        else
        {
            EditorUtility.DisplayDialog ("MpireNxusMeasurement", GenerateErrorScriptMessage (BuildTarget.Android, exitCode), "OK");
        }
#else
        EditorUtility.DisplayDialog ("MpireNxusMeasurement", "Option only valid for the Android platform.", "OK");
#endif
    }

    [MenuItem ("Assets/MpireNxusMeasurement/Set iOS build path")]
    static void SetiOSBuildPath ()
    {
#if UNITY_IOS
        MpireNxusMeasurementEditor.iOSBuildPath = EditorUtility.OpenFolderPanel (
            title: "iOs build path",
            folder: EditorUserBuildSettings.GetBuildLocation (BuildTarget.iOS),
            defaultName: "");
        
        if (MpireNxusMeasurementEditor.iOSBuildPath == "")
        {
            UnityEngine.Debug.Log ("iOS build path reset to default path");
        }
        else
        {
            UnityEngine.Debug.Log (string.Format ("iOS build path: {0}", MpireNxusMeasurementEditor.iOSBuildPath));
        }
#else
        EditorUtility.DisplayDialog ("MpireNxusMeasurement", "Option only valid for the iOS platform.", "OK");
#endif
    }

    [MenuItem ("Assets/MpireNxusMeasurement/Change post processing status")]
    static void ChangePostProcessingStatus ()
    {
        isEnabled = !isEnabled;
        EditorUtility.DisplayDialog ("MpireNxusMeasurement", "The post processing for MpireNxusMeasurement is now " + (isEnabled ? "enabled." : "disabled."), "OK");
    }

    static int RunPostBuildScript (BuildTarget target, bool preBuild, string pathToBuiltProject = "")
    {
        string resultContent;
        string arguments = null;
        string pathToScript = null;

        string filePath = System.IO.Path.Combine (Environment.CurrentDirectory, @"Assets/Editor/PostprocessBuildPlayer_MpireNxusMeasurementPostBuildiOS.py");

        // Check if Unity is running on Windows operating system.
        // If yes - fix line endings in python scripts.
        if (Application.platform == RuntimePlatform.WindowsEditor)
        {
            UnityEngine.Debug.Log ("Windows platform");

            using (System.IO.StreamReader streamReader = new System.IO.StreamReader (filePath))
            {
                string fileContent = streamReader.ReadToEnd ();
                resultContent = Regex.Replace (fileContent, @"\r\n|\n\r|\n|\r", "\r\n");
            }

            if (File.Exists (filePath))
            {
                File.WriteAllText (filePath, resultContent);
            }
        }
        else
        {
            UnityEngine.Debug.Log ("Unix platform");

            using (System.IO.StreamReader streamReader = new System.IO.StreamReader (filePath))
            {
                string replaceWith = "\n";
                string fileContent = streamReader.ReadToEnd ();
                
                resultContent = fileContent.Replace ("\r\n", replaceWith);
            }

            if (File.Exists (filePath))
            {
                File.WriteAllText (filePath, resultContent);
            }
        }

        if (target == BuildTarget.Android)
        {
            pathToScript = "/Editor/PostprocessBuildPlayer_MpireNxusMeasurementPostBuildAndroid.py";
            arguments = "\"" + Application.dataPath + "\"";
        
            if (preBuild)
            {
                arguments = "--pre-build " + arguments;
            }
        }
        else if (target == BuildTarget.iOS)
        {
            pathToScript = "/Editor/PostprocessBuildPlayer_MpireNxusMeasurementPostBuildiOS.py";
        
            if (MpireNxusMeasurementEditor.iOSBuildPath == "")
            {
                arguments = "\"" + pathToBuiltProject + "\"";
            }
            else
            {
                arguments = "\"" + MpireNxusMeasurementEditor.iOSBuildPath + "\"";
            }
        }
        else
        {
            return -1;
        }

		UnityEngine.Debug.Log("RUNNING POST BUILD SCRIPT: " + Application.dataPath + pathToScript);

        Process proc = new Process ();
        proc.EnableRaisingEvents = false; 
        proc.StartInfo.FileName = Application.dataPath + pathToScript;
        proc.StartInfo.Arguments = arguments;
        proc.Start ();
        proc.WaitForExit ();
        
        return proc.ExitCode;
    }

    static string GenerateErrorScriptMessage (BuildTarget target, int exitCode)
    {
        if (target == BuildTarget.Android)
        {
            if (exitCode == 1)
            {
                return "The AndroidManifest.xml file was only changed or created after building the package. " +
                        "Please build again the Android Unity package so it can use the new file";
            }
        }

        if (exitCode != 0)
        {
            var message = "Build script exited with error. " +
                          "Please check the MpireNxusMeasurement log file for more information at {0}";
            string projectPath = Application.dataPath.Substring (0, Application.dataPath.Length - 7);
            string logFile = null;
            
            if (target == BuildTarget.Android)
            {
                logFile = projectPath + "/MpireNxusMeasurementPostBuildAndroidLog.txt";
            }
            else if (target == BuildTarget.iOS)
            {
                logFile = projectPath + "/MpireNxusMeasurementPostBuildiOSLog.txt";
            }
            else
            {
                return null;
            }

            return string.Format (message, logFile);
        } 

        return null;
    }
}
