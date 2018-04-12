from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import object
from past.builtins import basestring

import os
import re
import uuid
import copy
import shutil
import datetime


class TreeType:
    ABSOLUTE = u'<absolute>'
    GROUP = u'<group>'
    BUILT_PRODUCTS_DIR = u'BUILT_PRODUCTS_DIR'
    DEVELOPER_DIR = u'DEVELOPER_DIR'
    SDKROOT = u'SDKROOT'
    SOURCE_ROOT = u'SOURCE_ROOT'

    @classmethod
    def options(cls):
        return [TreeType.SOURCE_ROOT, TreeType.SDKROOT, TreeType.GROUP, TreeType.ABSOLUTE,
                TreeType.DEVELOPER_DIR, TreeType.BUILT_PRODUCTS_DIR]


class FileOptions:
    """
    Wrapper class for all file parameters required at the moment of adding a file to the project.
    """
    def __init__(self, create_build_files=True, weak=False, ignore_unknown_type=False, embed_framework=True,
                 code_sign_on_copy=True):
        """
        Creates an object specifying options to be consided during the file creation into the project.

        :param create_build_files: Creates any necessary PBXBuildFile section when adding the file
        :param weak: When adding a framework set it as a weak reference
        :param ignore_unknown_type: Stop insertion if the file type is unknown (Default is false)
        :param embed_framework: When adding a framework sets the embed section
        :param code_sign_on_copy: When embedding a framework, sets the code sign attribute
        """
        self.create_build_files = create_build_files
        self.weak = weak
        self.ignore_unknown_type = ignore_unknown_type
        self.embed_framework = embed_framework
        self.code_sign_on_copy = code_sign_on_copy

    def get_attributes(self, file_ref, build_phase):
        if file_ref.get_file_type() != u'wrapper.framework':
            return None

        attributes = [u'Weak'] if self.weak and build_phase.isa == u'PBXFrameworksBuildPhase' else None
        if file_ref.sourceTree != TreeType.SDKROOT and self.code_sign_on_copy and build_phase.isa == u'PBXCopyFilesBuildPhase':
            if attributes is None:
                attributes = []
            attributes += [u'CodeSignOnCopy', u'RemoveHeadersOnCopy']
        return attributes


