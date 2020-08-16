# -*- coding: utf-8 -*-
from timeit import default_timer


class Report:
    def __init__(self, file_path, input_name):
        self.file_path = file_path
        self.input_name = input_name
        self.timed_section = []
        self.qt_section = []

    def add_qt_section(self, title, qt):
        self.qt_section.append({'title': title, 'qt': qt})

    def add_timed_section(self, title, time_elapsed):
        self.timed_section.append({'title': title, 'time_elapsed': time_elapsed})

    def save_report(self):
        file = open(self.file_path, 'w', encoding='utf-8')

        file.write('Report file for: {0}\n\n\n'.format(self.input_name))

        for section in self.qt_section:
            file.write('{0}: {1}\n'.format(section['title'], section['qt']))

        file.write('\n')

        total_time = 0
        for section in self.timed_section:
            file.write('{0} took {1} seconds\n'.format(section['title'], '{:.4f}'.format(section['time_elapsed'])))
            total_time += section['time_elapsed']

        file.write('\nTotal time: {0} seconds (or {1} minutes) (or {2} == hours)\n'.format('{:.4}'.format(total_time), '{:.4}'.format(total_time/60), '{:.4}'.format(total_time/3600)))
        file.close()

        print('Report saved at {0}\n\n'.format(self.file_path))