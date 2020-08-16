# -*- coding: utf-8 -*-
import json
import os

from Report import Report
from Timer import Timer
from DyadicContext import DyadicContext
from TriadicContext import TriadicContext


def mine_file(input_file_path, dyadic_context_file_path, dyadic_concepts_file_path, dyadic_links_file_path,
              dyadic_generators_file_path, dyadic_rules_file_path, report_file_path):
    report = Report(report_file_path, input_file_path)
    Timer.start('Reading triadic context from: {0}'.format(input_file_path))
    triadic_context = TriadicContext.read_triadic_context(input_file_path)
    obj_count, attr_count, cond_count = TriadicContext.show_size(triadic_context)
    time = Timer.stop()
    report.add_timed_section('Reading triadic context', time)
    report.add_qt_section('TRIADIC objects count', obj_count)
    report.add_qt_section('TRIADIC Attributes count', attr_count)
    report.add_qt_section('TRIADIC Conditions count', cond_count)

    Timer.start('Flattening the triadic context...')
    context, objects_count, attributes_count = TriadicContext.to_dyadic(triadic_context)
    dyadic_context = DyadicContext(context, objects_count, attributes_count)
    obj_count, attr_count = dyadic_context.show_size()
    dyadic_context.save_context(dyadic_context_file_path)
    time = Timer.stop()
    report.add_timed_section('Flattening triadic context to a dyadic context', time)
    report.add_qt_section('DYADIC objects count', obj_count)
    report.add_qt_section('DYADIC Attributes count', attr_count)

    Timer.start('Generating concepts: {0} -> {1}'.format(dyadic_context_file_path, dyadic_concepts_file_path))
    dyadic_context.mine_concepts(dyadic_context_file_path, dyadic_concepts_file_path)
    dyadic_context.read_concepts_from_file(dyadic_concepts_file_path)
    concepts_count = dyadic_context.show_concepts_count()
    time = Timer.stop()
    report.add_timed_section('Generating concepts', time)
    report.add_qt_section('Concepts count', concepts_count)

    Timer.start('Running iPred on concepts...')
    dyadic_context.iPred()
    links_count = dyadic_context.show_links_count()
    dyadic_context.save_links(dyadic_links_file_path)
    time = Timer.stop()
    report.add_timed_section('Running iPred', time)
    report.add_qt_section('Concepts count', links_count)

    Timer.start('Computing feature generators')
    dyadic_context.compute_feature_generators()
    generators_count = dyadic_context.show_generators_count()
    dyadic_context.save_generators(dyadic_generators_file_path)
    time = Timer.stop()
    report.add_timed_section('Computing feature generators', time)
    report.add_qt_section('Generators count', generators_count)

    Timer.start('Computing association rules')
    dyadic_context.compute_association_rules()
    rules_count = dyadic_context.show_rules_count()
    dyadic_context.save_rules(dyadic_rules_file_path)
    time = Timer.stop()
    report.add_timed_section('Computing association rules', time)
    report.add_qt_section('Rules count', rules_count)

    report.save_report()


def main():
    with open('configs.json') as json_file:
        data = json.load(json_file)
        for input_file_path in data['input_files']:
            _, file_name = os.path.split(input_file_path)
            output_dir = data['output_dir']

            dyadic_context_file_path = '{0}{1}.context'.format(output_dir, file_name)
            dyadic_concepts_file_path = '{0}{1}.concepts'.format(output_dir, file_name)
            dyadic_links_file_path = '{0}{1}.links'.format(output_dir, file_name)
            dyadic_generators_file_path = '{0}{1}.generators'.format(output_dir, file_name)
            dyadic_rules_file_path = '{0}{1}.rules'.format(output_dir, file_name)
            report_file_path = '{0}{1}.report'.format(output_dir, file_name)

            mine_file(input_file_path, dyadic_context_file_path, dyadic_concepts_file_path, dyadic_links_file_path,
                      dyadic_generators_file_path, dyadic_rules_file_path, report_file_path)


if __name__ == "__main__":
    main()