class ProjectFiles:
    _FILE_TYPES = {
        u'': (u'text', u'PBXResourcesBuildPhase'),
        u'.a': (u'archive.ar', u'PBXFrameworksBuildPhase'),
        u'.app': (u'wrapper.application', None),
        u'.s': (u'sourcecode.asm', u'PBXSourcesBuildPhase'),
        u'.c': (u'sourcecode.c.c', u'PBXSourcesBuildPhase'),
        u'.cpp': (u'sourcecode.cpp.cpp', u'PBXSourcesBuildPhase'),
        u'.framework': (u'wrapper.framework', u'PBXFrameworksBuildPhase'),
        u'.h': (u'sourcecode.c.h', None),
        u'.hpp': (u'sourcecode.c.h', None),
        u'.pch': (u'sourcecode.c.h', None),
        u'.d': (u'sourcecode.dtrace', u'PBXSourcesBuildPhase'),
        u'.def': (u'text', u'PBXResourcesBuildPhase'),
        u'.swift': (u'sourcecode.swift', u'PBXSourcesBuildPhase'),
        u'.icns': (u'image.icns', u'PBXResourcesBuildPhase'),
        u'.m': (u'sourcecode.c.objc', u'PBXSourcesBuildPhase'),
        u'.j': (u'sourcecode.c.objc', u'PBXSourcesBuildPhase'),
        u'.mm': (u'sourcecode.cpp.objcpp', u'PBXSourcesBuildPhase'),
        u'.nib': (u'wrapper.nib', u'PBXResourcesBuildPhase'),
        u'.plist': (u'text.plist.xml', u'PBXResourcesBuildPhase'),
        u'.json': (u'text.json', u'PBXResourcesBuildPhase'),
        u'.png': (u'image.png', u'PBXResourcesBuildPhase'),
        u'.rtf': (u'text.rtf', u'PBXResourcesBuildPhase'),
        u'.tiff': (u'image.tiff', u'PBXResourcesBuildPhase'),
        u'.txt': (u'text', u'PBXResourcesBuildPhase'),
        u'.xcodeproj': (u'wrapper.pb-project', None),
        u'.xib': (u'file.xib', u'PBXResourcesBuildPhase'),
        u'.strings': (u'text.plist.strings', u'PBXResourcesBuildPhase'),
        u'.bundle': (u'wrapper.plug-in', u'PBXResourcesBuildPhase'),
        u'.dylib': (u'compiled.mach-o.dylib', u'PBXFrameworksBuildPhase'),
        u'.xcdatamodeld': (u'wrapper.xcdatamodel', u'PBXSourcesBuildPhase'),
        u'.xcassets': (u'folder.assetcatalog', u'PBXResourcesBuildPhase'),
        u'.xcconfig': (u'sourcecode.xcconfig', u'PBXSourcesBuildPhase'),
        u'.tbd': (u'sourcecode.text-based-dylib-definition', u'PBXFrameworksBuildPhase'),
    }
    _SPECIAL_FOLDERS = [
        u'.bundle',
        u'.framework',
        u'.xcodeproj',
        u'.xcassets',
        u'.xcdatamodeld',
        u'.storyboardc'
    ]

    def __init__(self):
        raise EnvironmentError('This class cannot be instantiated directly, use XcodeProject instead')

    def add_file(self, path, parent=None, tree=TreeType.SOURCE_ROOT, target_name=None, force=True, file_options=FileOptions()):
        """
        Adds a file to the project, taking care of the type of the file and creating additional structures depending on
        the file type. For instance, frameworks will be linked, embedded and search paths will be adjusted automatically.
        Header file will be added to the headers sections, but not compiled, whereas the source files will be added to
        the compilation phase.
        :param path: Path to the file to be added
        :param parent: Parent group to be added under
        :param tree: Tree where the path is relative to
        :param target_name: Target name where the file should be added (none for every target)
        :param force: Add the file without checking if the file already exists
        :param file_options: FileOptions object to be used during the addition of the file to the project.
        :return: a list of elements that were added to the project successfully as PBXBuildFile objects
        """
        results = []
        # if it's not forced to add the file stop if the file already exists.
        if not force:
            for section in self.objects.get_sections():
                for obj in self.objects.get_objects_in_section(section):
                    if u'path' in obj and ProjectFiles._path_leaf(path) == ProjectFiles._path_leaf(obj.path):
                        return []

        file_ref, abs_path, path, tree, expected_build_phase = self._add_file_reference(path, parent, tree, force,
                                                                                        file_options)
        if path is None or tree is None:
            return None

        # no need to create the build_files, done
        if not file_options.create_build_files:
            return results

        # create build_files for the targets
        results.extend(self._create_build_files(file_ref, target_name, expected_build_phase, file_options))

        # special case for the frameworks and libraries to update the search paths
        if tree != TreeType.SOURCE_ROOT or abs_path is None:
            return results

        # the path is absolute and it's outside the scope of the project for linking purposes
        library_path = os.path.join(u'$(SRCROOT)', os.path.split(file_ref.path)[0])
        if os.path.isfile(abs_path):
            self.add_library_search_paths([library_path], recursive=False)
        else:
            self.add_framework_search_paths([library_path, u'$(inherited)'], recursive=False)

        return results

    def add_project(self, path, parent=None, tree=TreeType.GROUP, target_name=None, force=True, file_options=FileOptions()):
        """
        Adds another Xcode project into this project. Allows to use the products generated from the given project into
        this project during compilation time. Optional: it can add the products into the different sections: frameworks
        and bundles.

        :param path: Path to the .xcodeproj file
        :param parent: Parent group to be added under
        :param tree: Tree where the path is relative to
        :param target_name: Target name where the file should be added (none for every target)
        :param force: Add the file without checking if the file already exists
        :param file_options: FileOptions object to be used during the addition of the file to the project.
        :return: list of PBXReferenceProxy objects that can be used to create the PBXBuildFile phases.
        """
        results = []
        # if it's not forced to add the file stop if the file already exists.
        if not force:
            for section in self.objects.get_sections():
                for obj in self.objects.get_objects_in_section(section):
                    if u'path' in obj and ProjectFiles._path_leaf(path) == ProjectFiles._path_leaf(obj.path):
                        return []

        file_ref, _, path, tree, expected_build_phase = self._add_file_reference(path, parent, tree, force,
                                                                                 file_options)
        if path is None or tree is None:
            return None

        # load project and add the things
        child_project = self.__class__.load(os.path.join(path, u'project.pbxproj'))
        child_products = child_project.get_build_phases_by_name(u'PBXNativeTarget')

        # create an special group without parent (ref proxies)
        products_group = PBXGroup.create(name=u'Products', children=[])
        self.objects[products_group.get_id()] = products_group

        for child_product in child_products:
            product_file_ref = child_project.objects[child_product.productReference]

            # create the container proxies
            container_proxy = PBXContainerItemProxy.create(file_ref, child_product)
            self.objects[container_proxy.get_id()] = container_proxy

            # create the reference proxies
            reference_proxy = PBXReferenceProxy.create(product_file_ref, container_proxy)
            self.objects[reference_proxy.get_id()] = reference_proxy

            # add reference proxy to the product group
            products_group.add_child(reference_proxy)

            # append the result
            results.append(reference_proxy)

            if file_options.create_build_files:
                _, expected_build_phase = self._determine_file_type(reference_proxy, file_options.ignore_unknown_type)
                self._create_build_files(reference_proxy, target_name, expected_build_phase, file_options)

        # add new PBXFileReference and PBXGroup to the PBXProject object
        project_object = self.objects.get_objects_in_section(u'PBXProject')[0]
        project_ref = PBXGenericObject(project_object).parse({
            u'ProductGroup': products_group.get_id(),
            u'ProjectRef': file_ref.get_id()
        })

        if u'projectReferences' not in project_object:
            project_object[u'projectReferences'] = PBXList()

        project_object.projectReferences.append(project_ref)

        return results

    def get_file_by_id(self, file_id):
        """
        Gets the PBXFileReference to the given id
        :param file_id: Identifier of the PBXFileReference to be retrieved.
        :return: A PBXFileReference if the id is found, None otherwise.
        """
        file_ref = self.objects[file_id]
        if not isinstance(file_ref, PBXFileReference):
            return None
        return file_ref

    def get_files_by_name(self, name, parent=None):
        """
        Gets all the files references that have the given name, under the specified parent PBXGroup object or
        PBXGroup id.
        :param name: name of the file to be retrieved
        :param parent: PBXGroup that should be used to narrow the search or None to retrieve files from all project
        :return: List of all PBXFileReference that match the name and parent criteria.
        """
        if parent is not None:
            parent = self._get_parent_group(parent)

        files = []
        for file_ref in self.objects.get_objects_in_section(u'PBXFileReference'):
            if file_ref.get_name() == name and (parent is None or parent.has_child(file_ref.get_id())):
                files.append(file_ref)

        return files

    def get_files_by_path(self, path, tree=TreeType.SOURCE_ROOT):
        """
        Gets the files under the given tree type that match the given path.
        :param path: Path to the file relative to the tree root
        :param tree: Tree type to look for the path. By default the SOURCE_ROOT
        :return: List of all PBXFileReference that match the path and tree criteria.
        """
        files = []
        for file_ref in self.objects.get_objects_in_section(u'PBXFileReference'):
            if file_ref.path == path and file_ref.sourceTree == tree:
                files.append(file_ref)

        return files

    def remove_file_by_id(self, file_id, target_name=None):
        """
        Removes the file id from given target name. If no target name is given, the file is removed
        from all targets
        :param file_id: identifier of the file to be removed
        :param target_name: The target name to remove the file from, if None, it's removed from all targets.
        :return: True if the file id was removed. False if the file was not removed.
        """

        file_ref = self.get_file_by_id(file_id)
        if file_ref is None:
            return False

        for target in self.objects.get_targets(target_name):
            for build_phase_id in target.buildPhases:
                build_phase = self.objects[build_phase_id]

                for build_file_id in build_phase.files:
                    build_file = self.objects[build_file_id]

                    if build_file.fileRef == file_ref.get_id():
                        # remove the build file from the phase
                        build_phase.remove_build_file(build_file)

                # if the build_phase is empty remove it too, unless it's a shell script.
                if build_phase.files.__len__() == 0 and build_phase.isa != u'PBXShellScriptBuildPhase':
                    # remove the build phase from the target
                    target.remove_build_phase(build_phase)

        # remove it iff it's removed from all targets or no build file reference it
        for build_file in self.objects.get_objects_in_section(u'PBXBuildFile'):
            if build_file.fileRef == file_ref.get_id():
                return True

        # remove the file from any groups if there is no reference from any target
        for group in self.objects.get_objects_in_section(u'PBXGroup'):
            if file_ref.get_id() in group.children:
                group.remove_child(file_ref)

        # the file is not referenced in any build file, remove it
        del self.objects[file_ref.get_id()]
        return True

    def remove_files_by_path(self, path, tree=TreeType.SOURCE_ROOT, target_name=None):
        """
        Removes all files for the given path under the same tree
        :param path: Path to the file relative to the tree root
        :param tree: Tree type to look for the path. By default the SOURCE_ROOT
        :param target_name: Target name where the file should be added (none for every target)
        :return: True if all the files were removed without problems. False if at least one file failed.
        """
        files = self.get_files_by_path(path, tree)
        result = 0
        total = files.__len__()
        for file_ref in files:
            if self.remove_file_by_id(file_ref.get_id(), target_name=target_name):
                result += 1

        return result != 0 and result == total

    def add_folder(self, path, parent=None, excludes=None, recursive=True, create_groups=True, target_name=None,
                   file_options=FileOptions()):
        """
        Given a directory, it will create the equivalent group structure and add all files in the process.
        If groups matching the logical path already exist, it will use them instead of creating a new one. Same
        apply for file within a group, if the file name already exists it will be ignored.

        :param path: OS path to the directory to be added.
        :param parent: Parent group to be added under
        :param excludes: list of regexs to ignore
        :param recursive: add folders recursively or stop in the first level
        :param create_groups: add folders recursively as groups or references
        :param target_name: Target name where the file should be added (none for every target)
        :param file_options: FileOptions object to be used during the addition of the file to the project.
        :return: a list of elements that were added to the project successfully as PBXBuildFile objects
        """
        if not os.path.isdir(path):
            return None

        if not excludes:
            excludes = []

        results = []

        # add the top folder as a group, make it the new parent
        path = os.path.abspath(path)
        if not create_groups and os.path.splitext(path)[1] not in ProjectFiles._SPECIAL_FOLDERS:
            return self.add_file(path, parent, target_name=target_name, force=False, file_options=file_options)

        parent = self.get_or_create_group(os.path.split(path)[1], path, parent)

        # iterate over the objects in the directory
        for child in os.listdir(path):
            # exclude dirs or files matching any of the expressions
            if [pattern for pattern in excludes if re.match(pattern, child)]:
                continue

            full_path = os.path.join(path, child)
            children = []
            if os.path.isfile(full_path) or os.path.splitext(child)[1] in ProjectFiles._SPECIAL_FOLDERS or \
                    not create_groups:
                # check if the file exists already, if not add it
                children = self.add_file(full_path, parent, target_name=target_name, force=False,
                                         file_options=file_options)
            else:
                # if recursive is true, go deeper, otherwise create the group here.
                if recursive:
                    children = self.add_folder(full_path, parent, excludes, recursive, target_name=target_name,
                                               file_options=file_options)
                else:
                    self.get_or_create_group(child, child, parent)

            results.extend(children)

        return results

    # miscellaneous functions, candidates to be extracted and decouple implementation

    def _add_file_reference(self, path, parent, tree, force, file_options):
        # decide the proper tree and path to add
        abs_path, path, tree = ProjectFiles._get_path_and_tree(self._source_root, path, tree)
        if path is None or tree is None:
            return None, abs_path, path, tree, None

        # create a PBXFileReference for the new file
        file_ref = PBXFileReference.create(path, tree)

        # determine the type of the new file:
        file_type, expected_build_phase = ProjectFiles._determine_file_type(file_ref, file_options.ignore_unknown_type)

        # set the file type on the file ref add the files
        file_ref.set_last_known_file_type(file_type)
        self.objects[file_ref.get_id()] = file_ref

        # determine the parent and add it to it
        self._get_parent_group(parent).add_child(file_ref)

        return file_ref, abs_path, path, tree, expected_build_phase

    def _create_build_files(self, file_ref, target_name, expected_build_phase, file_options):
        results = []
        for target in self.objects.get_targets(target_name):
            # determine if there is a suitable build phase created
            build_phases = target.get_or_create_build_phase(expected_build_phase)

            # if it's a framework and it needs to be embedded
            if file_options.embed_framework and expected_build_phase == u'PBXFrameworksBuildPhase' and \
                    file_ref.get_file_type() == u'wrapper.framework':
                embed_phase = target.get_or_create_build_phase(u'PBXCopyFilesBuildPhase',
                                                               search_parameters={'dstSubfolderSpec': '10'},
                                                               create_parameters=(PBXCopyFilesBuildPhaseNames.EMBEDDED_FRAMEWORKS,))
                # add runpath search flag
                self.add_flags(XCBuildConfigurationFlags.LD_RUNPATH_SEARCH_PATHS,
                               u'$(inherited) @executable_path/Frameworks', target_name)
                build_phases.extend(embed_phase)

            # create the build file and add it to the phase
            for target_build_phase in build_phases:
                build_file = PBXBuildFile.create(file_ref, file_options.get_attributes(file_ref, target_build_phase))
                self.objects[build_file.get_id()] = build_file
                target_build_phase.add_build_file(build_file)

                results.append(build_file)

        return results

    @classmethod
    def _determine_file_type(cls, file_ref, unknown_type_allowed):
        ext = os.path.splitext(file_ref.get_name())[1]
        if os.path.isdir(os.path.abspath(file_ref.path)) and ext not in ProjectFiles._SPECIAL_FOLDERS:
            file_type = 'folder'
            build_phase = u'PBXResourcesBuildPhase'
        else:
            file_type, build_phase = ProjectFiles._FILE_TYPES.get(ext, (None, u'PBXResourcesBuildPhase'))

        if not unknown_type_allowed and file_type is None:
            raise ValueError(
                u'Unknown file extension: {0}. Please add the extension and Xcode type to ProjectFiles._FILE_TYPES' \
                    .format(os.path.splitext(file_ref.get_name())[1]))

        return file_type, build_phase

    @classmethod
    def _path_leaf(cls, path):
        head, tail = os.path.split(path)
        return tail or os.path.basename(head)

    @classmethod
    def _get_path_and_tree(cls, source_root, path, tree):
        # returns the absolute path, the relative path and the tree
        abs_path = None
        if os.path.isabs(path):
            abs_path = path

            if not os.path.exists(path):
                return None, None, None

            if tree == TreeType.SOURCE_ROOT:
                path = os.path.relpath(path, source_root)
            else:
                tree = TreeType.ABSOLUTE

        return abs_path, path, tree

