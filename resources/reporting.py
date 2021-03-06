# --- Python standard library ---
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod

from utils import *
from utils_kodi import *

class Reporter(object):
    __metaclass__ = ABCMeta

    def __init__(self, launcher, decoratorReporter = None):

        self.launcher = launcher
        self.decoratorReporter = decoratorReporter

    @abstractmethod
    def open(self):
        pass
    
    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def _write_message(self, message):
        pass

    def write(self, message):
        
        self._write_message(message)

        if self.decoratorReporter:
            self.decoratorReporter.write(message)

class LogReporter(Reporter):
       
    def open(self, report_title):
        return super(LogReporter, self).close()

    def close(self):
        return super(LogReporter, self).close()

    def _write_message(self, message):
        log_info(message)

class FileReporter(Reporter):
    
    def __init__(self, reports_dir, launcher, decoratorReporter = None):
        
        self.report_file = reports_dir.pjoin(launcher['roms_base_noext'] + '_report.txt')
        super(FileReporter, self).__init__(launcher, decoratorReporter)

    def open(self, report_title):

        log_info('Report file OP "{0}"'.format(self.report_file.getOriginalPath()))

        self.report_file.open('w')

        # --- Get information from launcher ---
        launcher_path = FileNameFactory.create(self.launcher['rompath'])
        
        self.write('******************** Report: {} ...  ********************'.format(report_title))
        self.write('  Launcher name "{0}"'.format(self.launcher['m_name']))
        self.write('  Launcher type "{0}"'.format(self.launcher['type'] if 'type' in self.launcher else 'Unknown'))
        self.write('  launcher ID   "{0}"'.format(self.launcher['id']))
        self.write('  ROM path      "{0}"'.format(launcher_path.getPath()))
        self.write('  ROM ext       "{0}"'.format(self.launcher['romext']))
        self.write('  Platform      "{0}"'.format(self.launcher['platform']))
        self.write(  'Multidisc     "{0}"'.format(self.launcher['multidisc']))
    
    def close(self):
        self.report_file.close()

    def _write_message(self, message):
        self.report_file.write(message.encode('utf-8'))
        self.report_file.write('\n'.encode('utf-8'))