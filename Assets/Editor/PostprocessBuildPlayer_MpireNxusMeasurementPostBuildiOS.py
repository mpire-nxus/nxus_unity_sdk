#!/usr/bin/env python

import sys
import re
from subprocess import Popen, PIPE
import argparse

from mod_pbxproj import XcodeProject

def main():
    parser = argparse.ArgumentParser(description="MpireNxusMeasurement post build iOS script")
    parser.add_argument('ios_project_path', help="path to the folder of the iOS project generated by unity3d")
    
    with open('MpireNxusMeasurementPostBuildiOSLog.txt', 'w') as fileLog:
        # Log function with file injected.
        LogFunc = LogInput(fileLog)
       
        # Path of the Xcode SDK on the system.
        xcode_sdk_path = get_xcode_sdk_path(LogFunc)

        # Path for unity iOS Xcode project and framework on the system.
        unity_xcode_project_path, framework_path = get_paths(LogFunc, parser, xcode_sdk_path)

        # Edit the Xcode project using mod_pbxproj:
        #  - Add the adSupport framework library.
        #  - Add the iAd framework library.
        #  - Change the compilation flags of the adjust project files to support non-ARC.
        edit_unity_xcode_project(LogFunc, unity_xcode_project_path, framework_path)

        # Removed.
        # Change the Xcode project directly:
        #  - Allow objective-c exceptions
        # rewrite_unity_xcode_project(LogFunc, unity_xcode_project_path)
    sys.exit(0)

def LogInput(writeObject):
    def Log(message, *args):
        messageNLine = (message if message else "None") + "\n"
        writeObject.write(messageNLine.format(*args))
    return Log

def get_paths(Log, parser, xcode_sdk_path):
    args, ignored_args = parser.parse_known_args()
    ios_project_path = args.ios_project_path

    unity_xcode_project_path = ios_project_path + "/Unity-iPhone.xcodeproj/project.pbxproj"
    Log("Unity3d Xcode project path: {0}", unity_xcode_project_path)

    framework_path = xcode_sdk_path + "/System/Library/Frameworks/"
    Log("framework path: {0}", framework_path)

    return unity_xcode_project_path, framework_path

def edit_unity_xcode_project(Log, unity_xcode_project_path, framework_path):
    # load unity iOS pbxproj project file
    unity_XcodeProject = XcodeProject.Load(unity_xcode_project_path)

    # add SafariService framework to unity if it's not already there
    # unity_XcodeProject.add_file_if_doesnt_exist(framework_path + "SafariServices.framework", tree="SDKROOT", create_build_files=True,weak=True)
    # Log("added SafariServices framework")

    # add Security framework to unity if it's not already there
    unity_XcodeProject.add_file_if_doesnt_exist(framework_path + "Security.framework", tree="SDKROOT", create_build_files=True,weak=True)
    Log("added Security framework")

    # Add -ObjC to "Other Linker Flags" project settings.
    unity_XcodeProject.add_other_ldflags('-ObjC')

    # Save changes.
    unity_XcodeProject.save()

def rewrite_unity_xcode_project(Log, unity_xcode_project_path):
    unity_xcode_lines = []
    
    # Allow objective-c exceptions
    re_objc_excep = re.compile(r"\s*GCC_ENABLE_OBJC_EXCEPTIONS *= *NO.*")
    with open(unity_xcode_project_path) as upf:
        for line in upf:
            if re_objc_excep.match(line):
                #Log("matched line: {0}", re_objc_excep.match(line).group())
                line = line.replace("NO","YES")
                Log("Objective-c exceptions enabled")
            unity_xcode_lines.append(line)
    with open(unity_xcode_project_path, "w+") as upf:
        upf.writelines(unity_xcode_lines)

def get_xcode_sdk_path(Log):
    # Output all info from Xcode.
    proc = Popen(["xcodebuild", "-version", "-sdk"], stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    
    if proc.returncode not in [0, 66]:
        Log("Could not retrieve Xcode sdk path. code: {0}, err: {1}", proc.returncode, err)
        return None

    match = re.search("iPhoneOS.*?Path: (?P<sdk_path>.*?)\n", out, re.DOTALL)
    xcode_sdk_path = match.group('sdk_path') if match else None
    Log("Xcode sdk path: {0}", xcode_sdk_path)
    return xcode_sdk_path

if __name__ == "__main__":
    main()