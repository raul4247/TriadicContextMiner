# -*- coding: utf-8 -*-
import json
import os
from Timer import Timer
from DyadicContext import DyadicContext
from TriadicContext import TriadicContext


def mine_file(input_file_path, dyadic_context_file_path, dyadic_concepts_file_path, dyadic_links_file_path,
              dyadic_generators_file_path, dyadic_rules_file_path):
    Timer.start('Reading triadic context from: {0}'.format(input_file_path))
    triadic_context = TriadicContext.read_triadic_context(input_file_path)
    TriadicContext.show_size(triadic_context)
    Timer.stop()

    Timer.start('Flattening the triadic context...')
    context, objects_count, attributes_count = TriadicContext.to_dyadic(triadic_context)
    dyadic_context = DyadicContext(context, objects_count, attributes_count)
    dyadic_context.show_size()
    dyadic_context.save_context(dyadic_context_file_path)
    Timer.stop()

    Timer.start('Generating concepts: {0} -> {1}'.format(dyadic_context_file_path, dyadic_concepts_file_path))
    # dyadic_context.mine_concepts(dyadic_context_file_path, dyadic_concepts_file_path)
    dyadic_context.read_concepts_from_file(dyadic_concepts_file_path)
    dyadic_context.show_concepts_count()
    Timer.stop()

    Timer.start('Running iPred on concepts...')
    dyadic_context.iPred()
    dyadic_context.show_links_count()
    dyadic_context.save_links(dyadic_links_file_path)
    Timer.stop()

    Timer.start('Computing feature generators')
    dyadic_context.compute_feature_generators()
    dyadic_context.show_generators_count()
    dyadic_context.save_generators(dyadic_generators_file_path)
    Timer.stop()

    Timer.start('Computing association rules')
    dyadic_context.compute_association_rules()
    dyadic_context.show_rules_count()
    dyadic_context.save_rules(dyadic_rules_file_path)
    Timer.stop()


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

            mine_file(input_file_path, dyadic_context_file_path, dyadic_concepts_file_path, dyadic_links_file_path,
                      dyadic_generators_file_path, dyadic_rules_file_path)


if __name__ == "__main__":
    main()