class ProjectFlags:
    """
    This class provides separation of concerns, this class contains all methods related to flags manipulations.
    This class should not be instantiated on its own
    """

    def __init__(self):
        raise EnvironmentError('This class cannot be instantiated directly, use XcodeProject instead')

    def add_flags(self, flag_name, flags, target_name=None, configuration_name=None):
        """
        Adds the given flags to the flag_name section of the target on the configurations
        :param flag_name: name of the flag to be added the values to
        :param flags: A string or array of strings
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        for configuration in self.objects.get_configurations_on_targets(target_name, configuration_name):
            configuration.add_flags(flag_name, flags)

    def set_flags(self, flag_name, flags, target_name=None, configuration_name=None):
        """
        Sets the given flags to the flag_name section of the target on the configurations, full override.
        :param flag_name: name of the flag to be added the values to
        :param flags: A string or array of strings
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        for configuration in self.objects.get_configurations_on_targets(target_name, configuration_name):
            configuration.set_flags(flag_name, flags)

    def remove_flags(self, flag_name, flags, target_name=None, configuration_name=None):
        """
        Removes the given flags from the flag_name section of the target on the configurations
        :param flag_name: name of the flag to be removed the values from
        :param flags: A string or array of strings. If none, removes all values from the flag.
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        for configuration in self.objects.get_configurations_on_targets(target_name, configuration_name):
            configuration.remove_flags(flag_name, flags)

    def add_other_cflags(self, flags, target_name=None, configuration_name=None):
        """
        Adds flag values to the OTHER_CFLAGS flag.
        :param flags: A string or array of strings. If none, removes all values from the flag.
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        self.add_flags(XCBuildConfigurationFlags.OTHER_CFLAGS, flags, target_name, configuration_name)

    def remove_other_cflags(self, flags, target_name=None, configuration_name=None):
        """
        Removes the given flags from the OTHER_CFLAGS section of the target on the configurations
        :param flags: A string or array of strings. If none, removes all values from the flag.
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        self.remove_flags(XCBuildConfigurationFlags.OTHER_CFLAGS, flags, target_name, configuration_name)

    def add_other_ldflags(self, flags, target_name=None, configuration_name=None):
        """
        Adds flag values to the OTHER_LDFLAGS flag.
        :param flags: A string or array of strings. If none, removes all values from the flag.
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        self.add_flags(XCBuildConfigurationFlags.OTHER_LDFLAGS, flags, target_name, configuration_name)

    def remove_other_ldflags(self, flags, target_name=None, configuration_name=None):
        """
        Removes the given flags from the OTHER_LDFLAGS section of the target on the configurations
        :param flags: A string or array of strings. If none, removes all values from the flag.
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        self.remove_flags(XCBuildConfigurationFlags.OTHER_LDFLAGS, flags, target_name, configuration_name)

    def add_search_paths(self, path_type, paths, recursive=True, escape=False, target_name=None,
                         configuration_name=None):
        """
        Adds the given search paths to the path type section of the target on the configurations
        :param path_type: name of the flag to be added the values to
        :param paths: A string or array of strings
        :param recursive: Add the paths as recursive ones
        :param escape: Escape the path in case it contains spaces
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        for configuration in self.objects.get_configurations_on_targets(target_name, configuration_name):
            configuration.add_search_paths(path_type, paths, recursive, escape)

    def remove_search_paths(self, path_type, paths, target_name=None, configuration_name=None):
        """
        Removes the given search paths from the path_type section of the target on the configurations
        :param path_type: name of the path type to be removed the values from
        :param paths: A string or array of strings
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        for configuration in self.objects.get_configurations_on_targets(target_name, configuration_name):
            configuration.remove_search_paths(path_type, paths)

    def add_header_search_paths(self, paths, recursive=True, escape=False, target_name=None, configuration_name=None):
        """
        Adds paths to the HEADER_SEARCH_PATHS configuration.
        :param paths: A string or array of strings
        :param recursive: Add the paths as recursive ones
        :param escape: Escape the path in case it contains spaces
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        self.add_search_paths(XCBuildConfigurationFlags.HEADER_SEARCH_PATHS, paths, recursive, escape, target_name,
                              configuration_name)

    def remove_header_search_paths(self, paths, target_name=None, configuration_name=None):
        """
        Removes the given search paths from the HEADER_SEARCH_PATHS section of the target on the configurations
        :param paths: A string or array of strings
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        self.remove_search_paths(XCBuildConfigurationFlags.HEADER_SEARCH_PATHS, paths, target_name, configuration_name)

    def add_library_search_paths(self, paths, recursive=True, escape=False, target_name=None, configuration_name=None):
        """
        Adds paths to the LIBRARY_SEARCH_PATHS configuration.
        :param paths: A string or array of strings
        :param recursive: Add the paths as recursive ones
        :param escape: Escape the path in case it contains spaces
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        self.add_search_paths(XCBuildConfigurationFlags.LIBRARY_SEARCH_PATHS, paths, recursive, escape, target_name,
                              configuration_name)

    def remove_library_search_paths(self, paths, target_name=None, configuration_name=None):
        """
        Removes the given search paths from the LIBRARY_SEARCH_PATHS section of the target on the configurations
        :param paths: A string or array of strings
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        self.remove_search_paths(XCBuildConfigurationFlags.LIBRARY_SEARCH_PATHS, paths, target_name, configuration_name)

    def add_framework_search_paths(self, paths, recursive=True, escape=False, target_name=None,
                                   configuration_name=None):
        """
        Adds paths to the FRAMEWORK_SEARCH_PATHS configuration.
        :param paths: A string or array of strings
        :param recursive: Add the paths as recursive ones
        :param escape: Escape the path in case it contains spaces
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        self.add_search_paths(XCBuildConfigurationFlags.FRAMEWORK_SEARCH_PATHS, paths, recursive, escape, target_name,
                              configuration_name)

    def remove_framework_search_paths(self, paths, target_name=None, configuration_name=None):
        """
        Removes the given search paths from the FRAMEWORK_SEARCH_PATHS section of the target on the configurations
        :param paths: A string or array of strings
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        self.remove_search_paths(XCBuildConfigurationFlags.FRAMEWORK_SEARCH_PATHS, paths, target_name, configuration_name)

    def add_run_script(self, script, target_name=None, insert_before_compile=False):
        """
        Adds a run script phase into the given target, optionally before compilation phase
        :param script: Script to be inserted on the run script
        :param target_name: Target name to add the flag to or None for every target
        :param insert_before_compile: Insert the run script phase before the compilation of the source files. By default,
        it's added at the end.
        :return:
        """
        for target in self.objects.get_targets(target_name):
            shell = PBXShellScriptBuildPhase.create(script)

            self.objects[shell.get_id()] = shell
            target.add_build_phase(shell, 0 if insert_before_compile else None)

    def remove_run_script(self, script, target_name=None):
        """
        Removes the given script string from the given target
        :param script: The script string to be removed from the target
        :param target_name: Target name to add the flag to or None for every target
        :return:
        """
        for target in self.objects.get_targets(target_name):
            for build_phase_id in target.buildPhases:
                build_phase = self.objects[build_phase_id]
                if not isinstance(build_phase, PBXShellScriptBuildPhase):
                    continue

                if build_phase.shellScript == script:
                    del self.objects[build_phase_id]
                    target.remove_build_phase(build_phase)

    def add_code_sign(self, code_sign_identity, development_team, provisioning_profile_uuid,
                      provisioning_profile_specifier, target_name=None, configuration_name=None):
        """
        Adds the code sign information to the project and creates the appropriate flags in the configuration.
        In xcode 8+ the provisioning_profile_uuid becomes optional, and the provisioning_profile_specifier becomes
        mandatory. Contrariwise, in xcode 8< provisioning_profile_uuid becomes mandatory and
        provisioning_profile_specifier becomes optional.

        :param code_sign_identity: Code sign identity name. Usually formatted as: 'iPhone Distribution[: <Company name> (MAAYFEXXXX)]'
        :param development_team: Development team identifier string. Usually formatted as: 'MAAYFEXXXX'
        :param provisioning_profile_uuid: Provisioning profile UUID string. Usually formatted as: '6f1ffc4d-xxxx-xxxx-xxxx-6dc186280e1e'
        :param provisioning_profile_specifier: Provisioning profile specifier (a.k.a. name) string.
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return:
        """
        self.set_flags(u'CODE_SIGN_IDENTITY[sdk=iphoneos*]', code_sign_identity, target_name, configuration_name)
        self.set_flags(u'DEVELOPMENT_TEAM', development_team, target_name, configuration_name)
        self.set_flags(u'PROVISIONING_PROFILE', provisioning_profile_uuid, target_name, configuration_name)
        self.set_flags(u'PROVISIONING_PROFILE_SPECIFIER', provisioning_profile_specifier, target_name, configuration_name)

        for target in self.objects.get_targets(target_name):
            self.objects[self.rootObject].set_provisioning_style(PBXProvioningTypes.MANUAL, target)

class ProjectGroups:
    """
    This class provides separation of concerns, this class contains all methods related to groups manipulations.
    This class should not be instantiated on its own
    """

    def __init__(self):
        raise EnvironmentError('This class cannot be instantiated directly, use XcodeProject instead')

    def add_group(self, name, path=None, parent=None, source_tree=u'<group>'):
        """
        Add a new group with the given name and optionally path to the parent group. If parent is None, the group will
        be added to the 'root' group.
        Additionally the source tree type can be specified, normally it's group.
        :param name: Name of the group to be added (visible folder name)
        :param path: Path relative to the project where this group points to. If not present, name will match the path
            name
        :param parent: The PBXGroup that will be the parent of this group. If parent is None, the default 'root' group
            will be used as parent
        :param source_tree: The type of group to be created
        :return: PBXGroup created
        """
        group = PBXGroup.create(name=name, path=path, tree=source_tree)

        parent = self._get_parent_group(parent)

        parent.add_child(group)
        self.objects[group.get_id()] = group

        return group

    def remove_group_by_id(self, group_id, recursive=True):
        """
        Remove the group matching the given group_id. If recursive is True, all descendants of this group are also removed.
        :param group_id: The group id to be removed
        :param recursive: All descendants should be removed as well
        :return: True if the element was removed successfully, False if an error occured or there was nothing to remove.
        """
        group = self.objects[group_id]
        if group is None:
            return False

        result = True
        # iterate over the children and determine if they are file/group and call the right method.
        for subgroup_id in list(group.children):
            subgroup = self.objects[subgroup_id]
            if subgroup is None:
                return False

            if recursive and isinstance(subgroup, PBXGroup):
                result &= self.remove_group_by_id(subgroup.get_id(), recursive)
            if isinstance(subgroup, PBXFileReference):
                result &= self.remove_file_by_id(subgroup.get_id())

        if not result:
            return False

        del self.objects[group.get_id()]

        # remove the reference from any other group object that could be containing it.
        for other_group in self.objects.get_objects_in_section(u'PBXGroup'):
            other_group.remove_child(group)

        return True

    def remove_group_by_name(self, group_name, recursive=True):
        """
        Remove the groups matching the given name. If recursive is True, all descendants of this group are also removed.
        This method could cause the removal of multiple groups that not necessarily are intended to be removed, use with
        caution
        :param group_name: The group name to be removed
        :param recursive: All descendants should be removed as well
        :return: True if the element was removed successfully, False otherwise
        """
        groups = self.get_groups_by_name(name=group_name)

        if groups.__len__() == 0:
            return False

        for group in groups:
            if not self.remove_group_by_id(group.get_id(), recursive):
                return False

        return True

    def get_groups_by_name(self, name, parent=None):
        """
        Retrieve all groups matching the given name and optionally filtered by the given parent node.
        :param name: The name of the group that has to be returned
        :param parent: A PBXGroup object where the object has to be retrieved from. If None all matching groups are returned
        :return: An list of all matching groups
        """
        groups = self.objects.get_objects_in_section(u'PBXGroup')
        groups = [group for group in groups if group.get_name() == name]

        if parent:
            return [group for group in groups if parent.has_child(group)]

        return groups

    def get_groups_by_path(self, path, parent=None):
        """
        Retrieve all groups matching the given path and optionally filtered by the given parent node.
        The path is converted into the absolute path of the OS before comparison.
        :param path: The name of the group that has to be returned
        :param parent: A PBXGroup object where the object has to be retrieved from. If None all matching groups are returned
        :return: An list of all matching groups
        """
        groups = self.objects.get_objects_in_section(u'PBXGroup')
        groups = [group for group in groups if group.get_path() == path]

        if parent:
            return [group for group in groups if parent.has_child(group)]

        return groups

    def get_or_create_group(self, name, path=None, parent=None):
        if not name:
            return None

        groups = self.get_groups_by_name(name, parent)
        if groups.__len__() > 0:
            return groups[0]

        return self.add_group(name, path, parent)

    def _get_parent_group(self, parent):
        if parent is None:
            # search for the mainGroup of the project
            project = self.objects[self[u'rootObject']]
            if project:
                parent = self.objects[project[u'mainGroup']]
                if parent is not None:
                    return parent

            # search for the group without name
            parent = self.get_groups_by_name(None)

            # if there is no parent, create and empty parent group, add it to the objects
            if parent.__len__() > 0:
                return parent[0]

            parent = PBXGroup.create(path=None, name=None)
            self.objects[parent.get_id()] = parent
            return parent

        # it's not a group instance, assume it's an id
        if not isinstance(parent, PBXGroup):
            return self.objects[parent]

        return parent

class PBXGenericObject(object):
    """
    Generic class that creates internal attributes to match the structure of the tree used to create the element.
    Also, prints itself using the openstep format. Extensions might be required to insert comments on right places.
    """
    _VALID_KEY_REGEX = '[a-zA-Z0-9\\._/]*'

    def __init__(self, parent=None):
        self._parent = parent

    def get_parent(self):
        return self._parent

    def parse(self, value):
        if isinstance(value, dict):
            return self._parse_dict(value)

        if isinstance(value, basestring):
            return self._parse_string(value)

        if isinstance(value, list):
            return self._parse_list(value)

        return value

    def _parse_dict(self, obj):
        # all top level objects are added as variables to this object
        for key, value in list(obj.items()):
            if value is None:
                continue

            key = self._parse_string(key)
            setattr(self, key, self._get_instance(key, value))

        return self

    def _parse_list(self, obj):
        ret = []
        for item in obj:
            ret.append(copy.copy(self).parse(item))

        return ret

    def _parse_string(self, obj):
        if re.match('([0-9A-F]{24})', obj) is not None:
            return PBXKey(obj, self)

        return obj

    def _get_instance(self, class_type, content):
        # check if the key maps to a kind of object
        return self._get_class_reference(class_type)(self).parse(content)

    @classmethod
    def _get_class_reference(cls, class_type):
        module = __import__(u'pbxproj')
        if hasattr(module, class_type):
            class_ = getattr(module, class_type)
            return class_
        return PBXGenericObject

    def __repr__(self):
        return self._print_object()

    def _print_object(self, indentation_depth=u'', entry_separator=u'\n', object_start=u'\n',
                      indentation_increment=u'\t'):
        ret = u'{' + object_start

        for key in self.get_keys():
            value = self._format(getattr(self, key), indentation_depth, entry_separator, object_start,
                                 indentation_increment)

            # use key decorators, could simplify the generation of the comments.
            ret += indentation_depth + u'{3}{0} = {1};{2}'.format(PBXGenericObject._escape(key), value, entry_separator,
                                                                  indentation_increment)
        ret += indentation_depth + u'}'
        return ret

    def _print_list(self, obj, indentation_depth=u'', entry_separator=u'\n', object_start=u'\n',
                    indentation_increment=u'\t'):
        ret = u'(' + object_start
        for item in obj:
            value = self._format(item, indentation_depth, entry_separator, object_start, indentation_increment)

            ret += indentation_depth + u'{1}{0},{2}'.format(value, indentation_increment, entry_separator)
        ret += indentation_depth + u')'
        return ret

    def _format(self, value, indentation_depth=u'', entry_separator=u'\n', object_start=u'\n',
                indentation_increment=u'\t'):
        if hasattr(value, u'_print_object'):
            value = value._print_object(indentation_depth + indentation_increment,
                                        entry_separator,
                                        object_start,
                                        indentation_increment)
        elif isinstance(value, list):
            value = self._print_list(value, indentation_depth + indentation_increment,
                                     entry_separator,
                                     object_start,
                                     indentation_increment)
        elif isinstance(value, PBXKey):
            value = value.__repr__()
        else:
            value = PBXGenericObject._escape(value.__str__(), exclude=[u"\'"])

        return value

    def get_keys(self):
        fields = list([x for x in dir(self) if not x.startswith(u'_') and not hasattr(getattr(self, x), '__call__')])
        if u'isa' in fields:
            fields.remove(u'isa')
            fields = sorted(fields)
            fields.insert(0, u'isa')
        else:
            fields = sorted(fields)

        return fields

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)

        return None

    def __setitem__(self, key, value):
        if type(value) == list:
            if value.__len__() == 1:
                value = value[0]
            if value.__len__() == 0:
                if hasattr(self, key):
                    delattr(self, key)
                return

        setattr(self, key, value)

    def __delitem__(self, key):
        delattr(self, key)

    def __contains__(self, item):
        return hasattr(self, item)

    def _resolve_comment(self, key):
        parent = self.get_parent()
        if key in self:
            return self[key]._get_comment()

        if parent is None:
            return None

        return parent._resolve_comment(key)

    def get_id(self):
        return self['_id']

    def _get_comment(self):
        if hasattr(self, u'name'):
            return self.name
        if hasattr(self, u'path'):
            return self.path

        return None

    @classmethod
    def _generate_id(cls):
        return ''.join(str(uuid.uuid4()).upper().split('-')[1:])

    @classmethod
    def _escape(cls, item, exclude=None):
        replacements = [(u'\\', u'\\\\'),
                        (u'\n', u'\\n'),
                        (u'\"', u'\\"'),
                        (u'\0', u'\\0'),
                        (u'\t', u'\\\t'),
                        (u'\'', u'\\\'')]
        if exclude is not None:
            replacements = [x for x in replacements for y in exclude if x[0] != y]

        if item.__len__() == 0 or re.match(cls._VALID_KEY_REGEX, item).group(0) != item:
            escaped = item
            for replacement in replacements:
                escaped = escaped.replace(replacement[0], replacement[1])

            return u'"{0}"'.format(escaped)
        return item

class PBXKey(str):
    def __new__(cls, value, parent):
        obj = str.__new__(cls, value)
        obj._parent = parent
        return obj

    def __repr__(self):
        comment = self._get_comment()
        if comment is not None:
            comment = u' /* {0} */'.format(comment)
        else:
            comment = u''

        return u'{0}{1}'.format(self.__str__(), comment)

    def get_parent(self):
        return self._parent

    def _get_comment(self):
        return self.get_parent()._resolve_comment(self)

class PBXList(list):
    pass

class objects(PBXGenericObject):
    def __init__(self, parent=None):
        super(objects, self).__init__(parent)

        # sections: dict<isa, [tuple(id, obj)]>
        # sections get aggregated under the isa type. Each contains a list of tuples (id, obj) with every object defined
        self._sections = {}

    def parse(self, object_data):
        # iterate over the keys and fill the sections
        if isinstance(object_data, dict):
            for key, value in list(object_data.items()):
                key = self._parse_string(key)
                obj_type = key
                if 'isa' in value:
                    obj_type = value['isa']

                child = self._get_instance(obj_type, value)
                child[u'_id'] = key
                self[key] = child

            return self

        # safe-guard: delegate to the parent how to deal with non-object values
        return super(objects, self).parse(object_data)

    def _print_object(self, indentation_depth=u'', entry_separator=u'\n', object_start=u'\n',
                      indentation_increment=u'\t'):
        # override to change the way the object is printed out
        result = u'{\n'
        for section in self.get_sections():
            phase = self._sections[section]
            phase.sort(key=lambda x: x.get_id())
            result += u'\n/* Begin {0} section */\n'.format(section)
            for value in phase:
                obj = value._print_object(indentation_depth + u'\t', entry_separator, object_start,
                                          indentation_increment)
                result += indentation_depth + u'\t{0} = {1};\n'.format(value.get_id().__repr__(), obj)
            result += u'/* End {0} section */\n'.format(section)
        result += indentation_depth + u'}'
        return result

    def get_keys(self):
        """
        :return: all the keys of the object (ids of objects)
        """
        keys = []
        for section in self.get_sections():
            phase = self._sections[section]
            for obj in phase:
                keys += obj.get_id()
        keys.sort()
        return keys

    def get_sections(self):
        sections = list(self._sections.keys())
        sections.sort()
        return sections

    def __getitem__(self, key):
        for section in self.get_sections():
            phase = self._sections[section]
            for obj in phase:
                if key == obj.get_id():
                    return obj
        return None

    def __setitem__(self, key, value):
        if value.isa not in self._sections:
            self._sections[value.isa] = []

        self._sections[value.isa].append(value)
        value._parent = self

    def __delitem__(self, key):
        obj = self[key]
        if obj is not None:
            phase = self._sections[obj.isa]
            phase.remove(obj)

            # remove empty phases
            if phase.__len__() == 0:
                del self._sections[obj.isa]

    def __contains__(self, item):
        return self[item] is not None

    def __len__(self):
        return sum([section.__len__() for section in self._sections])

    def get_objects_in_section(self, *sections):
        result = []
        for name in sections:
            if name in self._sections:
                result.extend(self._sections[name])
        return result

    def get_targets(self, name=None):
        """
        Retrieve all/one target objects
        :param name: name of the target to search for, None for everything
        :return: A list of target objects
        """
        targets = []
        for section in self.get_sections():
            if section.endswith(u'Target'):
                targets += [value for value in self._sections[section]]

        if name is None:
            return targets

        for target in targets:
            if target.name == name:
                return [target]
        return []

    def get_configurations_on_targets(self, target_name=None, configuration_name=None):
        """
        Retrieves all configuration given a name on the specified target
        :param target_name: Searches for a specific target name, if None all targets are used
        :param configuration_name: Searches for a specific configuration, if None all configuration of the target
            are used
        :return: A generator of configurations objects matching the target and configuration given (or all if nothing is
            specified)
        """
        for target in self.get_targets(target_name):
            configuration_list = self[target.buildConfigurationList]
            for configuration in configuration_list.buildConfigurations:
                if configuration_name is None or self[configuration].name == configuration_name:
                    yield self[configuration]

class rootObject(PBXGenericObject):
    def _resolve_comment(self, key):
        return self.get_parent().objects._resolve_comment(key)

class PBXGenericTarget(PBXGenericObject):
    def get_or_create_build_phase(self, build_phase_type, search_parameters=None, create_parameters=()):
        result = []
        parent = self.get_parent()
        search_parameters = search_parameters if search_parameters is not None else {}

        if build_phase_type is None:
            return result

        for build_phase_id in self.buildPhases:
            target_build_phase = parent[build_phase_id]
            current_build_phase = target_build_phase.isa

            if current_build_phase == build_phase_type and \
                    all(key in target_build_phase and target_build_phase[key] == search_parameters[key] for key in search_parameters):
                result.append(target_build_phase)

        if result.__len__() == 0:
            build_phase = self._get_class_reference(build_phase_type).create(*create_parameters)
            parent[build_phase.get_id()] = build_phase
            self.add_build_phase(build_phase)
            result.append(build_phase)

        return result

    def add_build_phase(self, build_phase, position=None):
        if position is None:
            position = self.buildPhases.__len__()

        self.buildPhases.insert(position, build_phase.get_id())

    def remove_build_phase(self, build_phase):
        if not isinstance(build_phase, PBXGenericBuildPhase):
            return False

        self.buildPhases.remove(build_phase.get_id())
        del self.get_parent()[build_phase.get_id()]

        return True


class PBXAggregatedTarget(PBXGenericTarget):
    pass

class PBXBuildFile(PBXGenericObject):
    @classmethod
    def create(cls, file_ref, attributes=None, compiler_flags=None):
        return cls().parse({
            u'_id': cls._generate_id(),
            u'isa': cls.__name__,
            u'fileRef': file_ref.get_id(),
            u'settings': cls._get_settings(attributes, compiler_flags)
        })

    @classmethod
    def _get_settings(cls, attributes=None, compiler_flags=None):
        if attributes is None and compiler_flags is None:
            return None

        settings = {}
        if attributes is not None:
            if not isinstance(attributes, list):
                attributes = [attributes]
            settings[u'ATTRIBUTES'] = attributes

        if compiler_flags is not None:
            if not isinstance(compiler_flags, list):
                compiler_flags = [compiler_flags]
            settings[u'COMPILER_FLAGS'] = u' '.join(compiler_flags)

        return settings

    def _print_object(self, indentation_depth=u'', entry_separator=u'\n', object_start=u'\n',
                      indentation_increment=u'\t'):
        return super(PBXBuildFile, self)._print_object(u'', entry_separator=u' ', object_start=u'',
                                                       indentation_increment=u'')

    def _get_comment(self):
        return u'{0} in {1}'.format(self.fileRef._get_comment(), self._get_section())

    def _get_section(self):
        objects = self.get_parent()
        target = self.get_id()

        for section in objects.get_sections():
            for obj in objects.get_objects_in_section(section):
                if u'files' in obj and target in obj.files:
                    return obj._get_comment()

    def add_attributes(self, attributes):
        if not isinstance(attributes, list):
            attributes = [attributes]

        if u'settings' not in self:
            self[u'settings'] = PBXGenericObject()

        if u'ATTRIBUTES' not in self.settings:
            self.settings[u'ATTRIBUTES'] = PBXList()

        # append, if it's assigned and the list only has 1 element it will turn it into a string
        self.settings.ATTRIBUTES += attributes

    def remove_attributes(self, attributes):
        if u'settings' not in self or u'ATTRIBUTES' not in self.settings:
            # nothing to remove
            return False

        if not isinstance(attributes, list):
            attributes = [attributes]

        for attribute in self.settings.ATTRIBUTES:
            self.settings.ATTRIBUTES.remove(attribute)

        return self._clean_up_settings()

    def add_compiler_flags(self, compiler_flags):
        if isinstance(compiler_flags, list):
            compiler_flags = u' '.join(compiler_flags)

        if u'settings' not in self:
            self[u'settings'] = PBXGenericObject()

        if u'COMPILER_FLAGS' not in self.settings:
            self.settings[u'COMPILER_FLAGS'] = u''

        self.settings[u'COMPILER_FLAGS'] += u' ' + compiler_flags
        self.settings[u'COMPILER_FLAGS'] = self.settings[u'COMPILER_FLAGS'].strip()

    def remove_compiler_flags(self, compiler_flags):
        if u'settings' not in self or u'COMPILER_FLAGS' not in self.settings:
            # nothing to remove
            return False

        if not isinstance(compiler_flags, list):
            compiler_flags = [compiler_flags]

        for flag in compiler_flags:
            self.settings[u'COMPILER_FLAGS'] = self.settings[u'COMPILER_FLAGS'].replace(flag, u'')
        self.settings[u'COMPILER_FLAGS'] = self.settings[u'COMPILER_FLAGS'].strip()

        return self._clean_up_settings()

    def _clean_up_settings(self):
        # no attributes remain, remove the element
        if u'ATTRIBUTES' in self.settings and self.settings.ATTRIBUTES.__len__() == 0:
            del self.settings[u'ATTRIBUTES']

        # no flags remain, remove the element
        if u'COMPILER_FLAGS' in self.settings and self.settings.COMPILER_FLAGS.__len__() == 0:
            del self.settings[u'COMPILER_FLAGS']

        if self.settings.get_keys().__len__() == 0:
            del self[u'settings']

        return True

class PBXContainerItemProxy(PBXGenericObject):
    @classmethod
    def create(cls, file_ref, remote_ref, proxy_type=2):
        return cls().parse({
            u'_id': cls._generate_id(),
            u'isa': cls.__name__,
            u'containerPortal': file_ref.get_id(),
            u'proxyType': proxy_type,
            u'remoteGlobalIDString': remote_ref.productReference,
            u'remoteInfo': remote_ref.productName
        })

    def _get_comment(self):
        return u'PBXContainerItemProxy'

class PBXCopyFilesBuildPhaseNames:
    EMBEDDED_FRAMEWORKS = u'Embed Frameworks'

class PBXGenericBuildPhase(PBXGenericObject):
    @classmethod
    def create(cls, name=None, files=None):
        return cls().parse({
            u'_id': cls._generate_id(),
            u'isa': cls.__name__,
            u'name': name,
            u'files': files if files else [],
            u'buildActionMask': 0x7FFFFFFF,
            u'runOnlyForDeploymentPostprocessing': 0
        })

    def add_build_file(self, build_file):
        if not isinstance(build_file, PBXBuildFile):
            return False

        self.files.append(build_file.get_id())
        return True

    def remove_build_file(self, build_file):
        if not isinstance(build_file, PBXBuildFile):
            return False

        self.files.remove(build_file.get_id())
        del self.get_parent()[build_file.get_id()]

        return True

class PBXCopyFilesBuildPhase(PBXGenericBuildPhase):
    @classmethod
    def create(cls, name=None, files=None, dest_path=u'', dest_subfolder_spec='10'):
        return cls().parse({
            u'_id': cls._generate_id(),
            u'isa': cls.__name__,
            u'name': name,
            u'files': files if files else [],
            u'buildActionMask': 0x7FFFFFFF,
            u'dstSubfolderSpec': dest_subfolder_spec,
            u'dstPath': dest_path,
            u'runOnlyForDeploymentPostprocessing': 0
        })

    def _get_comment(self):
        comment = super(PBXCopyFilesBuildPhase, self)._get_comment()
        if comment is None:
            return u'CopyFiles'
        return comment

class PBXFileReference(PBXGenericObject):
    @classmethod
    def create(cls, path, tree=u'SOURCE_ROOT'):
        return cls().parse({
            u'_id': cls._generate_id(),
            u'isa': cls.__name__,
            u'path': path,
            u'name': os.path.split(path)[1],
            u'sourceTree': tree
        })

    def set_explicit_file_type(self, file_type):
        if u'lastKnownFileType' in self:
            del self[u'lastKnownFileType']
        self[u'explicitFileType'] = file_type

    def set_last_known_file_type(self, file_type):
        if u'explicitFileType' in self:
            del self[u'explicitFileType']
        self[u'lastKnownFileType'] = file_type

    def get_file_type(self):
        if u'explicitFileType' in self:
            return self.explicitFileType
        return self.lastKnownFileType

    def _print_object(self, indentation_depth=u'', entry_separator=u'\n', object_start=u'\n',
                      indentation_increment=u'\t'):
        return super(PBXFileReference, self)._print_object(u'', entry_separator=u' ', object_start=u'',
                                                           indentation_increment=u'')

    def get_name(self):
        if hasattr(self, u'name'):
            return self.name
        if hasattr(self, u'path'):
            return self.path
        return None

    def remove(self, recursive=True):
        # search on the BuildFiles if there is a build file to be removed, and remove it
        # search for each phase that has a reference to the build file and remove it from it.
        # remove the file reference from it's parent
        pass


class PBXFrameworksBuildPhase(PBXGenericBuildPhase):
    def _get_comment(self):
        return u'Frameworks'

class PBXGenericBuildPhase(PBXGenericObject):
    @classmethod
    def create(cls, name=None, files=None):
        return cls().parse({
            u'_id': cls._generate_id(),
            u'isa': cls.__name__,
            u'name': name,
            u'files': files if files else [],
            u'buildActionMask': 0x7FFFFFFF,
            u'runOnlyForDeploymentPostprocessing': 0
        })

    def add_build_file(self, build_file):
        if not isinstance(build_file, PBXBuildFile):
            return False

        self.files.append(build_file.get_id())
        return True

    def remove_build_file(self, build_file):
        if not isinstance(build_file, PBXBuildFile):
            return False

        self.files.remove(build_file.get_id())
        del self.get_parent()[build_file.get_id()]

        return True

class PBXGenericTarget(PBXGenericObject):
    def get_or_create_build_phase(self, build_phase_type, search_parameters=None, create_parameters=()):
        result = []
        parent = self.get_parent()
        search_parameters = search_parameters if search_parameters is not None else {}

        if build_phase_type is None:
            return result

        for build_phase_id in self.buildPhases:
            target_build_phase = parent[build_phase_id]
            current_build_phase = target_build_phase.isa

            if current_build_phase == build_phase_type and \
                    all(key in target_build_phase and target_build_phase[key] == search_parameters[key] for key in search_parameters):
                result.append(target_build_phase)

        if result.__len__() == 0:
            build_phase = self._get_class_reference(build_phase_type).create(*create_parameters)
            parent[build_phase.get_id()] = build_phase
            self.add_build_phase(build_phase)
            result.append(build_phase)

        return result

    def add_build_phase(self, build_phase, position=None):
        if position is None:
            position = self.buildPhases.__len__()

        self.buildPhases.insert(position, build_phase.get_id())

    def remove_build_phase(self, build_phase):
        if not isinstance(build_phase, PBXGenericBuildPhase):
            return False

        self.buildPhases.remove(build_phase.get_id())
        del self.get_parent()[build_phase.get_id()]

        return True

class PBXGroup(PBXGenericObject):
    @classmethod
    def create(cls, path=None, name=None, tree=u'<group>', children=None):
        return cls().parse({
            u'_id': cls._generate_id(),
            u'isa': cls.__name__,
            u'children': children if children else [],
            u'name': name,
            u'path': path,
            u'sourceTree': tree
        })

    def get_name(self):
        if u'name' in self:
            return self.name
        if u'path' in self:
            return self.path
        return None

    def get_path(self):
        if u'path' in self:
            return self.path
        if u'name' in self:
            return self.name
        return None

    def has_child(self, child):
        """
        Checks if the given child id
        :param child: The id to check if it's a child of the group
        :return: True if the given id it's a child of this group, False otherwise
        """
        if u'children' not in self:
            return False

        if not isinstance(child, basestring):
            child = child.get_id()

        return child in self.children

    def add_child(self, child):
        # if it's not the right type of children for the group
        if not isinstance(child, PBXGroup) \
                and not isinstance(child, PBXFileReference) \
                and not isinstance(child, PBXReferenceProxy):
            return False

        self.children.append(child.get_id())
        return True

    def remove_child(self, child):
        if self.has_child(child):
            self.children.remove(child.get_id())
            return True

        return False

    def remove(self, recursive=True):
        parent = self.get_parent()
        # remove from the objects reference
        del parent[self.get_id()]

        # remove children if necessary
        if recursive:
            for subgroup_id in self.children:
                subgroup = parent[subgroup_id]
                if subgroup is None or not subgroup.remove(recursive):
                    return False

        return True

class PBXHeadersBuildPhase(PBXGenericBuildPhase):
    def _get_comment(self):
        return u'Headers'

class PBXLegacyTarget(PBXGenericTarget):
    pass

class PBXNativeTarget(PBXGenericTarget):
    pass

class PBXProvioningTypes:
    MANUAL = u'Manual'
    AUTOMATIC = u'Automatic'


class PBXProject(PBXGenericObject):
    def _get_comment(self):
        return u'Project object'

    def set_provisioning_style(self, provisioning_type, target):
        if u'attributes' not in self:
            self[u'attributes'] = PBXGenericObject()

        if u'TargetAttributes' not in self.attributes:
            self.attributes[u'TargetAttributes'] = PBXGenericObject()

        if target.get_id() not in self.attributes.TargetAttributes:
            self.attributes.TargetAttributes[target.get_id()] = PBXGenericObject()

        self.attributes.TargetAttributes[target.get_id()][u'ProvisioningStyle'] = provisioning_type


class PBXReferenceProxy(PBXGenericObject):
    @classmethod
    def create(cls, file_ref, remote_ref, tree=u'BUILT_PRODUCTS_DIR'):
        return cls().parse({
            u'_id': cls._generate_id(),
            u'isa': cls.__name__,
            u'path': file_ref.path,
            u'fileType': file_ref.get_file_type(),
            u'remoteRef': remote_ref.get_id(),
            u'sourceTree': tree
        })

    def get_file_type(self):
        return self.fileType

    def get_name(self):
        return self.path

class PBXResourcesBuildPhase(PBXGenericBuildPhase):
    def _get_comment(self):
        return u'Resources'

class PBXShellScriptBuildPhase(PBXGenericBuildPhase):
    @classmethod
    def create(cls, script, shell_path=u"/bin/sh", files=None, input_paths=None, output_paths=None, show_in_log='0'):
        return cls().parse({
            u'_id': cls._generate_id(),
            u'isa': cls.__name__,
            u'files': files if files else [],
            u'buildActionMask': 0x7FFFFFFF,
            u'inputPaths': input_paths if input_paths else [],
            u'outputPaths': output_paths if output_paths else [],
            u'runOnlyForDeploymentPostprocessing': 0,
            u'shellPath': shell_path,
            u'shellScript': script,
            u'showEnvVarsInLog': show_in_log
        })

    def _get_comment(self):
        return u'ShellScript'

class PBXSourcesBuildPhase(PBXGenericBuildPhase):
    def _get_comment(self):
        return u'Sources'

class PBXTargetDependency(PBXGenericObject):
    def _get_comment(self):
        return u'PBXTargetDependency'

class XCBuildConfigurationFlags:
    OTHER_CFLAGS = u'OTHER_CFLAGS'
    OTHER_LDFLAGS = u'OTHER_LDFLAGS'
    HEADER_SEARCH_PATHS = u'HEADER_SEARCH_PATHS'
    LIBRARY_SEARCH_PATHS = u'LIBRARY_SEARCH_PATHS'
    FRAMEWORK_SEARCH_PATHS = u'FRAMEWORK_SEARCH_PATHS'
    LD_RUNPATH_SEARCH_PATHS = u'LD_RUNPATH_SEARCH_PATHS'


class XCBuildConfiguration(PBXGenericObject):

    def add_flags(self, flag_name, flags):
        if u'buildSettings' not in self:
            self[u'buildSettings'] = PBXGenericObject()

        current_flags = self.buildSettings[flag_name]
        if current_flags is None:
            self.set_flags(flag_name, flags)
            return

        if not isinstance(current_flags, list):
            current_flags = [current_flags]

        if not isinstance(flags, list):
            flags = [flags]

        self.set_flags(flag_name, current_flags + flags)

    def set_flags(self, flag_name, flags):
        if u'buildSettings' not in self:
            self[u'buildSettings'] = PBXGenericObject()

        self.buildSettings[flag_name] = flags

    def remove_flags(self, flag_name, flags):
        if u'buildSettings' not in self or self.buildSettings[flag_name] is None:
            # nothing to remove
            return False

        current_flags = self.buildSettings[flag_name]
        if not isinstance(current_flags, list):
            current_flags = [current_flags]

        if flags is None:
            flags = current_flags

        if not isinstance(flags, list):
            flags = [flags]

        self.buildSettings[flag_name] = [x for x in current_flags if x not in flags]
        return True

    def add_search_paths(self, key, paths, recursive=False, escape=False):
        if not isinstance(paths, list):
            paths = [paths]

        # build the recursive/escaped strings and add the flags accordingly
        flags = []
        for path in paths:
            if path == '$(inherited)':
                escape = False
                recursive = False

            if escape:
                path = u'"{0}"'.format(path)

            if recursive and not path.endswith('/**'):
                path = os.path.join(path, '**')

            flags.append(path)

        self.add_flags(key, flags)

    def remove_search_paths(self, key, paths):
        return self.remove_flags(key, paths)

class XCConfigurationList(PBXGenericObject):
    def _get_comment(self):
        info = self._get_section()
        return u'Build configuration list for {0} "{1}"'.format(*info)

    def _get_section(self):
        objects = self.get_parent()
        target = self.get_id()

        for obj in objects.get_objects_in_section(u'PBXNativeTarget', u'PBXAggregateTarget'):
            if target in obj.buildConfigurationList:
                return obj.isa, obj.name

        for obj in objects.get_objects_in_section(u'PBXProject'):
            if target in obj.buildConfigurationList:
                return obj.isa, objects[obj.targets[0]].productName

        return u'', u''


class XcodeProject(PBXGenericObject, ProjectFiles, ProjectFlags, ProjectGroups):
    """
    Top level class, handles the project CRUD operations, new, load, save, delete. Also, exposes methods to manipulate
    the project's content, add/remove files, add/remove libraries/frameworks, query sections. For more advanced
    operations, underlying objects are exposed that can be manipulated using said objects.
    """

    def __init__(self, tree=None, path=None):
        super(XcodeProject, self).__init__(parent=None)

        if path is None:
            path = os.path.join(os.getcwd(), 'project.pbxproj')

        self._pbxproj_path = os.path.abspath(path)
        self._source_root = os.path.abspath(os.path.join(os.path.split(path)[0], '..'))

        # initialize the structure using the given tree
        self.parse(tree)

    def save(self, path=None):
        if path is None:
            path = self._pbxproj_path

        f = open(path, 'w')
        f.write(self.__repr__())
        f.close()

    def backup(self):
        backup_name = "%s_%s.backup" % (self._pbxproj_path, datetime.datetime.now().strftime('%d%m%y-%H%M%S'))

        shutil.copy2(self._pbxproj_path, backup_name)
        return backup_name

    def __repr__(self):
        return u'// !$*UTF8*$!\n' + super(XcodeProject, self).__repr__()

    def get_ids(self):
        return self.objects.get_keys()

    def get_build_phases_by_name(self, phase_name):
        return self.objects.get_objects_in_section(phase_name)

    def get_build_files_for_file(self, file_id):
        return [build_file for build_file in self.objects.get_objects_in_section(u'PBXBuildFile')
                if build_file.fileRef == file_id]

    def get_target_by_name(self, name):
        targets = self.objects.get_targets(name)
        if targets.__len__() > 0:
            return targets[0]
        return None

    def get_object(self, object_id):
        return self.objects[object_id]

    @classmethod
    def load(cls, path):
        import openstep_parser as osp
        tree = osp.OpenStepDecoder.ParseFromFile(open(path, 'r'))
        return XcodeProject(tree, path)
