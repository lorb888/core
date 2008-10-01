#--
# Copyright (c) 2008, Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
#--

"""Extensions to Setuptools

Add the commands:

  - ``generate_html`` to generate a HTML page from a ReStructuredText
  - ``generate_api`` to generate HTML pages from the elements and comments of modules
"""

from __future__ import with_statement

import sys, os
import distutils

from nagare.doc import code_block

from setuptools import find_packages
import docutils
from rstdoc.setuplib import rstdocs
from rstdoc.rstlib.astdoc import documentPackages, documentFile

settings = {
            'stylesheet' : 'doc.css',
            'stylesheet_path' : None,
            'embed_stylesheet' : False
           }

class GenerateHTML(distutils.cmd.Command):
    """ReStructuredText to HTML converter
    
    The ``generate_html`` command can generate HTML from ReStructuredText
    containing ``code-block`` directive and Trac roles.
    
    The command accepts a list of ReStructuredText to convert.
    """    
    description = __doc__.strip()
    user_options = [
                    ('path=', 'p', 'Path to docs directory'),
                    ('trac=', None, 'The Trac project URL'),
                   ]
    command_consumes_arguments = True
    
    def initialize_options(self):
        """Default options values
        
        The ``-p`` or ``--path`` option is the directory where the HTML pages
        will generated.
        
        The ``--trac`` option is the URL to the Trac project. Used when a
        Trac role is found into the ReStructuredText.
        """
        self.path = 'docs'
        self.trac = 'http://yoursite.com/trac/project'
        self.args = []

    def finalize_options(self):
        pass

    def run(self):
        if not self.args:
            raise distutils.errors.DistutilsOptionError('No file to convert')

        code_block.register_role(self.trac)
        code_block.register_directive()

        docPath = os.path.abspath(self.path)
        print 'Documentation directory:', docPath

        for filename in self.args:
            if not os.path.isfile(filename):
                raise distutils.errors.DistutilsOptionError("The path '%s' is not a file" % filename)
            
            print 'Processing:', filename
                            
            out_filename = os.path.splitext(os.path.basename(filename))[0] + '.html'
            out_filename = os.path.join(docPath, out_filename)
            
            docutils.core.publish_file(
                                       source_path=filename,
                                       destination_path=out_filename,
                                       writer_name='html', settings_overrides=settings
                                      )
        

class GenerateAPI(rstdocs):
    """API generation
    
    The ``generate_api`` command accepts a list of Python files to analyse.
    
    If no files are given, it generates the API documentation for all the
    Python files of the distribution.
    """        
    def run (self):
        if self.dry_run:
            return
    
        code_block.register_directive()

        docPath = os.path.abspath(self.path)
        if self.no_status:
            output = None
        else:
            output = sys.stderr

        if not self.args:
            docDirs = sorted(find_packages())

            documentPackages(
                docPath=docPath, 
                packages=docDirs,
                writer_name='html', 
                output=output, 
                title=self.title,
                settings=settings
                )
        else:
            print 'Documentation directory:', docPath
            
            for filename in self.args:
                if not os.path.isfile(filename):
                    raise distutils.errors.DistutilsOptionError("The path '%s' is not a file" % filename)
                    
                print 'Processing:', filename
                
                tree = documentFile(filename).docTree()
                
                out_filename = os.path.splitext(filename.replace(os.sep, '-'))[0] + '.html'
                out_filename = os.path.join(docPath, out_filename)
                
                with open(out_filename, 'w') as f:
                    f.write(docutils.core.publish_from_doctree(tree, writer_name='html', settings_overrides=settings))