#!/usr/bin/env python

import argparse
import errno
import shutil
import os.path
import sys
from xml.dom.minidom import parse, parseString

def main():
    parser = argparse.ArgumentParser(description="MpireNxusMeasurement post build android script")
    parser.add_argument('assets_path', help="path to the assets folder of unity3d")
    
    # Pre build must be set manually.
    parser.add_argument('--pre-build', action="store_true", help="used to check and change the AndroidManifest.xml to conform to the MpireNxusMeasurement")
    exit_code = 0
    
    with open('MpireNxusMeasurementPostBuildAndroidLog.txt', 'w') as fileLog:
        # Log function with file injected.
        LogFunc = LogInput(fileLog)
        
        # Get the path of the android plugin folder.
        android_plugin_path, nxusdsp_android_path, pre_build = parse_input(LogFunc, parser)

        # Try to open an existing manifest file.
        try:
            manifest_path = os.path.join(android_plugin_path + "AndroidManifest.xml")
            edited_xml = None
            
            with open(manifest_path, 'r+') as mf:
                check_dic = check_manifest(LogFunc, mf)
                
                # Check if manifest has all changes needed.
                all_check = check_dic["has_nxusdsp_receiver"] and \
                            check_dic["has_internet_permission"] and \
                            check_dic["has_access_network_state_permission"]
                
                # Edit manifest if has any change missing.
                if not all_check:
                    # Warn unity if it was pos-build, if something is missing.
                    if not pre_build:
                        LogFunc("Android manifest used in unity did not " + \
                                "had all the changes MpireNxusMeasurement needs. " + \
                                "Please build again the package.")
                    edited_xml = edit_manifest(LogFunc, mf, check_dic, android_plugin_path)
            
            # Write changed xml
            if edited_xml:
                with open(manifest_path, 'w+') as mf:
                    edited_xml.writexml(mf)
                exit_code = 1
        except IOError as ioe:
            # If it does not exist,
            if ioe.errno == errno.ENOENT:
                # warn Unity that needed manifest wasn't used.
                if not pre_build:
                    LogFunc("Used default Android manifest file from " + \
                            "unity. Please build again the package to " +
                            "include the changes for MpireNxusMeasurement")
                copy_nxusdsp_manifest(LogFunc, android_plugin_path, nxusdsp_android_path)
                exit_code = 1
            else:
                LogFunc(ioe)
        except Exception as e:
            LogFunc(e)

    # Exit with return code for Unity.
    sys.exit(exit_code)

def edit_manifest(Log, manifest_file, check_dic, android_plugin_path):
    manifest_xml = check_dic["manifest_xml"]

    # Add the nxusDSP install referrer to the application element.
    if not check_dic["has_nxusdsp_receiver"]:
        receiver_string = """<?xml version="1.0" ?>
        <receiver
            xmlns:android="http://schemas.android.com/apk/res/android"
            android:name="com.nxus.measurement.receivers.InstallReceiver"
            android:exported="true" >
            <intent-filter>
                <action android:name="com.android.vending.INSTALL_REFERRER" />
            </intent-filter>
        </receiver>
        """
        receiver_xml = parseString(receiver_string)
        receiver_xml.documentElement.removeAttribute("xmlns:android")

        for app_element in manifest_xml.getElementsByTagName("application"):
            app_element.appendChild(receiver_xml.documentElement)
        
        Log("Successfully added the MpireNxusMeasurement install referrer receiver")

    # Add the internet permission to the manifest element
    if not check_dic["has_internet_permission"]:
        ip_element = manifest_xml.createElement("uses-permission")
        ip_element.setAttribute("android:name", "android.permission.INTERNET")
        manifest_xml.documentElement.appendChild(ip_element)
        
        Log("Successfully added INTERNET permission")

    # Add the access network state permission to the manifest element
    if not check_dic["has_access_network_state_permission"]:
        ip_element = manifest_xml.createElement("uses-permission")
        ip_element.setAttribute("android:name", "android.permission.ACCESS_NETWORK_STATE")
        manifest_xml.documentElement.appendChild(ip_element)
        
        Log("Successfully added ACCESS_NETWORK_STATE permission")

    # Log(manifest_xml.toxml())
    return manifest_xml

def check_manifest(Log, manifest_file):
    
    manifest_xml = parse(manifest_file)
    # Log(manifest_xml.toxml())
    
    has_nxusdsp_receiver = has_element_attr(manifest_xml, "receiver", "android:name", "com.nxus.measurement.receivers.InstallReceiver")
    Log("Does manifest have nxusDSP install referrer receiver?: {0}", has_nxusdsp_receiver)

    has_internet_permission = has_element_attr(manifest_xml, "uses-permission", "android:name", "android.permission.INTERNET")
    Log("Does manifest have INTERNET permission?: {0}", has_internet_permission)
    
    has_access_network_state_permission = has_element_attr(manifest_xml, "uses-permission", "android:name", "android.permission.ACCESS_NETWORK_STATE")
    Log("Does manifest have ACCESS_NETWORK_STATE permission?: {0}", has_access_network_state_permission)

    return {"manifest_xml" : manifest_xml,
            "has_nxusdsp_receiver" : has_nxusdsp_receiver,
            "has_internet_permission" : has_internet_permission,
            "has_access_network_state_permission" : has_access_network_state_permission}

def has_element_attr(xml_dom, tag_name, attr_name, attr_value):
    for node in xml_dom.getElementsByTagName(tag_name):
        attr_dom = node.getAttribute(attr_name)
        if attr_dom == attr_value:
            return True
    return False

def copy_nxusdsp_manifest(Log, android_plugin_path, nxusdsp_android_path):
    nxusdsp_manifest_path = os.path.join(nxusdsp_android_path, "MpireNxusMeasurementAndroidManifest.xml")
    new_manifest_path = os.path.join(android_plugin_path, "AndroidManifest.xml")

    if not os.path.exists(android_plugin_path):
        os.makedirs(android_plugin_path)

    try:
        shutil.copyfile(nxusdsp_manifest_path, new_manifest_path)
    except Exception as e:
        Log(e)
    else:
        Log("Manifest copied from {0} to {1}", nxusdsp_manifest_path, new_manifest_path)

def LogInput(writeObject):
    def Log(message, *args):
        messageNLine = str(message) + "\n"
        writeObject.write(messageNLine.format(*args))
    return Log

def parse_input(Log, parser):
    args, ignored_args = parser.parse_known_args()
    assets_path = args.assets_path

    android_plugin_path = os.path.join(assets_path, "Plugins/Android/")
    nxusdsp_android_path = os.path.join(assets_path, "MpireNxusMeasurement/Android/");

    Log("Android plugin path: {0}", android_plugin_path)
    Log("Android MpireNxusMeasurement path: {0}", nxusdsp_android_path)

    return android_plugin_path, nxusdsp_android_path, args.pre_build

if __name__ == "__main__":
    main()
