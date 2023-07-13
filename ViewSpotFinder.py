import sys
import os
import json
import logging
from datetime import datetime


def get_viewspots_dict(elements, values, n):
    viewspots = []

    # iterate through elements to find neighbours
    for element in elements:
        el_nodes = list(element.get('nodes'))
        local_max = True
        for el_node in el_nodes:
            if local_max:
                for pos_neighbour in elements:
                    if element.get('id') != pos_neighbour.get('id'):

                        # when a neighbour is found, checking which one is higher
                        if el_node in list(pos_neighbour.get('nodes')):
                            el_value = values[element.get('id')].get('value')
                            neighbour_val = values[pos_neighbour.get('id')].get('value')
                            if el_value <= neighbour_val:
                                local_max = False
                                break
                            elements.remove(pos_neighbour)
            if not local_max:
                break

        # when local maximum is found, it's sorted into the viewpoint list
        if local_max:
            i = 0
            while i < len(viewspots)+1:
                if not viewspots or viewspots[i].get('value') <= values[element.get('id')].get('value'):
                    viewspots.insert(i, {'element_id': element.get('id'), 'value': values[element.get('id')].get('value')})
                    break
                else:
                    i += 1
        elements.remove(element)
    return viewspots[:n]


if __name__ == '__main__':
    date_time_save_start = datetime.now()

    # setup logging
    logging.basicConfig(filename='ViewSpotFinderLog_{}.log'.format(date_time_save_start.strftime('%Y_%m_%d_%H_%M_%S')),
                        format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.INFO, filemode='w')
    logger = logging.getLogger()
    logger.info('Starting ViewSpotFinder')

    # read parameters
    if len(sys.argv) != 3:
        logger.error('Wrong number of arguments')
        raise ValueError('Wrong number of arguments')
    json_file = sys.argv[1]
    n = int(sys.argv[2])

    if not os.path.exists(json_file):
        logging.error('JSON file not found')
        raise ValueError('JSON file not found')
    f = open(json_file)

    mesh = json.load(f)

    nodes = mesh.get('nodes')
    elements = mesh.get('elements')
    values = mesh.get('values')

    top_viewspots = get_viewspots_dict(elements, values, n)

    with open('top_view_points_' + date_time_save_start.strftime('%Y_%m_%d_%H_%M_%S') + '.json', 'w') as file:
        json.dump(top_viewspots, file)
    date_time_save_end = datetime.now()
    logger.info('Ending ViewSpotFinder, Duration: {}'.format(date_time_save_end - date_time_save_start))