# -*- coding: utf-8 -*-
import configs
from Timer import Timer
from DyadicContext import DyadicContext
from TriadicContext import TriadicContext


def main():
    Timer.start('Reading triadic context from: {0}'.format(configs.input_file))
    triadic_context = TriadicContext.read_triadic_context(configs.input_file)
    TriadicContext.show_size(triadic_context)
    Timer.stop()

    Timer.start('Flattening the triadic context...')
    context, objects_count, attributes_count = TriadicContext.to_dyadic(triadic_context)
    dyadic_context = DyadicContext(context, objects_count, attributes_count)
    dyadic_context.save(configs.dyadic_file)
    dyadic_context.show_size()
    Timer.stop()

    Timer.start('Generating concepts: {0} -> {1}'.format(configs.dyadic_file, configs.concepts_file))
    dyadic_context.mine_concepts(configs.dyadic_file, configs.concepts_file)
    dyadic_context.read_concepts_from_file(configs.concepts_file)
    dyadic_context.show_concepts_count()
    Timer.stop()

    Timer.start('Running iPred on concepts...')
    dyadic_context.iPred()
    dyadic_context.save_links(configs.links_file)
    dyadic_context.show_links_count()
    Timer.stop()


if __name__ == "__main__":
    main()
